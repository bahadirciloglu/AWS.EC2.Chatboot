#!/usr/bin/env python3
"""
Enhanced PDF Generator for Kartal.AI Architecture
Creates a comprehensive, visually appealing PDF document
"""

from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics import renderPDF
import os

def create_enhanced_pdf():
    """Create a comprehensive, professional PDF with enhanced visuals"""
    doc = SimpleDocTemplate("Kartal.AI_Architecture_Enhanced.pdf", pagesize=A4, 
                           topMargin=0.5*inch, bottomMargin=0.5*inch)
    styles = getSampleStyleSheet()
    story = []
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        spaceAfter=30,
        alignment=TA_CENTER,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=20,
        alignment=TA_CENTER,
        textColor=colors.grey,
        fontName='Helvetica-Oblique'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        spaceBefore=20,
        spaceAfter=10,
        textColor=colors.darkblue,
        fontName='Helvetica-Bold'
    )
    
    # Title Page
    story.append(Spacer(1, 1*inch))
    story.append(Paragraph("🤖 Kartal.AI Chatbot", title_style))
    story.append(Paragraph("System Architecture & Technical Documentation", subtitle_style))
    story.append(Spacer(1, 0.5*inch))
    
    # Project summary box
    summary_text = """
    <b>Project Type:</b> RAG-based AI Chatbot Platform<br/>
    <b>Industry:</b> Hospitality & Tourism<br/>
    <b>Architecture:</b> Microservices with AI/ML Pipeline<br/>
    <b>Deployment:</b> AWS Cloud Infrastructure<br/>
    <b>Compliance:</b> KVKV/GDPR Compliant
    """
    
    summary_style = ParagraphStyle(
        'Summary',
        parent=styles['Normal'],
        fontSize=12,
        leading=18,
        leftIndent=20,
        rightIndent=20,
        spaceAfter=20,
        borderWidth=2,
        borderColor=colors.darkblue,
        borderPadding=15,
        backColor=colors.lightblue
    )
    
    story.append(Paragraph(summary_text, summary_style))
    story.append(PageBreak())
    
    # Table of Contents
    story.append(Paragraph("📋 Table of Contents", heading_style))
    toc_data = [
        ["Section", "Page"],
        ["1. System Overview", "3"],
        ["2. Architecture Diagram", "3"],
        ["3. Component Details", "4"],
        ["4. Technology Stack", "5"],
        ["5. API Documentation", "5"],
        ["6. RAG Pipeline Process", "6"],
        ["7. Security & Compliance", "6"],
        ["8. Deployment & DevOps", "7"],
        ["9. Performance Features", "7"]
    ]
    
    toc_table = Table(toc_data, colWidths=[4*inch, 1*inch])
    toc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10)
    ]))
    
    story.append(toc_table)
    story.append(PageBreak())
    
    # 1. System Overview
    story.append(Paragraph("1. 🎯 System Overview", heading_style))
    overview_text = """
    Kartal.AI is a sophisticated RAG (Retrieval Augmented Generation) chatbot platform specifically 
    designed for the hospitality and tourism industry. The system combines cutting-edge AI 
    technologies with robust infrastructure to deliver intelligent, context-aware responses 
    to user queries.
    
    <b>Key Capabilities:</b><br/>
    • Natural language understanding and generation<br/>
    • Context-aware responses using RAG pipeline<br/>
    • Real-time chat with session management<br/>
    • Scalable vector database for knowledge retrieval<br/>
    • Production-ready deployment on AWS infrastructure<br/>
    • GDPR/KVKV compliant data handling
    """
    story.append(Paragraph(overview_text, styles['Normal']))
    story.append(Spacer(1, 20))
    
    # 2. Architecture Diagram (Text-based)
    story.append(Paragraph("2. 🏗️ System Architecture", heading_style))
    
    arch_text = """
    <font name="Courier" size="9">
    ┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐<br/>
    │   User/Client   │───▶│   Nginx Proxy    │───▶│   FastAPI App   │<br/>
    │   (Browser)     │    │  (SSL/HTTPS)     │    │   (Port 8000)   │<br/>
    └─────────────────┘    └──────────────────┘    └─────────────────┘<br/>
                                                             │<br/>
                                                             ▼<br/>
    ┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐<br/>
    │   Google Sheets │◀───│   Agent Module   │───▶│  LlamaIndex RAG │<br/>
    │   (Logging)     │    │  (run_agent)     │    │    Pipeline     │<br/>
    └─────────────────┘    └──────────────────┘    └─────────────────┘<br/>
                                                             │<br/>
                                                             ▼<br/>
    ┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐<br/>
    │   Redis Cache   │◀───│   Session Mgmt   │    │   ChromaDB      │<br/>
    │  (Optional)     │    │   & State        │    │ Vector Store    │<br/>
    └─────────────────┘    └──────────────────┘    └─────────────────┘<br/>
                                                             │<br/>
                                                             ▼<br/>
    ┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐<br/>
    │  HuggingFace    │───▶│   Embeddings     │    │   AWS Bedrock   │<br/>
    │  Transformers   │    │   Processing     │    │   Claude LLM    │<br/>
    └─────────────────┘    └──────────────────┘    └─────────────────┘
    </font>
    """
    story.append(Paragraph(arch_text, styles['Normal']))
    story.append(PageBreak())
    
    # 3. Component Details
    story.append(Paragraph("3. 🔧 Component Details", heading_style))
    
    components_data = [
        ['Layer', 'Component', 'Technology', 'Purpose', 'Key Features'],
        ['Frontend', 'Nginx Proxy', 'Nginx + SSL', 'Reverse proxy, load balancing', 'SSL termination, CORS handling'],
        ['API', 'FastAPI Backend', 'Python FastAPI', 'REST API, validation', 'Async processing, auto docs'],
        ['AI Core', 'RAG Pipeline', 'LlamaIndex', 'Query processing', 'Context retrieval, orchestration'],
        ['AI Core', 'LLM Service', 'AWS Bedrock Claude', 'Response generation', 'Advanced reasoning, multilingual'],
        ['AI Core', 'Embeddings', 'HuggingFace Transformers', 'Text vectorization', 'Semantic understanding'],
        ['Data', 'Vector Database', 'ChromaDB', 'Semantic search', 'Persistent storage, similarity search'],
        ['Data', 'Session Cache', 'Redis', 'State management', 'Fast access, session persistence'],
        ['Data', 'Analytics', 'Google Sheets', 'Chat logging', 'Real-time analytics, easy access'],
        ['Infrastructure', 'Compute', 'AWS EC2', 'Application hosting', 'Scalable, reliable hosting'],
        ['Infrastructure', 'Process Mgmt', 'systemd', 'Service management', 'Auto-restart, logging']
    ]
    
    components_table = Table(components_data, colWidths=[0.8*inch, 1.2*inch, 1.2*inch, 1.3*inch, 1.5*inch])
    components_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))
    
    story.append(components_table)
    story.append(PageBreak())
    
    # 4. Technology Stack
    story.append(Paragraph("4. 💻 Technology Stack", heading_style))
    
    tech_categories = [
        ("Backend Framework", ["FastAPI", "Python 3.9+", "Pydantic", "Uvicorn"]),
        ("AI/ML Technologies", ["AWS Bedrock Claude 3.5", "LlamaIndex", "HuggingFace Transformers", "sentence-transformers"]),
        ("Databases", ["ChromaDB (Vector)", "Redis (Cache)", "Google Sheets (Analytics)"]),
        ("Infrastructure", ["AWS EC2", "Nginx", "systemd", "SSL/TLS"]),
        ("DevOps & Monitoring", ["Cron jobs", "Log rotation", "Health checks", "Environment management"]),
        ("Testing & Quality", ["pytest", "httpx", "Type hints", "API documentation"])
    ]
    
    for category, technologies in tech_categories:
        story.append(Paragraph(f"<b>{category}:</b>", styles['Normal']))
        tech_list = " • ".join(technologies)
        story.append(Paragraph(f"• {tech_list}", styles['Normal']))
        story.append(Spacer(1, 10))
    
    # 5. API Documentation
    story.append(Paragraph("5. 🔌 API Documentation", heading_style))
    
    api_data = [
        ['Endpoint', 'Method', 'Purpose', 'Request Format', 'Response'],
        ['/welcome', 'GET', 'Welcome & health check', 'No body', '{"response": "Welcome message"}'],
        ['/chat', 'POST', 'Main chat interface', '{"user_id", "session_id", "message"}', '{"response", "session_id"}'],
        ['/rag-query', 'POST', 'Direct RAG query', '{"soru": "question"}', '{"yanit": "answer"}'],
        ['/health', 'GET', 'System health status', 'No body', '{"status": "ok"}'],
        ['/test-redis', 'GET', 'Redis connectivity', 'No body', '{"redis": "ok"}'],
        ['/test-bedrock', 'GET', 'Bedrock connectivity', 'No body', '{"bedrock": "ok"}']
    ]
    
    api_table = Table(api_data, colWidths=[1*inch, 0.6*inch, 1.2*inch, 1.4*inch, 1.8*inch])
    api_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'TOP')
    ]))
    
    story.append(api_table)
    story.append(PageBreak())
    
    # 6. RAG Pipeline Process
    story.append(Paragraph("6. 🔄 RAG Pipeline Process", heading_style))
    
    rag_steps = [
        ("1. Query Input", "User submits natural language question"),
        ("2. Text Embedding", "HuggingFace transforms text to vectors using sentence-transformers/all-MiniLM-L6-v2"),
        ("3. Vector Search", "ChromaDB performs semantic similarity search across knowledge base"),
        ("4. Context Retrieval", "Top-K most relevant documents/chunks are retrieved"),
        ("5. Prompt Construction", "Query + retrieved context combined into structured prompt"),
        ("6. LLM Generation", "AWS Bedrock Claude 3.5 Sonnet generates contextual response"),
        ("7. Response Processing", "Output formatting, logging, and session management"),
        ("8. Delivery", "Final response returned to user via FastAPI")
    ]
    
    for step, description in rag_steps:
        story.append(Paragraph(f"<b>{step}:</b> {description}", styles['Normal']))
        story.append(Spacer(1, 8))
    
    # 7. Security & Compliance
    story.append(Paragraph("7. 🔒 Security & Compliance", heading_style))
    
    security_text = """
    <b>Data Protection:</b><br/>
    • KVKV/GDPR compliant data handling<br/>
    • PII masking and removal from logs<br/>
    • Automated log cleanup (90-day retention)<br/>
    • No personal data stored in vector database<br/>
    
    <b>Communication Security:</b><br/>
    • SSL/TLS encryption for all communications<br/>
    • CORS protection for web requests<br/>
    • AWS IAM for secure cloud resource access<br/>
    • Environment-based configuration management<br/>
    
    <b>Operational Security:</b><br/>
    • Health check endpoints for monitoring<br/>
    • Structured logging with no sensitive data<br/>
    • Automated backup and recovery procedures<br/>
    • Service isolation and process management
    """
    story.append(Paragraph(security_text, styles['Normal']))
    story.append(PageBreak())
    
    # 8. Deployment & DevOps
    story.append(Paragraph("8. 🚀 Deployment & DevOps", heading_style))
    
    deployment_text = """
    <b>Infrastructure:</b><br/>
    • AWS EC2 instance with Ubuntu/Amazon Linux<br/>
    • Nginx reverse proxy with SSL certificate<br/>
    • systemd service management for reliability<br/>
    • Environment variable configuration<br/>
    
    <b>Automation:</b><br/>
    • Cron jobs for automated maintenance<br/>
    • Log rotation and cleanup scripts<br/>
    • Health monitoring and alerting<br/>
    • Automated service restart on failure<br/>
    
    <b>Monitoring & Logging:</b><br/>
    • Comprehensive application logging<br/>
    • Google Sheets integration for analytics<br/>
    • System health check endpoints<br/>
    • Performance metrics collection
    """
    story.append(Paragraph(deployment_text, styles['Normal']))
    
    # 9. Performance Features
    story.append(Paragraph("9. ⚡ Performance Features", heading_style))
    
    performance_data = [
        ['Feature', 'Technology', 'Benefit'],
        ['Async Processing', 'FastAPI async/await', 'High concurrency, non-blocking I/O'],
        ['Vector Search', 'ChromaDB optimization', 'Fast semantic similarity matching'],
        ['Session Caching', 'Redis in-memory store', 'Quick session state retrieval'],
        ['Load Balancing', 'Nginx upstream', 'Distributed request handling'],
        ['Connection Pooling', 'Database connections', 'Efficient resource utilization'],
        ['Response Caching', 'Application-level cache', 'Reduced API response times'],
        ['Embedding Cache', 'Vector storage', 'Avoid re-computation of embeddings']
    ]
    
    performance_table = Table(performance_data, colWidths=[1.5*inch, 2*inch, 2.5*inch])
    performance_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.purple),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lavender),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 9)
    ]))
    
    story.append(performance_table)
    story.append(Spacer(1, 20))
    
    # Project Highlights
    highlights_style = ParagraphStyle(
        'Highlights',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        leftIndent=15,
        rightIndent=15,
        spaceAfter=15,
        borderWidth=2,
        borderColor=colors.green,
        borderPadding=12,
        backColor=colors.lightgreen
    )
    
    highlights_text = """
    <b>🎯 Project Highlights:</b><br/>
    ✓ <b>Production-Ready:</b> Deployed on AWS EC2 with proper service management<br/>
    ✓ <b>Scalable Architecture:</b> Microservices approach with clear separation of concerns<br/>
    ✓ <b>AI-Powered:</b> Advanced RAG implementation with state-of-the-art LLM<br/>
    ✓ <b>Compliance-First:</b> KVKV/GDPR compliant with automated data management<br/>
    ✓ <b>Full-Stack Expertise:</b> From infrastructure to AI, comprehensive technical implementation<br/>
    ✓ <b>Industry-Focused:</b> Specialized for hospitality and tourism sector requirements
    """
    
    story.append(Paragraph(highlights_text, highlights_style))
    
    # Build PDF
    doc.build(story)
    print("✅ Enhanced PDF created: Kartal.AI_Architecture_Enhanced.pdf")

if __name__ == "__main__":
    create_enhanced_pdf()