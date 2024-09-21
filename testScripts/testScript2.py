import requests
import concurrent.futures
import time


url = 'http://localhost:5000/Proto1.html' 

# send HTTP requests to the adminvote route
def send_requests(num_requests):
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(requests.get, url) for _ in range(num_requests)]

        # Wait for all the futures to complete
        for future in concurrent.futures.as_completed(futures):
            try:
                # Retrieve the result of each future (this will raise an exception if the function raised one)
                future.result().raise_for_status()
            except Exception as e:
                print(f"Error: {e}")
    end_time = time.time()
    return end_time - start_time, num_requests


min_concurrency = 1
max_concurrency = 50  

# Simulate increasing concurrency levels and measure response times
for concurrency in range(min_concurrency, max_concurrency + 1):
    response_time, num_requests = send_requests(concurrency)
    throughput = num_requests / response_time if response_time > 0 else 0
    print(f"Concurrency: {concurrency}, Response Time: {response_time:.2f} seconds, Throughput: {throughput:.2f} requests/second")
