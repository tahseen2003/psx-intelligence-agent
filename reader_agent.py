# =====================================================
#  📄 READER AGENT — Multi-Source Data Reader
#  Reads TXT, CSV, JSON files and URLs
#  Auto-detects format and handles errors
# =====================================================

import csv
import json
import os
import requests
from bs4 import BeautifulSoup


def read_txt(filepath):
    """Read a plain text file and return its content."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        print(f"  ✅ TXT file loaded: {os.path.basename(filepath)}")
        return content
    except FileNotFoundError:
        print(f"  ❌ File not found: {filepath}")
        return f"[ERROR] File not found: {filepath}"
    except Exception as e:
        print(f"  ❌ Error reading TXT: {e}")
        return f"[ERROR] Could not read file: {e}"


def read_csv(filepath):
    """Read a CSV file and return it as formatted text."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            rows = list(reader)

        if not rows:
            return "[ERROR] CSV file is empty"

        # Format header
        header = rows[0]
        result = "| " + " | ".join(header) + " |\n"
        result += "| " + " | ".join(["---"] * len(header)) + " |\n"

        # Format data rows
        for row in rows[1:]:
            result += "| " + " | ".join(row) + " |\n"

        print(f"  ✅ CSV file loaded: {os.path.basename(filepath)} ({len(rows)-1} rows)")
        return result
    except FileNotFoundError:
        print(f"  ❌ File not found: {filepath}")
        return f"[ERROR] File not found: {filepath}"
    except Exception as e:
        print(f"  ❌ Error reading CSV: {e}")
        return f"[ERROR] Could not read CSV: {e}"


def read_json(filepath):
    """Read a JSON file and return it as formatted text."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        content = json.dumps(data, indent=2, ensure_ascii=False)
        print(f"  ✅ JSON file loaded: {os.path.basename(filepath)}")
        return content
    except FileNotFoundError:
        print(f"  ❌ File not found: {filepath}")
        return f"[ERROR] File not found: {filepath}"
    except json.JSONDecodeError:
        print(f"  ❌ Invalid JSON format: {filepath}")
        return f"[ERROR] Invalid JSON format in {filepath}"
    except Exception as e:
        print(f"  ❌ Error reading JSON: {e}")
        return f"[ERROR] Could not read JSON: {e}"


def read_url(url):
    """Scrape text content from a URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script and style tags
        for tag in soup(["script", "style"]):
            tag.decompose()

        # Get text from paragraphs
        paragraphs = soup.find_all("p")
        content = "\n".join([p.get_text().strip() for p in paragraphs[:20]])

        if not content:
            content = soup.get_text()[:2000]

        print(f"  ✅ URL loaded: {url[:50]}...")
        return content
    except requests.exceptions.Timeout:
        print(f"  ❌ URL timeout: {url}")
        return f"[ERROR] Request timed out for {url}"
    except requests.exceptions.RequestException as e:
        print(f"  ❌ URL error: {e}")
        return f"[ERROR] Could not fetch URL: {e}"


def detect_format(source):
    """Auto-detect the format of a source (txt, csv, json, or url)."""
    if source.startswith("http://") or source.startswith("https://"):
        return "url"

    # Get file extension
    ext = os.path.splitext(source)[1].lower()

    if ext == ".csv":
        return "csv"
    elif ext == ".json":
        return "json"
    elif ext in [".txt", ".text", ".md", ".log"]:
        return "txt"
    else:
        # Default to txt for unknown formats
        return "txt"


def read_all_sources(source_list):
    """
    Master function: reads all sources with auto-detection.

    Args:
        source_list: list of file paths or URLs

    Returns:
        list of dicts: [{"name": "filename", "content": "text"}, ...]
    """
    print("\n📄 READER AGENT — Processing Sources")
    print("=" * 45)

    results = []

    for source in source_list:
        # Get display name
        if source.startswith("http"):
            name = source[:60]
        else:
            name = os.path.basename(source)

        # Auto-detect and read
        fmt = detect_format(source)
        print(f"\n  📂 Reading: {name} (format: {fmt})")

        if fmt == "csv":
            content = read_csv(source)
        elif fmt == "json":
            content = read_json(source)
        elif fmt == "url":
            content = read_url(source)
        else:
            content = read_txt(source)

        results.append({
            "name": name,
            "format": fmt,
            "content": content
        })

    print(f"\n✅ Total sources processed: {len(results)}")
    print("=" * 45)

    return results


# ── TEST ──────────────────────────────────────────
if __name__ == "__main__":
    # Test with our sample data files
    sources = [
        "data/psx_market_report.txt",
        "data/psx_stock_data.csv",
        "data/psx_news_article.txt"
    ]

    results = read_all_sources(sources)

    for r in results:
        print(f"\n{'='*50}")
        print(f"📄 Source: {r['name']} ({r['format']})")
        print(f"{'='*50}")
        print(r["content"][:300] + "...")
