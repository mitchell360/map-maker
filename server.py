import os
import asyncio
from flask import Flask, request, send_file, Response
from playwright.async_api import async_playwright
from io import BytesIO

CHROMIUM_PATH = '/nix/store/qa9cnw4v5xkxyip6mb9kxqfq1z4x2dx1-chromium-138.0.7204.100/bin/chromium'

app = Flask(__name__, static_folder='.', static_url_path='')

REPLIT_DOMAIN = os.environ.get('REPLIT_DEV_DOMAIN', 'localhost:5000')
BASE_URL = f"https://{REPLIT_DOMAIN}" if REPLIT_DOMAIN != 'localhost:5000' else 'http://localhost:5000'

@app.route('/')
def serve_index():
    return app.send_static_file('index.html')

@app.route('/llm.md')
def serve_llm():
    return app.send_static_file('llm.md')

@app.route('/screenshot')
def screenshot():
    query_string = request.query_string.decode('utf-8')
    
    if not query_string:
        query_string = ''
    
    map_url = f"{BASE_URL}/index.html?{query_string}" if query_string else f"{BASE_URL}/index.html"
    
    width = request.args.get('width', 1200, type=int)
    height = request.args.get('height', 800, type=int)
    
    width = min(max(width, 400), 2000)
    height = min(max(height, 300), 1500)
    
    try:
        screenshot_bytes = asyncio.run(capture_screenshot(map_url, width, height))
        return Response(screenshot_bytes, mimetype='image/png')
    except Exception as e:
        return Response(f"Screenshot failed: {str(e)}", status=500, mimetype='text/plain')

async def capture_screenshot(url, width, height):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, executable_path=CHROMIUM_PATH)
        page = await browser.new_page(viewport={'width': width, 'height': height})
        
        await page.goto(url, wait_until='networkidle')
        
        await page.wait_for_function('''() => {
            const overlay = document.getElementById('loadingOverlay');
            return !overlay || overlay.style.display === 'none';
        }''', timeout=30000)
        
        await page.wait_for_timeout(2000)
        
        screenshot = await page.screenshot(type='png', full_page=False)
        
        await browser.close()
        
        return screenshot

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
