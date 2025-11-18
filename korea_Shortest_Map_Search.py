import matplotlib.pyplot as plt
import cv2

#이미지 저장 위치로 변경 필요
image = cv2.imread("C:/Users/user/PyCharmMiscProject/korea_map.png")
plt.figure(figsize=(10, 7))
plt.imshow(image)
plt.show()