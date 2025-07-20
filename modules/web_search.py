# rayi_modules/web_search.py

import requests
from bs4 import BeautifulSoup
import re
import google.generativeai as genai
import os

HEADERS = {"User-Agent": "Mozilla/5.0"}

genai.configure(api_key=os.getenv("API_KEY"))  # Use same key from main

def search_web(query, max_results=5):
    print(f"\n🌐 Scanning the web for: \033[1m{query}\033[0m\n")
    url = f"https://html.duckduckgo.com/html/?q={query}"
    res = requests.post(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    results = []
    for a in soup.select(".result__a", limit=max_results):
        link = a["href"]
        title = a.get_text(strip=True)
        results.append((title, link))

    return results

def extract_text_from_url(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=8)
        soup = BeautifulSoup(res.text, "html.parser")
        text = soup.get_text(separator="\n")
        return text[:3000]  # Limit to first 3k chars for summary
    except Exception as e:
        return f"❌ Error extracting: {e}"

def summarize_with_gemini(text):
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(
            f"Summarize this page for a tech-savvy user:\n\n{text[:3000]}"
        )
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Gemini summarization failed: {e}"

def handle_search(query):
    results = search_web(query)

    if not results:
        print("❌ No search results found.")
        return

    for idx, (title, link) in enumerate(results, 1):
        print(f"\n🔹 Result {idx}: \033[94m{title}\033[0m\n🔗 {link}\n")

        article_text = extract_text_from_url(link)
        summary = summarize_with_gemini(article_text)

        print("📝 Summary:")
        print(summary)
        print("-" * 60)
