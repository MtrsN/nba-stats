
import sys
import pandas as pd
import requests
from bs4 import BeautifulSoup

def scrape_stats(year_start, year_end):
    """Gets the NBA stats

    Few modifications from: https://medium.com/data-hackers/como-fazer-web-scraping-em-python-23c9d465a37f"""

    base_url = 'https://www.basketball-reference.com/leagues/NBA_{}_totals.html'

    years = range(year_start, year_end + 1, 1)

    final_df = pd.DataFrame()

    for year in years:

        print('Extracting year {}'.format(year))

        req_url = base_url.format(year)

        req = requests.get(req_url)

        soup = BeautifulSoup(req.content, 'html.parser')

        table = soup.find('table', {'id':'totals_stats'})

        df = pd.read_html(str(table))[0]
        df['Year'] = year

        final_df = final_df.append(df)

    final_df = final_df[final_df["Rk"] != "Rk"]

    final_df["Player"] = final_df["Player"].str.replace("*", "")

    numerics = [var for var in final_df.columns if var not in ["Rk", "Player", "Pos", "Tm"]]

    for i in numerics:
        final_df[i] = final_df[i].apply(pd.to_numeric)

    return final_df

if __name__ == "__main__":

    sys.path.append("..")
    
    df = scrape_stats(2000, 2018)
    
    df.to_csv("Data/nba_stats.csv", index= False)