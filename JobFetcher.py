#Indeed Job Scraper
#Z6Z_^#nb]V2ylhfi - Password for gcp db
import requests
import logging
import time
from requests.adapters import Retry, HTTPAdapter


logging.basicConfig(level=logging.INFO)

class JobFetcher:
    def __init__(self, timeout=5, retries=3):
        self.timeout = timeout
        self.retries = retries
        
    def fetch_jobs_from_remoteok(self, search, location, sort, remote, timeout=5, retries=3):
        """
        Fetch remote job listings using the RemoteOK API.
        This function makes a GET request to the RemoteOK API to retrieve a list of remote job listings.
        It takes 2 optional parameters:
            timeout (int): The number of seconds to wait for a response from the API before timing out (default: 5).
            retries (int): The number of times to retry the request in case of failure (default: 3).
        It returns a list of job listings in JSON format, or None if the request fails.
        """
        # Log that the script is running
        logging.info("Fetching jobs from RemoteOK...")
        start_time = time.time()
        session = requests.Session()
        # retry
        retry = Retry(total=retries,
                      backoff_factor=0.1,
                      status_forcelist=[ 500, 502, 503, 504 ])
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        try:
            # Log the parameters being passed
            logging.debug(f"Search: {search}, Location: {location}, Sort: {sort}, Remote: {remote}")
            # The parameters for the API call
            params = {
                "search": search,
                "location": location,
                "sort": sort,
                "remote": remote
            }
            # Make the API call
            url = "https://remoteok.io/api"
            response = session.get(url, timeout=timeout)
            response.raise_for_status()
            # Log the number of jobs fetched
            jobs = response.json()
            logging.info(f"{len(jobs)} jobs fetched")
            end_time = time.time()
            logging.info(f'Time Taken: {round(end_time - start_time, 2)} seconds')
            # Return the results
            return jobs
        except requests.exceptions.HTTPError as errh:
            logging.error("HTTP Error:",errh)
        except requests.exceptions.ConnectionError as errc:
            logging.error("Error Connecting:",errc)
        except requests.exceptions.Timeout as errt:
            logging.error("Timeout Error:",errt)
        except requests.exceptions.RequestException as err:
            logging.error("Something went wrong",err)
        return None

