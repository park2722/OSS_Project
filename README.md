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
![전체 UI](https://github.com/park2722/OSS_Project/blob/main/README%20image/GUI.png)
- **입력 영역**
  - 출발 도시 선택
  - 도착 도시 선택
  - 탐색 기준 선택 (시간 / 비용 / 믹스)  
![입력 영역 init](https://github.com/park2722/OSS_Project/blob/main/README%20image/GUI_input.png)  
![입력 영역 select](https://github.com/park2722/OSS_Project/blob/main/README%20image/GUI_input_select.png)

- **지도 영역**
  - 대한민국 지도 이미지 출력
  - 최단 경로 시각화
    - 출발지 : 빨간색
    - 도착지 : 파란색
    - 이동 경로 : 주황색  
![empty map](https://github.com/park2722/OSS_Project/blob/main/README%20image/GUI_empty.png) ![path map](https://github.com/park2722/OSS_Project/blob/main/README%20image/GUI_pathdraw.png)  

- **결과 출력 영역**
  - 이동 경로 출력
  - 구간별 교통수단, 비용, 시간
  - 총 비용 및 총 소요 시간  
![출력 영역 init](https://github.com/park2722/OSS_Project/blob/main/README%20image/GUI_init_txt.png)
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

---

##  부록

사용한 지도 이미지  
![map](https://github.com/park2722/OSS_Project/blob/main/korea_map.png)
