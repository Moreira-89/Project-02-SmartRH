from typing import Dict, Any
import requests
import json


class FirebaseAPI:
    def __init__(self, database_url: str, secret_key: str):
        self.base_url = database_url.rstrip('/')
        self.secret = secret_key
    
    def _request(self, method: str, path: str, data: Dict[str, Any] = None):
        """Método interno para requisições"""
        url = f"{self.base_url}/{path}.json?auth={self.secret}"
        headers = {'Content-Type': 'application/json'}
        
        response = requests.request(
            method,
            url,
            data=json.dumps(data),
            headers=headers
        )
        response.raise_for_status()
        return response.json() if response.text else None
    
    def create_document(self, collection: str, doc_id: str, data: Dict[str, Any]):
        """
        Cria/Atualiza um documento com ID customizado
        - Substitui totalmente o documento se já existir
        """
        return self._request(method="PUT", path=f"{collection}/{doc_id}", data=data)
    
    def get_document(self, collection: str, doc_id: str = None) -> Dict[str, Any]:
        """Obtém um documento específico"""
        path = collection if doc_id is None else f"{collection}/{doc_id}"
        data = self._request("GET", path)
        
        if doc_id is None and data is None:
            return {} 
        return data

    def delete_document(self, collection: str, doc_id: str):
        """Remove um documento"""
        return self._request(method="DELETE", path=f"{collection}/{doc_id}")
            
