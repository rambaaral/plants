import tkinter as tk
from tkinter import ttk

# 메인 윈도우 생성
window = tk.Tk()
window.title("Gauge and Buttons Example")

# 윈도우 크기 설정
window.geometry("400x500")

# 게이지와 이름을 담을 프레임 생성
gauge_frame = tk.Frame(window)
gauge_frame.pack(side=tk.TOP, pady=20)

# 4개의 세로 게이지와 이름 생성
gauges = []
gauge_names = ["체급", "효율", "활력", "저항력"]

for i in range(4):
    gauge = ttk.Progressbar(gauge_frame, orient="vertical", length=200, mode="determinate")
    gauge.grid(row=0, column=i, padx=10)
    gauges.append(gauge)
    
    label = tk.Label(gauge_frame, text=gauge_names[i])
    label.grid(row=1, column=i, padx=10)

# 하단 중앙의 편집 불가능한 텍스트 라벨
text_frame = tk.Frame(window)
text_frame.pack(side=tk.TOP, pady=20)

central_label = tk.Label(text_frame, text="Central Text", relief="solid", width=20)
central_label.pack(side=tk.TOP)

# 버튼 프레임 생성
button_frame = tk.Frame(window)
button_frame.pack(side=tk.TOP, pady=20)

# 버튼 생성
left_button = tk.Button(button_frame, text="Left Button", width=20)
left_button.grid(row=0, column=0, padx=10)

right_button = tk.Button(button_frame, text="Right Button", width=20)
right_button.grid(row=0, column=1, padx=10)

window.mainloop()