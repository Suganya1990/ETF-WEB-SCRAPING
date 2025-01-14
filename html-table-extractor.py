import datetime
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
from datetime import datetime
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
# US english
LANGUAGE = "en-US,en;q=0.5"


def get_soup(url):
    """Constructs and returns a soup using the HTML content of 'url' passed"""
    #initialize a session
    session  = requests.Session()
    #set the User-Agent as a regular browser
    session.headers['User-Agent'] = USER_AGENT
    #request for english content (optional)

    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE

    #make the request

    html = session.get(url)

    return bs(html.content, "html.parser")


def get_table(soup):
    # """Extracts and returns all tables in a soup object"""
    div = soup.find('div', {'class':'holdings-table'})
    table = div.find('table')
    return table

def get_date(soup):
    #gets the div of the holdings table
     div_date = soup.find('div', {'class':'holdings-table'})
     #gets the update-date p tag of the holdings table
     p_date = div_date.find('p', {'class':'update-date'})
     #extrats just the date string 
     temp_date_str =  p_date.text.strip().split("As of")[1].split()
     #converts date string into date obj
     date_format = '%m/%d/%Y'
     date_time_obj = datetime.strptime(temp_date_str[0], date_format)
     date_obj = date_time_obj.date()
     
     print(date_obj)
     return date_obj

# def get_etf(soup):
#     div_etf = 

    

# def add_etf(etf):

def get_table_headers(table):
    """Given a tabe soup, returns all the headers"""
    headers = []
    for th in table.find("tr").find_all("th"):
        headers.append(th.text.strip())
    return headers

def get_table_rows(table):
    """Given a table, returns all its rows"""
    rows=[]
    for tr in table.find_all("tr")[1:]:
        cells=[]
        #grabs all td tags in this table row
        tds = tr.find_all("td")
        if len(tds) == 0:
            #if no td tags, search for th tags
            #can be found especially in wikipedia tables below the table
            ths = tr.find_all("th")
            for th in ths:
                cells.append(th.text.strip())

        else:
             #use reuglar td tags
            for td in tds:
                cells.append(td.text.strip())

        rows.append(cells)
    return rows

def save_as_csv(table_name, headers, rows, date_obj, etf):
    # print(headers)
   df =  pd.DataFrame(rows, columns=headers)
   df = df.assign(ETF = etf)
   df = df.assign(Date = date_obj)
   path='C:\\Users\\smahe\\Desktop\\DataSets\\ETF_U Datasets\\'
   date_obj_str= '%s-%s-%s' % (date_obj.month, date_obj.day, date_obj.year)
   df.to_csv(f"{path+etf+'_'+date_obj_str}.csv", index=False)

def main(url, etf):
    #get the soup
    soup=get_soup(url)

    #extract all the tables from the web page
    table= get_table(soup)
    last_updated_holdings = get_date(soup)

    print(f"[+] found a total of {len(table)} tables.")

    #iterate ovre all tables

    headers=get_table_headers(table)
    
    #get all the rows of the table
    rows= get_table_rows(table)
        #save tables as csv file
        # table_name = f"table-{i}"
        # print(f"[+] Saving {table_name}")
    save_as_csv('table-1', headers, rows, last_updated_holdings, etf)


if __name__=="__main__":
    import sys
    try:
        url=sys.argv[1]
        etf = sys.argv[2]
    except IndexError:
        print("Please specify a URL. \nUsage: python html_table_extractor.py [URL]")
        exit(1)

    main(url, etf)