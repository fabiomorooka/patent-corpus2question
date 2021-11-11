#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import sys
import time
import csv  
import pandas as pd
from operator import itemgetter

from utils import file_handling as file

# Ref.: https://pypi.org/project/google-patent-scraper/
from google_patent_scraper import scraper_class
 
def get_number_lines(filename):
  csv_file = open(filename, encoding="utf8")
  reader = csv.reader(csv_file)
  return len(list(reader))
  
def create_ordered_patent_list(filename, orderkey):
  patents_df = pd.read_csv(filename)
  ordered_patent = sorted(patents_df.to_dict('records'), key=itemgetter(orderkey))
  return ordered_patent

def get_abstract_info(search_filename):

    header = ['doc_id','pub_dt','appl_id','predict50_any_ai','ai_score_ml', 'predict50_ml', 'ai_score_evo', 'predict50_evo', 'ai_score_nlp', 'predict50_nlp', 'ai_score_speech', 'predict50_speech', 'ai_score_vision', 'predict50_vision', 'ai_score_kr', 'predict50_kr', 'ai_score_planning', 'predict50_planning', 'ai_score_hardware', 'predict50_hardware', 'abstract']
    abstract_filename = "patent_dataset.csv"
    no_abstract_filename = "no_abstract_dataset.csv"
    if not(os.path.exists(abstract_filename)): file.create_file(abstract_filename, header)
    if not(os.path.exists(no_abstract_filename)): file.create_file(no_abstract_filename, header)

    # Global variables, for now they are hardcoded and these files must be provided by the authors
    DOCID_KEYNAME = "doc_id"

    ordered_patent_list = create_ordered_patent_list(search_filename, DOCID_KEYNAME)
    print(ordered_patent_list[0:10])
    print(ordered_patent_list[2:10])

    N = len(ordered_patent_list)

    # ~ Initialize scraper class ~ #
    scraper = scraper_class(return_abstract=True)  #<- TURN ON ABSTRACT TEXT  

    # ~~ Scrape patents individually ~~ #
    number_of_actual_lines = get_number_lines(abstract_filename)

    if number_of_actual_lines < N+1:
      it = number_of_actual_lines
      print(f'Actual line: {it}')
      for patent in ordered_patent_list[number_of_actual_lines-1:N]:
        http_error_code, soup_answer, url = scraper.request_single_patent(patent['doc_id'])
        # ~ Parse results of scrape ~ #
        try:
          patent_parsed = scraper.get_scraped_data(soup_answer, patent, url)
          patent_abstract_list = patent_parsed['abstract_text'].split()
          patent['abstract'] = " ".join(patent_abstract_list)
          patent_df = pd.DataFrame(patent, index=[0])
          patent_df.to_csv(abstract_filename, mode='a', header=False, index=False, sep=";")
        except:
          patent['abstract'] = "There is not an abstract"
          patent_df = pd.DataFrame(patent, index=[0])
          patent_df.to_csv(no_abstract_filename, mode='a', header=False, index=False, sep=";")

        if (it - number_of_actual_lines) == 3000: break
        it+=1
        print(f'Requision number: {it - number_of_actual_lines}:{3000}')
        print(f'Document line number: {it}')
        
    else:
      print("Finished to get all abstracts!")
      
    
if __name__ == '__main__':
    get_abstract_info("filtered_ai_documents_2.csv")
    time.sleep(10)

    # Run a new iteration of the current script, providing any command line args from the current iteration.
    os.execv(sys.executable, [sys.executable, __file__] + sys.argv)