import csv
import math
import heapq

from numpy.f2py.auxfuncs import throw_error


class CityGraph:
    City_pos = {"서울": (353., 205.), "파주": (332., 159.), "김포": (300., 180.), "인천": (312., 211.), "남양주": (393., 188.),
                "가평": (418., 162.), "용인": (386., 262.), "화성": (340., 272.), "여주": (445., 246.),
                "안성": (393., 297.), "춘천": (454., 150.), "홍천": (500., 170.), "횡성": (515., 215.), "평창": (557., 206.),
                "강릉": (614., 174.), "인제": (530., 120.), "천안": (390., 332.), "아산": (356., 333.), "대전": (413., 410.),
                "세종": (394., 362.), "공주": (374., 386.), "논산": (377., 438.), "태안": (261., 335.), "보령": (301., 406.),
                "청주": (422., 363.), "충주": (480., 297.), "보은": (461., 384.), "영동": (469., 447.), "단양": (544., 300.),
                "영주": (578., 322.), "안동": (606., 370.), "영양": (655., 352.), "영덕": (680., 390), "포항": (658., 431.),
                "의성": (580., 405.), "김천": (506., 460.), "대구": (577., 494.), "경주": (670., 500.), "울산": (670., 545.),
                "거창": (485., 510.), "산청": (480., 580.), "진주": (513., 605.), "고성": (538., 635.), "김해": (616., 592.),
                "부산": (645., 605.), "함안": (555., 590.), "창녕": (565., 550.), "익산": (355., 468.), "전주": (372., 492.),
                "진안": (415., 500.), "순창": (375., 570.), "영광": (278., 593.), "나주": (328., 632.), "목포": (272., 668.),
                "광주": (328., 612.), "담양": (360., 592.), "곡성": (397., 605.), "순천": (413., 643.), "보성": (374., 677.),
                "제주": (288., 832.)}
    def __init__(self):
        self.graph = {}
        self.adj = {}

    def load_data(self):
        COLUMN_TYPE = [str, str, str, float, float]
        with open('./citys_info.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                type_row = [col_type(val) for col_type, val in zip(COLUMN_TYPE, row)]
                start = type_row[0]
                end = type_row[1]
                info = type_row[2:]
                if start not in self.graph.keys():
                    self.graph[start] = {}
                if end not in self.graph[start].keys():
                    self.graph[start][end] = []
                self.graph[start][end].append(info)

    def print_data(self):
        for start in self.graph.keys():
            for end in self.graph[start].keys():
                print(f'{start} - {end}')
                for traffic, cost, time in self.graph[start][end]:
                    print(f' -> 교통: {traffic}, 비용 : {cost}, 시간 : {time}')

    def distance(self, cur, nxt):
        xc, yc = self.City_pos[cur]
        xn, yn = self.City_pos[nxt]
        return (xc - xn)**2 + (yc - yn)**2

    def heuristic(self, start, end):
        try:
            return self.distance(start, end)
        except KeyError:
            return 0.0


