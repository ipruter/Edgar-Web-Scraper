#!/usr/bin/env python
# coding: utf-8

# In[34]:


real_password = "fakepassword"
real_header = {
'User-Agent': 'fake user agent'
}


# In[36]:


import mysql.connector
import sqlite3
import requests
import time
from bs4 import BeautifulSoup
import pandas as pd

CIK = ''
file_number = ''
count_cik = 0
count_file = 0
breaker = False
total = 0.0
same = False
exists = False
percent = 0.0
data_list = []
pass_variable = real_password
# establishes a user-agent to prevent a 404
header = real_header


# 

# In[37]:


# create database connection
db =mysql.connector.connect(host = "localhost", user = "root", password = pass_variable, database = "CCTrading")
cursor = db.cursor()
# retrieve hedge fund manager and asset manager data from database
cursor.execute("SELECT * FROM managers")

# iterates through each table row to retrieve the CIK number for each company filings
for row in cursor:
    breaker = False
    count_cik = 0
    count_file = 0
    CIK = row[0]
    db_name = row[1]
    # reformats the company name to be compliant with SQL syntax
    db_name = db_name.replace(" ", "_")
    # creates a URL with the current CIK number 
    cik_url = fr"https://www.sec.gov/Archives/edgar/data/{CIK}"
    # creates a connection with the Edgar database
    response_cik = requests.get(url = cik_url, headers = header)
    # verifies the success of the connection
    print(response_cik.status_code)
    print(response_cik.url)
    # creates a Beautiful Soup object with the web page content in xml format
    soup_cik = BeautifulSoup(response_cik.content, 'lxml')
    # creates a dictionary of all table content in the BS object
    soup_dic_cik = soup_cik.find_all('td')

    # parses each table line to get each file number from the table
    for line_cik in soup_dic_cik:
        # checks if a loop breaker was triggered from a lower nested for loop meaning the most recent f-13 filing was found
        if breaker == True:
            break
        # counts each line for later parsing purposes
        count_cik = count_cik + 1
        # converts BS object to string for parsing
        string_version_lc = str(line_cik)
        # checks counter and uses modulus to only parse lines that contain file names
        if count_cik == 1 or count_cik % 3 == 1:
            # parses line down to the file name and adds it to new URL
            first_split_cik = string_version_lc.split("/")
            second_split_cik = first_split_cik[5].split("\"")
            file_number = second_split_cik[0]
            file_url = fr"https://www.sec.gov/Archives/edgar/data/{CIK}/{file_number}"
            response_file = requests.get(url = file_url, headers = header)
            print(response_file.status_code)
            print(response_file.url)
            # creates new BS object with new page
            soup_file = BeautifulSoup(response_file.content, 'lxml')
            soup_dic_file = soup_file.find_all('td')
            
            # parses each line in table to find xml files
            for line_file in soup_dic_file:
                count_file = count_file + 1
                string_version_lf = str(line_file)
            
                # checks only lines that would have file names
                if count_file == 1 or count_file % 3 == 1:
                    # checks for xml file
                    find_xml = string_version_lf.find('xml')
                    # excludes unwanted xml files
                    find_doc4 = string_version_lf.find('doc4.xml')
                    find_primary_doc = string_version_lf.find('primary_doc')
                    
                    # checks the type of xml file and then parses it
                    if find_xml != -1 and find_primary_doc == -1 and find_doc4 == -1:
                        first_split_file = string_version_lf.split(">")
                        second_split_file = first_split_file[3].split("<")
                        xml_file = second_split_file[0]
                        # adds xml file to URL
                        url_xml = fr"https://www.sec.gov/Archives/edgar/data/{CIK}/{file_number}/{xml_file}"
                        response_xml = requests.get(url = url_xml, headers = header)
                        print(response_xml.status_code)
                        print(response_xml.url)
                        soup_xml = BeautifulSoup(response_xml.content, 'lxml')
                        string_version_xml = str(soup_xml)
                        # looks for 13-f file
                        thirteen_f = string_version_xml.find('thirteenf')
                        
                        # if file is an 13-f file breaks two inner loops and goes to the next company
                        if thirteen_f != -1:
                            breaker = True
                            url_13f = url_xml
                            response_13f = requests.get(url = url_13f, headers = header)
                            soup_13f = BeautifulSoup(response_13f.content, 'xml')
                            # creates a BS object of all info tables in the 13-f file
                            entries = soup_13f.find_all('infoTable')
                            dic_list = []
                            
                            # creates a dictionary of values for each entry of investments
                            for entry in entries:
                                entry_dic = {}
                                entry_dic['nameOfIssuer'] = entry.find('nameOfIssuer').text
                                entry_dic['titleOfClass'] = entry.find('titleOfClass').text
                                entry_dic['cusip'] = entry.find('cusip').text
                                entry_dic['sshPrnamt'] = entry.find('sshPrnamt').text
                                entry_dic['sshPrnamtType'] = entry.find('sshPrnamtType').text
                                entry_dic['investmentDiscretion'] = entry.find('investmentDiscretion').text
                                if entry.find('otherManager') != None:
                                    entry_dic['otherManager'] = entry.find('otherManager').text
                                entry_dic['value'] = entry.find('value').text
                                entry_dic['Sole'] = entry.find('Sole').text
                                entry_dic['None'] = entry.find('None').text
                                # creates a list of each entry dictionary
                                dic_list.append(entry_dic)
                            
                            list_cleaned = []
                            # creates a copy of the list of dictionaries which will contained cleaned data
                            for entry_dic in dic_list:
                                dic_cleaned = {}
                                # copies the name of each issuer
                                dic_cleaned['name'] = entry_dic['nameOfIssuer']
                                # initializes numeric values to zero
                                dic_cleaned['value'] = 0
                                dic_cleaned['sshPrnamt'] = 0
                                list_cleaned.append(dic_cleaned)
                            
                            # compares the issuer name from each dictionary of entries to against its cloned list to remove duplicate entries
                            for entry_dic in dic_list:   
                                for dic_cleaned in list_cleaned:
                                    # checks for a identical entry from cloned list allowing for only one
                                    if entry_dic['nameOfIssuer'] == dic_cleaned['name'] and same == False:
                                        # signals that one identical entry was found
                                        same = True
                                    # checks for duplicate entries after the one expected identical entry has been marked as found
                                    elif entry_dic['nameOfIssuer'] == dic_cleaned['name'] and same == True:
                                        # deletes duplicate entry from the clean version of the list
                                        list_cleaned.remove(dic_cleaned)
                                # resets Boolean value to mark identical matches in the next iteration of the original list
                                same = False
                            
                            # adds each duplicate numeric value from the original list and stores the sum in the cleaned list
                            for dic_cleaned in list_cleaned:
                                for entry_dic in dic_list:
                                    # checks that values in both lists match
                                    if entry_dic['nameOfIssuer'] == dic_cleaned['name']:
                                        # adds numeric value to running sum in the cleaned list
                                        dic_cleaned['value'] = dic_cleaned['value'] + int(entry_dic['value'])
                                        dic_cleaned['sshPrnamt'] = dic_cleaned['sshPrnamt'] + int(entry_dic['sshPrnamt'])
                                        
                            # drops table of entries if it exists
                            db_drop_table = mysql.connector.connect(host = "localhost", user = "root", password = pass_variable, database = "CCTrading" )
                            cursor_drop_table = db_drop_table.cursor()
                            cursor_drop_table.execute(fr"DROP TABLE IF EXISTS {db_name}")
                            db_drop_table.commit()
                            # creates table of entries if it does not exist
                            db_create_table = mysql.connector.connect(host = "localhost", user = "root", password = pass_variable, database = "CCTrading" )
                            cursor_create_table = db_create_table.cursor()
                            cursor_create_table.execute(fr"CREATE TABLE {db_name} (CompanyName varchar(255), Value int, Share int)")
                            db_create_table.commit()
                            # drops table of investments above 7.5% of total investments if it exists
                            db_drop_safe_table = mysql.connector.connect(host = "localhost", user = "root", password = pass_variable, database = "CCTrading" )
                            cursor_drop_safe_table = db_drop_safe_table.cursor()
                            cursor_drop_safe_table.execute(fr"DROP TABLE IF EXISTS {db_name}_Top_Picks")
                            db_drop_safe_table.commit()
                            # creates table of investments above 7.5% of total investments if it does not exists
                            db_create_safe_table = mysql.connector.connect(host = "localhost", user = "root", password = pass_variable, database = "CCTrading" )
                            cursor_create_safe_table = db_create_safe_table.cursor()
                            cursor_create_safe_table.execute(fr"CREATE TABLE {db_name}_Top_Picks (CompanyName varchar(255), Value int, Share int)")
                            db_create_safe_table.commit()
                            
                            # fills in table with content of cleaned list
                            print("\nAll Entries:")
                            for dic_cleaned in list_cleaned:
                                db_fill_table = mysql.connector.connect(host = "localhost", user = "root", password = pass_variable, database = "CCTrading" )
                                cursor_fill_table = db_fill_table.cursor()
                                df_cleaned = pd.DataFrame([dic_cleaned])
                                val_to_insert = df_cleaned.values.tolist()
                                cursor_fill_table.executemany(fr"insert into {db_name} (CompanyName, Value, Share) values (%s, %s, %s)", val_to_insert)
                                db_fill_table.commit()
                                
                                print("Invester: {0:30} Value: {1} Shares: {2}".format(dic_cleaned['name'], dic_cleaned['value'], dic_cleaned['sshPrnamt']))
                            
                            total = 0
                            # calculates the sum of all asset values for each holding
                            for dic_cleaned in list_cleaned:
                                total = total + float(dic_cleaned['value'])
                            print("\nNoteable Holdings")
                            
                            # divides each asset value by the sum of all values to get the percent of value of each holding
                            for dic_cleaned in list_cleaned:
                                percent = float(dic_cleaned['value']) / total
                                # fills table with each holding if its higher than 7.5% of the total portfolio
                                if percent >= 0.075:
                                    db_fill_safe_table =mysql.connector.connect(host = "localhost", user = "root", password = pass_variable, database = "CCTrading" )
                                    cursor_fill_safe_table = db_fill_safe_table.cursor()
                                    df_top_cleaned = pd.DataFrame([dic_cleaned])
                                    val_to_insert_top = df_top_cleaned.values.tolist()
                                    cursor_fill_safe_table.executemany(fr"insert into {db_name}_Top_Picks (CompanyName, Value, Share) values (%s, %s, %s)", val_to_insert_top)
                                    db_fill_safe_table.commit()
                                    print("Invester: {0:21} Value: {1} Shares: {2}".format(dic_cleaned['name'], dic_cleaned['value'], dic_cleaned['sshPrnamt']))
                            
                            # appends saved list to a master list for analysis
                            data_list.append(list_cleaned)
                            break
        


# In[31]:


concatenated_data_list = []
quant_values = []

# iterates through the list of each managers lists of dictionaries of entries
for list_cleaned in data_list:
    # iterates through each dictionary in each list of dictionaries
    for dic_cleaned in list_cleaned:
        # concatenates each dictionary into one big list of entries for analysis
        concatenated_data_list.append(dic_cleaned)

# converts the list into a data frame
data_frame = pd.DataFrame.from_dict(concatenated_data_list)
# reduces the data to just the relevant numeric values
quant_values = data_frame[['value','sshPrnamt']]

    
    


# In[32]:


from scipy.cluster import hierarchy
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt

# creates a graph dendrogram of the hierarchical clusters of the data
graph_data = hierarchy.linkage(quant_values, method='average')
# displays graph with a title
plt.figure()
plt.title("Dendrograms")
dendrogram = hierarchy.dendrogram(graph_data)


# In[33]:


# creates a histogram of the data
data_frame.value.hist()

