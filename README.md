### Job Board Automation
This is a simple automation tool for job boards. The tool includes two classes, JobFetcher and JobExplorer. The JobFetcher class is used to scrape job listings from various job boards, while the JobExplorer class is used to explore and filter the scraped data.

### Getting Started
To use this tool, you will need to have Python and the following packages installed: pandas, requests, and beautifulsoup4.

#### JobFetcher
The JobFetcher class is used to scrape job listings from various job boards. Currently, the class includes methods for scraping job listings from remotepoc.com and angel.co. The scraped data is saved in json format.

#### JobExplorer
The JobExplorer class is used to explore and filter the scraped data. You can use this class to filter job listings by job type, company, location, and salary range. The class also includes a method for displaying the filtered data in a Streamlit app.

### Using the tool
To use the tool, you will need to run the main function. This function imports the JobFetcher and JobExplorer classes and calls the appropriate methods.

#### Copy code
"""
if __name__ == "__main__":
    main()
"""
Once the main function is run, the scraped data will be saved in json format and can then be explored using the JobExplorer class.

Authors
Your Name - Initial work - Your Github
License
This project is licensed under the MIT License - see the LICENSE.md file for details

Acknowledgments
Hat tip to anyone whose code was used
Inspiration
etc



