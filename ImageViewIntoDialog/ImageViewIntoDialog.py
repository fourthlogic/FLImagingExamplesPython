# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()

import tkinter as tk
from tkinter import messagebox
import time

def get_hwnd(widget):
    # 윈도우 핸들 얻기 (Tkinter 내부 식별자를 사용)
    # Get window handle (using Tkinter internal identifier)
    widget.update_idletasks()
    hwnd = widget.winfo_id()
    return hwnd

class ImageViewIntoDialog(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ImageViewIntoDialog")
        self.geometry("740x500")

        # 왼쪽 패널 (이미지 뷰 영역)
        # Left panel (image view area)
        self.left_panel = tk.Frame(self, bd=2, relief="solid")
        self.left_panel.pack(side="left", fill="both", expand=True)
        
        # 오른쪽 컨트롤 패널
        # Right control panel
        self.right_panel = tk.Frame(self, bd=2, relief="solid", width=160)
        self.right_panel.pack(side="right", fill="y")

        self._create_right_controls()

        # 이미지 뷰어 생성
        # Create controls inside the right panel
        self.m_viewImage = CGUIViewImage()
        result = self.m_viewImage.CreateAndFitParent(get_hwnd(self.left_panel))
        if result.IsFail():
            print("Failed to create ViewImage")
            
        # 타이머 시작
        # Start the periodic timer (tick every 100 ms)
        self.after(100, self.timer_tick)
        self.focus_force()

    # 주기적으로 컨트롤들의 활성화 여부를 업데이트하는 타이머 함수
    # Timer function that periodically updates the enable/disable state of controls
    def timer_tick(self):
        self.update_controls()
        self.after(100, self.timer_tick)

    # 컨트롤들의 활성화 여부를 업데이트하는 함수
    # Function to update the enable/disable state of the controls
    def update_controls(self):
        enabled = False
        if self.m_viewImage and self.m_viewImage.IsAvailable():
            if self.m_viewImage.GetFigureObjectCount() > 0:
                enabled = True

        state = "normal" if enabled else "disabled"
        self.pop_front_button.config(state=state)

    # 오른쪽 패널의 컨트롤들을 생성 및 배치하는 함수
    # Function to create and place controls in the right panel
    def _create_right_controls(self):
        tk.Label(self.right_panel, text="RectFigure Object").place(x=7, y=10, width=140)

        self.create_button = tk.Button(self.right_panel, text="Create", command=self.on_create_button_click)
        self.create_button.place(x=7, y=40, width=140)

        self.pop_front_button = tk.Button(self.right_panel, text="Pop Front", command=self.on_pop_front_button_click, state="disabled")
        self.pop_front_button.place(x=7, y=80, width=140)

        tk.Label(self.right_panel, text="Info").place(x=7, y=120, width=140)

        self.info_box = tk.Text(self.right_panel, height=15, width=18, wrap="word", state="disabled")
        self.info_box.place(x=7, y=140, width=140, height=300)

    # Create 버튼 클릭에 대한 이벤트 처리기
    # Event handler for Create button click
    def on_create_button_click(self):
        while True:
            # 1. 뷰 유효성 체크
            # 1. Check if the image view is valid
            if not self.m_viewImage.IsAvailable():
                return

            # 2. 캔버스 좌표 얻기
            # 2. Get canvas coordinate region
            flrlCanvas = self.m_viewImage.GetClientRectCanvasRegion()

            # 3. 이미지 좌표계로 변환
            # 3. Convert to image coordinate space
            flrdImage = self.m_viewImage.ConvertCanvasCoordToImageCoord(flrlCanvas) # CFLRect[Double]

            # 4. 사각형 크기 계산
            # 4. Calculate the size of the rectangle
            f64Width = flrdImage.GetWidth() / 10.0
            f64Height = flrdImage.GetHeight() / 10.0
            f64Size = Math.Min(f64Width, f64Height)

            # 5. 중심 좌표 계산
            # 5. Calculate the center point
            flpdCenter = CFLPoint[Double](0.0, 0.0)
            flrdImage.GetCenter(flpdCenter)

            # 6. 중심 기준 사각형 생성
            # 6. Create a rectangle centered at the center point
            flrFigure = CFLRect[Double](
                flpdCenter.x - f64Size,
                flpdCenter.y - f64Size,
                flpdCenter.x + f64Size,
                flpdCenter.y + f64Size
            )

            # 7. 이미지 뷰에 Figure 추가
            # 7. Add the rectangle figure to the image view
            self.m_viewImage.PushBackFigureObject(flrFigure)
            break

    # PopFront 버튼 클릭에 대한 이벤트 처리기
    # Event handler for Pop Front button click
    def on_pop_front_button_click(self):
        flFigure = None
        strFigureInfo = "Error"

        if self.m_viewImage.IsAvailable():
            # PopFrontFigureObject()로 Figure 꺼내기
            # Pop the first (front-most) figure from the image view
            flFigure = self.m_viewImage.PopFrontFigureObject()
    
            if flFigure is not None:
                # Figure를 문자열로 변환
                # Convert the figure object to a string representation
                strFigure = CFigureUtilities.ConvertFigureObjectToString(flFigure)
                strFigureInfo = strFigure
                
        # info_box에 문자열을 출력
        # Display text in the info_box
        self._append_info(strFigureInfo)
        
    # info_box에 문자열을 출력하는 함수
    # Function to display text in the info_box
    def _append_info(self, text):
        self.info_box.config(state="normal") # 편집 가능하게 변경
        self.info_box.delete("1.0", "end")   # 기존 텍스트 삭제
        self.info_box.insert("end", text + "") # 새 텍스트 삽입
        self.info_box.config(state="disabled") # 다시 읽기 전용으로 변경


if __name__ == "__main__":
    app = ImageViewIntoDialog()
    app.mainloop()


# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}')
