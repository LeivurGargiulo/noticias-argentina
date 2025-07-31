from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def get_news_with_browser():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.argentina.gob.ar/noticias")
        await page.wait_for_selector("a[href*='/noticia']", timeout=10000)
        content = await page.content()
        await browser.close()

    soup = BeautifulSoup(content, "html.parser")
    news = []

    for a in soup.select("a[href*='/noticia']"):
        title = a.get_text(strip=True)
        href = a["href"]
        description = ""

        parent = a.find_parent()
        if parent:
            sibling_texts = parent.find_all(["p", "span", "div"], recursive=False)
            for s in sibling_texts:
                if s != a and len(s.get_text(strip=True)) > 20:
                    description = s.get_text(strip=True)
                    break

        if href.startswith("/"):
            href = "https://www.argentina.gob.ar" + href

        if title and href:
            news.append((title, description, href))

    return news
