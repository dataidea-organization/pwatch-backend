# Chatbot API Documentation

## Overview

The Chatbot API provides an intelligent question-answering system that reads documents from the server's media folder and uses Claude AI to generate contextual responses with document references.

## Features

- **Document Reading**: Automatically scans and reads PDF documents from the `media/` folder
- **Intelligent Search**: Uses Claude AI to find the most relevant document for each query
- **Contextual Answers**: Generates answers based on document content
- **Document Links**: Returns links to the source documents for reference

## Setup

### 1. Install Dependencies

The chatbot requires the following Python packages:

```bash
pip install anthropic PyPDF2
```

Or using Poetry:

```bash
poetry add anthropic PyPDF2
```

### 2. Configure Claude API Key

Add your Claude API key to your environment variables or `.env` file:

```bash
CLAUDE_API_KEY=your_claude_api_key_here
```

**Where to get your API key:**
1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and add it to your environment variables

**Note**: The chatbot uses `claude-3-haiku-20240307`, which is Claude's cheapest model, optimized for cost-effective responses.

### 3. Run Migrations

```bash
python manage.py makemigrations chatbot
python manage.py migrate
```

## API Endpoint

### POST `/api/chatbot/chat/`

Send a question to the chatbot and receive an intelligent answer with document reference.

#### Request Body

```json
{
  "query": "What was discussed in the anti-corruption bill session?"
}
```

#### Response

```json
{
  "answer": "The anti-corruption bill session discussed...",
  "document_name": "Hansard Special Session Anti Corruption Bill",
  "document_url": "/media/hansard_special_session___anti_corruption_bill.pdf",
  "confidence": 0.8
}
```

#### Response Fields

- `answer` (string): The AI-generated answer to the question
- `document_name` (string): Name of the most relevant document
- `document_url` (string): URL to access the source document
- `confidence` (float): Confidence score (0-1) of the answer relevance

#### Error Responses

**400 Bad Request**: Invalid request format
```json
{
  "query": ["This field is required."]
}
```

**404 Not Found**: No documents found
```json
{
  "error": "No documents found in media folder"
}
```

**500 Internal Server Error**: Missing API key or other errors
```json
{
  "error": "Claude API key not configured. Please set CLAUDE_API_KEY in your environment variables."
}
```

## How It Works

### 1. Document Discovery
- The system automatically scans the `media/` folder for PDF files
- It recursively searches all subdirectories
- Each PDF is indexed with its name and path

### 2. Document Relevance Selection
- When a query is received, the system extracts text previews from all documents
- Claude AI analyzes the query against document previews
- The most relevant document is selected based on semantic similarity

### 3. Answer Generation
- The full text of the selected document is extracted
- Claude AI generates a contextual answer based on the document content
- The answer is limited to 300 words for conciseness

### 4. Response Formatting
- The answer is combined with document metadata
- A direct link to the source document is included
- A confidence score is provided

## Tools and Technologies

### Core Technologies
- **Django REST Framework**: API endpoint structure
- **Anthropic Claude API**: AI-powered document search and answer generation
- **PyPDF2**: PDF text extraction

### Claude Model
- **Model**: `claude-3-haiku-20240307`
- **Why**: Most cost-effective Claude model, optimized for speed and efficiency
- **Use Cases**: Document search, text analysis, question answering

### File Processing
- **Format Support**: PDF files (`.pdf`)
- **Text Extraction**: Full document text extraction
- **Chunking**: Large documents are processed in chunks for efficiency

## Usage Examples

### Example 1: Question about Budget

**Request:**
```bash
curl -X POST http://localhost:8000/api/chatbot/chat/ \
  -H "Content-Type: application/json" \
  -d '{"query": "What was the budget allocation for education in 2024?"}'
```

**Response:**
```json
{
  "answer": "According to the budget debate session, the education sector received...",
  "document_name": "Hansard Special Session Budget Debate 2024",
  "document_url": "/media/hansard_special_session___budget_debate_2024.pdf",
  "confidence": 0.8
}
```

### Example 2: Question about Parliamentary Proceedings

**Request:**
```bash
curl -X POST http://localhost:8000/api/chatbot/chat/ \
  -H "Content-Type: application/json" \
  -d '{"query": "What bills were discussed in March 2024?"}'
```

**Response:**
```json
{
  "answer": "In March 2024, the parliament discussed several bills including...",
  "document_name": "Hansard Parliamentary Proceedings March 2024",
  "document_url": "/media/hansard_parliamentary_proceedings___march_2024.pdf",
  "confidence": 0.8
}
```

## File Structure

```
backend/
├── chatbot/
│   ├── __init__.py
│   ├── models.py          # Document model
│   ├── views.py           # ChatbotView with AI logic
│   ├── serializers.py     # Request/response serializers
│   ├── urls.py            # URL routing
│   ├── admin.py           # Django admin configuration
│   └── README.md          # This file
└── media/                 # Document storage folder
    ├── hansard_*.pdf
    └── bill_documents/
        └── *.pdf
```

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `CLAUDE_API_KEY` | Your Anthropic Claude API key | Yes |
| `DEBUG` | Django debug mode | Optional |
| `MEDIA_ROOT` | Path to media folder | Auto-configured |

### Settings

The chatbot is automatically registered in `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... other apps
    'chatbot',
    # ...
]
```

URL routing is configured in `main/urls.py`:

```python
urlpatterns = [
    # ... other paths
    path('api/chatbot/', include('chatbot.urls')),
]
```

## Limitations

1. **PDF Only**: Currently only supports PDF documents
2. **Text Extraction**: Some PDFs with complex layouts may not extract text perfectly
3. **Document Size**: Very large documents (>50k characters) are truncated for processing
4. **Language**: Optimized for English text
5. **Rate Limits**: Subject to Claude API rate limits

## Future Enhancements

- Support for other document formats (Word, TXT, etc.)
- Document indexing and caching for faster responses
- Multi-document answer synthesis
- Conversation history and context
- User feedback and answer improvement

## Troubleshooting

### "Claude API key not configured"
- Ensure `CLAUDE_API_KEY` is set in your environment
- Check `.env` file if using python-decouple
- Verify the key is valid at https://console.anthropic.com/

### "No documents found"
- Ensure PDF files exist in the `media/` folder
- Check file permissions
- Verify `MEDIA_ROOT` setting is correct

### "Error reading PDF"
- PDF may be corrupted or password-protected
- Check PDF file format compatibility
- Verify PyPDF2 is installed correctly

### Import Errors
- Run: `pip install anthropic PyPDF2`
- Or: `poetry add anthropic PyPDF2`
- Restart Django development server

## Support

For issues or questions:
1. Check the error message in the API response
2. Verify all dependencies are installed
3. Ensure Claude API key is valid and has credits
4. Check Django logs for detailed error information

