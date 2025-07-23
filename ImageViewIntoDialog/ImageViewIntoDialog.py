# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *
import tkinter as tk
from tkinter import messagebox
from ctypes import windll
import clr
import ctypes
import sys
import time

def get_hwnd(widget):
    # 윈도우 핸들 얻기 (Tkinter 내부 식별자를 사용)
    widget.update_idletasks()
    hwnd = widget.winfo_id()
    print(f"HWND: {hwnd}")
    return hwnd

class ImageViewIntoDialog(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("ImageViewIntoDialog")
        self.geometry("740x500")

        # 왼쪽 패널 (이미지 뷰 영역)
        self.left_panel = tk.Frame(self, bd=2, relief="solid")
        self.left_panel.pack(side="left", fill="both", expand=True)
        
        # 오른쪽 컨트롤 패널
        self.right_panel = tk.Frame(self, bd=2, relief="solid", width=160)
        self.right_panel.pack(side="right", fill="y")

        self._create_right_controls()

        # 이미지 뷰어 생성
        self.m_viewImage = CGUIViewImage()
        result = self.m_viewImage.CreateAndFitParent(get_hwnd(self.left_panel))
        if result.IsFail():
            print("Failed to create ViewImage")
            
        # 타이머 시작
        self.after(100, self.timer_tick)

    def timer_tick(self):
        self.update_controls()
        self.after(100, self.timer_tick)

    def update_controls(self):
        enabled = False
        if self.m_viewImage and self.m_viewImage.IsAvailable():
            if self.m_viewImage.GetFigureObjectCount() > 0:
                enabled = True

        state = "normal" if enabled else "disabled"
        self.pop_front_button.config(state=state)

    def _create_right_controls(self):
        tk.Label(self.right_panel, text="RectFigure Object").place(x=7, y=10, width=140)

        self.create_button = tk.Button(self.right_panel, text="Create", command=self.on_create_button_click)
        self.create_button.place(x=7, y=40, width=140)

        self.pop_front_button = tk.Button(self.right_panel, text="Pop Front", command=self.on_pop_front_button_click, state="disabled")
        self.pop_front_button.place(x=7, y=80, width=140)

        tk.Label(self.right_panel, text="Info").place(x=7, y=120, width=140)

        self.info_box = tk.Text(self.right_panel, height=15, width=18, wrap="word", state="disabled")
        self.info_box.place(x=7, y=140, width=140, height=300)

    def _append_info(self, text):
        self.info_box.config(state="normal")
        self.info_box.insert("end", text + "\n")
        self.info_box.config(state="disabled")

    def on_create_button_click(self):
        while True:
            # 1. 뷰 유효성 체크
            if not self.m_viewImage.IsAvailable():
                return

            # 2. 캔버스 좌표 얻기
            flrlCanvas = self.m_viewImage.GetClientRectCanvasRegion()

            # 3. 이미지 좌표계로 변환
            flrdImage = self.m_viewImage.ConvertCanvasCoordToImageCoord(flrlCanvas)  # CFLRect[Double]

            # 4. 사각형 크기 계산
            f64Width = flrdImage.GetWidth() / 10.0
            f64Height = flrdImage.GetHeight() / 10.0
            f64Size = Math.Min(f64Width, f64Height)

            # 5. 중심 좌표 계산
            flpdCenter = CFLPoint[Double](0.0, 0.0)
            flrdImage.GetCenter(flpdCenter)

            # 6. 중심 기준 사각형 생성
            flrFigure = CFLRect[Double](
                flpdCenter.x - f64Size,
                flpdCenter.y - f64Size,
                flpdCenter.x + f64Size,
                flpdCenter.y + f64Size
            )

            # 7. 이미지 뷰에 Figure 추가
            self.m_viewImage.PushBackFigureObject(flrFigure, EAvailableFigureContextMenu.All)
            break

    def on_pop_front_button_click(self):
        flFigure = None
        strFigureInfo = "Error"

        if self.m_viewImage.IsAvailable():
            # PopFrontFigureObject로 Figure 꺼내기
            flFigure = self.m_viewImage.PopFrontFigureObject()
    
            if flFigure is not None:
                # Figure → 문자열 변환
                strFigure = CFigureUtilities.ConvertFigureObjectToString(flFigure)
                strFigureInfo = strFigure

        self.info_box.config(state="normal")  # 편집 가능하게 변경
        self.info_box.delete("1.0", "end")    # 기존 텍스트 삭제
        self.info_box.insert("end", strFigureInfo)  # 새 텍스트 삽입
        self.info_box.config(state="disabled")  # 다시 읽기 전용으로 변경



if __name__ == "__main__":
    app = ImageViewIntoDialog()
    app.mainloop()


# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')
