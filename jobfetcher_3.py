#job_fetcher_3.py
import requests
import logging
import time
import json
import datetime
from requests.adapters import Retry, HTTPAdapter
from bs4 import BeautifulSoup


class JobFetcher:
    def __init__(self, timeout=5, retries=3):
        self.timeout = timeout
        self.retries = retries
    def fetch_jobs(self):
        start_time = time.time()
        session = requests.Session()
        retry = Retry(total=self.retries,
                      backoff_factor=0.1,
                      status_forcelist=[ 500, 502, 503, 504 ])
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        try:
            url = "https://remoteok.io/api"
            jobs = self.make_api_call(session, url, self.timeout)
            self.log_jobs_info(jobs, start_time)
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

    def make_api_call(self, session, url, timeout):
        """
        Makes an API call and returns the response in json format
        """
        logging.info("Fetching jobs from RemoteOK...")
        response = session.get(url, timeout=timeout)
        response.raise_for_status()
        return response.json()
    def save_to_json(self, data, filename):
        with open(f'{filename}.json', 'w') as outfile:
            json.dump(data, outfile)

    # def log_jobs_info(self,jobs, start_time):
    #     """
    #     Logs the number of jobs fetched and the time taken
    #     """
    #     logging.info(f"{len(jobs)} jobs fetched")
    #     end_time = time.time()
    #     logging.info(f'Time Taken: {round(end_time - start_time, 2)} seconds')
        
    def read_jobs_to_df(filepath):
        """
        Reads a JSON file containing job listings and returns a Pandas DataFrame
        """
        try:
            with open(filepath, "r") as f:
                jobs = json.load(f)
            # remove the first item from the list
            jobs.pop(0)
            # clean the description of each job using BeautifulSoup
            for job in jobs:
                soup = BeautifulSoup(job["description"], "lxml")
                job["description"] = soup.get_text()
            df = pd.DataFrame(jobs)
            return df
        except FileNotFoundError:
            logging.error(f"{filepath} not found.")
            return None
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON: {e}")
            return None
    
    def fetch_remote_poc(self):
        links = []
        response = self.make_api_call("remotepoc.com")
        soup = BeautifulSoup(response.text, "html.parser")
        # Find all links in the textwidget
        for link in soup.select("div.textwidget a[href*='::before'] ~ a[href*='::after']"):
            links.append(link.get("href"))
        # Remove duplicates
        links = list(set(links))
        jobs_data = []
        for link in links:
            job_response = self.make_api_call(link)
            job_soup = BeautifulSoup(job_response.text, "html.parser")
            title = job_soup.find("h1", class_="job_title").text
            company = job_soup.find("a", class_="company").text
            location = job_soup.find("div", class_="job_location").text
            tags = [tag.text for tag in job_soup.find_all("a", class_="job_tag")]
            link = link
            source = "remotepoc.com"
            jobs_data.append({"title": title, "company": company, "location": location, "tags": tags, "link": link, "source": source})
        #self.save_to_json(jobs_data, "remotepoc.com")
        return jobs_data

    
    def fetch_angel_co(self):
        website_name = "angel.co"
        start_time = datetime.now()

        # Make the API call to angel.co
        url = "https://api.angel.co/1/jobs"
        params = {"page": 1}
        response = requests.get(url, params=params)
        jobs_data = response.json()["jobs"]

        # Loop through the pages of results
        while "next" in response.json()["links"]:
            params["page"] += 1
            response = requests.get(url, params=params)
            jobs_data += response.json()["jobs"]

        # Tag the positions with the website name and position type
        for job in jobs_data:
            job["source"] = website_name
            job["tags"] = [job["job_type"]]

        self.log_jobs_info(len(jobs_data), start_time)
        self.save_to_json(jobs_data, website_name)
        return jobs_data
    
# Configure logging
# logging.basicConfig(level=logging.INFO)

# job_fetcher = JobFetcher()
# jobs = job_fetcher.fetch_jobs()

# if jobs:
#     # Do something with the job listings
#     print(jobs)
# else:
#     print("Failed to fetch job listings.")
