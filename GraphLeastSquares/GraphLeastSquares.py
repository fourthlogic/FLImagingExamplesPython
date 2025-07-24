# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *
from ctypes import windll
import clr
import sys
import time
import random
import tkinter as tk
from tkinter import scrolledtext

def get_hwnd(widget):
    # 윈도우 핸들 얻기 (Tkinter 내부 식별자를 사용)
    widget.update_idletasks()
    hwnd = widget.winfo_id()
    print(f"HWND: {hwnd}")
    return hwnd

class FormGraphLeastSquares(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Form Graph Least Squares")
        self.geometry("800x500")

        self.view_frame = tk.Frame(self, bd=1, relief="solid")
        self.view_frame.pack(side="left", fill="both", expand=True)

        control_panel = tk.Frame(self, width=250, bd=1, relief="solid")
        control_panel.pack(side="right", fill="y")
        self._create_controls(control_panel)

        self.m_viewGraph = CGUIViewGraph()
        self.m_timer = self.after(100, self.timer_tick)

        # 그래프 뷰 생성 및 부착
        self.dock_graph_view()
        self.click_button_add()

    def _create_controls(self, parent):
        label_name = tk.Label(parent, text="Name")
        label_name.pack(pady=(10, 0))
        self.text_name = tk.Entry(parent, width=25)
        self.text_name.pack()

        label_degree = tk.Label(parent, text="Degree")
        label_degree.pack(pady=(10, 0))
        self.text_degree = tk.Entry(parent, width=25)
        self.text_degree.insert(0, "2")
        self.text_degree.pack()

        self.button_add = tk.Button(parent, text="Add", command=self.click_button_add)
        self.button_add.pack(pady=(10, 0))

        self.button_clear = tk.Button(parent, text="Clear", command=self.click_button_clear)
        self.button_clear.pack(pady=(5, 10))

        tk.Label(parent, text="Info").pack()
        self.rich_text_info = scrolledtext.ScrolledText(parent, height=18, width=30, state="normal")
        self.rich_text_info.pack(pady=(0, 10))

    def error_message_box(self, result, msg):
        err_msg = f"Error code : {result.GetResultCode()}\nError name : {result.GetString()}"
        if msg:
            err_msg += msg
        tk.messagebox.showerror("Error", err_msg)

    def dock_graph_view(self):
        hwnd = get_hwnd(self.view_frame)
        self.m_viewGraph = CGUIViewGraph()
        result = self.m_viewGraph.CreateAndFitParent(hwnd)
        if result.IsFail():
            self.error_message_box(result, "")

    def click_button_add(self):
        if not self.m_viewGraph.IsAvailable():
            return

        rand = random.Random()
        e_color = EColor(rand.randint(0, 255) |
                         (rand.randint(0, 255) << 8) |
                         (rand.randint(0, 255) << 16), True)

        str_chart_name = self.text_name.get()
        if str_chart_name == "":
            str_chart_name = "Random Data"

        str_degree = self.text_degree.get()

        try:
            degree = int(str_degree)
        except ValueError:
            self.rich_text_info.config(state="normal")
            self.rich_text_info.delete("1.0", "end")
            self.rich_text_info.insert("end", "Please check the degree.")
            self.rich_text_info.config(state="disabled")
            return

        count = 100
        arr_x = [0.0] * count
        arr_y = [0.0] * count
        prev_x, prev_y = 0.0, 0.0
        for i in range(count):
            arr_x[i] = prev_x + rand.randint(0, 99) / 10.0
            offset = rand.randint(0, 99) / 10.0
            arr_y[i] = prev_y + offset if rand.randint(0, 1) else prev_y - offset
            prev_x, prev_y = arr_x[i], arr_y[i]

        self.m_viewGraph.Plot(arr_x, arr_y, count, EChartType.Scatter, e_color, str_chart_name)
        self.m_viewGraph.ZoomFit()
        self.m_viewGraph.Invalidate()

        if degree == 0:
            self.rich_text_info.config(state="normal")
            self.rich_text_info.delete("1.0", "end")
            self.rich_text_info.insert("end", "Please check the degree.")
            self.rich_text_info.config(state="disabled")
            return

        ls = CLeastSquares[Double]()
        ls.Assign(arr_x, arr_y, count)
        list_output = List[Double]()
        r_square = 0.0
        res, list_output, r_square = ls.GetPoly(degree, list_output, r_square)

        if list_output.Count == 0:
            self.rich_text_info.config(state="normal")
            self.rich_text_info.delete("1.0", "end")
            self.rich_text_info.insert("end", "Empty result")
            self.rich_text_info.config(state="disabled")
            return

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

        if equation:
            exp = CExpression()
            exp.SetExpression(equation)
            self.m_viewGraph.Plot(exp, e_color)
            self.m_viewGraph.Invalidate()

        self.rich_text_info.config(state="normal")
        self.rich_text_info.delete("1.0", "end")
        self.rich_text_info.insert("end", f"R square value: {r_square}")
        self.rich_text_info.config(state="disabled")

    def click_button_clear(self):
        if not self.m_viewGraph.IsAvailable():
            return
        self.m_viewGraph.Clear()
        self.m_viewGraph.Invalidate()

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
