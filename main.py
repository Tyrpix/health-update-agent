import random

import requests
from datetime import datetime
import time
import json

POLLING_TIME = 10

# Gets Json data from API
def get_data():
    response = requests.get('http://localhost:9018/health-indicators/indicators?sort=asc')
    print(response)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to get Data")


# Gets saved data from json file
def get_previous_data() -> dict:
    try:
        with open("data.json", "r") as f:
            return json.load(f)

    except IOError:
        return {}


# Replicates live changes
def replicate_changes(previous_data) -> dict:
    dict_to_list = list(previous_data.items())
    for i in range(5):
        random_entry = list(random.choice(dict_to_list))
        random_entry[1] = random.randint(1, 20) * 5
        previous_data[random_entry[0]] = random_entry[1]
    return previous_data


# Compares Data from API with saved Data and returns differences
def compare_data(current, previous) -> list:

    changes = []

    for i in current:
        # Only interested in Services
        if i.get('repoType') == "Service":

            service_name = i.get('repoName')
            current_score = i.get('overallScore')
            previous_score = previous.get(service_name)

            if previous_score != current_score and previous_score is not None:
                changes.append(payload(service_name, previous_score, current_score))

    return changes


# Saves the data from the API
def save_data(current):
    new_history = {}
    with open("data.json", "w") as f:
        for i in current:
            service_name = i.get('repoName')
            overall_score = i.get('overallScore')
            new_history[service_name] = overall_score
        json.dump(new_history, f)


def payload(service_name, previous_score, current_score) -> dict:
    now = datetime.now()
    api_data = {
        "service": service_name,
        "date": now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z",
        "environment": "production",
        "eventType": "health-update",
        "message": "Health changed from {} to {}".format(current_score, previous_score)
    }
    return api_data


# Send Single Event
def send_to_timeline(event):
    api_url = "http://localhost:2000/catalogue-timeline/insert"
    requests.post(url=api_url, json=event)


if __name__ == '__main__':
    while True:
        try:
            current = get_data()
            data = get_previous_data()
            previous = replicate_changes(data)

            if len(previous) > 0:
                changes = compare_data(current, previous)

                for c in changes:
                    print("Sending to timeline {}".format(c))
                    send_to_timeline(c)
            save_data(current)  # current becomes new history so the next run will work

        except Exception as ex:
            print(ex)
        time.sleep(POLLING_TIME)
