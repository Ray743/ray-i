import shutil
import webbrowser
import requests
from bs4 import BeautifulSoup
import subprocess
import os

HEADERS = {"User-Agent": "Mozilla/5.0"}

# Expanded trusted sites
MOVIE_SITES = [
    "vidsrc.to", "vidplay.net", "123moviesfree.net", "fmovies.to",
    "goku.sx", "cloudstream", "cineb.rs", "flixhq.to", "myflixer", "soap2day", "gdriveplayer.to","tinyzone"
]

LIVE_STREAM_SITES = [
    "youtube.com", "twitch.tv", "m3u8", "stream", "embed", "dailymotion.com",
    "streamsb.net", "watchsport.live"
]


def search_for_stream(query, max_results=10):
    print(f"\n📡 Searching for stream: \033[1m{query}\033[0m\n")
    search_url = f"https://html.duckduckgo.com/html/?q={query}"
    res = requests.post(search_url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")

    results = []
    # Determine intent
    query_lower = query.lower()
    is_movie = any(term in query_lower for term in ["full movie", "watch", "download", "film"])
    is_live = any(term in query_lower for term in ["live", "livestream", "match", "game", "event"])

    for a in soup.select(".result__a", limit=max_results):
        title = a.get_text(strip=True)
        url = a["href"]

        if is_movie and any(site in url for site in MOVIE_SITES):
            results.append((title, url))
        elif is_live and any(site in url for site in LIVE_STREAM_SITES):
            results.append((title, url))
        elif not is_movie and not is_live:
            # fallback: accept any semi-streamable link
            if any(site in url for site in (MOVIE_SITES + LIVE_STREAM_SITES)):
                results.append((title, url))

    return results


def detect_players():
    players = []
    if shutil.which("mpv"):
        players.append("mpv")
    if shutil.which("vlc"):
        players.append("vlc")
    players.append("browser")
    return players


def launch_stream(url):
    players = detect_players()
    print("\n🎮 Choose a player:")
    for i, p in enumerate(players, 1):
        print(f"{i}. {p.upper()}")

    choice = input("👉 Enter number (default 1): ").strip()
    choice = int(choice) if choice.isdigit() and 1 <= int(choice) <= len(players) else 1
    selected = players[choice - 1]

    print(f"\n🚀 Launching with {selected.upper()}...\n")

    try:
        if selected == "mpv":
            subprocess.run(["mpv", url])
        elif selected == "vlc":
            subprocess.run(["vlc", url])
        else:
            webbrowser.open(url)
    except Exception as e:
        print("❌ Failed to launch stream:", e)


def handle_stream(query):
    streams = search_for_stream(query)

    if not streams:
        print("❌ No streamable links found.")
        return

    title, url = streams[0]
    print(f"🎬 Found Stream: \033[92m{title}\033[0m")
    print(f"🔗 Link: {url}")

    confirm = input("\n🎥 Do you want to play this stream? (y/n): ").strip().lower()
    if confirm == "y":
        launch_stream(url)
    else:
        print("❌ Skipped.")
