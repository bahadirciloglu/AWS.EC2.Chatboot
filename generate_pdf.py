#!/usr/bin/env python3
"""
PDF Generator for Kartal.AI Architecture Diagram
Uses reportlab to create a professional PDF document
"""

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    print("ReportLab is available")
    REPORTLAB_AVAILABLE = True
except ImportError:
    print("ReportLab not available, will create alternative PDF")
    REPORTLAB_AVAILABLE = False

import os

def create_simple_pdf():
    """Create a simple text-based PDF alternative"""
    content = """
KARTAL.AI CHATBOT - SYSTEM ARCHITECTURE
==================================

PROJECT OVERVIEW
----------------
RAG-based AI chatbot platform for hospitality industry using:
- FastAPI backend
- AWS Bedrock Claude LLM
- LlamaIndex RAG pipeline
- ChromaDB vector database
- Redis session management
- Nginx reverse proxy

SYSTEM ARCHITECTURE
-------------------
User/Client (Browser) 
    ↓
Nginx Proxy (SSL/HTTPS)
    ↓
FastAPI App (Port 8000)
    ↓
Agent Module (run_agent) → Google Sheets (Logging)
    ↓
LlamaIndex RAG Pipeline
    ↓
ChromaDB Vector Store ← Session Management → Redis Cache
    ↓
Embeddings Processing ← HuggingFace Transformers
    ↓
AWS Bedrock Claude LLM

DATA FLOW PROCESS
-----------------
1. User Request → Browser
2. HTTPS → Nginx Proxy
3. API Validation → FastAPI
4. RAG Processing → Agent Module
5. Vector Search → ChromaDB
6. LLM Generation → AWS Bedrock
7. Response & Logging → Google Sheets

TECHNOLOGY STACK
----------------
Backend: FastAPI, Python
AI/ML: AWS Bedrock Claude, LlamaIndex, HuggingFace
Database: ChromaDB (Vector), Redis (Cache)
Infrastructure: AWS EC2, Nginx, systemd
DevOps: Cron jobs, automated log rotation
Testing: pytest, httpx
Security: SSL/TLS, CORS, KVKV/GDPR compliance

API ENDPOINTS
-------------
GET  /welcome     - Welcome message & health check
POST /chat        - Main chat interface with sessions
POST /rag-query   - Direct RAG query without session
GET  /health      - System health status
GET  /test-redis  - Redis connectivity test
GET  /test-bedrock - AWS Bedrock connectivity test

RAG PIPELINE PROCESS
--------------------
1. User Query Input
2. Text Embedding (HuggingFace Transformers)
3. Vector Search (ChromaDB similarity matching)
4. Context Retrieval (Top-K relevant documents)
5. LLM Generation (AWS Bedrock Claude + Context)
6. Final Response Output

KEY FEATURES
------------
Performance:
- FastAPI async processing
- Vector database optimization
- Redis caching layer
- Nginx load balancing

Security:
- SSL/TLS encryption
- CORS protection
- PII data masking
- AWS IAM integration

Monitoring:
- Comprehensive logging
- Google Sheets analytics
- Health check endpoints
- Automated log rotation

DevOps:
- systemd service management
- Automated deployments
- Cron job maintenance
- Environment configuration

PROJECT HIGHLIGHTS
------------------
✓ Production-Ready: Deployed on AWS EC2 with proper service management
✓ Scalable Architecture: Microservices approach with clear separation
✓ AI-Powered: Advanced RAG implementation with state-of-the-art LLM
✓ Compliance-First: KVKV/GDPR compliant with automated data management
✓ Full-Stack: From infrastructure to AI, comprehensive implementation

COMPLIANCE & SECURITY
---------------------
- KVKV/GDPR compliant logging
- No personal data stored in logs
- Automated log cleanup (90-day retention)
- SSL/TLS encrypted communication
- AWS IAM secure resource access
- Data masking for PII protection
"""
    
    with open('Kartal.AI_Architecture_Simple.txt', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("Created Kartal.AI_Architecture_Simple.txt")

def create_reportlab_pdf():
    """Create a professional PDF using ReportLab"""
    doc = SimpleDocTemplate("Kartal.AI_Architecture.pdf", pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue
    )
    story.append(Paragraph("🤖 Kartal.AI Chatbot - System Architecture", title_style))
    story.append(Spacer(1, 20))
    
    # Project Overview
    story.append(Paragraph("Project Overview", styles['Heading2']))
    overview_text = """
    RAG-based AI chatbot platform for hospitality industry using FastAPI, 
    AWS Bedrock Claude, LlamaIndex, and ChromaDB vector database. 
    Production-ready system with comprehensive security and compliance features.
    """
    story.append(Paragraph(overview_text, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Architecture Components
    story.append(Paragraph("System Components", styles['Heading2']))
    
    components_data = [
        ['Layer', 'Component', 'Technology', 'Purpose'],
        ['Frontend', 'Nginx Proxy', 'Nginx + SSL', 'Reverse proxy, load balancing'],
        ['API', 'FastAPI Backend', 'Python FastAPI', 'REST API, validation'],
        ['AI/ML', 'RAG Pipeline', 'LlamaIndex', 'Query processing'],
        ['AI/ML', 'LLM Service', 'AWS Bedrock Claude', 'Response generation'],
        ['AI/ML', 'Embeddings', 'HuggingFace', 'Text vectorization'],
        ['Data', 'Vector DB', 'ChromaDB', 'Semantic search'],
        ['Data', 'Cache', 'Redis', 'Session management'],
        ['Data', 'Logging', 'Google Sheets', 'Chat analytics'],
        ['Infrastructure', 'Compute', 'AWS EC2', 'Application hosting'],
        ['Infrastructure', 'Service Mgmt', 'systemd', 'Process management']
    ]
    
    components_table = Table(components_data)
    components_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(components_table)
    story.append(Spacer(1, 20))
    
    # API Endpoints
    story.append(Paragraph("API Endpoints", styles['Heading2']))
    
    api_data = [
        ['Endpoint', 'Method', 'Purpose'],
        ['/welcome', 'GET', 'Welcome message & health check'],
        ['/chat', 'POST', 'Main chat interface with sessions'],
        ['/rag-query', 'POST', 'Direct RAG query without session'],
        ['/health', 'GET', 'System health status'],
        ['/test-redis', 'GET', 'Redis connectivity test'],
        ['/test-bedrock', 'GET', 'AWS Bedrock connectivity test']
    ]
    
    api_table = Table(api_data)
    api_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(api_table)
    story.append(PageBreak())
    
    # Technology Stack
    story.append(Paragraph("Technology Stack", styles['Heading2']))
    tech_text = """
    <b>Backend:</b> FastAPI, Python<br/>
    <b>AI/ML:</b> AWS Bedrock Claude, LlamaIndex, HuggingFace<br/>
    <b>Database:</b> ChromaDB (Vector), Redis (Cache)<br/>
    <b>Infrastructure:</b> AWS EC2, Nginx, systemd<br/>
    <b>DevOps:</b> Cron jobs, automated log rotation<br/>
    <b>Testing:</b> pytest, httpx<br/>
    <b>Security:</b> SSL/TLS, CORS, KVKV/GDPR compliance
    """
    story.append(Paragraph(tech_text, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # Key Features
    story.append(Paragraph("Key Features & Benefits", styles['Heading2']))
    features_text = """
    <b>Performance:</b> FastAPI async processing, vector database optimization, Redis caching<br/>
    <b>Security:</b> SSL/TLS encryption, CORS protection, PII data masking<br/>
    <b>Monitoring:</b> Comprehensive logging, Google Sheets analytics, health checks<br/>
    <b>DevOps:</b> systemd service management, automated deployments, maintenance scripts<br/>
    <b>Compliance:</b> KVKV/GDPR compliant with automated data management
    """
    story.append(Paragraph(features_text, styles['Normal']))
    
    # Build PDF
    doc.build(story)
    print("Created Kartal.AI_Architecture.pdf")

if __name__ == "__main__":
    try:
        create_reportlab_pdf()
        print("✅ Professional PDF created successfully!")
    except Exception as e:
        print(f"Error creating PDF: {e}")
        print("Creating simple text version as backup...")
        create_simple_pdf()