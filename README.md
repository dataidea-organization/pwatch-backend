# Parliament Watch Backend

## Overview

Parliament Watch Uganda monitors and tracks the Ugandan Parliament on a regular basis, providing relevant data and expert insights. This Django REST API backend powers the Parliament Watch website, providing comprehensive APIs for accessing parliamentary data, news, blogs, trackers, multimedia content, and interactive features like a chatbot.

## Features

### Trackers API
- **Members of Parliament (MPs)**: Manage MP profiles with personal information, political affiliation, constituency, district, contact details, photos, and biographies
- **Bills Tracker**: Track bills through reading stages (1st, 2nd, 3rd reading, passed, assented, withdrawn) with detailed reading history, documents, committee reports, and analysis
- **Loans Tracker**: Monitor parliamentary loans with sector and source information
- **Debt Tracker**: Track national debt data and statistics
- **Budget Tracker**: Manage budget documents organized by financial year
- **Hansards Tracker**: Store and serve parliamentary proceedings and debate transcripts
- **Order Paper Tracker**: Manage parliamentary order papers
- **Parliament Performance Tracker**: Track and analyze parliamentary performance metrics
- **Committees**: Manage parliamentary committees and committee documents

### News & Content API
- **News Articles**: Full CRUD operations for news articles with categories, images, rich text content, author information, and publication dates
- **Blog Posts**: Manage blog posts with categories, filtering, search, and pagination support

### Multimedia API
- **X Spaces**: Archive Twitter Spaces discussions with scheduling, recordings, thumbnails, topics, and speakers
- **Podcasts**: Manage podcast library with episodes, YouTube integration, thumbnails, categories, and tags
- **Gallery**: Photo gallery with categories, featured images, event dates, and photographer credits
- **Polls**: Public engagement polls with multiple options, voting functionality, results tracking, and featured polls

### Resources API
- **Explainers**: Educational documents explaining parliamentary processes
- **Reports & Briefs**: Research reports and policy briefs
- **Partner Publications**: Publications from partner organizations
- **Statements**: Official statements and press releases

### Interactive Features
- **Chatbot API**: AI-powered Q&A chatbot for parliamentary information (Alpha version)
  - Document-based Q&A using Claude AI (claude-3-haiku-20240307)
  - Automatic PDF document scanning and reading from media folder
  - Intelligent document search and contextual answer generation
  - Session-based conversations with chat history
  - Document source links for answers
- **Global Search**: Unified search across all content types (news, blogs, MPs, bills, resources, multimedia) with concurrent querying and result aggregation

### Home Page API
- **Hero Images**: Manage hero carousel images with ordering and activation
- **Headlines**: Manage scrolling headlines/tickers with formatting options

### About API
- **Objectives**: Manage organizational objectives with icons and ordering
- **Team Members**: Manage team member profiles with photos, bios, contact information, and social media links

### Contact & Engagement API
- **Contact Submissions**: Handle contact form submissions
- **Donation Submissions**: Process donation form submissions with donor information

### Additional Features
- **Django Admin**: Full admin interface for content management
- **REST Framework**: RESTful API endpoints with pagination, filtering, and search
- **CORS Support**: Cross-origin resource sharing for frontend integration
- **Media Management**: File upload and serving for documents, images, and media files
- **Rich Text Editor**: CKEditor integration for rich content editing
- **Caching**: Optimized endpoints with caching for home page summaries
- **Management Commands**: Utility commands for data import and population
