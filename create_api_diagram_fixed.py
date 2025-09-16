#!/usr/bin/env python3
"""
API Diagram Fixed Size Generator
Creates the API endpoints diagram in exactly 1280x720 size
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

def render_api_diagram_fixed():
    """Render API diagram to exactly 1280x720 PNG"""
    try:
        # API Endpoints diagram content - optimized for 1280x720
        mermaid_code = """graph TD
    API[🔌 FastAPI Application<br/>AWS.Chatbot Chatbot] --> Welcome[GET /welcome<br/>💚 Health Check]
    API --> Chat[POST /chat<br/>💬 Main Chat Interface]
    API --> RAGQuery[POST /rag-query<br/>🔍 Direct RAG Query]
    API --> Health[GET /health<br/>❤️ System Status]
    API --> TestRedis[GET /test-redis<br/>⚡ Redis Test]
    API --> TestBedrock[GET /test-bedrock<br/>☁️ Bedrock Test]
    
    Chat --> SessionMgmt[👥 Session Management<br/>User Sessions]
    Chat --> Logging[📝 Interaction Logging<br/>Chat History]
    
    RAGQuery --> DirectRAG[🧠 Direct RAG Processing<br/>Vector Search]
    
    Health --> SystemCheck[⚙️ System Health Check<br/>Service Status]
    TestRedis --> RedisConn[⚡ Redis Connection Test<br/>Cache Status]
    TestBedrock --> BedrockConn[☁️ AWS Bedrock Test<br/>LLM Status]
    
    style API fill:#2196f3,color:#fff,stroke:#1976d2,stroke-width:3px
    style Chat fill:#4caf50,color:#fff,stroke:#388e3c,stroke-width:2px
    style RAGQuery fill:#9c27b0,color:#fff,stroke:#7b1fa2,stroke-width:2px
    style Health fill:#ff9800,color:#fff,stroke:#f57c00,stroke-width:2px
    style Welcome fill:#e91e63,color:#fff
    style TestRedis fill:#607d8b,color:#fff
    style TestBedrock fill:#795548,color:#fff"""
        
        # HTML template with fixed dimensions
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>API Endpoints Diagram - AWS.Chatbot</title>
            <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
            <style>
                body {{ 
                    margin: 0; 
                    padding: 0; 
                    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
                    width: 1280px;
                    height: 720px;
                    overflow: hidden;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }}
                .mermaid {{ 
                    width: 1280px !important;
                    height: 720px !important;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}
                .mermaid svg {{
                    width: 1280px !important;
                    height: 720px !important;
                }}
                .header {{
                    position: absolute;
                    top: 20px;
                    left: 20px;
                    right: 20px;
                    text-align: center;
                    color: #333;
                    font-size: 24px;
                    font-weight: bold;
                    z-index: 1000;
                }}
            </style>
        </head>
        <body>
            <div class="header">🔌 AWS.Chatbot Chatbot - API Endpoints</div>
            <div class="mermaid">
                {mermaid_code}
            </div>
            <script>
                mermaid.initialize({{
                    startOnLoad: true,
                    theme: 'default',
                    graph: {{ 
                        useMaxWidth: false, 
                        htmlLabels: true,
                        width: 1280,
                        height: 720,
                        nodeSpacing: 50,
                        rankSpacing: 50
                    }}
                }});
            </script>
        </body>
        </html>
        """
        
        # Save HTML to temporary file
        temp_html = "temp_api_diagram_fixed.html"
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

def force_exact_dimensions(image_data, target_width=1280, target_height=720):
    """Force image to exact dimensions"""
    try:
        # Open image from bytes
        img = Image.open(io.BytesIO(image_data))
        
        # Create new image with exact dimensions
        new_img = Image.new('RGB', (target_width, target_height), '#f5f7fa')
        
        # Calculate scaling to fit diagram within bounds
        img_width, img_height = img.size
        
        # Calculate scale factor to fit within target dimensions
        scale_x = target_width / img_width
        scale_y = target_height / img_height
        scale = min(scale_x, scale_y) * 0.9  # 90% to add some padding
        
        # Calculate new dimensions
        new_width = int(img_width * scale)
        new_height = int(img_height * scale)
        
        # Resize image
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Calculate position to center the image
        x_offset = (target_width - new_width) // 2
        y_offset = (target_height - new_height) // 2
        
        # Paste resized image onto new canvas
        new_img.paste(resized_img, (x_offset, y_offset))
        
        # Convert to bytes
        output = io.BytesIO()
        new_img.save(output, format='PNG', optimize=True)
        output.seek(0)
        
        return output.getvalue()
        
    except Exception as e:
        print(f"❌ Boyut dönüştürme hatası: {e}")
        return image_data

def main():
    """Main function to create fixed-size API diagram"""
    print("🎨 AWS.Chatbot API Diagram Generator (Tam 1280x720)")
    print("=" * 55)
    
    # Create output directory
    output_dir = "api_diagram_exact_1280x720"
    os.makedirs(output_dir, exist_ok=True)
    
    print("🔄 API diagram render ediliyor...")
    
    # Render API diagram
    png_data = render_api_diagram_fixed()
    
    if png_data:
        # Force exact dimensions
        final_png = force_exact_dimensions(png_data, 1280, 720)
        
        # Save PNG
        output_path = os.path.join(output_dir, "API_Endpoints_Diagram_1280x720.png")
        with open(output_path, 'wb') as f:
            f.write(final_png)
        
        # Verify final image dimensions
        final_img = Image.open(io.BytesIO(final_png))
        print(f"✅ API diagram oluşturuldu ({final_img.width}x{final_img.height})")
        
        # Check if dimensions are correct
        if final_img.width == 1280 and final_img.height == 720:
            print(f"   ✅ Boyut tam: 1280x720")
        else:
            print(f"   ❌ Boyut hala yanlış: {final_img.width}x{final_img.height}")
        
        print(f"📁 Çıktı dosyası: {output_path}")
        
        # Clean up temp file
        if os.path.exists("temp_api_diagram_fixed.html"):
            os.remove("temp_api_diagram_fixed.html")
            
    else:
        print("❌ API diagram oluşturulamadı")

if __name__ == "__main__":
    main() 