#!/usr/bin/env python3
"""
System Diagram Test Generator
Creates the system architecture diagram in 1280x720 size for testing
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

def render_system_diagram():
    """Render system architecture diagram to 1280x720 PNG"""
    try:
        # System Architecture diagram content - optimized for 1280x720
        mermaid_code = """graph TB
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
    style Sheets fill:#e8f5e8"""
        
        # HTML template with fixed dimensions
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>System Architecture Diagram - AWS.Chatbot</title>
            <script src="https://cdn.jsdelivr.net/npm/mermaid@10.6.1/dist/mermaid.min.js"></script>
            <style>
                body {{ 
                    margin: 0; 
                    padding: 0; 
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
                    color: white;
                    font-size: 28px;
                    font-weight: bold;
                    z-index: 1000;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
                }}
            </style>
        </head>
        <body>
            <div class="header">🏗️ AWS.Chatbot Chatbot - System Architecture</div>
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
                        nodeSpacing: 40,
                        rankSpacing: 40
                    }}
                }});
            </script>
        </body>
        </html>
        """
        
        # Save HTML to temporary file
        temp_html = "temp_system_diagram.html"
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
        print(f"❌ System diagram render edilemedi: {e}")
        return None

def force_exact_dimensions(image_data, target_width=1280, target_height=720):
    """Force image to exact dimensions"""
    try:
        # Open image from bytes
        img = Image.open(io.BytesIO(image_data))
        
        # Create new image with exact dimensions
        new_img = Image.new('RGB', (target_width, target_height), '#667eea')
        
        # Calculate scaling to fit diagram within bounds
        img_width, img_height = img.size
        
        # Calculate scale factor to fit within target dimensions
        scale_x = target_width / img_width
        scale_y = target_height / img_height
        scale = min(scale_x, scale_y) * 0.85  # 85% to add some padding
        
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
    """Main function to create system diagram"""
    print("🏗️ AWS.Chatbot System Diagram Test Generator (1280x720)")
    print("=" * 60)
    
    # Create output directory
    output_dir = "system_diagram_test_1280x720"
    os.makedirs(output_dir, exist_ok=True)
    
    print("🔄 System diagram render ediliyor...")
    
    # Render system diagram
    png_data = render_system_diagram()
    
    if png_data:
        # Force exact dimensions
        final_png = force_exact_dimensions(png_data, 1280, 720)
        
        # Save PNG
        output_path = os.path.join(output_dir, "System_Architecture_Diagram_1280x720.png")
        with open(output_path, 'wb') as f:
            f.write(final_png)
        
        # Verify final image dimensions
        final_img = Image.open(io.BytesIO(final_png))
        print(f"✅ System diagram oluşturuldu ({final_img.width}x{final_img.height})")
        
        # Check if dimensions are correct
        if final_img.width == 1280 and final_img.height == 720:
            print(f"   ✅ Boyut tam: 1280x720")
        else:
            print(f"   ❌ Boyut hala yanlış: {final_img.width}x{final_img.height}")
        
        print(f"📁 Çıktı dosyası: {output_path}")
        
        # Clean up temp file
        if os.path.exists("temp_system_diagram.html"):
            os.remove("temp_system_diagram.html")
            
    else:
        print("❌ System diagram oluşturulamadı")

if __name__ == "__main__":
    main() 