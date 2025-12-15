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


def get_documents_from_media():
    """Scan entire media folder and return list of PDF documents"""
    documents = []
    media_path = Path(settings.MEDIA_ROOT)
    
    # Walk through entire media folder (not just chatbot/documents)
    for root, dirs, files in os.walk(media_path):
        for file in files:
            if file.lower().endswith('.pdf'):
                file_path = Path(root) / file
                relative_path = os.path.relpath(file_path, media_path)
                
                # Create a readable name from filename
                name = file.replace('.pdf', '').replace('_', ' ').replace('-', ' ').title()
                
                # Build URL - use full backend URL from settings
                full_media_url = getattr(settings, 'FULL_MEDIA_URL', None)
                if full_media_url:
                    # Remove trailing slash if present, then add relative path
                    full_media_url = full_media_url.rstrip('/')
                    url = f"{full_media_url}/{relative_path}"
                else:
                    # Fallback: construct from MEDIA_URL
                    if settings.DEBUG:
                        url = f"http://localhost:8000{settings.MEDIA_URL}{relative_path}"
                    else:
                        # In production, try to get from environment or use default
                        backend_domain = config('BACKEND_DOMAIN', default='https://pwatch-backend-production.up.railway.app')
                        url = f"{backend_domain}{settings.MEDIA_URL}{relative_path}"
                
                documents.append({
                    'name': name,
                    'path': str(file_path),
                    'relative_path': relative_path,
                    'url': url,
                })
    
    return documents


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
            
            # Get all PDF documents from entire media folder
            documents = get_documents_from_media()
            
            if not documents:
                return Response(
                    {'error': 'No PDF documents found in media folder'},
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
            answer_prompt = f"""You are a helpful assistant for Parliament Watch Uganda. You have access to a collection of parliamentary documents and can search through them to answer questions.

            A user has asked: {query}

            I have searched through the available parliamentary documents and found the following document that is most relevant to this question:

            Document: {selected_doc['name']}

            Document Content:
            {selected_doc['full_text'][:50000]}

            Based on the information in this document, provide a clear and direct answer to the user's question. Answer naturally as if you are providing information from your knowledge base. Do not mention that you are reading from a document or that the user provided anything. Simply answer the question directly.

            If the information needed to answer the question is not found in this document, clearly state that you could not find the specific information requested. Keep your answer concise and under 300 words."""

            answer_response = client.messages.create(
                model="claude-3-haiku-20240307",  # Cheapest Claude model
                max_tokens=500,
                messages=[{"role": "user", "content": answer_prompt}]
            )
            
            answer = answer_response.content[0].text.strip()
            
            # Use document URL - should already be full backend URL from get_documents_from_media()
            document_url = selected_doc.get('url', '')
            if not document_url:
                # Fallback: construct full backend URL
                full_media_url = getattr(settings, 'FULL_MEDIA_URL', None)
                if full_media_url:
                    full_media_url = full_media_url.rstrip('/')
                    document_url = f"{full_media_url}/{selected_doc['relative_path']}"
                else:
                    document_url = f"/media/{selected_doc['relative_path']}"
            
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
