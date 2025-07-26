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
from tkinter import ttk, messagebox

def get_hwnd(widget):
    # 윈도우 핸들 얻기 (Tkinter 내부 식별자를 사용)
    widget.update_idletasks()
    hwnd = widget.winfo_id()
    print(f"HWND: {hwnd}")
    return hwnd

class GraphViewContextMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GraphViewContextMenu")
        self.geometry("840x500")

        # 왼쪽 패널 (그래프 뷰 영역)
        # Create and place the graph view frame
        self.left_panel = tk.Frame(self, bd=1, relief="solid")
        self.left_panel.pack(side="left", fill="both", expand=True)

        # 오른쪽 패널
        # Create and place the right-side control panel
        self.right_panel = tk.Frame(self, width=260, bd=1, relief="solid")
        self.right_panel.pack(side="right", fill="y")

        # 그래프 뷰 생성
        # Create the CGUIViewGraph instance
        self.m_viewGraph = CGUIViewGraph()
        if self.m_viewGraph.CreateAndFitParent(get_hwnd(self.left_panel)).IsFail():
            print("ViewGraph 생성 실패")

        # 메뉴 아이템 목록
        # list of menu items
        self.menuItems = [
            (EAvailableViewGraphContextMenu.Load, "Load"),
            (EAvailableViewGraphContextMenu.Append, "Append"),
            (EAvailableViewGraphContextMenu.Save, "Save"),
            (EAvailableViewGraphContextMenu.Close, "Close"),
            (EAvailableViewGraphContextMenu.Clear, "Clear"),
            (EAvailableViewGraphContextMenu.Copy, "Copy"),
            (EAvailableViewGraphContextMenu.ClearThenPaste, "ClearThenPaste"),
            (EAvailableViewGraphContextMenu.Paste, "Paste"),
            (EAvailableViewGraphContextMenu.ClearDisplayedValue, "ClearDisplayedValue"),
            (EAvailableViewGraphContextMenu.ChangeChartType, "ChangeChartType"),
            (EAvailableViewGraphContextMenu.ShowToolBar, "ShowToolbar"),
            (EAvailableViewGraphContextMenu.Zoom, "Zoom"),
            (EAvailableViewGraphContextMenu.ZoomAxisNone, "ZoomAxisNone"),
            (EAvailableViewGraphContextMenu.ZoomAxisHorz, "ZoomAxisHorizontal"),
            (EAvailableViewGraphContextMenu.ZoomAxisVert, "ZoomAxisVertical"),
            (EAvailableViewGraphContextMenu.Panning, "Panning"),
            (EAvailableViewGraphContextMenu.ViewSettings, "ViewSettings"),
            (EAvailableViewGraphContextMenu.Help, "Help"),
            (EAvailableViewGraphContextMenu.ChangeColor, "ChangeColor"),
            (EAvailableViewGraphContextMenu.EditChartName, "EditChartName"),
            (EAvailableViewGraphContextMenu.ShowCrosshair, "ShowCrosshair"),
            (EAvailableViewGraphContextMenu.ShowLegend, "ShowLegend"),
            (EAvailableViewGraphContextMenu.MagnetCrosshair, "MagnetCrosshair"),
            (EAvailableViewGraphContextMenu.ChangeGraphOrder, "ChangeGraphOrder"),
            (EAvailableViewGraphContextMenu.GetTrendline, "GetTrendline"),
            (EAvailableViewGraphContextMenu.EditAxisLabel, "EditAxisLabel"),
            (EAvailableViewGraphContextMenu.SwitchAxis, "SwitchAxis"),
            (EAvailableViewGraphContextMenu.EditExpression, "EditExpression"),
            (EAvailableViewGraphContextMenu.AddExpression, "AddExpression"),
            (EAvailableViewGraphContextMenu.AddData, "AddData"),
            (EAvailableViewGraphContextMenu.AddDataByClick, "AddDataByClick"),
            (EAvailableViewGraphContextMenu.ShowGraph, "ShowGraph"),
            (EAvailableViewGraphContextMenu.RemoveGraph, "RemoveGraph"),
            (EAvailableViewGraphContextMenu.RemoveData, "RemoveData"),
            (EAvailableViewGraphContextMenu.EditData, "EditData"),
            (EAvailableViewGraphContextMenu.IndicateMinMax, "IndicateMin/Max"),
            (EAvailableViewGraphContextMenu.SetRange, "SetRange"),
            (EAvailableViewGraphContextMenu.SetOpacityOfLegend, "SetOpacityOfLegend"),
        ]

        self._create_right_controls()
        self.after(100, self.update_button_apply_state)

    def _create_right_controls(self):
        frame = tk.LabelFrame(self.right_panel, text="Context Menu", padx=5, pady=5)

        frame.pack(fill="both", expand=True, padx=5, pady=5)
        # 라디오 버튼 - 비활성 메뉴 아이템에 대한 표시/숨김 여부 설정
        # Radio buttons - Show/hide unavailable menu items
        self.unavailable_var = tk.StringVar(value="show")
        tk.Label(frame, text="Unavailable Menu Display Option").pack(anchor="w")

        radio_frame = tk.Frame(frame)
        radio_frame.pack(anchor="w")
        tk.Radiobutton(radio_frame, text="Show", variable=self.unavailable_var, value="show",
                       command=self.on_toggle_unavailable).pack(side="left")
        tk.Radiobutton(radio_frame, text="Hide", variable=self.unavailable_var, value="hide",
                       command=self.on_toggle_unavailable).pack(side="left")

        # 라디오 버튼 - 전체 선택/전체 선택 해제
        # Radio buttons - Select all / Deselect all available context menu items
        self.available_var = tk.StringVar(value="show")
        tk.Label(frame, text="Available Context Menu").pack(anchor="w", pady=(10, 0))

        self.select_var = tk.StringVar(value="none")
        radio2_frame = tk.Frame(frame)
        radio2_frame.pack(anchor="w")
        tk.Radiobutton(radio2_frame, text="All", variable=self.select_var, value="all",
                       command=self.on_select_toggle).pack(side="left")
        tk.Radiobutton(radio2_frame, text="None", variable=self.select_var, value="none",
                       command=self.on_select_toggle).pack(side="left")

        # 체크박스 스크롤 영역
        # Scrollable area for checkboxes
        scroll_frame = tk.Frame(frame, bd=1, relief="solid")
        scroll_frame.pack(fill="both", expand=True, pady=(10, 0))

        canvas = tk.Canvas(scroll_frame)
        scrollbar = tk.Scrollbar(scroll_frame, orient="vertical", command=canvas.yview)
        self.checkbox_frame = tk.Frame(canvas)

        self.checkbox_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=self.checkbox_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.check_vars = []
        for key, label in self.menuItems:
            var = tk.BooleanVar()
            chk = tk.Checkbutton(self.checkbox_frame, text=label, variable=var)
            chk.pack(anchor="w")
            self.check_vars.append((var, key))

        # Apply 버튼
        # Apply Button
        self.apply_button = tk.Button(self.right_panel, text="Apply", command=self.apply_context_menu)
        self.apply_button.pack(pady=10)

    def on_toggle_unavailable(self):
        if self.m_viewGraph.IsAvailable():
            # 비활성 메뉴 아이템에 대한 표시/숨김 여부 설정
            # Show/hide unavailable menu items
            self.m_viewGraph.ShowUnavailableContextMenu(self.unavailable_var.get() == "show")

    def on_select_toggle(self):
        check_all = self.select_var.get() == "all"
        for var, _ in self.check_vars:
            var.set(check_all)

    def apply_context_menu(self):
        if not self.m_viewGraph.IsAvailable():
            return

        final_menu = getattr(EAvailableViewGraphContextMenu, "None")

        # 체크 박스 선택한 메뉴들을 or 로 연산
        # Combine selected checkbox menu items using bitwise OR
        for var, enum_val in self.check_vars:
            if var.get():
                final_menu = EAvailableViewGraphContextMenu(int(final_menu) | int(enum_val), True)

        # 그래프 뷰에 선택한 메뉴들만 활성화 처리
        # Apply the selected menu items as enabled context menu options to the graph view
        self.m_viewGraph.SetAvailableViewGraphContextMenu(final_menu)

    def update_button_apply_state(self):
        self.apply_button.config(state="normal" if self.m_viewGraph.IsAvailable() else "disabled")
        self.after(100, self.update_button_apply_state)


if __name__ == "__main__":
    app = GraphViewContextMenu()
    app.mainloop()


# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}')
