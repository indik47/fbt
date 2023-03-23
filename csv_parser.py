import csv
import re

"""Automate batch export of character assets into outsource repository
Uses content tracker dump (into .csv)
"""
file_ = 'K1 - NX - Tech.Art Optimization Process - Characters - Assets for 3d Art.csv'
chars = ['Scorpion', 'SubZero', 'Ashrah', 'KungLao', 'Raiden', 'Smoke', 'LiuKang', 'LiMei', 'Havik', 'Reiko', 'Nitara', 'Kenshi', 'RainMage', 'JohnnyCage',
'Tanya', 'ShaoKahn', 'Baraka', 'ShangTsung', 'Mileena', 'Sindel', 'Kitana', 'Reptile', 'Geras', 'QuanChi', 'Ermac']

char_end_delimiters = ['Total', 'Skin', 'Cloth', 'Hair', 'Gear', 'Other', 'Number']
char_end_regex = re.compile('|'.join(char_end_delimiters))

class Categorisation:
    categories = {
        'skin': ['skin'],
        'cloth': ['cloth', 'cloth additional'],
        'hair': ['hair', 'hair strand'],
        'gear': ['mask', 'scabbard', 'sword', 'texture variation'],
        'prop': ['prop'],
    }

    def __init__(self) -> None:
        pass
    
    @classmethod
    def categorise(cls, string):
        for k,v in cls.categories.items():
            regex = re.compile('|'.join(v))
            match = re.match(regex, string)

            if match:
                category = k
                return category
            
        return 'other'

class CSVParser:
    def __init__(self) -> None:
        self.data = {}            

    def parse_(self, csv_file):
        with open(csv_file, newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            
            next_row_is_an_asset=False
            current_char = ''

            for row in spamreader:
                # Character name starts a section
                if row[0] in chars:
                    next_row_is_an_asset = True
                    current_char = row[0]
                    self.data[current_char] = dict()
                    continue
                
                # Any of the delimiters ends section
                char_end_match = re.match(char_end_regex, row[0])
                if char_end_match:
                    current_char = ''
                    next_row_is_an_asset = False
                    continue
                
                if next_row_is_an_asset:
                    type_= Categorisation.categorise(row[4])
                    self.data[current_char].setdefault(type_, [])

                    self.data[current_char][type_].append(row[0])


parser = CSVParser()
data = parser.parse_(file_)

for k in data.keys():
    categories = data[k].keys()
    print(categories)
    for category in categories:
        print(f'{category} number of assets {len(data[k][category])}')
    
        
        