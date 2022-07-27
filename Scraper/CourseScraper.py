import pandas as pd
import re

from Scraper.Scraper import Scraper

class CourseScraper(Scraper):
    def __init__(self, email, password):
        super().__init__(email, password)
        self.link = "/curriculums"

        self.df = pd.DataFrame({
            # Curriculum fields
            'curriculum_name': [], 
            'curriculum_id': [],
            'organization': [],
            'cip': [], 
            'catalog_year': [], 
            'date_created': [],

            # Course fields
            'course_id': [],
            'course_name': [],
            'prefix': [],
            'number': [],
            'prerequisite': [],
            'corequisite': [],
            'strict_corequisite': [],
            'credit_hours': [],
            'institution': [],
            'canonical_name': [],
            'complexity': [],
            'blocking': [],
            'delay': [],
            'centrality': []
        })

    def download_files_with_metrics(self):
        self.empty_download_dir()

        for row in self.get_page_rows():
            self.pause(1)

            # How many files in downloads dir?
            start_files = self.get_csv_files_download_dir()

            current_row_cols = row.find_all("td") # all columns in row
        
            curriculum_name = current_row_cols[0].find("a").text
            curriculum_id = re.search("curriculums\/(\d*)", current_row_cols[0].find("a")['href']).group(1)
            organization = current_row_cols[1].find("a").text
            cip = current_row_cols[2].text
            catalog_year = current_row_cols[3].text
            date_created = current_row_cols[4].text

            # Add course data
            if row.find_all("div", class_="dropdown") == []:
                new_df = pd.DataFrame({
                    # Curriculum fields
                    'curriculum_name': [curriculum_name], 
                    'curriculum_id': [curriculum_id],
                    'organization': [organization],
                    'cip': [cip], 
                    'catalog_year': [catalog_year], 
                    'date_created': [date_created],

                    # Course fields
                    'course_id': [None],
                    'course_name': [None],
                    'prefix': [None],
                    'number': [None],
                    'prerequisite': [None],
                    'corequisite': [None],
                    'strict_corequisite': [None],
                    'credit_hours': [None],
                    'institution': [None],
                    'canonical_name': [None],
                    'complexity': [None],
                    'blocking': [None],
                    'delay': [None],
                    'centrality': [None]
                })

            else:
                download_url = self.url + str(row.find_all("a", class_="dropdown-item")[-1]['href'])
                self.driver.get(download_url)

                while len(self.get_csv_files_download_dir()) <= len(start_files):
                    self.pause(.5)

                current_file = self.get_full_path_downloads(self.get_new_file(start_files, self.get_csv_files_download_dir()))
                new_df = pd.read_csv(current_file, skiprows=6)
                new_df['curriculum_name'] = curriculum_name
                new_df['curriculum_id'] = curriculum_id
                new_df['organization'] = organization
                new_df['cip'] = cip
                new_df['catalog_year'] = catalog_year
                new_df['date_created'] = date_created

            self.add_data(new_df)
            
        self.export_data()
    # Economics
    # Computer Science
    # Civil Engineering
    # Biology
    # Animal Science

    def add_data(self, df):
        df.columns = df.columns.str.lower()
        df.columns = df.columns.str.replace(" ", "_")
        df.rename(columns={
            "strict-corequisite": "strict_corequisite"
        }, inplace=True)
        self.df = pd.concat([self.df, df], ignore_index=True)
        return
    
    def get_new_file(self, start_list, new_list):
        for f in new_list:
            if f not in start_list:
                return f
    
    def export_data(self, filename="course_data.csv"):
        self.df.to_csv(filename)
        print(f"File saved to {self.get_cwd()}/{filename}")
        print(f"Total time: {self.get_time()/60} minutes.")

    def scrape(self, filename='data.csv'):
        self.empty_download_dir()
        self.login()
        self.go_to()
        self.show_public()
        self.select_show_x_entries(100)
        self.go_through_all_pages(
            self.download_files_with_metrics
        )
        self.empty_download_dir()
        self.export_data(filename)