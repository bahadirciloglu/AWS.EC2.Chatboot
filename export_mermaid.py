#!/usr/bin/env python3
"""
Mermaid Diagram Exporter
Mermaid diagramlarını PNG formatına çevirir
"""

import os
import subprocess
import json

def check_mermaid_cli():
    """Mermaid CLI'nin yüklü olup olmadığını kontrol et"""
    try:
        result = subprocess.run(['mmdc', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Mermaid CLI bulundu: {result.stdout.strip()}")
            return True
        else:
            print("❌ Mermaid CLI bulunamadı")
            return False
    except FileNotFoundError:
        print("❌ Mermaid CLI yüklü değil")
        return False

def install_mermaid_cli():
    """Mermaid CLI'yi yükle"""
    print("📦 Mermaid CLI yükleniyor...")
    try:
        # npm ile global yükleme
        result = subprocess.run(['npm', 'install', '-g', '@mermaid-js/mermaid-cli'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Mermaid CLI başarıyla yüklendi")
            return True
        else:
            print(f"❌ Yükleme hatası: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ npm bulunamadı. Node.js yüklü olduğundan emin olun.")
        return False

def extract_mermaid_diagrams():
    """Markdown dosyasından Mermaid diagramlarını çıkar"""
    diagrams = []
    
    with open('mermaid_diagrams.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Mermaid code block'larını bul
    import re
    pattern = r'```mermaid\n(.*?)\n```'
    matches = re.findall(pattern, content, re.DOTALL)
    
    for i, match in enumerate(matches, 1):
        diagram_name = f"diagram_{i}"
        
        # Diagram türünü belirle
        if 'graph TB' in match or 'graph TD' in match:
            diagram_name = f"architecture_{i}"
        elif 'flowchart' in match:
            diagram_name = f"flowchart_{i}"
        elif 'sequenceDiagram' in match:
            diagram_name = f"sequence_{i}"
        elif 'mindmap' in match:
            diagram_name = f"mindmap_{i}"
        
        diagrams.append({
            'name': diagram_name,
            'content': match.strip()
        })
    
    return diagrams

def create_mermaid_files(diagrams):
    """Her diagram için ayrı .mmd dosyası oluştur"""
    os.makedirs('mermaid_output', exist_ok=True)
    
    for diagram in diagrams:
        filename = f"mermaid_output/{diagram['name']}.mmd"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(diagram['content'])
        print(f"📝 Oluşturuldu: {filename}")

def export_to_png(diagrams):
    """Mermaid diagramlarını PNG'ye çevir"""
    if not check_mermaid_cli():
        print("🔧 Mermaid CLI yüklemeye çalışılıyor...")
        if not install_mermaid_cli():
            print("❌ Mermaid CLI yüklenemedi. Manuel yükleme gerekli:")
            print("   npm install -g @mermaid-js/mermaid-cli")
            return False
    
    success_count = 0
    
    for diagram in diagrams:
        input_file = f"mermaid_output/{diagram['name']}.mmd"
        output_file = f"mermaid_output/{diagram['name']}.png"
        
        try:
            # Mermaid CLI ile PNG'ye çevir
            cmd = [
                'mmdc',
                '-i', input_file,
                '-o', output_file,
                '-t', 'default',
                '--width', '1200',
                '--height', '800',
                '--backgroundColor', 'white'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ PNG oluşturuldu: {output_file}")
                success_count += 1
            else:
                print(f"❌ Hata ({diagram['name']}): {result.stderr}")
                
        except Exception as e:
            print(f"❌ Exception ({diagram['name']}): {e}")
    
    print(f"\n🎉 {success_count}/{len(diagrams)} diagram başarıyla PNG'ye çevrildi")
    return success_count > 0

def create_html_preview():
    """Tüm diagramları içeren HTML önizleme oluştur"""
    html_content = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AWS.Chatbot Chatbot - Mermaid Diagrams</title>
    <script src="https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js"></script>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #34495e;
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-top: 40px;
        }
        .diagram-container {
            margin: 30px 0;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 8px;
            background: #fafafa;
        }
        .mermaid {
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 AWS.Chatbot Chatbot - System Diagrams</h1>
        
        <h2>1. System Architecture</h2>
        <div class="diagram-container">
            <div class="mermaid">
graph TB
    User[👤 User/Client<br/>Browser] --> Nginx[🔒 Nginx Proxy<br/>SSL/HTTPS]
    Nginx --> FastAPI[⚡ FastAPI Backend<br/>Port 8000]
    
    FastAPI --> Agent[🤖 Agent Module<br/>run_agent]
    Agent --> RAG[🧠 LlamaIndex<br/>RAG Pipeline]
    
    RAG --> Embed[🔤 HuggingFace<br/>Embeddings]
    RAG --> Vector[🗄️ ChromaDB<br/>Vector Store]
    RAG --> LLM[☁️ AWS Bedrock<br/>Claude LLM]
    
    Agent --> Redis[(⚡ Redis Cache<br/>Sessions)]
    Agent --> Sheets[📊 Google Sheets<br/>Logging]
    
    FastAPI --> Health[💚 Health Checks]
    
    subgraph "AI/ML Layer"
        Embed
        Vector
        LLM
        RAG
    end
    
    subgraph "Data Layer"
        Redis
        Vector
        Sheets
    end
    
    subgraph "Infrastructure"
        Nginx
        FastAPI
        Health
    end
    
    style User fill:#e1f5fe
    style Nginx fill:#fff3e0
    style FastAPI fill:#e8f5e8
    style Agent fill:#f3e5f5
    style RAG fill:#f3e5f5
    style Embed fill:#e1f5fe
    style Vector fill:#fff9c4
    style LLM fill:#e1f5fe
    style Redis fill:#ffebee
    style Sheets fill:#e8f5e8
            </div>
        </div>
        
        <h2>2. RAG Pipeline Flow</h2>
        <div class="diagram-container">
            <div class="mermaid">
flowchart TD
    Start([🚀 User Query]) --> Validate{✅ Validate Input}
    Validate -->|Valid| Embed[🔤 Generate Embeddings<br/>HuggingFace Transformers]
    Validate -->|Invalid| Error[❌ Return Error]
    
    Embed --> Search[🔍 Vector Search<br/>ChromaDB Similarity]
    Search --> Retrieve[📚 Retrieve Context<br/>Top-K Documents]
    
    Retrieve --> Construct[🔧 Construct Prompt<br/>Query + Context]
    Construct --> Generate[🤖 LLM Generation<br/>AWS Bedrock Claude]
    
    Generate --> Process[⚙️ Process Response<br/>Format & Validate]
    Process --> Log[📝 Log Interaction<br/>Google Sheets]
    
    Log --> Cache[💾 Cache Session<br/>Redis Storage]
    Cache --> Return([📤 Return Response])
    
    Error --> Return
    
    style Start fill:#4caf50,color:#fff
    style Return fill:#2196f3,color:#fff
    style Error fill:#f44336,color:#fff
    style Generate fill:#9c27b0,color:#fff
            </div>
        </div>
        
        <h2>3. API Endpoints</h2>
        <div class="diagram-container">
            <div class="mermaid">
graph TD
    API[🔌 FastAPI Application] --> Welcome[GET /welcome<br/>💚 Health Check]
    API --> Chat[POST /chat<br/>💬 Main Chat Interface]
    API --> RAGQuery[POST /rag-query<br/>🔍 Direct RAG Query]
    API --> Health[GET /health<br/>❤️ System Status]
    API --> TestRedis[GET /test-redis<br/>⚡ Redis Test]
    API --> TestBedrock[GET /test-bedrock<br/>☁️ Bedrock Test]
    
    Chat --> SessionMgmt[👥 Session Management]
    Chat --> Logging[📝 Interaction Logging]
    
    RAGQuery --> DirectRAG[🧠 Direct RAG Processing]
    
    Health --> SystemCheck[⚙️ System Health Check]
    TestRedis --> RedisConn[⚡ Redis Connection Test]
    TestBedrock --> BedrockConn[☁️ AWS Bedrock Test]
    
    style API fill:#2196f3,color:#fff
    style Chat fill:#4caf50,color:#fff
    style RAGQuery fill:#9c27b0,color:#fff
    style Health fill:#ff9800,color:#fff
            </div>
        </div>
    </div>
    
    <script>
        mermaid.initialize({ 
            startOnLoad: true,
            theme: 'default',
            themeVariables: {
                primaryColor: '#3498db',
                primaryTextColor: '#2c3e50',
                primaryBorderColor: '#2980b9',
                lineColor: '#34495e'
            }
        });
    </script>
</body>
</html>
"""
    
    with open('mermaid_preview.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ HTML önizleme oluşturuldu: mermaid_preview.html")

def main():
    print("🎨 AWS.Chatbot Mermaid Diagram Exporter")
    print("=" * 40)
    
    # Mermaid diagramlarını çıkar
    print("📖 Markdown dosyasından diagramlar çıkarılıyor...")
    diagrams = extract_mermaid_diagrams()
    print(f"✅ {len(diagrams)} diagram bulundu")
    
    # .mmd dosyalarını oluştur
    print("\n📝 Mermaid dosyaları oluşturuluyor...")
    create_mermaid_files(diagrams)
    
    # PNG'ye çevir
    print("\n🖼️ PNG dosyaları oluşturuluyor...")
    export_success = export_to_png(diagrams)
    
    # HTML önizleme oluştur
    print("\n🌐 HTML önizleme oluşturuluyor...")
    create_html_preview()
    
    print("\n" + "=" * 40)
    print("🎉 İşlem tamamlandı!")
    print("\n📁 Oluşturulan dosyalar:")
    print("   • mermaid_output/ klasöründe .mmd ve .png dosyaları")
    print("   • mermaid_preview.html - Tarayıcıda açılabilir önizleme")
    
    if export_success:
        print("\n💡 Portfolio için PNG dosyalarını kullanabilirsin!")
    else:
        print("\n💡 PNG oluşturulamadı, HTML önizlemeyi kullan!")
        print("   Tarayıcıda mermaid_preview.html'i aç ve screenshot al")

if __name__ == "__main__":
    main()