# Health Update Agent

Retrieves health information for microservices from the health-indicators API.

## Description

- Polls the health-indicators API to replicate live microservice health updates. 
- Most recent data is
compared with previously retrieved data, to check for changes in a microservice's health.
- Sends POST requests to the timeline API to monitor health updates.


## Getting Started

### Dependencies
- Python 3
- [Requests](https://docs.python-requests.org/en/latest/)
- [catalogue-timeline](https://github.com/hmrc/catalogue-timeline)
- health-indicators API




### Installation
- pip install requests

### Usage
Run the application, and it will poll the health-indicators API and check for health updates for all microservices.

Polling time intervals can be changed with the variable POLLING_TIME.
