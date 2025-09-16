#!/usr/bin/env python3
"""
API Diagram Only Generator
Creates only the API endpoints diagram in 1280x720 size
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import io

def create_chrome_driver():
    """Create Chrome driver with headless options"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1280,720")
    chrome_options.add_argument("--force-device-scale-factor=1")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Chrome driver oluşturulamadı: {e}")
        return None

def render_api_diagram():
    """Render only the API diagram to 1280x720 PNG"""
    try:
        # API Endpoints diagram content
        mermaid_code = """graph TD
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
    style Health fill:#ff9800,color:#fff"""
        
        # HTML template optimized for API diagram
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>API Endpoints Diagram</title>
            <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
            <style>
                body {{ 
                    margin: 0; 
                    padding: 20px; 
                    background: white; 
                    width: 1280px;
                    height: 720px;
                    overflow: hidden;
                }}
                .mermaid {{ 
                    width: 100%;
                    height: 100%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}
                .mermaid svg {{
                    max-width: 100% !important;
                    max-height: 100% !important;
                }}
            </style>
        </head>
        <body>
            <div class="mermaid">
                {mermaid_code}
            </div>
            <script>
                mermaid.initialize({{
                    startOnLoad: true,
                    theme: 'default',
                    graph: {{ 
                        useMaxWidth: true, 
                        htmlLabels: true,
                        width: 1200,
                        height: 600
                    }}
                }});
            </script>
        </body>
        </html>
        """
        
        # Save HTML to temporary file
        temp_html = "temp_api_diagram.html"
        with open(temp_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Get Chrome driver
        driver = create_chrome_driver()
        if not driver:
            print("❌ Chrome driver bulunamadı.")
            return None
        
        try:
            # Load in browser
            driver.get(f"file://{os.path.abspath(temp_html)}")
            
            # Wait for Mermaid to render
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "mermaid"))
            )
            
            # Additional wait for rendering
            time.sleep(3)
            
            # Take screenshot of entire page
            screenshot = driver.get_screenshot_as_png()
            
            return screenshot
            
        finally:
            driver.quit()
        
    except Exception as e:
        print(f"❌ API diagram render edilemedi: {e}")
        return None

def main():
    """Main function to create API diagram"""
    print("🎨 AWS.Chatbot API Diagram Generator (1280x720)")
    print("=" * 50)
    
    # Create output directory
    output_dir = "api_diagram_1280x720"
    os.makedirs(output_dir, exist_ok=True)
    
    print("🔄 API diagram render ediliyor...")
    
    # Render API diagram
    png_data = render_api_diagram()
    
    if png_data:
        # Save PNG
        output_path = os.path.join(output_dir, "API_Endpoints_Diagram.png")
        with open(output_path, 'wb') as f:
            f.write(png_data)
        
        # Verify image dimensions
        img = Image.open(io.BytesIO(png_data))
        print(f"✅ API diagram oluşturuldu ({img.width}x{img.height})")
        
        # Check if dimensions are correct
        if img.width == 1280 and img.height == 720:
            print(f"   ✅ Boyut doğru: 1280x720")
        else:
            print(f"   ⚠️  Boyut farklı: {img.width}x{img.height}")
        
        print(f"📁 Çıktı dosyası: {output_path}")
        
        # Clean up temp file
        if os.path.exists("temp_api_diagram.html"):
            os.remove("temp_api_diagram.html")
            
    else:
        print("❌ API diagram oluşturulamadı")

if __name__ == "__main__":
    main() 