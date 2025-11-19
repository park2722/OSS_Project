import csv
import math
import heapq

class CityGraph:
    def __init__(self):
        self.graph = []
        self.adj = []

    def load_data(self):
        COLUMN_TYPE = [str, str, str, float, float]
        with open('./citys_info.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                type_row = [col_type(row) for col_type, row in zip(COLUMN_TYPE, row)]
                self.graph.append(type_row)

    def print_data(self):
        for lists in self.graph:
            print(lists)