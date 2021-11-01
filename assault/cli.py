from typing import TextIO

import click
import sys
import json

from .http import assault
from .stats import Results


@click.command()
@click.option("--requests", "-r", default=500, help="Number of requests")
@click.option("--concurrency", "-c", default=1, help='Number of concurrent requests')
@click.option("--json-file", '-j', default=None, help="Path to output json file")
@click.argument("url")
def cli(requests, concurrency, json_file, url):
    print(f"Requests: {requests}")
    print(f"Concurrency: {concurrency}")
    print(f"Json file: {json_file}")
    print(f"Url: {url}")

    output_file = None
    if json_file:
        print(f"We're writing to {json_file}")
        try:
            output_file = open(json_file, 'w')
        except:
            print(f"Unable to open json_file {json_file}")
            sys.exit(1)

    total_time, requests_dict = assault(url, requests, concurrency)
    results = Results(total_time, requests_dict)

    def display(results: Results, output_file: TextIO):
        if json_file:
            json.dump({
                "Successful_requests": results.successful_requests(),
                 "Slowest": results.slowest(),
                 "Fastest": results.fastest(),
                 "total_time": results.total_time,
                 "Request_per_second": results.requests_per_second(),
                 "Request_per_minute: ": results.requests_per_minute()
            }, output_file)

        else:
            print('-----')
            print(f"Successful requests     \t{results.successful_requests()}")
            print(f"Slowest                 \t{results.slowest()}")
            print(f"Fastest                 \t{results.fastest()}")
            print(f"Total time:             \t{results.total_time}")
            print(f"Requests per minute:    \t{results.requests_per_minute()}")
            print(f"Request per second:     \t{results.requests_per_second()}")

            print('------------')

    display(results, output_file)


if __name__ == "__main__":
    cli()
