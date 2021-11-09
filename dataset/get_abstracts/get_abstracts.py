import pandas as pd
import csv  
import os
from operator import itemgetter
import re

# Ref.: https://pypi.org/project/google-patent-scraper/
from google_patent_scraper import scraper_class
# Variáveis globais da extração de resumos das patentes

def create_empty_csv_file(filename, header):
  with open(filename, 'w', encoding='UTF8') as f:
    writer = csv.writer(f, delimiter=";")

    # write the header
    writer.writerow(header)

def create_file(filename):
  if os.path.exists(filename): os.remove(filename)
  create_empty_csv_file(filename=filename, header=['doc_id', 'pub_dt', 'appl_id', 'abstract'])
  
def get_number_lines(filename):
  csv_file = open(filename, encoding="utf8")
  reader = csv.reader(csv_file)
  return len(list(reader))
  
  
def create_ordered_patent_list(filename, orderkey):
  patents_df = pd.read_csv(filename)
  ordered_patent = sorted(patents_df.to_dict('records'), key=itemgetter(orderkey))
  return ordered_patent
  
# total = 3217526
search_filename = "filtered_ai_documents.csv"
patent_filename = "patent_dataset.csv"
doc_id_keyname = "doc_id"

ordered_patent_list = create_ordered_patent_list(search_filename, doc_id_keyname)
print(ordered_patent_list[0:10])
print(ordered_patent_list[2:10])

N = len(ordered_patent_list)

# ~ Initialize scraper class ~ #
scraper = scraper_class(return_abstract=True)  #<- TURN ON ABSTRACT TEXT  

# ~~ Scrape patents individually ~~ #
number_of_actual_lines = get_number_lines(patent_filename)

if number_of_actual_lines < N+1:
  it = number_of_actual_lines
  print(f'Actual line: {it}')
  for patent in ordered_patent_list[number_of_actual_lines-1:N]:
    http_error_code, soup_answer, url = scraper.request_single_patent(patent['doc_id'])
    # ~ Parse results of scrape ~ #
    try:
      patent_parsed = scraper.get_scraped_data(soup_answer, patent, url)
      patent['abstract'] = patent_parsed['abstract_text'].strip().replace("\n", "")
    except:
      patent['abstract'] = "There is not an abstract"
    patent_df = pd.DataFrame(patent, index=[0])
    patent_df.to_csv(patent_filename, mode='a', header=False, index=False, sep=";")

    #if it > 1000 and (it % 1000 == 1): files.download(patent_filename)
    it+=1
    print(it)
    
else:
  print("Finished to get all abstracts!")