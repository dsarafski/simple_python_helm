from prometheus_client import start_http_server, Summary, Gauge
import random
import time
import requests

# Create a metric to track time spent and requests made.
CHECK_STATUS_CODE = Gauge('sample_external_url_up', 'Check if url is up', ['url'])
REQUEST_TIME = Summary('sample_external_url_response_ms', 'Time spent processing request', ['url'])


# Function for querying url 200
def query_200():
    url_200 = "https://httpstat.us/200"
    response = requests.get(url_200).status_code
    if response == 200:
        CHECK_STATUS_CODE.labels('https://httpstat.us/200').set(1)
    else:
        CHECK_STATUS_CODE.labels('https://httpstat.us/200').set(0)
        print('You receive different code than 200')
    print(response)


# Function for querying url 503
def query_503():
    url_503 = "https://httpstat.us/503"
    response1 = requests.get(url_503).status_code
    CHECK_STATUS_CODE.labels('https://httpstat.us/503').set(0)
    print(response1)


# Decorate functions with metric.
def process_request(t):
    # CHECK_STATUS_CODE.labels('https://httpstat.us/200').set(1)
    start_time = time.time()
    query_200()
    req_time_count = (time.time() - start_time) * 1000
    REQUEST_TIME.labels('https://httpstat.us/200').observe(req_time_count)


def process_request_503(t):
    # CHECK_STATUS_CODE.labels('https://httpstat.us/503').set(0)
    start_time = time.time()
    query_503()
    req_time_count = (time.time() - start_time) * 1000
    REQUEST_TIME.labels('https://httpstat.us/503').observe(req_time_count)


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8081)
    # Generate some requests.
    while True:
        time.sleep(10)
        process_request(random.random())
        process_request_503(random.random())
