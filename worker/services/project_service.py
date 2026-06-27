import requests
from loguru import logger
from config.settings import settings

class ProjectService:
    def __init__(self):
        self.base_url = f"{settings.API_BASE_URL}/projects"
        
    def get_by_id(self, project_id: str) -> dict:
        url = f"{self.base_url}/{project_id}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get project {project_id}: {e}")
            return {}

    def update(self, project_id: str, data: dict) -> dict:
        url = f"{self.base_url}/{project_id}"
        try:
            response = requests.patch(url, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to update project {project_id}: {e}")
            return {}

project_service = ProjectService()
