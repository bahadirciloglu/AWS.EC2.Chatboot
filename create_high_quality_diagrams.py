#!/usr/bin/env python3
"""
High-Quality Mermaid Diagram Generator
Creates PNG images from all Mermaid diagrams using web rendering
"""

import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import io
import base64

def create_chrome_driver():
    """Create Chrome driver with headless options"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1280,720")  # 1280x720 boyutunda
    chrome_options.add_argument("--force-device-scale-factor=1")  # Normal DPI
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"Chrome driver oluşturulamadı: {e}")
        return None

def render_mermaid_to_png(mermaid_code, diagram_name, driver):
    """Render Mermaid diagram to PNG using web browser"""
    try:
        # HTML template with Mermaid
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{diagram_name}</title>
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
                    text-align: center; 
                    width: 100%;
                    height: 100%;
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
                    flowchart: {{ useMaxWidth: false, htmlLabels: true }},
                    graph: {{ useMaxWidth: false, htmlLabels: true }},
                    sequence: {{ useMaxWidth: false, htmlLabels: true }},
                    mindmap: {{ useMaxWidth: false, htmlLabels: true }},
                    gantt: {{ useMaxWidth: false, htmlLabels: true }}
                }});
            </script>
        </body>
        </html>
        """
        
        # Save HTML to temporary file
        temp_html = f"temp_{diagram_name}.html"
        with open(temp_html, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Load in browser
        driver.get(f"file://{os.path.abspath(temp_html)}")
        
        # Wait for Mermaid to render
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "mermaid"))
        )
        
        # Additional wait for rendering
        time.sleep(2)
        
        # Find the diagram element
        diagram_element = driver.find_element(By.CLASS_NAME, "mermaid")
        
        # Get screenshot
        screenshot = diagram_element.screenshot_as_png
        
        # Clean up temp file
        os.remove(temp_html)
        
        return screenshot
        
    except Exception as e:
        print(f"❌ {diagram_name} render edilemedi: {e}")
        return None

def process_mermaid_files():
    """Process all Mermaid files and create PNG images"""
    print("🎨 Kartal.AI 1280x720 Mermaid Diagram Generator")
    print("=" * 50)
    
    # Create output directory
    output_dir = "diagrams_1280x720"
    os.makedirs(output_dir, exist_ok=True)
    
    # Get Chrome driver
    driver = create_chrome_driver()
    if not driver:
        print("❌ Chrome driver bulunamadı. Lütfen Chrome yükleyin.")
        return
    
    try:
        # Process each Mermaid file
        mermaid_files = [f for f in os.listdir("mermaid_output") if f.endswith('.mmd')]
        mermaid_files.sort()
        
        print(f"📁 {len(mermaid_files)} Mermaid dosyası bulundu")
        
        for i, filename in enumerate(mermaid_files, 1):
            filepath = os.path.join("mermaid_output", filename)
            
            # Read Mermaid content
            with open(filepath, 'r', encoding='utf-8') as f:
                mermaid_content = f.read()
            
            # Extract diagram name
            diagram_name = filename.replace('.mmd', '')
            
            print(f"\n🔄 [{i}/{len(mermaid_files)}] {diagram_name} işleniyor...")
            
            # Render to PNG
            png_data = render_mermaid_to_png(mermaid_content, diagram_name, driver)
            
            if png_data:
                # Save PNG
                output_path = os.path.join(output_dir, f"{diagram_name}.png")
                with open(output_path, 'wb') as f:
                    f.write(png_data)
                
                # Get image info
                img = Image.open(io.BytesIO(png_data))
                print(f"✅ {diagram_name}.png oluşturuldu ({img.width}x{img.height})")
            else:
                print(f"❌ {diagram_name} PNG oluşturulamadı")
        
        print(f"\n🎉 Tüm diyagramlar tamamlandı!")
        print(f"📁 Çıktı klasörü: {output_dir}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    process_mermaid_files() 