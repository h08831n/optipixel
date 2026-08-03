from typing import Optional, Dict, Any
from app.config.constants import APP_VERSION

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

class GitHubService:
    REPO_URL = "https://api.github.com/repos/ahaninja/OptiPixel/releases/latest"

    @classmethod
    def check_latest_release(cls) -> Optional[Dict[str, Any]]:
        if not HAS_REQUESTS:
            return None
        try:
            res = requests.get(cls.REPO_URL, timeout=5)
            if res.status_code == 200:
                data = res.json()
                tag_name = data.get("tag_name", "").lstrip("v")
                return {
                    "tag_name": tag_name,
                    "html_url": data.get("html_url", "https://github.com/ahaninja/OptiPixel"),
                    "body": data.get("body", "No release notes available."),
                    "has_update": tag_name > APP_VERSION if tag_name else False
                }
        except Exception:
            pass
        return None
