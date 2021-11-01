from typing import List, Dict
from statistics import mean


class Results:
    """
    Results handles calculating statistics based on a list of requests that were made.
    Here is an example of what the information wil look like:


    Successful requests     3000
    Slowest                 0.010s
    Fastest                 0.001s
    Average                 0.003s
    Total time              2.400s
    Requests Per Minute     90000
    Requests Per Second     1250


    """

    def __init__(self, total_time: float, requests: List[Dict]):
        self.total_time = total_time
        self.requests = sorted(requests, key=lambda r: r["request_time"])

    def slowest(self) -> float:
        """
        Returns the slowest request completion time

        >>> results = Results(10.6, [{ 'status_code': 200, 'request_time': 3.4},{ 'status_code': 500, 'request_time': 6.1}, { 'status_code': 200, 'request_time': 1.04} ])
        >>> results.slowest()
        6.1
        """
        return self.requests[-1]["request_time"]

    def fastest(self) -> float:
        """
                Returns the fastest request completion time

                >>> results = Results(10.6, [{ 'status_code': 200, 'request_time': 3.4},{ 'status_code': 500, 'request_time': 6.1}, { 'status_code': 200, 'request_time': 1.04} ])
                >>> results.fastest()
                1.04
        """
        return self.requests[0]['request_time']

    def average_time(self) -> float:
        """
            Returns the avarage request completion time

            >>> results = Results(10.6, [{ 'status_code': 200, 'request_time': 3.4},{ 'status_code': 500, 'request_time': 6.1}, { 'status_code': 200, 'request_time': 1.04} ])
            >>> results.average_time()
            3.51
        """
        return round(mean(r["request_time"] for r in self.requests), 2)

    def successful_requests(self) -> int:
        """
            Returns the avarage request completion time

            >>> results = Results(10.6, [{
            ...    'status_code': 200,
            ...    'request_time': 3.4
            ... },
            ... {
            ...    'status_code': 500,
            ...     'request_time': 6.1
            ... },
            ... {
            ...    'status_code': 200,
            ...    'request_time':1.04
            ... }])

            >>> results.successful_requests()
            2
        """
        return len([request for request in self.requests if request['status_code'] in range(200, 299)])

    def requests_per_minute(self) -> float:
        """
            Returns the avarage request completion time

            >>> results = Results(10.6, [{ 'status_code': 200, 'request_time': 3.4},{ 'status_code': 500, 'request_time': 6.1}, { 'status_code': 200, 'request_time': 1.04} ])
            >>> results.requests_per_minute()
            0.05
        """
        return round(len(self.requests) / 60, 2)

    def requests_per_second(self) -> float:
        """
            Returns the avarage request completion time

            >>> results = Results(10.6, [{ 'status_code': 200, 'request_time': 3.4},{ 'status_code': 500, 'request_time': 6.1}, { 'status_code': 200, 'request_time': 1.04} ])
            >>> results.requests_per_second()
            0.28
        """
        return round(len(self.requests) / self.total_time, 2)
