import os
import re
from pathlib import Path
from django.conf import settings
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decouple import config
from .serializers import ChatbotQuerySerializer, ChatbotResponseSerializer
from .models import Document

try:
    import anthropic
    from PyPDF2 import PdfReader
    HAS_DEPENDENCIES = True
except ImportError:
    HAS_DEPENDENCIES = False


def extract_text_from_pdf(file_path):
    """Extract text from a PDF file"""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error reading PDF {file_path}: {str(e)}")
        return ""


def get_documents_from_db():
    """Get all documents from the database"""
    documents = Document.objects.all()
    result = []
    for doc in documents:
        if doc.file and doc.file_type == 'pdf':
            result.append({
                'name': doc.name,
                'path': doc.full_path,
                'relative_path': doc.file.name,
                'url': doc.file_url,
            })
    return result


def chunk_text(text, chunk_size=8000, overlap=200):
    """Split text into chunks for processing"""
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    
    return chunks


class ChatbotView(APIView):
    """
    Chatbot endpoint that answers questions based on documents in the media folder.
    Uses Claude API for intelligent responses.
    """
    
    def post(self, request):
        if not HAS_DEPENDENCIES:
            return Response(
                {'error': 'Required dependencies not installed. Please install: anthropic, PyPDF2'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        serializer = ChatbotQuerySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        query = serializer.validated_data['query']
        
        # Get Claude API key from environment
        claude_api_key = config('CLAUDE_API_KEY', default=None)
        if not claude_api_key:
            return Response(
                {'error': 'Claude API key not configured. Please set CLAUDE_API_KEY in your environment variables.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        try:
            # Initialize Claude client
            client = anthropic.Anthropic(api_key=claude_api_key)
            
            # Get all PDF documents from database
            documents = get_documents_from_db()
            
            if not documents:
                return Response(
                    {'error': 'No documents found. Please upload documents via Django admin.'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Extract text from all documents and find the most relevant one
            document_contents = []
            for doc in documents:
                text = extract_text_from_pdf(doc['path'])
                if text:
                    # Take first 10000 characters for relevance check
                    preview = text[:10000]
                    document_contents.append({
                        'name': doc['name'],
                        'path': doc['path'],
                        'relative_path': doc['relative_path'],
                        'preview': preview,
                        'full_text': text
                    })
            
            if not document_contents:
                return Response(
                    {'error': 'No readable text found in documents'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Use Claude to find the most relevant document
            doc_summaries = "\n\n".join([
                f"Document {i+1}: {doc['name']}\nPreview: {doc['preview'][:500]}..."
                for i, doc in enumerate(document_contents)
            ])
            
            relevance_prompt = f"""You are a document search assistant. Given a user question and a list of documents, identify which document is most relevant.

User Question: {query}

Available Documents:
{doc_summaries}

Respond with ONLY the document number (1, 2, 3, etc.) that is most relevant to the question. If no document is relevant, respond with "0"."""
            
            relevance_response = client.messages.create(
                model="claude-3-haiku-20240307",  # Cheapest Claude model
                max_tokens=10,
                messages=[{"role": "user", "content": relevance_prompt}]
            )
            
            selected_doc_num = relevance_response.content[0].text.strip()
            
            # Parse document number
            try:
                doc_index = int(re.search(r'\d+', selected_doc_num).group()) - 1
                if doc_index < 0 or doc_index >= len(document_contents):
                    doc_index = 0  # Default to first document
            except:
                doc_index = 0
            
            selected_doc = document_contents[doc_index]
            
            # Generate answer using the selected document
            answer_prompt = f"""You are a helpful assistant answering questions about parliamentary proceedings in Uganda based on the provided document.

User Question: {query}

Document Name: {selected_doc['name']}

Document Content:
{selected_doc['full_text'][:50000]}  # Limit to 50k chars for Claude

Please provide a clear, concise answer to the user's question based on the document content. If the answer is not in the document, say so clearly. Keep your answer under 300 words."""
            
            answer_response = client.messages.create(
                model="claude-3-haiku-20240307",  # Cheapest Claude model
                max_tokens=500,
                messages=[{"role": "user", "content": answer_prompt}]
            )
            
            answer = answer_response.content[0].text.strip()
            
            # Use document URL from model
            document_url = selected_doc.get('url', f"/media/{selected_doc['relative_path']}")
            
            response_data = {
                'answer': answer,
                'document_name': selected_doc['name'],
                'document_url': document_url,
                'confidence': 0.8  # Simple confidence score
            }
            
            response_serializer = ChatbotResponseSerializer(data=response_data)
            if response_serializer.is_valid():
                return Response(response_serializer.validated_data, status=status.HTTP_200_OK)
            else:
                return Response(response_data, status=status.HTTP_200_OK)
                
        except Exception as e:
            return Response(
                {'error': f'Error processing request: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
