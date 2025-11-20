import matplotlib.pyplot as plt
import cv2
from graph_core import CityGraph

#이미지 저장 위치로 변경 필요
image = cv2.imread("./korea_map.png")
height, width = image.shape[:2]
Scale_up = cv2.resize(image, None, None,2,2, cv2.INTER_CUBIC)
plt.figure(figsize=(10, 7))
plt.imshow(image)

myGraph = CityGraph()
CityGraph.load_data(myGraph)
CityGraph.print_data(myGraph)

x_values = [myGraph.City_pos[city][0] for city in myGraph.City_pos]
y_values = [myGraph.City_pos[city][1] for city in myGraph.City_pos]
plt.scatter(x_values, y_values, color="blue",s = 5)
plt.show()
