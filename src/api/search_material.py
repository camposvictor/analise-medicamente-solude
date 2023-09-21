from api.api_service import api_service
from urllib.parse import quote  

def search_material(material):
    response = api_service.get(f'search?Material={quote(material)}')
    return response