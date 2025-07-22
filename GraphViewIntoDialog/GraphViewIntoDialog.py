# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *
import tkinter as tk
from tkinter import messagebox
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

class GraphViewInToDialog(Form):
    def __init__(self):
        Form.__init__(self)
        self.Text = "GraphViewInToDialog"
        self.Size = Size(740, 500)

        # 왼쪽 패널 (그래프 뷰 영역)
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

        # 그래프 뷰어 생성
        self.m_viewGraph = CGUIViewGraph()
        result = self.m_viewGraph.CreateAndFitParent((self.left_panel.Handle.ToInt32()))
        if result.IsFail():
            print("ViewGraph 생성 실패")

        self.on_click_button_add(None, None)

    def _create_right_controls(self):
        y = 10
        # 중간 패널 생성 (여백을 위한 컨테이너 역할)
        self.padding_panel = Panel()
        self.padding_panel.Dock = DockStyle.Fill
        self.padding_panel.Padding = Padding(5) # 상하좌우 5px 여백
        self.right_panel.Controls.Add(self.padding_panel)

        # GroupBox를 패딩 패널에 추가
        self.group = GroupBox()
        self.group.Text = "Quartic Equation"
        self.group.Dock = DockStyle.Fill
        self.padding_panel.Controls.Add(self.group)
        
        # 입력 필드 레이블 및 텍스트박스
        labels = ['a:', 'b:', 'c:', 'd:', 'e:']
        value = ['0.003', '-0.003', '-1', '1', '0']
        self.inputs = []

        y = 25
        for i, lbl in enumerate(labels):
            label = Label()
            label.Text = lbl
            label.Location = Point(5, y)
            label.Width = 20
            self.group.Controls.Add(label)
            
            self.textbox = TextBox()
            self.textbox.Location = Point(25, y - 5)
            self.textbox.Size = Size(115, 25)
            self.textbox.Text = value[i]
            self.group.Controls.Add(self.textbox)
            self.inputs.append(self.textbox)
            y += 25

        # Add 버튼
        self.add_button = Button()
        self.add_button.Text = "Add"
        self.add_button.Size = Size(135, 23)
        self.add_button.Location = Point(5, y)
        self.add_button.Click += self.on_click_button_add
        self.group.Controls.Add(self.add_button)
        y += 25

        # Clear 버튼
        self.clear_button = Button()
        self.clear_button.Text = "Clear"
        self.clear_button.Size = Size(135, 23)
        self.clear_button.Location = Point(5, y)
        self.clear_button.Click += self.on_click_button_clear
        self.group.Controls.Add(self.clear_button)
        y += 32

        # Info 라벨
        info_label = Label()
        info_label.Text = "Info"
        info_label.Location = Point(5, y)
        info_label.Size = Size(115, 15)
        self.group.Controls.Add(info_label)
        y += 17

        # 결과 출력 TextBox
        self.result_box = TextBox()
        self.result_box.Multiline = True
        self.result_box.ReadOnly = True
        self.result_box.ScrollBars = ScrollBars.Vertical
        self.result_box.Size = Size(135, 218)
        self.result_box.Location = Point(5, y)
        self.group.Controls.Add(self.result_box)

        # Resize 이벤트 연결
        self.group.Resize += self.adjust_result_box_position


    def adjust_result_box_position(self, sender, event):
        margin = 6
        self.result_box.Height = self.group.Height - self.result_box.Location.Y - margin 

    def on_click_button_add(self, sender, event):
        str_info = ""
        rand_gen = random.Random()

        if not self.m_viewGraph.IsAvailable():
            return

        arrF64Coef = [0.0] * 5
        arrCpxCoef = [Complex(0, 0)] * 5
        strEquation = ""

        for i in range(5):
            strCoef = self.inputs[i].Text
            success, value = Double.TryParse(strCoef)
            arrF64Coef[i] = value
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
        from System.Collections.Generic import List
        listResult = List[Complex]()
        result = CEquation.Quartic(arrCpxCoef[0], arrCpxCoef[1], arrCpxCoef[2], arrCpxCoef[3], arrCpxCoef[4], listResult)[0]

        if result.IsOK():
            for cp in listResult:
                if cp.Imaginary == 0:
                    strCP = f"{cp.Real}"
                elif cp.Imaginary > 0:
                    strCP = f"{cp.Real}+{cp.Imaginary}i"
                else:
                    strCP = f"{cp.Real}{cp.Imaginary}i"
                str_info += strCP + "\r\n\r\n"

        # 수식 객체 생성 및 그래프에 추가
        exp = CExpression()
        exp.SetExpression(strEquation)

        # 무작위 색상 생성 (R | G<<8 | B<<16)
        color_int = (rand_gen.randint(0, 255) |
                     (rand_gen.randint(0, 255) << 8) |
                     (rand_gen.randint(0, 255) << 16))
        color = EColor(color_int, True)

        self.m_viewGraph.Plot(exp, color)
        self.m_viewGraph.Invalidate()

        self.result_box.Text = "[root]\r\n" + str_info

    def on_click_button_clear(self, sender, event):
        if not self.m_viewGraph.IsAvailable():
            return

        self.m_viewGraph.Clear()
        self.m_viewGraph.Invalidate()
        self.result_box.Text = ""

if __name__ == "__main__":
    form = GraphViewInToDialog()
    Application.Run(form)


# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')
