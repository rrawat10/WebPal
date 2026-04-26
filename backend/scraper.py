import trafilatura

def scrape_url(url: str) -> str:

    downloaded = trafilatura.fetch_url(url)

    if not downloaded:
        return ""

    text = trafilatura.extract(
        downloaded,
        include_comments=False,
        include_tables=True,
        include_links=False
    )

    return text or ""