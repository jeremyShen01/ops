# apollo_sync.py
import requests
import json
import time
import logging

# 配置 Apollo 服务器地址
APOLLO_PORTAL_URL = "http://apollo-portal-dev.htx.com"
NAMESPACE = "application"
SYNC_INTERVAL = 30  # 每 30 秒同步一次

# 配置日志
logging.basicConfig(filename='apollo_sync.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_apollo_config():
    """ 从 Apollo 获取最新配置 """
    url = f"{APOLLO_PORTAL_URL}/configs/{NAMESPACE}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        config_data = response.json()
        logging.info("Fetched config: %s", json.dumps(config_data, indent=4))
        return config_data
    except requests.exceptions.RequestException as e:
        logging.error("Failed to fetch config: %s", e)
        return None

def save_config_to_file(config_data):
    """ 将配置写入本地 JSON 文件 """
    with open("apollo_config_cache.json", "w") as f:
        json.dump(config_data, f, indent=4)
        logging.info("Saved config to local cache")

def sync_loop():
    """ 持续同步 Apollo 配置 """
    while True:
        logging.info("Starting new sync cycle...")
        config = fetch_apollo_config()
        if config:
            save_config_to_file(config)
        logging.info("Sync cycle completed, waiting for next cycle...")
        time.sleep(SYNC_INTERVAL)

if __name__ == "__main__":
    logging.info("Apollo Sync Service Started")
    sync_loop()
