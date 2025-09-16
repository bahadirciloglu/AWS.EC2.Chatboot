#!/usr/bin/env python3
"""
Exact 1280x720 Mermaid Diagram Generator
Creates PNG images from all Mermaid diagrams that are exactly 1280x720 pixels
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image, ImageDraw
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

def render_mermaid_to_exact_size(mermaid_code, diagram_name, driver):
    """Render Mermaid diagram to exactly 1280x720 PNG"""
    try:
        # HTML template with fixed dimensions
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
                    padding: 0; 
                    background: white; 
                    width: 1280px;
                    height: 720px;
                    overflow: hidden;
                }}
                .mermaid {{ 
                    width: 1280px !important;
                    height: 720px !important;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }}
                .mermaid svg {{
                    max-width: 1280px !important;
                    max-height: 720px !important;
                    width: 100% !important;
                    height: 100% !important;
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
                    flowchart: {{ 
                        useMaxWidth: true, 
                        htmlLabels: true,
                        width: 1280,
                        height: 720
                    }},
                    graph: {{ 
                        useMaxWidth: true, 
                        htmlLabels: true,
                        width: 1280,
                        height: 720
                    }},
                    sequence: {{ 
                        useMaxWidth: true, 
                        htmlLabels: true,
                        width: 1280,
                        height: 720
                    }},
                    mindmap: {{ 
                        useMaxWidth: true, 
                        htmlLabels: true,
                        width: 1280,
                        height: 720
                    }},
                    gantt: {{ 
                        useMaxWidth: true, 
                        htmlLabels: true,
                        width: 1280,
                        height: 720
                    }}
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
        time.sleep(3)
        
        # Take screenshot of entire page
        screenshot = driver.get_screenshot_as_png()
        
        # Clean up temp file
        os.remove(temp_html)
        
        return screenshot
        
    except Exception as e:
        print(f"❌ {diagram_name} render edilemedi: {e}")
        return None

def force_exact_dimensions(image_data, target_width=1280, target_height=720):
    """Force image to exact dimensions by adding padding or cropping"""
    try:
        # Open image from bytes
        img = Image.open(io.BytesIO(image_data))
        
        # Create new image with exact dimensions
        new_img = Image.new('RGB', (target_width, target_height), 'white')
        
        # Calculate scaling to fit diagram within bounds
        img_width, img_height = img.size
        
        # Calculate scale factor to fit within target dimensions
        scale_x = target_width / img_width
        scale_y = target_height / img_height
        scale = min(scale_x, scale_y)
        
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
        new_img.save(output, format='PNG')
        output.seek(0)
        
        return output.getvalue()
        
    except Exception as e:
        print(f"❌ Boyut dönüştürme hatası: {e}")
        return image_data

def process_mermaid_files():
    """Process all Mermaid files and create exact-size PNG images"""
    print("🎨 AWS.Chatbot Tam 1280x720 Mermaid Diagram Generator")
    print("=" * 60)
    
    # Create output directory
    output_dir = "diagrams_exact_1280x720"
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
            png_data = render_mermaid_to_exact_size(mermaid_content, diagram_name, driver)
            
            if png_data:
                # Force exact dimensions
                final_png = force_exact_dimensions(png_data, 1280, 720)
                
                # Save PNG
                output_path = os.path.join(output_dir, f"{diagram_name}.png")
                with open(output_path, 'wb') as f:
                    f.write(final_png)
                
                # Verify final image dimensions
                final_img = Image.open(io.BytesIO(final_png))
                print(f"✅ {diagram_name}.png oluşturuldu ({final_img.width}x{final_img.height})")
                
                # Check if dimensions are correct
                if final_img.width == 1280 and final_img.height == 720:
                    print(f"   ✅ Boyut tam: 1280x720")
                else:
                    print(f"   ❌ Boyut hala yanlış: {final_img.width}x{final_img.height}")
            else:
                print(f"❌ {diagram_name} PNG oluşturulamadı")
        
        print(f"\n🎉 Tüm diyagramlar tamamlandı!")
        print(f"📁 Çıktı klasörü: {output_dir}")
        print(f"📏 Hedef boyut: 1280x720 pixels (tam)")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    process_mermaid_files() 