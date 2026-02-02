import os
import re
from pathlib import Path
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from decouple import config
from .serializers import ChatbotQuerySerializer, ChatbotResponseSerializer
from .models import Document, ChatConversation, ChatMessage

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


@method_decorator(csrf_exempt, name='dispatch')
class ChatbotView(APIView):
    """
    Chatbot endpoint that answers questions based on documents in the media folder.
    Uses Claude API for intelligent responses.
    Exempt from CSRF so cross-origin (CORS) requests from the frontend are allowed.
    """
    
    def get_client_ip(self, request):
        """Get client IP address from request"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def get_or_create_conversation(self, request):
        """Get or create a conversation for the current session"""
        # Get session ID from request data or generate one
        session_id = request.data.get('session_id') or request.session.session_key
        if not session_id:
            # Generate a session ID if none exists
            import uuid
            session_id = str(uuid.uuid4())
        
        # Get client metadata
        ip_address = self.get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Get or create conversation
        conversation, created = ChatConversation.objects.get_or_create(
            session_id=session_id,
            defaults={
                'ip_address': ip_address,
                'user_agent': user_agent
            }
        )
        
        # Update metadata if conversation already exists
        if not created:
            if not conversation.ip_address:
                conversation.ip_address = ip_address
            if not conversation.user_agent:
                conversation.user_agent = user_agent
            conversation.save()
        
        return conversation, session_id
    
    def get_conversation_history(self, conversation, limit=5):
        """Get the last N message pairs (user + assistant) from conversation history"""
        # Get last messages ordered by creation time
        messages = conversation.messages.all().order_by('-created_at')[:limit * 2]
        
        # Reverse to get chronological order
        messages = list(reversed(messages))
        
        # Group into pairs (user, assistant)
        history = []
        i = 0
        while i < len(messages):
            if messages[i].role == 'user':
                user_msg = messages[i]
                assistant_msg = None
                if i + 1 < len(messages) and messages[i + 1].role == 'assistant':
                    assistant_msg = messages[i + 1]
                    i += 2
                else:
                    i += 1
                
                if assistant_msg:
                    history.append({
                        'user': user_msg.content,
                        'assistant': assistant_msg.content
                    })
            else:
                i += 1
        
        return history
    
    def is_greeting(self, query):
        """Check if the query is a greeting"""
        query_lower = query.lower().strip()
        greetings = [
            'hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon',
            'good evening', 'good day', 'howdy', 'what\'s up', 'whats up',
            'how are you', 'how do you do', 'nice to meet you', 'pleased to meet you'
        ]
        
        # Check if query is just a greeting (with optional punctuation)
        query_clean = re.sub(r'[^\w\s]', '', query_lower)
        words = query_clean.split()
        
        # If query is very short (1-3 words) and contains a greeting word
        if len(words) <= 3:
            for greeting in greetings:
                if greeting in query_lower:
                    return True
        
        return False
    
    def is_appreciation(self, query):
        """Check if the query is an appreciation/thanks"""
        query_lower = query.lower().strip()
        appreciations = [
            'thank you', 'thanks', 'thank', 'appreciate', 'appreciated', 'grateful',
            'much appreciated', 'thanks a lot', 'thank you very much', 'thanks so much',
            'thanks a bunch', 'i appreciate', 'i\'m grateful', 'im grateful'
        ]
        
        # Check if query is just an appreciation (with optional punctuation)
        query_clean = re.sub(r'[^\w\s]', '', query_lower)
        words = query_clean.split()
        
        # If query is very short (1-4 words) and contains an appreciation word
        if len(words) <= 4:
            for appreciation in appreciations:
                if appreciation in query_lower:
                    return True
        
        return False
    
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
        
        # Get or create conversation
        conversation, session_id = self.get_or_create_conversation(request)
        
        # Save user message
        user_message = ChatMessage.objects.create(
            conversation=conversation,
            role='user',
            content=query
        )
        
        # Get conversation history (last 5 message pairs)
        history = self.get_conversation_history(conversation, limit=5)
        
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
            
            # Build conversation history context
            history_context = ""
            if history:
                history_context = "\n\nPrevious conversation context:\n"
                for i, pair in enumerate(history, 1):
                    history_context += f"\nPrevious exchange {i}:\n"
                    history_context += f"User: {pair['user']}\n"
                    history_context += f"Assistant: {pair['assistant']}\n"
                history_context += "\nUse this context to provide more relevant and coherent responses.\n"
            
            # Check if query is a pure greeting or appreciation (no question)
            is_pure_greeting = self.is_greeting(query) and not any(word in query.lower() for word in ['what', 'when', 'where', 'who', 'why', 'how', 'which', 'tell', 'explain', 'show', 'find', 'search'])
            is_pure_appreciation = self.is_appreciation(query) and not any(word in query.lower() for word in ['what', 'when', 'where', 'who', 'why', 'how', 'which', 'tell', 'explain', 'show', 'find', 'search'])
            
            # Handle pure greetings/appreciations without document search
            if is_pure_greeting or is_pure_appreciation:
                # Build prompt for pure greetings/appreciations
                if is_pure_greeting:
                    prompt = f"""You are a helpful and friendly assistant for Parliament Watch Uganda. You help users find information about parliamentary proceedings, bills, and documents.
{history_context}
The user has sent a greeting: {query}

