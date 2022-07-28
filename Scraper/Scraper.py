from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
from bs4 import BeautifulSoup
from time import sleep, time
import os

class Scraper:

    def __init__(self, email, password, download_dir='tmp'):
        pd.set_option('display.max_columns', None)
        self.url = "https://www.curricularanalytics.org"
        self.email = email
        self.password = password
        self.logged_in = False
        self.start_time = time()
        self.link = "" # Implement this in all child classes
        self.download_dir = f'{os.getcwd()}\\{download_dir}\\'

        try:
            os.mkdir(f'{os.getcwd()}/{download_dir}')
        except OSError:
            print(f"There was an error creating the {download_dir} directory. It might already be created. Skipping this step.")

        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--start-maximized")
            options.add_argument("log-level=3")
            prefs = {
                "profile.default_content_settings.popups": 0,
                "download.default_directory": self.download_dir,
                "directory_upgrade": True
            }
            options.add_experimental_option("prefs", prefs)

            self.driver = webdriver.Chrome(chrome_options=options)
        except Exception:
            raise Exception("An error occurred. Have you correctly installed the Selenium driver?")

        self.data = {} # This field should be implemented in each scraper
    
    def get_cwd(self):
        return os.getcwd()

    def get_download_dir(self):
        return self.download_dir

    def empty_download_dir(self):
        d = self.get_download_dir()
        for f in os.listdir(d):
            path = os.path.join(d, f)
            try:
                if os.path.isfile(path) or os.path.islink(path):
                    os.unlink(path)
            except Exception as e:
                print(f"Failed to delete contents of directory {self.get_download_dir()}. Reason: {e}")

    def get_files_download_dir(self):
        return os.listdir(self.get_download_dir())
    
    def get_csv_files_download_dir(self):
        return [f for f in self.get_files_download_dir() if f[-3:].lower() == 'csv']

    def get_full_path_csv_files_download_dir(self):
        return [os.path.join(self.get_download_dir(), f) for f in self.get_csv_files_download_dir()]

    def get_full_path_downloads(self, file):
        return os.path.join(self.get_download_dir(), file)

    def login(self):
        self.driver.get(self.url + "/users/sign_in")

        elem = self.driver.find_element(By.ID, "user_email")
        elem.send_keys(self.email)

        elem = self.driver.find_element(By.ID, "user_password")
        elem.send_keys(self.password)
        elem.send_keys(Keys.RETURN)

        self.logged_in == True

    def go_to(self, link=None):
        if link:
            self.driver.get(self.url + link)
        else:
            self.driver.get(self.url + self.link)
    
    def show_public(self):
        self.driver.find_element(By.CLASS_NAME, "custom-control-label").click()

    def select_show_x_entries(self, x:'int'=100):
        if int(x) not in [10, 25, 50, 100]:
            raise ValueError("Incorrect value. Options are 10, 25, 50, and 100.")
        select = Select(self.driver.find_element(By.NAME, "data-table_length"))
        select.select_by_value(str(x))

    def next_page(self):
        self.driver.switch_to.window(self.driver.window_handles[0])
        self.driver.find_element(By.ID, "data-table_next").find_element(By.XPATH, ".//a").click()
        self.pause()

    def get_number_of_pages(self):
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        return int(soup.find("ul", class_="pagination").find_all("li")[-2].find("a").text)

    def open_new_link(self, link):
        # Go back to original window
        self.switch_to_tab(0)

        # Open a new window
        self.driver.execute_script("window.open('');")
    
        # Switch to the new window and open new URL
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.go_to(link)
    
    def get_page_rows(self):
        self.driver.switch_to.window(self.driver.window_handles[0])
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        table = soup.find("table", {"id": "data-table"}).find("tbody")
        return table.find_all("tr")

    def open_all_maps_in_new_page(self):
        for row in self.get_page_rows():
            cols = row.find_all("td")
            cc_link = cols[0].find("a")['href']
            self.open_new_link(cc_link)
        self.pause()

    def go_through_all_pages(self, *args):
        '''Goes through each page of the website and performs each function of 
           args, in order, on that page.
        '''
        self.pause()
        for page in range(self.get_number_of_pages()-1):
            print(f"Processing page {page+1} of {self.get_number_of_pages()}")
            for arg in args:
                if callable(arg):
                    arg()
                else:
                    raise ValueError("One of the actions to perform on each page was not a function/method.")
            self.next_page()

    def get_data(self):
        return pd.DataFrame(self.data)
    
    def export_data(self, filename):
        df = self.get_data()
        df.to_csv(filename)
        print(f"Saved file as {filename} to {os.getcwd()}/{filename}")
        print(f"Time taken: {self.get_time()} seconds")

    def get_number_of_tabs(self):
        return len(self.driver.window_handles)

    def close_tab_x(self, x):
        self.switch_to_tab(x)
        self.close()

    def switch_to_tab(self, t):
        self.driver.switch_to.window(self.driver.window_handles[t])

    def pause(self, pause=4):
        sleep(pause)

    def get_time(self):
        '''Returns time from start in seconds'''
        return time() - self.start_time
    
    def close(self):
        self.driver.close()


