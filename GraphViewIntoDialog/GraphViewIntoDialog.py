# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *
from ctypes import windll
import clr
import sys
import time
import random
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext

from System.Numerics import Complex
from System import Double
from System.Collections.Generic import List

def get_hwnd(widget):
    # 윈도우 핸들 얻기 (Tkinter 내부 식별자를 사용)
    widget.update_idletasks()
    hwnd = widget.winfo_id()
    print(f"HWND: {hwnd}")
    return hwnd
class GraphViewIntoDialog(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GraphViewIntoDialog")
        self.geometry("740x500")

        # 왼쪽 패널 (그래프 영역)
        # Left panel (graph view area)
        self.left_panel = tk.Frame(self, relief="solid", borderwidth=1)
        self.left_panel.pack(side="left", fill="both", expand=True)

        # 오른쪽 컨트롤 패널
        # Right control panel
        self.right_panel = tk.Frame(self, width=160, relief="solid", borderwidth=1)
        self.right_panel.pack(side="right", fill="y")

        self._create_right_controls()
        
        # 그래프 뷰어 생성
        # Create the graph viewer
        self.m_viewGraph = CGUIViewGraph()
        if (result := self.m_viewGraph.CreateAndFitParent(get_hwnd(self.left_panel))).IsFail():
            print("Failed to crate Graph View")

        # 시작 시 초기 그래프 추가
        # Add default graph on startup
        self.on_click_button_add()

    def _create_right_controls(self):
        # 컨트롤 그룹 프레임 생성
        # Create right-side control group
        group_frame = tk.LabelFrame(self.right_panel, text="Quartic Equation", padx=5, pady=5)
        group_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # 계수 입력 필드 생성
        # Create input fields for coefficients a, b, c, d, e
        labels = ['a:', 'b:', 'c:', 'd:', 'e:']
        values = ['0.003', '-0.003', '-1', '1', '0']
        self.inputs = []

        for i in range(5):
            tk.Label(group_frame, text=labels[i]).grid(row=i, column=0, sticky="w")
            entry = tk.Entry(group_frame, width=15)
            entry.insert(0, values[i])
            entry.grid(row=i, column=1)
            entry.config(state="normal")
            self.inputs.append(entry)

        # Add 버튼
        # Add button
        self.add_button = tk.Button(group_frame, text="Add", width=18, command=self.on_click_button_add)
        self.add_button.grid(row=5, column=0, columnspan=2, pady=(10, 0))

        # Clear 버튼
        # Clear button
        self.clear_button = tk.Button(group_frame, text="Clear", width=18, command=self.on_click_button_clear)
        self.clear_button.grid(row=6, column=0, columnspan=2, pady=(5, 0))

        # 결과 라벨
        # Result label
        tk.Label(group_frame, text="Info").grid(row=7, column=0, sticky="w", pady=(10, 0))

        # 결과 출력 박스
        # Output result text area
        self.result_box = scrolledtext.ScrolledText(group_frame, width=22, height=10, state="normal")
        self.result_box.grid(row=8, column=0, columnspan=2, pady=(0, 5))

    def on_click_button_add(self):
        if not self.m_viewGraph.IsAvailable():
            return
        
        arrF64Coef = [0.0] * 5
        arrCpxCoef = [Complex(0, 0)] * 5
        strEquation = ""

        # 입력된 계수로 방정식 문자열 구성
        # Build equation string from coefficient inputs
        for i in range(5):
            arrF64Coef[i] = float(self.inputs[i].get())
            if arrF64Coef[i] == 0:
                continue

            if strEquation != "" and arrF64Coef[i] > 0:
                strEquation += " + "

            if i == 3:
                strFormat = f"{arrF64Coef[i]}*x"
            elif i == 4:
                strFormat = f"{arrF64Coef[i]}"
            else:
                strFormat = f"{arrF64Coef[i]}*x^{4 - i}"

            arrCpxCoef[i] = Complex(arrF64Coef[i], 0)
            strEquation += strFormat

        if strEquation == "":
            return

        # 방정식 해 구하기
        # Solve the quartic equation
        str_info = ""
        listResult = List[Complex]()
        result = CEquation.Quartic(arrCpxCoef[0], arrCpxCoef[1], arrCpxCoef[2], arrCpxCoef[3], arrCpxCoef[4], listResult)[0]

        # 해 결과 문자열로 구성
        # Format solution roots to string
        if result.IsOK():
            for cp in listResult:
                if cp.Imaginary == 0:
                    strCP = f"{cp.Real}"
                elif cp.Imaginary > 0:
                    strCP = f"{cp.Real}+{cp.Imaginary}i"
                else:
                    strCP = f"{cp.Real}{cp.Imaginary}i"
                str_info += strCP + "\n"

        # 수식 객체 생성 및 그래프에 추가
        # Create expression and plot it to the graph view
        exp = CExpression()
        exp.SetExpression(strEquation)

        # 무작위 색상 생성 (R | G<<8 | B<<16)
        # Generate random RGB color
        color_int = (random.randint(0, 255) |
                     (random.randint(0, 255) << 8) |
                     (random.randint(0, 255) << 16))
        color = EColor(color_int, True)

        self.m_viewGraph.Plot(exp, color)
        self.m_viewGraph.ZoomFit()

        # 결과 출력
        # Output result to info box
        self.result_box.config(state="normal")
        self.result_box.delete("1.0", "end")
        self.result_box.insert("end", "[root]" + str_info)
        self.result_box.config(state="disabled")

    def on_click_button_clear(self):
        if not self.m_viewGraph.IsAvailable():
            return

        # 그래프 뷰의 데이터를 초기화
        # Clear data from the graph view
        self.m_viewGraph.Clear()
        self.m_viewGraph.Invalidate()

if __name__ == "__main__":
    app = GraphViewIntoDialog()
    app.mainloop()


# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}')
