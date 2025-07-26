# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()

import time
import tkinter as tk
from tkinter import scrolledtext
from System import Int64

def get_hwnd(widget):
    # 윈도우 핸들 얻기 (Tkinter 내부 식별자를 사용)
    # Get window handle (using Tkinter internal identifier)
    widget.update_idletasks()
    hwnd = widget.winfo_id()
    return hwnd

class View3DIntoDialog(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("3D View Into Dialog")
        self.geometry("740x500")

        # 왼쪽 패널 (3D view 영역)
        # Left panel (3D view area)
        self.left_panel = tk.Frame(self, bd=1, relief="solid")
        self.left_panel.pack(side="left", fill="both", expand=True)

        # 오른쪽 컨트롤 패널
        # Right control panel
        self.right_panel = tk.Frame(self, width=200, bd=1, relief="solid")
        self.right_panel.pack(side="right", fill="y")

        self._create_right_controls()
        
		# 3D 뷰 생성
        # Create 3D view
        self.m_view3D = CGUIView3D()
        result = self.m_view3D.CreateAndFitParent(get_hwnd(self.left_panel))
        if result.IsFail():
            print("View3D 생성 실패")
            return
        
		# 높이 맵 이미지와 텍스쳐 로드
        # Load height map and texture
        result = self.m_view3D.Load("../../ExampleImages/View3D/mountain.flif",
                                    "../../ExampleImages/View3D/mountain_texture.flif")
        if result.IsFail():
            print("View3D 로드 실패")
            return
        
    # 높이 프로파일 버튼 이벤트 핸들러 # Event handler for height profile button
    def on_click_height_profile(self):
        if not self.m_view3D.IsAvailable():
            return

        if self.m_view3D.GetObjectCount() == 0:
            self._set_result_text("Error: Load an image file.")
            return
        
		# 높이 프로파일을 구할 시작 좌표 및 종료 좌표를 Edit box 로부터 얻어 와 지정한다.
        # Get the start and end coordinates for the height profile from the edit boxes and set them.
        try:
            i64StartX = Int64.Parse(self.textBoxStartX.get())
            i64StartY = Int64.Parse(self.textBoxStartY.get())
            i64EndX = Int64.Parse(self.textBoxEndX.get())
            i64EndY = Int64.Parse(self.textBoxEndY.get())
        except Exception:
            self._set_result_text("Error: Invalid coordinate values.")
            return

        flpStart = CFLPoint[Int64](i64StartX, i64StartY)
        flpEnd = CFLPoint[Int64](i64EndX, i64EndY)
        
		# 높이 프로파일 정보를 얻어 온다.
        # Retrieve the height profile information.
        listF64HP = List[float]()        
        result = self.m_view3D.GetHeightProfile(flpStart, flpEnd, listF64HP)[0]

        if result.IsOK():
            lines = [f"[{i}] {listF64HP[i]}" for i in range(listF64HP.Count)]
            self._set_result_text("\n".join(lines))
        else:
            self._set_result_text(f"Error code : {result.GetResultCode()}\nError name : {result.GetString()}")

        self.m_view3D.Invalidate()
        
    # 오른쪽 컨트롤 패널 컨트롤 생성 및 배치 함수
    # Function to create and arrange controls in the right-side control panel
    def _create_right_controls(self):
        self.group = tk.LabelFrame(self.right_panel, text="Height Profile", padx=5, pady=5)
        self.group.pack(fill="both", expand=True, padx=5, pady=5)

        # 시작 좌표 # Start Point
        tk.Label(self.group, text="Start").grid(row=0, column=0, sticky="w")
        tk.Label(self.group, text="x").grid(row=0, column=1)
        self.textBoxStartX = tk.Entry(self.group, width=6)
        self.textBoxStartX.insert(0, "0")
        self.textBoxStartX.grid(row=0, column=2)

        tk.Label(self.group, text="y").grid(row=0, column=3)
        self.textBoxStartY = tk.Entry(self.group, width=6)
        self.textBoxStartY.insert(0, "0")
        self.textBoxStartY.grid(row=0, column=4)

        # 종료 좌표 # End Point
        tk.Label(self.group, text="End").grid(row=1, column=0, sticky="w", pady=(5, 0))
        tk.Label(self.group, text="x").grid(row=1, column=1)
        self.textBoxEndX = tk.Entry(self.group, width=6)
        self.textBoxEndX.insert(0, "104")
        self.textBoxEndX.grid(row=1, column=2, pady=(5, 0))

        tk.Label(self.group, text="y").grid(row=1, column=3)
        self.textBoxEndY = tk.Entry(self.group, width=6)
        self.textBoxEndY.insert(0, "120")
        self.textBoxEndY.grid(row=1, column=4, pady=(5, 0))

        # 높이 프로파일 버튼 # Height Profile button
        self.btnHeightProfile = tk.Button(self.group, text="Height Profile", command=self.on_click_height_profile)
        self.btnHeightProfile.grid(row=2, column=0, columnspan=5, pady=(10, 5), ipadx=40)

        # 결과 창 # Result box
        self.result_box = scrolledtext.ScrolledText(self.group, height=20, width=30, state="disabled")
        self.result_box.grid(row=3, column=0, columnspan=5, sticky="nsew")

        # 리사이즈 동작 정의 # Configure resize behavior
        self.group.grid_rowconfigure(3, weight=1)
        self.group.grid_columnconfigure(4, weight=1)
        
    # 결과 창에 텍스트를 디스플레이하는 함수
    # Function to display text in the result window
    def _set_result_text(self, text):
        self.result_box.config(state="normal")
        self.result_box.delete("1.0", "end")
        self.result_box.insert("end", text)
        self.result_box.config(state="disabled")

# Launch GUI
if __name__ == "__main__":
    app = View3DIntoDialog()
    app.mainloop()


# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}')
