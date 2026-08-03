from app.services.github_service import GitHubService

class UpdateService:
    def __init__(self):
        self.github_service = GitHubService()

    def check_for_updates(self):
        return self.github_service.check_latest_release()
