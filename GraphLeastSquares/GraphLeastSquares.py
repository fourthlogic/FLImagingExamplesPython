# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()

from ctypes import windll
import clr
import sys
import time
import random
import tkinter as tk
from tkinter import scrolledtext

def get_hwnd(widget):
    # 윈도우 핸들 얻기 (Tkinter 내부 식별자를 사용)
    # Get window handle (using Tkinter internal identifier)
    widget.update_idletasks()
    hwnd = widget.winfo_id()
    return hwnd

class FormGraphLeastSquares(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Form Graph Least Squares")
        self.geometry("800x500")

        # 그래프 뷰 영역 프레임 생성 및 배치  
        # Create and place the graph view frame
        self.view_frame = tk.Frame(self, bd=1, relief="solid")
        self.view_frame.pack(side="left", fill="both", expand=True)

        # 오른쪽 컨트롤 패널 생성 및 배치  
        # Create and place the right-side control panel
        control_panel = tk.Frame(self, width=250, bd=1, relief="solid")
        control_panel.pack(side="right", fill="y")
        self._create_controls(control_panel)

        # 그래프 뷰 인스턴스 생성  
        # Create the CGUIViewGraph instance
        self.m_viewGraph = CGUIViewGraph()

        # 타이머 시작  
        # Start the periodic timer
        self.m_timer = self.after(100, self.timer_tick)

        # 그래프 뷰 생성 및 부착  
        # Create and attach the graph view
        self.dock_graph_view()

        # 초기 데이터 생성  
        # Generate initial data
        self.click_button_add()

    # 컨트롤 패널 구성 함수  
    # Function to create the control panel UI
    def _create_controls(self, parent):
        label_name = tk.Label(parent, text="Name")
        label_name.pack(pady=(10, 0))

        # 그래프 이름 입력창  
        # Input field for graph name
        self.text_name = tk.Entry(parent, width=25)
        self.text_name.pack()

        label_degree = tk.Label(parent, text="Degree")
        label_degree.pack(pady=(10, 0))

        # 회귀식 차수 입력창  
        # Input field for polynomial degree
        self.text_degree = tk.Entry(parent, width=25)
        self.text_degree.insert(0, "2")
        self.text_degree.pack()

        # Add 버튼  
        # Add button
        self.button_add = tk.Button(parent, text="Add", command=self.click_button_add)
        self.button_add.pack(pady=(10, 0))

        # Clear 버튼  
        # Clear button
        self.button_clear = tk.Button(parent, text="Clear", command=self.click_button_clear)
        self.button_clear.pack(pady=(5, 10))

        # Info 출력창 라벨  
        # Info display label
        tk.Label(parent, text="Info").pack()

        # Info 출력 텍스트 박스  
        # Info text display area
        self.rich_text_info = scrolledtext.ScrolledText(parent, height=18, width=30, state="normal")
        self.rich_text_info.pack(pady=(0, 10))

    # 에러 메시지 박스 표시 함수  
    # Function to show an error message box
    def error_message_box(self, result, msg):
        err_msg = f"Error code : {result.GetResultCode()}\nError name : {result.GetString()}"
        if msg:
            err_msg += msg
        tk.messagebox.showerror("Error", err_msg)

    # 그래프 뷰 생성 및 도킹  
    # Create and dock the graph view into the frame
    def dock_graph_view(self):
        hwnd = get_hwnd(self.view_frame)
        self.m_viewGraph = CGUIViewGraph()
        result = self.m_viewGraph.CreateAndFitParent(hwnd)
        if result.IsFail():
            self.error_message_box(result, "")

    # Add 버튼 클릭 핸들러  
    # Event handler for Add button click
    def click_button_add(self):
        if not self.m_viewGraph.IsAvailable():
            return

        # 무작위 색상 생성  
        # Generate random color
        rand = random.Random()
        e_color = EColor(rand.randint(0, 255) |
                         (rand.randint(0, 255) << 8) |
                         (rand.randint(0, 255) << 16), True)

        # 그래프 이름 가져오기  
        # Get chart name
        str_chart_name = self.text_name.get()
        if str_chart_name == "":
            str_chart_name = "Random Data"

        # 차수(degree) 가져오기 및 유효성 검사  
        # Get and validate degree
        str_degree = self.text_degree.get()
        try:
            degree = int(str_degree)
        except ValueError:
            self.rich_text_info.config(state="normal")
            self.rich_text_info.delete("1.0", "end")
            self.rich_text_info.insert("end", "Please check the degree.")
            self.rich_text_info.config(state="disabled")
            return

        # 산점도용 난수 데이터 생성  
        # Generate random scatter data
        count = 100
        arr_x = [0.0] * count
        arr_y = [0.0] * count
        prev_x, prev_y = 0.0, 0.0
        for i in range(count):
            arr_x[i] = prev_x + rand.randint(0, 99) / 10.0
            offset = rand.randint(0, 99) / 10.0
            arr_y[i] = prev_y + offset if rand.randint(0, 1) else prev_y - offset
            prev_x, prev_y = arr_x[i], arr_y[i]

        # 산점도 플롯  
        # Plot scatter chart
        self.m_viewGraph.Plot(arr_x, arr_y, count, EChartType.Scatter, e_color, str_chart_name)
        self.m_viewGraph.ZoomFit()
        self.m_viewGraph.Invalidate()

        # 차수가 0이면 종료  
        # Abort if degree is zero
        if degree == 0:
            self.rich_text_info.config(state="normal")
            self.rich_text_info.delete("1.0", "end")
            self.rich_text_info.insert("end", "Please check the degree.")
            self.rich_text_info.config(state="disabled")
            return

        # 최소자승법 객체 생성 및 데이터 입력  
        # Create least squares instance and assign data
        ls = CLeastSquares[Double]()
        ls.Assign(arr_x, arr_y, count)

        # 회귀 결과 저장용 리스트 및 R² 초기화  
        # Prepare output list and initial R-squared
        list_output = List[Double]()
        r_square = 0.0
        res, list_output, r_square = ls.GetPoly(degree, list_output, r_square)

        # 결과 비었을 경우 안내  
        # Show message if result is empty
        if list_output.Count == 0:
            self.rich_text_info.config(state="normal")
            self.rich_text_info.delete("1.0", "end")
            self.rich_text_info.insert("end", "Empty result")
            self.rich_text_info.config(state="disabled")
            return

        # 회귀식 문자열 생성  
        # Build polynomial equation string
        equation = ""
        precision = degree + 12
        for i in range(list_output.Count):
            coef = list_output[i]
            if coef == 0:
                continue
            if equation and coef > 0:
                equation += " + "
            if i == list_output.Count - 2:
                equation += f"{coef:{precision}}*x"
            elif i == list_output.Count - 1:
                equation += f"{coef:{precision}}"
            else:
                power = list_output.Count - 1 - i
                equation += f"{coef:.{precision}f}*x^{power}"

        # 회귀식 그리기  
        # Plot the polynomial curve
        if equation:
            exp = CExpression()
            exp.SetExpression(equation)
            self.m_viewGraph.Plot(exp, e_color)
            self.m_viewGraph.Invalidate()

        # R² 결과 출력  
        # Display R-squared value
        self.rich_text_info.config(state="normal")
        self.rich_text_info.delete("1.0", "end")
        self.rich_text_info.insert("end", f"R square value: {r_square}")
        self.rich_text_info.config(state="disabled")

    # Clear 버튼 클릭 핸들러  
    # Event handler for Clear button click
    def click_button_clear(self):
        if not self.m_viewGraph.IsAvailable():
            return
        self.m_viewGraph.Clear()
        self.m_viewGraph.Invalidate()

    # 타이머 틱: 버튼 상태 업데이트  
    # Timer tick: update control states
    def timer_tick(self):
        self.button_add.config(state="normal" if self.m_viewGraph.IsAvailable() else "disabled")
        self.button_clear.config(state="normal" if self.m_viewGraph.IsAvailable() and self.m_viewGraph.DoesGraphExist() else "disabled")
        self.m_timer = self.after(100, self.timer_tick)


if __name__ == "__main__":
    app = FormGraphLeastSquares()
    app.mainloop()

# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}')
