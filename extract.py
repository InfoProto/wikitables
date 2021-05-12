import csv
import re

import requests
from bs4 import BeautifulSoup


def extract_wikitables(article):
    url = "https://en.wikipedia.org/wiki/" + article
    res = requests.get(url).text
    soup = BeautifulSoup(res, 'lxml')

    table_number = 1
    for table in soup.find_all('table', class_='wikitable'):
        csvfile = "{}_{:02d}.csv".format(article, table_number)
        with open(csvfile, "w", encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            write_table_as_csv(writer=writer, table=table)
            table_number += 1


def write_table_as_csv(writer, table):
    for tr in table.find_all('tr'):
        row = []
        for col in tr.find_all(['th', 'td']):
            colspan = 1
            if 'colspan' in col.attrs:
                colspan = int(re.sub(r'\D', '', col['colspan']))

            col_text = col.text.strip()
            for i in range(colspan):
                row.append(col_text)

            # print("{}".format(",".join(row)))

        writer.writerow(row)


if __name__ == '__main__':
    articles = [
        "List_of_current_heads_of_state_and_government",
        "Team_sport",
    ]

    for article in articles:
        extract_wikitables(article)
