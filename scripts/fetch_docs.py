import os
import requests
from bs4 import BeautifulSoup

DOCS_MAP = {
    "streamlit": "https://docs.streamlit.io/get-started/fundamentals/main-concepts",
    "fastapi": "https://fastapi.tiangolo.com/tutorial/first-steps/",
    "transformers": "https://huggingface.co/docs/transformers/quicktour",
    "whisper": "https://github.com/openai/whisper" # GitHub genelde HTML döner, metni ayıklamak yeter.
}

TARGET_DIR = "Knowledge/API_References"

def fetch_and_save(name, url):
    print(f"📚 Fetching docs for: {name}...")
    headers = {'User-Agent': 'Mozilla/5.0'} # Bazı siteler botları engeller
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Ana metni al (basitçe body, script/style hariç)
            for script in soup(["script", "style"]):
                script.extract()
                
            text = soup.get_text(separator='\n', strip=True)
            
            # Kaydet
            path = os.path.join(TARGET_DIR, f"{name}_docs.md")
            os.makedirs(TARGET_DIR, exist_ok=True)
            
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"# {name.upper()} DOCUMENTATION\n")
                f.write(f"Source: {url}\n\n")
                f.write(text[:50000]) # Çok uzunsa kes (Token limiti)
                
            print(f"✅ Saved to {path}")
        else:
            print(f"❌ Failed to fetch {url}: {response.status_code}")
    except Exception as e:
        print(f"❌ Error fetching {name}: {e}")

if __name__ == "__main__":
    for name, url in DOCS_MAP.items():
        fetch_and_save(name, url)