Respond warmly and naturally to the greeting. Introduce yourself as the Parliament Watch Uganda chatbot and offer to help with questions about the Ugandan Parliament, bills, parliamentary proceedings, or related documents. Be friendly, professional, and welcoming. Keep your response concise (under 100 words)."""
                else:  # is_pure_appreciation
                    prompt = f"""You are a helpful and friendly assistant for Parliament Watch Uganda.
{history_context}
The user has expressed appreciation: {query}

Respond warmly and naturally to the appreciation. Acknowledge their thanks and offer further assistance if they have more questions about the Ugandan Parliament. Be friendly and professional. Keep your response concise (under 100 words)."""
                
                # Build messages array with conversation history
                messages = []
                for pair in history:
                    messages.append({"role": "user", "content": pair['user']})
                    messages.append({"role": "assistant", "content": pair['assistant']})
                
                messages.append({"role": "user", "content": prompt})
                
                answer_response = client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=200,
                    messages=messages
                )
                
                answer = answer_response.content[0].text.strip()
                
                # Save assistant message
                assistant_message = ChatMessage.objects.create(
                    conversation=conversation,
                    role='assistant',
                    content=answer
                )
                
                response_data = {
                    'answer': answer,
                    'document_name': '',
                    'document_url': '',
                    'confidence': 1.0,
                    'session_id': session_id
                }
                
                response_serializer = ChatbotResponseSerializer(data=response_data)
                if response_serializer.is_valid():
                    return Response(response_serializer.validated_data, status=status.HTTP_200_OK)
                else:
                    return Response(response_data, status=status.HTTP_200_OK)
            
            # For questions (with or without greetings/appreciations), proceed with document search
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
                        'url': doc.get('url', ''),  # Include URL for later use
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
            
            relevance_prompt = f"""You are a document search assistant for Parliament Watch Uganda. You need to find documents related to the Ugandan Parliament, political parties, MPs, bills, or parliamentary proceedings.

User Question: {query}

Available Documents:
{doc_summaries}

IMPORTANT: 
- Only select documents that are clearly related to parliamentary matters, Ugandan politics, MPs, bills, or political parties.
- If a document is clearly about unrelated topics (programming, general topics, etc.) and the question is about parliamentary matters, respond with "0".
- If no document is relevant to the parliamentary question, respond with "0".
- Otherwise, respond with ONLY the document number (1, 2, 3, etc.) that is most relevant."""
                        
            relevance_response = client.messages.create(
                model="claude-3-haiku-20240307",  # Cheapest Claude model
                max_tokens=10,
                messages=[{"role": "user", "content": relevance_prompt}]
            )
            
            selected_doc_num = relevance_response.content[0].text.strip()
            
            # Parse document number
            doc_index = -1
            try:
                doc_num = int(re.search(r'\d+', selected_doc_num).group())
                if doc_num == 0:
                    # No relevant document found
                    doc_index = -1
                else:
                    doc_index = doc_num - 1
                    if doc_index < 0 or doc_index >= len(document_contents):
                        doc_index = -1
            except:
                doc_index = -1
            
            # If no relevant document found, respond directly without document
            if doc_index == -1:
                # Build conversation history context
                history_context = ""
                if history:
                    history_context = "\n\nPrevious conversation context:\n"
                    for i, pair in enumerate(history, 1):
                        history_context += f"\nPrevious exchange {i}:\n"
                        history_context += f"User: {pair['user']}\n"
                        history_context += f"Assistant: {pair['assistant']}\n"
                    history_context += "\nUse this context to provide more relevant and coherent responses.\n"
                
                no_doc_prompt = f"""You are a helpful assistant for Parliament Watch Uganda. You answer questions about the Ugandan Parliament, political parties, MPs, bills, and parliamentary proceedings.
{history_context}
User question: {query}

