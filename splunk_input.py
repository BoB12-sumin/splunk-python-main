import json
import logging
import requests
import urllib3

# SSL Warning 제거
urllib3.disable_warnings()

with open("./conf/conf.json", "r", encoding="utf-8") as mainconf:
    conf = json.load(mainconf)

SPLUNK_SERVER = conf["splunk"]["server"]
SPLUNK_HEC_TOKEN = conf["splunk"]["token"]
SPLUNK_HEADER = {"Authorization": "Splunk " + SPLUNK_HEC_TOKEN}
SPLUNK_HEC_URL = f"http://{SPLUNK_SERVER}:8088/services/collector/raw"

session = requests.Session()


def input_splunk(input_data, filepath=None, num_requests=100):
    """Splunk HEC Input"""
    try:
        if filepath:
            with open(filepath, "r", encoding="utf-8") as input_file:
                input_data = json.load(input_file)

        for _ in range(num_requests):
            response = session.post(
                SPLUNK_HEC_URL,
                data=json.dumps(input_data),
                verify=False,
                headers=SPLUNK_HEADER,
                timeout=10,
            )
            if response.status_code == 200:
                logging.info("Data sent successfully to Splunk HEC.")
            else:
                logging.error(f"Error sending data to Splunk HEC: {response.content}")

        return True

    except Exception as error:
        logging.error(error)
        return False


if __name__ == "__main__":
    test_dict = {"_time": "", "index": "bob12", "msg": "Test 100"}
    input_splunk(test_dict, num_requests=100)
