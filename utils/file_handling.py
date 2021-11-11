#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import csv

def create_empty_csv_file(filename, header):
    with open(filename, 'w', encoding='UTF8') as f:
        writer = csv.writer(f, delimiter=";")

        writer.writerow(header)

def delete_file(filename):
    if os.path.exists(filename): os.remove(filename)

def create_file(filename, header):
    create_empty_csv_file(filename=filename, header=header)
