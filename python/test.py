import tkinter as tk
from tkinter import ttk
import json
import os

# 현재 스크립트 파일이 있는 디렉토리의 절대 경로
base_dir = os.path.dirname(os.path.abspath(__file__))

# 현재 로드된 파일 번호와 최대 파일 번호
current_file_index = 0
max_file_index = 10

def load_json(file_index):
    file_name = f'{file_index}.json'
    file_path = os.path.join(base_dir, 'resources', 'case', file_name)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# 초기 JSON 파일 불러오기
data = load_json(current_file_index)

# 메인 윈도우 생성
root = tk.Tk()
root.title("Gauge and Buttons Example")

# 윈도우 크기 설정
root.geometry("400x500")

# 게이지의 초기 값들을 저장하는 리스트
gauge_values = [10, 10, 10, 10]  # 체급, 효율, 활력, 저항 각각의 초기값 10

# 게이지와 이름을 담을 프레임 생성
gauge_frame = tk.Frame(root)
gauge_frame.pack(side=tk.TOP, pady=20)

# 4개의 세로 게이지와 이름 생성
gauges = []
gauge_names = ["체급", "효율", "활력", "저항"]

for i in range(4):
    gauge = ttk.Progressbar(gauge_frame, orient="vertical", length=200, mode="determinate", maximum=20)
    gauge.grid(row=0, column=i, padx=10)
    gauge['value'] = gauge_values[i]  # 각 게이지의 초기값 설정
    gauges.append(gauge)
    
    label = tk.Label(gauge_frame, text=gauge_names[i])
    label.grid(row=1, column=i, padx=10)

# 게이지 값을 변경하는 함수
def modify_gauges(modification):
    gauge_values[0] = max(0, min(20, gauge_values[0] + modification['weight']))
    gauge_values[1] = max(0, min(20, gauge_values[1] + modification['efficiency']))
    gauge_values[2] = max(0, min(20, gauge_values[2] + modification['vitality']))
    gauge_values[3] = max(0, min(20, gauge_values[3] + modification['resistance']))
    
    # 게이지 값 업데이트
    for i in range(4):
        gauges[i]['value'] = gauge_values[i]

# 다음 파일을 로드하고 인터페이스를 업데이트하는 함수
def load_next_file():
    global current_file_index, data
    
    # 파일 인덱스 증가
    current_file_index += 1
    
    # 파일 인덱스가 범위를 넘어가면 다시 처음으로
    if current_file_index > max_file_index:
        current_file_index = 0
    
    # 새로운 JSON 파일 불러오기
    data = load_json(current_file_index)
    
    # 중앙 텍스트와 버튼 텍스트 업데이트
    central_label.config(text=data["cardText"])
    left_button.config(text=data["leftAction"]["text"])
    right_button.config(text=data["rightAction"]["text"])

    # 버튼의 command를 업데이트
    left_button.config(command=lambda: [modify_gauges(data["leftAction"]["statsModification"]), load_next_file()])
    right_button.config(command=lambda: [modify_gauges(data["rightAction"]["statsModification"]), load_next_file()])

# 하단 중앙의 편집 불가능한 텍스트 라벨
text_frame = tk.Frame(root)
text_frame.pack(side=tk.TOP, pady=20)

central_label = tk.Label(text_frame, text=data["cardText"], relief="solid", width=20)
central_label.pack(side=tk.TOP)

# 버튼 프레임 생성
button_frame = tk.Frame(root)
button_frame.pack(side=tk.TOP, pady=20)

# 왼쪽 버튼 (leftAction)
left_button = tk.Button(button_frame, text=data["leftAction"]["text"], width=20, 
                        command=lambda: [modify_gauges(data["leftAction"]["statsModification"]), load_next_file()])
left_button.grid(row=0, column=0, padx=10)

# 오른쪽 버튼 (rightAction)
right_button = tk.Button(button_frame, text=data["rightAction"]["text"], width=20, 
                         command=lambda: [modify_gauges(data["rightAction"]["statsModification"]), load_next_file()])
right_button.grid(row=0, column=1, padx=10)

root.mainloop()