I searched through the available parliamentary documents but could not find any documents relevant to this question.

Respond directly and concisely (1-2 sentences): "I couldn't find information about [specific topic] in the available parliamentary documents."

Do NOT:
- Add greetings or pleasantries
- Apologize excessively
- Mention searching documents
- Be verbose

Just state simply that the information wasn't found."""
                
                # Build messages array with conversation history
                messages = []
                for pair in history:
                    messages.append({"role": "user", "content": pair['user']})
                    messages.append({"role": "assistant", "content": pair['assistant']})
                
                messages.append({"role": "user", "content": no_doc_prompt})
                
                answer_response = client.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=100,
                    messages=messages
                )
                
                answer = answer_response.content[0].text.strip()
                
                # Save assistant message
                assistant_message = ChatMessage.objects.create(
                    conversation=conversation,
                    role='assistant',
                    content=answer
                )
                
                response_data = {
                    'answer': answer,
                    'document_name': '',
                    'document_url': '',
                    'confidence': 0.3,
                    'session_id': session_id
                }
                
                response_serializer = ChatbotResponseSerializer(data=response_data)
                if response_serializer.is_valid():
                    return Response(response_serializer.validated_data, status=status.HTTP_200_OK)
                else:
                    return Response(response_data, status=status.HTTP_200_OK)
            
            selected_doc = document_contents[doc_index]
            
            # Generate answer using the selected document with enhanced prompt
            answer_prompt = f"""You are a helpful assistant for Parliament Watch Uganda. You answer questions about the Ugandan Parliament, political parties, MPs, bills, and parliamentary proceedings.
{history_context}
User question: {query}

I have searched through parliamentary documents and found this document:

Document: {selected_doc['name']}

Document Content:
{selected_doc['full_text'][:100000]}

CRITICAL INSTRUCTIONS:
1. **Answer the question directly** - Do NOT start with greetings, introductions, or pleasantries. The user has already asked a question, so answer it immediately.

2. **Check document relevance** - If the document content is clearly not related to the question (e.g., programming, unrelated topics), state simply: "I couldn't find information about [topic] in the available parliamentary documents."

3. **If information is found** - Provide a clear, direct answer based on the document. Do not mention the document name or that you searched documents. Answer as if you know this information.

4. **If information is NOT found** - Simply state: "I couldn't find information about [specific topic] in the available parliamentary documents." Keep it brief (1-2 sentences). Do not apologize excessively.

5. **Greetings/appreciations** - Only acknowledge greetings or thanks if they appear WITH the question (e.g., "Hello, who is..."). For pure questions, skip pleasantries and answer directly.

6. **Be concise** - Keep answers under 200 words. Be direct and factual.

7. **Tone** - Professional and helpful, but not overly formal or apologetic.

Now answer the user's question directly:"""

            # Build messages array with conversation history for Claude
            messages = []
            
            # Add conversation history as alternating user/assistant messages
            for pair in history:
                messages.append({"role": "user", "content": pair['user']})
                messages.append({"role": "assistant", "content": pair['assistant']})
            
            # Add current query
            messages.append({"role": "user", "content": answer_prompt})
            
            answer_response = client.messages.create(
                model="claude-3-haiku-20240307",  # Cheapest Claude model
                max_tokens=500,
                messages=messages
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
            
            # Save assistant message
            assistant_message = ChatMessage.objects.create(
                conversation=conversation,
                role='assistant',
                content=answer,
                document_name=selected_doc['name'],
                document_url=document_url
            )
            
            response_data = {
                'answer': answer,
                'document_name': selected_doc['name'],
                'document_url': document_url,
                'confidence': 0.8,  # Simple confidence score
                'session_id': session_id  # Return session_id for frontend to use
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
