import requests
from bs4 import BeautifulSoup


class ForumParser:
    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.headers = {
            "User-Agent": self.USER_AGENT,
            "Accept-Language": "en-US,en;q=0.9,ru;q=0.8",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        }

    def fetch(self, url: str) -> str:
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        response.raise_for_status()
        return response.text

    def parse_html(self, html: str):
        soup = BeautifulSoup(html, "lxml")
        parsed = []
        for node in soup.select("[data-comment-id]"):
            raw_id = node.get("data-comment-id")
            try:
                comment_id = int(raw_id)
            except (TypeError, ValueError):
                continue

            name_el = node.select_one(".username")
            content_el = node.select_one(".content")
            if name_el is None or content_el is None:
                continue

            name = name_el.get_text(strip=True)
            message = content_el.decode_contents().strip()
            if not name or not message:
                continue

            parsed.append(
                {"id": comment_id, "name": name, "message": message}
            )
        return parsed

    def parse_page(self, url: str):
        return self.parse_html(self.fetch(url))

    def save_to_db(self, parsed_data, repository):
        saved = 0
        for item in parsed_data:
            repository.add(item["id"], item["name"], item["message"])
            saved += 1
        return saved
