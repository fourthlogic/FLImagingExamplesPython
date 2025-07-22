# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *
from ctypes import windll
import clr
import sys
import time
import random

# WinForms 관련
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import Application, Form, Panel, Timer, DockStyle, BorderStyle, Label, Button, TextBox, ScrollBars, GroupBox, Padding
from System import IntPtr
from System.Drawing import Size, Point
from System.Numerics import Complex
from System import Double

class View3DIntoDialog(Form):
    def __init__(self):
        Form.__init__(self)
        self.Text = "3D View Into Dialog"
        self.Size = Size(740, 500)

        # 왼쪽 패널 (3D 뷰 영역)
        self.left_panel = Panel()
        self.left_panel.Dock = DockStyle.Fill
        self.left_panel.BorderStyle = BorderStyle.FixedSingle
        self.Controls.Add(self.left_panel)

        # 오른쪽 컨트롤 패널
        self.right_panel = Panel()
        self.right_panel.Width = 200
        self.right_panel.Dock = DockStyle.Right
        self.right_panel.BorderStyle = BorderStyle.FixedSingle
        self.Controls.Add(self.right_panel)

        self._create_right_controls()

        # 3D 뷰어 생성
        self.m_view3D = CGUIView3D()
        
        if (result := self.m_view3D.CreateAndFitParent((self.left_panel.Handle.ToInt32()))).IsFail():
            print("View3D 생성 실패")
            return

		# 높이 맵 이미지와 텍스쳐 로드 # Load height map image and texture
        if (result := self.m_view3D.Load("../../ExampleImages/View3D/mountain.flif", "../../ExampleImages/View3D/mountain_texture.flif")).IsFail():
            print("View3D 생성 실패")
            return


    def _create_right_controls(self):
        y = 10
        # 중간 패널 생성 (여백을 위한 컨테이너 역할)
        self.padding_panel = Panel()
        self.padding_panel.Dock = DockStyle.Fill
        self.padding_panel.Padding = Padding(5) # 상하좌우 5px 여백
        self.right_panel.Controls.Add(self.padding_panel)

        # GroupBox를 패딩 패널에 추가
        self.group = GroupBox()
        self.group.Text = "Height Profile"
        self.group.Dock = DockStyle.Fill
        self.padding_panel.Controls.Add(self.group)
        
        y = 25
        
        # Start 좌표
        label_start = Label()
        label_start.Text = "Start"
        label_start.Size = Size(40, 20)
        label_start.Location = Point(5, y)
        self.group.Controls.Add(label_start)

        label_x1 = Label()
        label_x1.Text="x"
        label_x1.Size = Size(10, 20)
        label_x1.Location = Point(50, y)
        self.group.Controls.Add(label_x1)

        self.textBoxStartX = TextBox()
        self.textBoxStartX.Text = "0"
        self.textBoxStartX.Size = Size(47, 20)
        self.textBoxStartX.Location = Point(65, y - 5)
        self.group.Controls.Add(self.textBoxStartX)
        
        label_y1 = Label()
        label_y1.Text="y"
        label_y1.Location = Point(120, y)
        label_y1.Size = Size(10, 20)
        self.group.Controls.Add(label_y1)

        self.textBoxStartY = TextBox()
        self.textBoxStartY.Text = "0"
        self.textBoxStartY.Size = Size(47, 20)
        self.textBoxStartY.Location = Point(135, y - 5)
        self.group.Controls.Add(self.textBoxStartY)
        
        y += 25

        # End 좌표
        label_end = Label()
        label_end.Text = "End"
        label_end.Size = Size(40, 20)
        label_end.Location = Point(5, y)
        self.group.Controls.Add(label_end)
        
        label_x2 = Label()
        label_x2.Text="x"
        label_x2.Size = Size(10, 20)
        label_x2.Location = Point(50, y)
        self.group.Controls.Add(label_x2)

        self.textBoxEndX = TextBox()
        self.textBoxEndX.Text = "104"
        self.textBoxEndX.Size = Size(47, 20)
        self.textBoxEndX.Location = Point(65, y - 5)
        self.group.Controls.Add(self.textBoxEndX)
        
        label_y2 = Label()
        label_y2.Text="y"
        label_y2.Location = Point(120, y)
        label_y2.Size = Size(10, 20)
        self.group.Controls.Add(label_y2)

        self.textBoxEndY = TextBox()
        self.textBoxEndY.Text = "120"
        self.textBoxEndY.Size = Size(47, 20)
        self.textBoxEndY.Location = Point(135, y - 5)
        self.group.Controls.Add(self.textBoxEndY)
        
        y += 25

        # Height Profile 버튼
        self.btnHeightProfile = Button()
        self.btnHeightProfile.Text = "Height Profile"
        self.btnHeightProfile.Size = Size(180, 30)
        self.btnHeightProfile.Location = Point(5, y)
        self.btnHeightProfile.Click += self.on_click_height_profile
        self.group.Controls.Add(self.btnHeightProfile)

        y += 35

        # 결과 출력 TextBox
        self.result_box = TextBox()
        self.result_box.Multiline = True
        self.result_box.ReadOnly = True
        self.result_box.ScrollBars = ScrollBars.Vertical
        self.result_box.Size = Size(180, 333)
        self.result_box.Location = Point(5, y)
        self.group.Controls.Add(self.result_box)

        # Resize 이벤트 연결
        self.group.Resize += self.adjust_result_box_position


    def adjust_result_box_position(self, sender, event):
        margin = 6
        self.result_box.Height = self.group.Height - self.result_box.Location.Y - margin 

    def on_click_height_profile(self, sender, event):
        if not self.m_view3D.IsAvailable():
            return
        
        if self.m_view3D.GetObjectCount() == 0:
            self.result_box.Text = "Error: Load an image file."
            return

        # Edit box에서 좌표 읽기
        i64StartX = Int64.Parse(self.textBoxStartX.Text)
        i64StartY = Int64.Parse(self.textBoxStartY.Text)
        i64EndX = Int64.Parse(self.textBoxEndX.Text)
        i64EndY = Int64.Parse(self.textBoxEndY.Text)

        # CFLPoint[long] 좌표 객체 생성
        flpStart = CFLPoint[Int64](i64StartX, i64StartY)
        flpEnd = CFLPoint[Int64](i64EndX, i64EndY)

        # 결과 저장용 리스트
        listF64HP = List[float]()  # or List[float] / List[double] depending on FLImagingCLR API

        # 높이 프로파일 호출
        result = self.m_view3D.GetHeightProfile(flpStart, flpEnd, listF64HP)[0]

        if result.IsOK():
            lines = []
            for i in range(listF64HP.Count):
                value = listF64HP[i]
                lines.append(f"[{i}] {value}")
            self.result_box.Text = "\r\n".join(lines)
        else:
            self.result_box.Text = f'Error code : {result.GetResultCode()}\r\nError name : {result.GetString()}\r\n'

        self.m_view3D.Invalidate()

if __name__ == "__main__":
    form = View3DIntoDialog()
    Application.Run(form)


# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')
