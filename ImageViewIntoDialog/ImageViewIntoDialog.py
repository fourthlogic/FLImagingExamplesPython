# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *
import tkinter as tk
from tkinter import messagebox
from ctypes import windll
import clr
import sys
import time

# WinForms 관련
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import Application, Form, Panel, Timer, DockStyle, BorderStyle, Label, Button, TextBox, ScrollBars
from System import IntPtr
from System.Drawing import Size, Point

class ImageViewInToDialog(Form):
    def __init__(self):
        Form.__init__(self)
        self.Text = "ImageViewInToDialog"
        self.Size = Size(740, 500)

        # 왼쪽 패널 (이미지 뷰 영역)
        self.left_panel = Panel()
        self.left_panel.Dock = DockStyle.Fill
        self.left_panel.BorderStyle = BorderStyle.FixedSingle
        self.Controls.Add(self.left_panel)

        # 오른쪽 컨트롤 패널
        self.right_panel = Panel()
        self.right_panel.Width = 160
        self.right_panel.Dock = DockStyle.Right
        self.right_panel.BorderStyle = BorderStyle.FixedSingle
        self.Controls.Add(self.right_panel)

        self._create_right_controls()

        # 이미지 뷰어 생성
        self.m_viewImage = CGUIViewImage()
        result = self.m_viewImage.CreateAndFitParent((self.left_panel.Handle.ToInt32()))
        if result.IsFail():
            print("ViewImage 생성 실패")

        # 타이머 설정
        self.m_timer = Timer()
        self.m_timer.Interval = 100  # 100 ms
        self.m_timer.Tick += EventHandler(self.timer_tick)
        self.m_timer.Start()

    def timer_tick(self, sender, args):
        self.update_controls()

    def update_controls(self):
        bEnable = False

        if self.m_viewImage.IsAvailable():
            if self.m_viewImage.GetFigureObjectCount() > 0:
                bEnable = True

        self.pop_front_button.Enabled = bEnable

    def _create_right_controls(self):
        # 제목
        title = Label()
        title.Text = "RectFigure Object"
        title.Location = Point(10, 10)
        title.Width = 140
        self.right_panel.Controls.Add(title)
        
        # Create 버튼
        self.create_button = Button()
        self.create_button.Text = "Create"
        self.create_button.Location = Point(10, 40)
        self.create_button.Width = 140
        self.create_button.Click += self.on_create_button_click
        self.right_panel.Controls.Add(self.create_button)
        
        # Pop Front 버튼
        self.pop_front_button = Button()
        self.pop_front_button.Text = "Pop Front"
        self.pop_front_button.Location = Point(10, 80)
        self.pop_front_button.Width = 140
        self.pop_front_button.Enabled = False
        self.pop_front_button.Click += self.on_pop_front_button_click
        self.right_panel.Controls.Add(self.pop_front_button)
        
        # Info 라벨
        info_label = Label()
        info_label.Text = "Info"
        info_label.Location = Point(10, 120)
        info_label.Width = 140
        self.right_panel.Controls.Add(info_label)
        
        # Read-only TextBox (멀티라인)
        self.info_box = TextBox()
        self.info_box.Multiline = True
        self.info_box.ReadOnly = True
        self.info_box.ScrollBars = ScrollBars.Vertical
        self.info_box.Location = Point(10, 140)
        self.info_box.Size = Size(140, 300)
        self.right_panel.Controls.Add(self.info_box)
        
    def on_create_button_click(self, sender, event):
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

    def on_pop_front_button_click(self, sender, event):
        flFigure = None
        strFigureInfo = "Error"

        if self.m_viewImage.IsAvailable():
            # PopFrontFigureObject로 Figure 꺼내기
            flFigure = self.m_viewImage.PopFrontFigureObject()
    
            if flFigure is not None:
                # Figure → 문자열 변환
                strFigure = CFigureUtilities.ConvertFigureObjectToString(flFigure)
                strFigureInfo = strFigure
        self.info_box.Text = strFigureInfo


if __name__ == "__main__":
    form = ImageViewInToDialog()
    Application.Run(form)


# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')
