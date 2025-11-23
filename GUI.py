from graph_core import CityGraph
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False


class RouteWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1400x800") #창size

        self.cg = CityGraph()
        self.cg.load_data()
        self.title("최단거리 탐색기")

        self.start_var = tk.StringVar()
        self.end_var = tk.StringVar()
        self.mode_var = tk.StringVar()

        self.widget()
        self.draw_empty_map()

    def widget(self):
        # ───────── 입력 / 버튼 영역 ─────────
        frame_top = ttk.Frame(self)
        frame_top.pack(fill="x", padx=10, pady=10)

        city_names = sorted(self.cg.City_pos.keys())

        ttk.Label(frame_top, text="출발:").grid(row=0, column=0)
        ttk.Combobox(frame_top, textvariable=self.start_var, values=city_names, width=12).grid(row=0, column=1, padx=5)

        ttk.Label(frame_top, text="도착:").grid(row=0, column=2)
        ttk.Combobox(frame_top, textvariable=self.end_var, values=city_names, width=12).grid(row=0, column=3, padx=5)

        frame_mode = ttk.LabelFrame(frame_top, text="기준")
        frame_mode.grid(row=0, column=4, padx=20)
        ttk.Radiobutton(frame_mode, text="시간", value="time", variable=self.mode_var).pack(anchor="w")
        ttk.Radiobutton(frame_mode, text="비용", value="cost", variable=self.mode_var).pack(anchor="w")
        ttk.Radiobutton(frame_mode, text="믹스", value="mix", variable=self.mode_var).pack(anchor="w")

        ttk.Button(frame_top, text="경로 찾기", command=self.on_find_route).grid(row=0, column=5, padx=20)
        ttk.Button(frame_top,text = "초기화", command=self.draw_empty_map).grid(row=0, column=6, padx=20)

        # ───────── 아래 영역 좌/우 분할 ─────────
        frame_bottom = ttk.Frame(self)
        frame_bottom.pack(fill="both", expand=True)

        # 왼쪽: matplotlib
        self.frame_map = ttk.Frame(frame_bottom)
        self.frame_map.pack(side="left", fill="both", expand=True)

        # 오른쪽: 텍스트 출력
        self.frame_info = ttk.Frame(frame_bottom)
        self.frame_info.pack(side="right", fill="both", expand=True)

        self.text_result = tk.Text(self.frame_info, font=("맑은 고딕", 11))
        self.text_result.pack(fill="both", expand=True, padx=5, pady=5)

        # ───────── 초기 지도 (경로 없이 점만) 출력 ─────────

    def draw_empty_map(self):

        fig = Figure(figsize=(8, 6))
        img = mpimg.imread("./korea_map.png")
        ax = fig.add_subplot(111)
        ax.imshow(img, extent=(0, 878, 884, 0), aspect='auto')
        # 전체 도시 찍기
        for city, (x, y) in self.cg.City_pos.items():
            ax.scatter(x, y)
            ax.text(x, y, city, fontsize=7)
        self.text_result.delete("1.0", tk.END)
        self.text_result.insert(tk.END, "출발지와 도착지를 정해주세요\n")
        self.text_result.insert(tk.END, "출발지(빨간색), 도착지(파란색), 경로(주황색)으로 표현됩니다.")

        ax.set_title("Korea_shortest_path")
        ax.axis("off")
        self._render_figure(fig)

        # ───────── 경로 찾을 때 호출 ─────────

    def on_find_route(self):
        start, end = self.start_var.get(), self.end_var.get()
        mode = self.mode_var.get()

        if start not in self.cg.City_pos or end not in self.cg.City_pos:
            messagebox.showwarning("입력 오류", "리스트에 없는 도시입니다.")
            return
        if start == end:
            messagebox.showwarning("입력 오류", "출발지와 도착지가 같습니다.")
            return
        if not start or not end:
            messagebox.showwarning("입력 오류", "도시를 선택하세요.")
            return

        path = self.cg.astar(start, end, mode=mode)
        seg_list, total_cost, total_time = self.cg.path_total(path, mode)

        # 오른쪽 텍스트 갱신
        self.text_result.delete("1.0", tk.END)
        self.text_result.insert(tk.END, f"▶ {start} → {end} 최단 경로\n")
        self.text_result.insert(tk.END, " → ".join(path) + "\n\n")
        for (tname, time, cost), (a, b) in zip(seg_list, zip(path[:-1], path[1:])):
            time_min = time%60
            time_hour = time//60
            if time_hour <1:
                self.text_result.insert(tk.END, f"{a} → {b} / {tname} / 비용: {cost:.0f}원 / 시간: {time_min:.0f} min\n")
            else: self.text_result.insert(tk.END,f"{a} → {b} / {tname} / 비용: {cost:.0f}원 / 시간: {time_hour:.0f}h {time_min:.0f} min\n")
        total_time_hour = total_time//60
        total_time_min = total_time%60
        if total_time_hour <1:
            self.text_result.insert(tk.END, f"\n총 비용: {total_cost:.0f}원\n총 시간: {total_time_min:.0f} min\n")
        else: self.text_result.insert(tk.END, f"\n총 비용: {total_cost:.0f}원\n총 시간: {total_time_hour:.0f}h {total_time_min:.0f} min\n")

        # 지도 갱신
        self.draw_path_map(path)

        # ───────── 지도 + 경로 선 그리기 ─────────

    def draw_path_map(self, path):
        fig = Figure(figsize=(8, 6))
        img = mpimg.imread("./korea_map.png")
        ax = fig.add_subplot(111)

        ax.imshow(img, extent=(0, 878, 884, 0), aspect='auto')

        sx, sy = self.cg.City_pos[path[0]]
        ex, ey = self.cg.City_pos[path[-1]]
        ax.scatter(sx, sy, color='red',zorder=2)
        ax.scatter(ex, ey, color='blue',zorder=2)

        for city in path:
            x,y = self.cg.City_pos[city]
            ax.text(x, y, city, fontsize=7)

        xs = [self.cg.City_pos[c][0] for c in path]
        ys = [self.cg.City_pos[c][1] for c in path]
        ax.plot(xs, ys, '-o', linewidth=2, color='orange', zorder=1)


        ax.set_title("Korea_shortest_path")
        ax.axis("off")
        self._render_figure(fig)

        # ───────── matplotlib을 Tkinter frame에 embed ─────────

    def _render_figure(self, fig):
        # 기존 캔버스 제거
        for w in self.frame_map.winfo_children():
            w.destroy()

        canvas = FigureCanvasTkAgg(fig, master=self.frame_map)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

if __name__ == "__main__":
    app = RouteWindow()
    app.mainloop()

