# Curricular Analytics Scraping
 A program that scrapes curricular analytics data from curricularanalytics.org.

 ## Usage
 First, make sure that you have Python 3.10 installed on your computer. You can download Python at python.org.

Next, make sure that you have all of the required packages installed on your computer. You can do this by running the following command in the terminal or command prompt:

```
pip install selenium bs4 pandas
```

This command will install the three main libraries used in this project.

Selenium is a library that allows Python to take control of the computer and interact with the browser using keystrokes and mouse events. Selenium works with many different browsers, but each one has its own selenium driver that must be installed to the computer before it can be used.

The `bs4` package contains a class called `BeautifulSoup`, which is useful for parsing HTML. So, after Selenium navigates through the web pages, BeautifulSoup can look at the HTML and extract specific pieces of data from them.

Finally, `pandas` is a package that allows data to be stored in table-like structures called dataframes. These dataframes allow pandas to manage the data that gets extracted by BeautifulSoup and eventually export the data set as a CSV.

### Installing the Chrome driver for Selenium on Windows
By default, I have opted to use the Chrome driver for Selenium in this project. However, you could install other drivers if you wanted to.

To install the Chrome driver for Selenium, you can click [this link](https://chromedriver.storage.googleapis.com/104.0.5112.29/chromedriver_win32.zip). Once the download finishes, extract the contents of the zip folder to a location on your computer of your choosing. I put mine in the location `C:\Program Files (x86)\Chrome Driver`, which I chose randomly and which isn't important. What *is* important is to make note of the location.

After unzipping this folder, you should have a file called `chromedriver.exe` placed somewhere on your computer. Go to that file, right click it, and open up its Properties. Copy the Location from that window and then click the Windows key on the bottom of your screen. Type in "enviro" and then click the popup that says "Edit system environment variables".

On the resulting popup window, click the button that says "Environment Variables". On the next window, you should see two section, one of which is called "User variables" and the other called "System variables". Both sections have a variable called "Path", which contains references for Windows to run programs from the command line.

Click on the line that says "Path" under "User variables". Then, click "Edit" below the white box. Click "New" to add a new line to the variable, and then paste in the location of your `chromedriver.exe` file. You don't have to include the file name. It will look something like this:

```
C:\Program Files (x86)\Chrome Driver
```

Click "OK" and the "OK" again and then "OK" a third time. The chrome driver should be ready to go now.


### Running the file
To run the file, you only need to edit the file `main.py`. In this file, import the scraper that you need from `Scraper` and then create a new scraper object, passing in your username and password as strings to the scraper. Then, call the `.scrape()` method. In theory, it should be that easy.

```python
from Scraper.CourseScraper import CourseScraper

cs = CourseScraper("myemail@gmail.com", "password123")
cs.scrape()
```

Note that you will need an account at curricularanalytics.org to use this scraper.

## Bugs
For bugs, reach out to me at haydenthoopes@gmail.com or create an issue on this GitHub repository.