# OSS 프로젝트  
## **Korea_Shortest_Map_Search**

---

## 1. 개요

**Korea_Shortest_Map_Search**는 대한민국 주요 도시들을 그래프 구조로 모델링하고,  
A\* (A-star) 알고리즘을 이용하여 **최단 경로를 탐색·시각화하는 프로그램**이다.

도시 간 이동 정보(교통수단, 비용, 시간)를 기반으로  
- **시간 기준**
- **비용 기준**
- **시간 + 비용 혼합 기준**

중 하나를 선택하여 최적의 경로를 찾을 수 있으며,  
Tkinter와 Matplotlib을 활용한 GUI를 통해 결과를 **지도 위에 직관적으로 표현**한다.

---

## 2. 구현

본 프로젝트는 크게 **그래프 처리**, **GUI 시각화**, **메인 실행부**, **경로 csv**의 네 파일로 구성된다.

---

### 2.1 `graph_core.py`

도시 간 경로를 그래프로 구성하고, **A\* 알고리즘을 이용한 최단 경로 탐색**을 담당하는 핵심 모듈이다.

#### 주요 기능

- **도시 좌표 관리**
  - `City_pos` 딕셔너리를 통해 각 도시의 지도상 좌표를 저장  
- City_pos 딕셔너리  
  ![City_pos](https://github.com/park2722/OSS_Project/blob/main/README%20image/dict_city_pos.png)  
  - Heuristic 계산에 사용

- **CSV 기반 그래프 로딩**
  - `citys_info.csv` 파일을 읽어  
    `출발도시, 도착도시, 교통수단, 시간, 비용`  
    형태의 데이터를 그래프로 구성

- **A\* 알고리즘 적용**
  - `astar(start, end, mode)`
  - Heuristic: 도시 간 좌표 거리 기반
  - mode에 따라 가중치 결정
    - `time` : 소요 시간 우선
    - `cost` : 비용 우선
    - `mix` : (비용/1000 + 시간) 혼합 평가

- **최종 경로 비용 계산**
  - `path_total()`을 통해
    - 구간별 최적 교통수단
    - 총 비용
    - 총 소요 시간
    계산

#### 특징

- 휴리스틱을 활용한 **A\* 알고리즘 구현**
- 다양한 교통수단 중 최적의 선택 가능
- CSV 데이터 확장을 통한 범용성 확보

---

### 2.2 `GUI.py`

Tkinter와 Matplotlib을 이용하여 **사용자 인터페이스와 지도 시각화**를 담당하는 모듈이다.

#### GUI 구성
-전체 GUI  
![전체 UI](https://github.com/park2722/OSS_Project/blob/main/README%20image/GUI.png)
- **입력 영역**
  - 출발 도시 선택
  - 도착 도시 선택
  - 탐색 기준 선택 (시간 / 비용 / 믹스)  
  1. 초기 입력 상태  
![입력 영역 init](https://github.com/park2722/OSS_Project/blob/main/README%20image/GUI_input.png)  
  1. 도시 선택  
![입력 영역 select](https://github.com/park2722/OSS_Project/blob/main/README%20image/GUI_input_select.png)  

- **지도 영역**
  - 대한민국 지도 이미지 출력
  - 최단 경로 시각화
    - 출발지 : 빨간색
    - 도착지 : 파란색
    - 이동 경로 : 주황색  
    - 초기 지도 상태  
![empty map](https://github.com/park2722/OSS_Project/blob/main/README%20image/GUI_empty.png)
     - 경로 지도 출력  
![path map](https://github.com/park2722/OSS_Project/blob/main/README%20image/GUI_pathdraw.png)  

- **결과 출력 영역**
  - 이동 경로 출력
  - 구간별 교통수단, 비용, 시간
  - 총 비용 및 총 소요 시간  
  - 초기 텍스트  
![출력 영역 init](https://github.com/park2722/OSS_Project/blob/main/README%20image/GUI_init_txt.png)  
  - 경로 텍스트  
![출력 영역 rslt](https://github.com/park2722/OSS_Project/blob/main/README%20image/GUI_rslt_txt.png)  

#### 주요 기능

- `draw_empty_map()`  
  경로 없이 전체 도시만 지도에 출력

- `on_find_route()`  
  입력값 검증 후 A\* 알고리즘을 이용해 경로 계산 및 시각화

- `draw_path_map(path)`  
  최단 경로를 지도 상에 선으로 표시

#### 특징

- 알고리즘 로직과 UI 로직 분리
- Matplotlib을 Tkinter 내부에 삽입하여 실시간 갱신
- 한글 도시명 깨짐 방지를 위한 폰트 설정 적용

---

### 2.3 `korea_Shortest_Map_Search.py`

프로그램의 **메인 실행 파일**로, GUI를 실행하는 역할을 담당한다.

```python
from GUI import RouteWindow

app = RouteWindow()
app.mainloop()
```
-	GUI 객체 생성
-	이벤트 루프 실행

---

### 2.4 `city_info.csv`
도시간 간선을 저장하고 있는 `csv파일`이다.  
![csv image](https://github.com/park2722/OSS_Project/blob/main/README%20image/Csv_image.png)

- 위 이미지와 같은 형태로 데이터들을 저장  
    순서대로, `출발도시, 도착도시, 교통수단, 시간, 비용`  
    `총 302개의 경로`가 저장되어 있다

- 경로들은 **양방향** 간선을 보장
    - `출발지-도착지` 간선에 매칭되는  
    `도착지-출발지` 간선이 포함

- 동일한 `출발지-도착지`를 가진 경로 중,  
다른 `교통수단`을 가진 간선이 존재  
`graph_core.py`에서 이를 구분하여 저장

---

## 3. 소감
이번 프로젝트는 지금까지 다양한 과목들에서 배웠던 것을 최대한 활용해보기 위해 제작했습니다.  

2년의 기간동안 배운 **객체지향**, **알고리즘**, **파이썬**, **자료구조** 등의 개념들을 활용했습니다.  
`graph_core.py`, `GUI.py`, `korea_Shortest_Map_Search.py`로 나누는 과정은 **객체지향**에서,  
`A* 알고리즘`은 **알고리즘**에서, `A*`에 활용된 `Priority Queue`는 **자료구조**,  
마지막으로 작성된 코드는 **OSS**에서 배운 `파이썬`.  
이렇게 배운 것들을 실제 활용하여 프로그램을 만드는 것은 굉장히 신선한 경험이었습니다.  

프로젝트를 진행하면서 몇가지 어려움이 존재했습니다.  
- 파이썬 자체의 숙련도 문제
- 도시간 경로 저장 문제  
- 지도 상 도시 위치 저장 문제  

이러한 문제들을 해결하기 위해 최대한 노력했습니다.  

1. 파이썬 자체 숙련도 문제는 강의 자료에 있는 여러 예시 코드, 이미지를 보면서 따라 적어 보았습니다.  
이런 방식을 통해 파이썬에 대한 경험을 차근차근 쌓아 해당 프로젝트를 완성할 수 있을 정도까지 완성했습니다.  

2. 도시간 경로 저장 문제는 우선 경로를 선택하는 과정부터 어려움이 있었습니다.  
같은 도시간 경로지만 다양한 교통수단의 존재를 고려해야 되므로 기본적으로 **데이터가 너무 많았습니다.**   
추출하는 과정들은 **생성형 AI**를 통해 데이터를 생성해주었고, 이를 csv 형태로 저장하고자 했습니다.  
하지만 인코딩 방식이 작성한 코드와 맞지 않아, 이를 통일하기 위해 직접 csv 파일을 작성했습니다.  

    이를 `graph_core.py`에서 읽어야 하는데 이에 대한 저장 방식을 고민했습니다.  
    이것은 `딕셔너리`에 출발지를 `key`로써 하고, 도착지를 리스트의 형태로 해당 key에 할당했습니다.  
    이러한 방식으로 그래프의 형태를 제작하여 접근 및 확장에 용이하게 제작했습니다.  

3. 지도 상 도시 위치 저장 문제는 `GUI`의 크기에 따라 위치 조정의 필요성이 생겼습니다.  
이는 지도에 맞춰 좌표 생성의 무리가 있음을 의미했습니다.  
결국 지도의 크기를 고정하고, 해당 도시의 위치를 직접 딕셔너리의 형태로 `City_pos`에 저장했습니다.  

위 문제들을 해결 해나가며 완성한 작품에는 아쉬움이 남아있습니다.  
- 도시간 경로에 대한 정보도 csv에 저장하는 것이 아닌 실시간으로 반영할 수 있는 것으로 대체
- 지도 상 위치를 반영할 수 있는 좌표 설정 방법(수동이 아닌 방법)을 찾는 것
- 이 작품이 python 실행 환경이 아닌 웹페이지와 연결하여 조작할 수 있게 하는 방법

이러한 아쉬움을 이후 개인적으로 하나씩 해결하고 싶습니다.
---

##  부록

- 사용한 지도 이미지  
![map](https://github.com/park2722/OSS_Project/blob/main/korea_map.png)
