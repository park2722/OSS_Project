import matplotlib.pyplot as plt
import cv2
from graph_core import CityGraph

#이미지 저장 위치로 변경 필요
# image = cv2.imread("C:/Users/user/OneDrive/바탕 화면/OSS_Project/korea_map.png")
# plt.figure(figsize=(10, 7))
# plt.imshow(image)
# plt.show()

myGraph = CityGraph()
CityGraph.load_data(myGraph)
CityGraph.print_data(myGraph)

