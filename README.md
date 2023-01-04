### About Edgar Web Scraper
Edgar is a database containing data on the securities filings of companies, hedge funds, and asset managers who are required to share filings with the U.S Securities and Exchange Commission. The Edgar Web Scraper looks for F-13 filings which contains the data on companies invested in, number of shares and total value of shares. It cleans the data, stores it in a database, and uses it for analysis with the objective of copying investors who prefer to hold investments as oppose to holding long and shorting selling companies. Investments that make up 7.5% or higher of the portfolio will be saved to a database table and serve as good investments to copy to outperform the S&P 500. The analyses performed display a dendrogram of clusters between the investments of multiple investors and a histogram of the most popular investments.

### Web Scraping
Edgar provides tools for Python for integration with the API and key words for the URL which also serves as an API. The issue with those API options was they were bringing up the primary documents which included summery data as oppose to the HTML and XML information tables that accompanied the primary document. This inconvenience created an opportunity for a web scraping data analytics project where the data would be attained through the manipulation of HTML code as oppose to interacting with API's. To web scrape the program started with the Edgar URL and a CIK number of a specified investor. From there it would parse the HTML syntax using Beautifulsoup and use table tags and key words and characters to identify file names and loop through underlying directories. Once the F-13 fill is found the relevant data is extracted, cleaned, and saved to a database.

### Installation
- The program is written in Python 3 which is a flexible language that uses a powerful interpreter for fast development. https://www.python.org/downloads/
- The library mysql.connector contains functions that allow for the use of SQL syntax to be executed within the Python program. 
- The library requests allow python programs to send requests to servers and use the responding content within the program.
- The BeautifulSoup library contains functions that parse HTML syntax and organizes filtered content into a manageable XML file that is easier to parse further and retrieve data from.
- The pandas library is a great Python data analysis tool for manipulating quantitative data and time series.
- scipy is a library used for scientific computing and contains sub packages for clustering and visually representing quantitative data
- The matplotlib library creates mathematic, interactive visualizations for describing statistical data

### How to Use Edgar Web Scraper
The program was written, tested, and intended to run in the Jupyter Notebook environment. The user-Agent variable needs to be defined to prevent a 404 error. This can be found by inspecting a webpage's HTML and navigating to the network tab, click on the first file listed, select the header tab and scroll down to find the user agent.

The program begins by retrieving a table of investors to retrieve data on securities. The investors table was manually created and the selection of investors  is completely up to you. However, the table requires the CIK number to be the primary key and the column needs to be called CIK.

<img src="https://github.com/ipruter/Edgar-Web-Scraper/blob/main/Images/investor_db.png" height="50%" width="50%" >

The main cell extracts the data of the most recent F-13 filings from each investor and creates and saves it into an "investments" table in the database.

<img src="https://github.com/ipruter/Edgar-Web-Scraper/blob/main/Images/Investments_table.png" height="40%" width="40%">

The program displays the directories being searched and the data extracted that is held in memory

<img src="https://github.com/ipruter/Edgar-Web-Scraper/blob/main/Images/cctrading_connections.png" height="50%" width="50%" >

Cell four makes queries of the investors table and a table of investments that were 7.5% or greater of each investors portfolio

<img src="https://github.com/ipruter/Edgar-Web-Scraper/blob/main/Images/cctrading_investments.png" height="50%" width="50%" >
<img src="https://github.com/ipruter/Edgar-Web-Scraper/blob/main/Images/cctrading_safe_investments.png" height="50%" width="50%" >

Cell five constructs a data frame concatenating all of the data extracted and saving it into a data frame of quantitative data. 

Cell six creates a dendrogram for identifying clusters in the data

<img src="https://github.com/ipruter/Edgar-Web-Scraper/blob/main/Images/dendrogram.png" height="50%" width="50%" >

Cell seven creates a histogram for a more intuitive representation of the significance of certain investments

<img src="https://github.com/ipruter/Edgar-Web-Scraper/blob/main/Images/histogram.png" height="50%" width="50%" >

### How to Test Edgar Web Scraper
Anytime the program makes a connection to a page on Edgar is displays the status code. The code returned should be a 200 or else there may be a connection issues or denied access to the web page.

Test with investors that you know have F-13 filings. A failure to produce data does not mean the program didn't work but the program should display data in real time as it's scraping if the investor has filed an F-13 document.

After running cell three, the program should have created an investors table in the database. Any investment that is 7.5% or greater of the total portfolio of a single investor should have a 1 in the SafeInvestment column. This should be tested with an investor who have investments greater, but close to 7.5% to test the boundary. 

Cells six and seven should produce graphs
