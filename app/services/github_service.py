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
                    html_url = data.get("html_url", "https://github.com/h08831n/OptiPixel")
                    installer_url = None
                    for asset in data.get("assets", []):
                        name = asset.get("name", "")
                        if "Setup" in name or name.endswith(".exe"):
                            installer_url = asset.get("browser_download_url")
                            break

                    return {
                        "tag_name": tag_name,
                        "html_url": html_url,
                        "installer_url": installer_url or html_url,
                        "body": data.get("body", "No release notes available."),
                        "has_update": tag_name > APP_VERSION if tag_name else False
                    }
        except Exception:
            pass
        return None
