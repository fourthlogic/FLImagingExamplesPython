# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

CLibraryUtilities.Initialize()
import tkinter as tk
from tkinter import ttk, messagebox
import random

class FormGraphView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Form Graph View")
        self.geometry("420x221")
        self.resizable(False, False)

        self.m_bLockControls = False
        self.m_viewGraph = CGUIViewGraph()

        # 위젯 생성
        # Create UI widgets
        self.create_widgets()

        # 컨트롤 상태 초기화
        # Initialize control states
        self.update_controls()

        # 주기적 업데이트 타이머 시작
        # Start periodic control state timer
        self.after(100, self.timer_tick)

    def create_widgets(self):
        # 그래프 뷰 열기 버튼
        # Open Graph View button
        self.buttonOpenView = tk.Button(self, text="Open Graph View", width=25, command=self.click_button_open_view)
        self.buttonOpenView.place(x=10, y=10)

        # 그래프 뷰 종료 버튼
        # Terminate View button
        self.buttonTerminateView = tk.Button(self, text="Terminate View", width=25, command=self.click_button_terminate_view)
        self.buttonTerminateView.place(x=207, y=10)

        # 그래프 로드 버튼
        # Load Graph button
        self.buttonLoadGraph = tk.Button(self, text="Load Graph", width=25, command=self.click_button_load_graph)
        self.buttonLoadGraph.place(x=10, y=40)

        # 그래프 저장 버튼
        # Save Graph button
        self.buttonSaveGraph = tk.Button(self, text="Save Graph", width=25, command=self.click_button_save_graph)
        self.buttonSaveGraph.place(x=207, y=40)

        # 차트 그룹 박스
        # Chart group box
        self.group = tk.LabelFrame(self, text="Chart")
        self.group.place(x=10, y=75, width=382, height=98)

        # 이름 및 타입 라벨
        # Name and Type labels
        tk.Label(self.group, text="Name").place(x=5, y=3)
        tk.Label(self.group, text="Type").place(x=197, y=3)

        # 차트 이름 입력창
        # Chart name entry
        self.textboxName = tk.Entry(self.group, width=24)
        self.textboxName.place(x=5, y=21)

        # 차트 타입 콤보박스
        # Chart type combo box
        self.comboBoxChartType = ttk.Combobox(self.group, state="readonly", width=21)
        self.comboBoxChartType["values"] = ["Bar", "Line", "Scatter"]
        self.comboBoxChartType.current(0)
        self.comboBoxChartType.place(x=197, y=21)

        # 차트 추가 버튼
        # Add chart button
        self.buttonAdd = tk.Button(self.group, text="Add", width=23, command=self.click_button_chart_add)
        self.buttonAdd.place(x=5, y=50)

        # 차트 지우기 버튼
        # Clear chart button
        self.buttonClear = tk.Button(self.group, text="Clear", width=23, command=self.click_button_chart_clear)
        self.buttonClear.place(x=197, y=50)

    def error_message_box(self, code, msg):
        # 에러 메시지 박스 출력
        # Show error message box
        message = f"Error code : {code}\nError message : {msg}"
        messagebox.showerror("Error", message)

    def lock_controls(self, lock_flag):
        # 컨트롤 잠금 설정
        # Lock or unlock controls
        self.m_bLockControls = lock_flag
        self.update_controls()

    def timer_tick(self):
        # 주기적 상태 갱신
        # Periodic control state update
        self.update_controls()
        self.after(100, self.timer_tick)

    def update_controls(self):
        # 컨트롤 활성/비활성 상태 설정
        # Update enable/disable states of controls
        enabled = not self.m_bLockControls and self.m_viewGraph.IsAvailable()
        state_normal = tk.NORMAL if enabled else tk.DISABLED
        state_inverse = tk.NORMAL if not enabled else tk.DISABLED

        self.buttonOpenView.config(state=state_inverse)
        self.buttonTerminateView.config(state=state_normal)
        self.buttonLoadGraph.config(state=state_normal)
        self.buttonSaveGraph.config(state=tk.NORMAL if enabled and self.m_viewGraph.DoesGraphExist() else tk.DISABLED)
        self.buttonAdd.config(state=state_normal)
        self.buttonClear.config(state=tk.NORMAL if enabled and self.m_viewGraph.DoesGraphExist() else tk.DISABLED)
        self.textboxName.config(state=state_normal)
        self.comboBoxChartType.config(state="readonly" if enabled else tk.DISABLED)

    def click_button_open_view(self):
        # 그래프 뷰 열기 이벤트 처리
        # Open graph view handler
        if self.m_viewGraph.IsAvailable(): 
            return
        
        if (res := self.m_viewGraph.Create(0, 0, 500, 500)).IsFail(): 
            self.ErrorMessageBox(res, "")

        self.m_viewGraph.ZoomFit()

    def click_button_terminate_view(self):
        # 그래프 뷰 종료 이벤트 처리
        # Terminate graph view handler
        if not self.m_viewGraph.IsAvailable(): 
            return
        
        if (res := self.m_viewGraph.Destroy()).IsFail(): 
            self.ErrorMessageBox(res, "")

    def click_button_load_graph(self):
        # 그래프 로드 처리
        # Load graph from file
        if not self.m_viewGraph.IsAvailable(): 
            return
        self.lock_controls(True)
        self.m_viewGraph.Load("", EViewGraphLoadOption(int(EViewGraphLoadOption.Load) | int(EViewGraphLoadOption.OpenDialog), True))
        self.lock_controls(False)

    def click_button_save_graph(self):
        # 그래프 저장 처리
        # Save current graph
        if not self.m_viewGraph.IsAvailable(): 
            return
        if not self.m_viewGraph.DoesGraphExist(): 
            return
        self.lock_controls(True)
        self.m_viewGraph.Save()
        self.lock_controls(False)

    def click_button_chart_add(self):
        # 차트 추가 처리
        # Add a chart to the graph view
        if not self.m_viewGraph.IsAvailable(): 
            return

        # Chart Name
        strChartName = self.textboxName.get()
        if strChartName == "":
            strChartName = "Chart"

        # Chart Type
        eChartType = EChartType(self.comboBoxChartType.current() + 1, True)

        # Data Count
        i32DataCount = 30

        # Data Array
        dataX = [float(random.randint(0, 99)) for _ in range(i32DataCount)]
        dataY = [float(random.randint(0, 99)) for _ in range(i32DataCount)]
        arrF64DataX1 = Array[Double](dataX)
        arrF64DataY1 = Array[Double](dataY)

        # Chart Color
        eColor = EColor((random.randint(0, 255)) | (random.randint(0, 255) << 8) | (random.randint(0, 255) << 16), True)

        # Plot
        self.m_viewGraph.Plot(arrF64DataX1, arrF64DataY1, i32DataCount, eChartType, eColor, strChartName)
        self.m_viewGraph.Invalidate()

    def click_button_chart_clear(self):
        if not self.m_viewGraph.IsAvailable():
            return
        # 차트 클리어 처리
        # Clear the graph view
        self.m_viewGraph.Clear()
        self.m_viewGraph.Invalidate()

if __name__ == "__main__":
    app = FormGraphView()
    app.mainloop()
