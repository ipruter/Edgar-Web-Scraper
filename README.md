### About Edgar Web Scraper
Edgar is a database containing data on the securities filings of companies, hedgefunds, and asset managers who are required to share filings with the U.S Securities and Exchange Commission. The Edgar Web Scraper looks for F-13 filings which contains the data on companies invested in, number of shares and total value of shares. It cleans the data, stores it in a database, and uses it for analysis with the objective of copying investors who perfer to hold investments as opose to holding long and shorting selling companies. Investments that make up 7.5% or higher of the portfolio will be saved to a database table and serve as good investments to copy to outperform the S&P 500. The analyses performed display a dendomgram of clusters between the investments of multiple investors and a hystogram of the most popular investments.

### Web Scraping
Edgar provides tools for Python for integration with the API and key words for the URL which also serves as an API. The issue with those API options was they were bringing up the primary documents which included summery data as opose to the HTML and XML information tables that accumpanied the primary document. This inconvenience created an opertunity for a web scraping data analytics project where the data would be attained through the manipulation of HTML code as opose to interacting with API's. To web scrape the program started with the Edgar URL and a CIK number of a specified investor. From there it would parse the HTML syntax using Beautiful soup and use table tags and key words and characters to identify file names and loop through underlying directories. Once the F-13 fill is found  the relevent data is extracted, cleaned, and saved to a database.

### Installation
- The program is written in Python 3 which is a flexible language that uses a powerful interpreter for fast development. https://www.python.org/downloads/
- The library mysql.connector contains functions that allow for the use of SQL syntax to be executed within the Python program. 
- The library requests allows python programs to send requests to servers and use the responding content within the program.
- The BeautifulSoup library contains functions that parse HTML syntax and organizes filtered content into a manageble XML file that is easier to parse further and retrieve data from
- pandas
- hierarchy
- dendrogram
- matplotlib


### How to Use Edgar Web Scraper
The program was written, tested, and intended to run in the Jupyter Notebook environment which is why it is broken up into cells instead of methods for re-use of code. The user-Agent veriable needs to be defined to prevent a 404 error. This can be found by inspecting a webpage's HTML and navigating to the network tab, click on the first file listed, select the header tab and scroll down to find the user agent. The program begins by retrieving a table of investors to retrieve data on securities. The investors that are on that table are completely up to you. The table columns are CIK (unique ID) investor's name, and a description, in that order. However the program only requires a CIK column and an invester name column. The main cell will extract all the data and created tables in your database you can reference outside of the program as well. The following cell will construct a data frame concatinating all of the data extracted and saving it into a dataframe of quantitative data. The two cells create a dendogram and a hystogram from the datafame.

### How to Test Edgar Web Scraper
