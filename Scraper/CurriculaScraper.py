from bs4 import BeautifulSoup

from Scraper.Scraper import Scraper

class CurriculaScraper(Scraper):
    def __init__(self, email, password):
        super().__init__(email, password)
        self.link = "/curriculums"

        self.data = {
            'name': [], 
            'organization': [],
            'cip': [], 
            'catalog_year': [], 
            'date_created': [], 
            'complexity_score': [], 
            'credit_hours': []
        }
    
    def go_through_all_maps(self):
        self.driver.switch_to.window(self.driver.window_handles[0])
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        table = soup.find("table", {"id": "data-table"}).find("tbody")
        rows = table.find_all("tr")

        for row in range(self.get_number_of_tabs()-1):
            self.driver.switch_to.window(self.driver.window_handles[1])
            self.do_stuff(rows[row], self.data)

    def do_stuff(self, row, data):
        temp_soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        metrics_div = temp_soup.find("div", {"id": "metrics"})

        if metrics_div is None or len(metrics_div.find_all("div")) == 0:
            complexity = None
            credit_hours = None
        else:
            metrics = metrics_div.find_all("div")
            complexity = metrics[0].find("h3").text
            credit_hours = metrics[1].find("h3").text
            
        self.driver.close()

        # Get complexity score and credit_hours
        data['complexity_score'].append(complexity.split(": ")[-1]) if complexity else data['complexity_score'].append(None)
        data['credit_hours'].append(credit_hours.split(": ")[-1]) if credit_hours else data['credit_hours'].append(None)

        #current row
        current_row_cols = row.find_all("td")

        # Get name
        name = current_row_cols[0].find("a").text
        data['name'].append(name)

        # Get organization
        organization = current_row_cols[1].find("a").text
        data['organization'].append(organization)

        # Get CIP Code
        cip = current_row_cols[2].text
        data['cip'].append(cip)

        # Get Catalog Year
        catalog_year = current_row_cols[3].text
        data['catalog_year'].append(catalog_year)

        # Get Date Created
        date_created = current_row_cols[4].text
        data['date_created'].append(date_created)

    def scrape(self, filename='data.csv'):
        self.login()
        self.go_to()
        self.show_public()
        self.select_show_x_entries(100)
        self.go_through_all_pages(
            self.open_all_maps_in_new_page,
            self.go_through_all_maps
        )
        self.export_data(filename)