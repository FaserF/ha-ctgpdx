import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re

async def main():
    # Test cases
    test_texts = [
        "Latest Release If the link above doesn't work, try this one instead (Google Drive). Version: 1. 1.1 Download size : 3.86 GB Unpacked s ize: 4.52 GB",
        "VERSION: 1.2.3b DOWNLOAD   SIZE: 1.5 GB UNPACKED SIZE: 2.0 gb",
        "Version: 1.1.1 Download site",
    ]

    # regex = r"(?i:Version:)\s*([\d\.a-z\s]+?)(?=\s+[A-Z]|$)"
    regex = r"(?i:Version:)\s*([\d\.a-z\s]+?)(?=\s+[A-Z]|$)"

    print("--- EXTRACTION ATTEMPTS ---")
    for text in test_texts:
        print(f"Text: {text}")
        match = re.search(regex, text)
        if match:
            v = match.group(1).replace(" ", "").strip()
            print(f"  Result: '{v}'")
        else:
            print("  Result: FAILED")

if __name__ == "__main__":
    asyncio.run(main())
