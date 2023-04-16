# This script utilizes webscraping to extract required data from the articles provided in the original xlsx file
import openpyxl
import requests
import os
from bs4 import BeautifulSoup

cwd = os.getcwd()
src_files_dir = os.path.join(cwd, 'source_files')

if not os.path.exists(src_files_dir):
    os.makedirs(src_files_dir)

# Load the workbook
workbook = openpyxl.load_workbook('input.xlsx')

# Get the active sheet
sheet = workbook.active

# Iterate over rows and columns
for row in sheet.iter_rows(min_row = 2, max_row=115, min_col=2, max_col=2):
    for cell in row:
         url = cell.value
         response = requests.get(url)
         soup = BeautifulSoup(response.content, 'html.parser')
         article = soup.find('article')

         data = {
            'URL_ID': url,
            'TITLE': '',
            'TEXT': '',
         }

         if article is not None:

            data['TITLE'] = article.h1.text

            try:
                content = article.find('div', {'class': ['td-post-content tagdiv-type', 'td_block_wrap tdb_single_content tdi_126 td-pb-border-top td_block_template_1 td-post-content tagdiv-type']})
                data['TEXT'] = content.get_text()
            except AttributeError as err:
                print(data['TITLE'])
                print(err)

            # Save extracted article in text file
            fileURL = data['URL_ID']

            # Extract the last segment of the URL using os.path.basename
            filename = os.path.basename(fileURL.rstrip('/'))
            filename += ".txt"
            filepath = os.path.join(src_files_dir, filename)

            with open(filepath, "w", encoding='utf-8') as file:
                file.write(data['TITLE'])
                file.write('\n')
                file.write(str(data['TEXT']))