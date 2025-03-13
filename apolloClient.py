# apollo_client.py
import requests
import logging
import json

APOLLO_PORTAL_URL = "http://apollo-portal-dev.htx.com"

# 配置日志
logging.basicConfig(filename='apollo_client.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class ApolloClient:
    def __init__(self, portal_url=APOLLO_PORTAL_URL):
        self.portal_url = portal_url
        logging.info("ApolloClient initialized with URL: %s", self.portal_url)

    def get_config(self, namespace):
        url = f"{self.portal_url}/configs/{namespace}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            logging.info("Fetched config for namespace: %s", namespace)
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error("Error fetching config: %s", e)
            return {"error": "Namespace not found"}

    def update_config(self, namespace, data):
        url = f"{self.portal_url}/configs/{namespace}"
        try:
            response = requests.post(url, json=data, timeout=5)
            response.raise_for_status()
            logging.info("Updated config for namespace: %s", namespace)
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error("Error updating config: %s", e)
            return {"error": "Failed to update config"}

    def get_all_namespaces(self):
        url = f"{self.portal_url}/namespaces"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            logging.info("Fetched all namespaces")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error("Error fetching namespaces: %s", e)
            return {"error": "Failed to fetch namespaces"}

    def get_release_info(self, namespace):
        url = f"{self.portal_url}/releases/latest/{namespace}"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            logging.info("Fetched latest release for namespace: %s", namespace)
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error("Error fetching release info: %s", e)
            return {"error": "Failed to fetch release info"}

if __name__ == "__main__":
    client = ApolloClient()
    namespace = "application"
    
    print("Fetching all namespaces...")
    print(json.dumps(client.get_all_namespaces(), indent=4))
    
    print("Fetching configuration...")
    print(json.dumps(client.get_config(namespace), indent=4))
    
    print("Fetching latest release info...")
    print(json.dumps(client.get_release_info(namespace), indent=4))
    
    print("Attempting to update configuration...")
    update_data = {"key": "test", "value": "12345"}
    print(json.dumps(client.update_config(namespace, update_data), indent=4))

