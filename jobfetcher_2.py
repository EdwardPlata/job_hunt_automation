import requests
import logging
import time
from requests.adapters import Retry, HTTPAdapter
from bs4 import BeautifulSoup

class JobFetcher:
    def __init__(self, timeout=5, retries=3):
        self.timeout = timeout
        self.retries = retries

    def fetch_jobs_from_remoteok(timeout=5, retries=3):
        """
        Fetch remote job listings using the RemoteOK API.
        """
        start_time = time.time()
        session = requests.Session()
        retry = Retry(total=retries,
                    backoff_factor=0.1,
                    status_forcelist=[ 500, 502, 503, 504 ])
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        try:
            url = "https://remoteok.io/api"
            jobs = make_api_call(session, url, timeout)
            log_jobs_info(jobs, start_time)
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

    def make_api_call(session, url, timeout):
        """
        Makes an API call and returns the response in json format
        """
        logging.info("Fetching jobs from RemoteOK...")
        response = session.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()

    def log_jobs_info(jobs, start_time):
        """
        Logs the number of jobs fetched and the time taken
        """
        logging.info(f"{len(jobs)} jobs fetched")
        end_time = time.time()
        logging.info(f'Time Taken: {round(end_time - start_time, 2)} seconds')
        
    def fetch_remote_poc(self):
        url = "https://remotepoc.com"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        jobs = soup.find_all("div", class_="job")
        job_list = []
        for job in jobs:
            title = job.find("h2").text
            company = job.find("h3").text
            location = job.find("span", class_="location").text
            link = job.find("a")["href"]
            job_list.append({"title": title, "company": company, "location": location, "link": link, "source": "RemotePOC"})

        self.log_jobs_info(job_list)
        self.save_jobs_to_json(job_list, "remotepoc")