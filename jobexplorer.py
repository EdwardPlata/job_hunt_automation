import streamlit as st
import logging
import json
from bs4 import BeautifulSoup
import pandas as pd 

class JobExplorer:
    def __init__(self, filepath,source):
        self.filepath = filepath
        self.source = source
        self.df = self.read_jobs_to_df()
        
    def read_jobs_to_df(self):
            """
            Reads a JSON file containing job listings and returns a Pandas DataFrame
            """
            try:
                with open(self.filepath, "r") as f:
                    jobs = json.load(f)
                # remove the first item from the list
                jobs.pop(0)
                # clean the description of each job using BeautifulSoup
                for job in jobs:
                    soup = BeautifulSoup(job["description"], "lxml")
                    job["description"] = soup.get_text()
                # Create a new column for the source of the job listings
                for job in jobs:
                    job["source"] = self.source
                df = pd.DataFrame(jobs)
                # set the id column as the index of the DataFrame
                df.set_index("id", inplace=True)
                return df
            except FileNotFoundError:
                logging.error(f"{self.filepath} not found.")
                return None
            except json.JSONDecodeError as e:
                logging.error(f"Error decoding JSON: {e}")
                return None
            
    def run_app(self):
        st.set_page_config(page_title="Job Explorer", page_icon=":guardsman:", layout="wide")
        st.title("Explore Job Listings")

        # Create a dropdown to select the company
        if 'company' in self.df.columns:
            company_names = ["All"] + self.df["company"].unique().tolist()
            company_name = st.selectbox("Select company", company_names)
            if company_name == "All":
                filtered_df = self.df
            else:
                filtered_df = self.df[self.df["company"] == company_name]
        else:
            st.warning("Column 'company' not found in DataFrame.")
            filtered_df = self.df

        # Create a range slider to select the salary range
        if 'salary_min' and 'salary_max' in self.df.columns:
            min_salary, max_salary = st.slider("Select salary range (USD)", int(self.df["salary_min"].min()), int(self.df["salary_max"].max()), (int(self.df["salary_min"].min()), int(self.df["salary_max"].max())), step=1000)
            filtered_df = filtered_df[(filtered_df["salary_min"] >= min_salary) & (filtered_df["salary_max"] <= max_salary)]
        else:
            st.warning("Columns 'salary_min' and 'salary_max' not found in DataFrame.")

        # Show the filtered data
        if filtered_df.empty:
                st.warning("No jobs found for the selected criteria.")
        else:
            st.dataframe(filtered_df)



        # # Show the filtered data
        # if filtered_df.empty:
        #     st.warning("No jobs found for the selected criteria.")
        # else:
        #     st.dataframe(filtered_df)


    # def run_app(self):
    #     st.set_page_config(page_title="Job Explorer", page_icon=":guardsman:", layout="wide")
    #     st.title("Explore Job Listings")

    #     # Create a dropdown to select the type of job
    #     job_type = st.selectbox("Select job type", self.df["position"].unique())

    #     # Create a range slider to select salary range
    #     min_salary, max_salary = st.slider("Select salary range (USD)", self.df["salary_min"].min(), self.df["salary_max"].max(), (self.df["salary_min"].min(), self.df["salary_max"].max()))

    #     # Filter the DataFrame based on the selected job type and salary range
    #     filtered_df = self.df[(self.df["position"] == job_type) & (self.df["salary_min"] >= min_salary) & (self.df["salary_max"] <= max_salary)]

    #     # Display the number of jobs matching the selected criteria
    #     st.write(f"{len(filtered_df)} job listings found.")

    #     # Display a summary of the filtered DataFrame
    #     if not filtered_df.empty:
    #         st.dataframe(filtered_df)
