import json
import urllib.request
from typing import Optional, Dict, Any
from app.config.constants import APP_VERSION

class GitHubService:
    REPO_URL = "https://api.github.com/repos/h08831n/OptiPixel/releases/latest"

    @classmethod
    def check_latest_release(cls) -> Optional[Dict[str, Any]]:
        try:
            req = urllib.request.Request(
                cls.REPO_URL,
                headers={"User-Agent": "OptiPixel-App"}
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    tag_name = data.get("tag_name", "").lstrip("v")
                    return {
                        "tag_name": tag_name,
                        "html_url": data.get("html_url", "https://github.com/h08831n/OptiPixel"),
                        "body": data.get("body", "No release notes available."),
                        "has_update": tag_name > APP_VERSION if tag_name else False
                    }
        except Exception:
            pass
        return None
