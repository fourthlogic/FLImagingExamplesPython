# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()

import time
import random
import tkinter as tk
from tkinter import ttk, messagebox

def get_hwnd(widget):
    # 윈도우 핸들 얻기 (Tkinter 내부 식별자를 사용)
    # Get window handle (using Tkinter internal identifier)
    widget.update_idletasks()
    hwnd = widget.winfo_id()
    return hwnd

def ErrorMessageBox(res, string_msg):
    msg = f"Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n"
    if len(string_msg) > 1:
        msg += string_msg
    messagebox.showerror("Error", msg)

class GraphViewContextMenu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GraphViewContextMenu")
        self.geometry("880x600")

        # 왼쪽 패널 (그래프 뷰 영역)
        # Create and place the graph view frame
        self.left_panel = tk.Frame(self, bd=1, relief="solid")
        self.left_panel.pack(side="left", fill="both", expand=True)

        # 오른쪽 패널
        # Create and place the right-side control panel
        self.right_panel = tk.Frame(self, width=320, bd=1, relief="solid")
        self.right_panel.pack(side="right", fill="y")

        # 메뉴 아이템 목록
        # list of menu items
        self.menuItems = [
            (EViewGraphMenuItem.Load, "Load File"),
            (EViewGraphMenuItem.Append, "Append"),
            (EViewGraphMenuItem.Save, "Save"),
            (EViewGraphMenuItem.Close, "Close"),
            (EViewGraphMenuItem.Clear, "Clear"),
            (EViewGraphMenuItem.Copy, "Copy && Paste@Copy to Clipboard"),
            (EViewGraphMenuItem.ClearThenPaste, "Copy && Paste@Paste from Clipboard (Clear then Paste)"),
            (EViewGraphMenuItem.Paste, "Copy && Paste@Paste from Clipboard (Append)"),
            (EViewGraphMenuItem.ToggleLogScale, "Log Scale Mode"),
            (EViewGraphMenuItem.ClearPointAnnotation, "Clear Point Annotations"),
            (EViewGraphMenuItem.MenuGroup_ChangeChartType, "Chart Settings@Change Chart Type"),
            (EViewGraphMenuItem.ShowToolBar, "Show@Show ToolBar"),
            (EViewGraphMenuItem.MenuGroup_Zoom, "Zoom"),
            (EViewGraphMenuItem.ZoomIn, "Point of View@Zoom In Mode"),
            (EViewGraphMenuItem.ZoomOut, "Point of View@Zoom Out Mode"),
            (EViewGraphMenuItem.ZoomFit, "Point of View@Zoom Fit"),
            (EViewGraphMenuItem.ViewSettings, "View Settings.."),
            (EViewGraphMenuItem.Help, "Help"),
            (EViewGraphMenuItem.MenuGroup_ChangeColor, "Change Color"),
            (EViewGraphMenuItem.ChangeColor, "Change Color"),
            (EViewGraphMenuItem.MenuGroup_EditChartName, "Edit Chart Name"),
            (EViewGraphMenuItem.EditChartName, "Edit Chart Name"),
            (EViewGraphMenuItem.ShowCrosshair, "Show@Show Crosshair"),
            (EViewGraphMenuItem.ShowLegend, "Show@Show Legend"),
            (EViewGraphMenuItem.ShowPointAnnotation, "Show@Show Point Annotations"),
            (EViewGraphMenuItem.MagnetCrosshair, "Show@Magnet Crosshair"),
            (EViewGraphMenuItem.ChangeGraphOrder, "Change Graph Order"),
            (EViewGraphMenuItem.GetTrendline, "Get Trendline"),
            (EViewGraphMenuItem.ZoomAxisNone, "Point of View@Select Zoom Axis@Both"),
            (EViewGraphMenuItem.ZoomAxisHorz, "Point of View@Select Zoom Axis@Horizontal"),
            (EViewGraphMenuItem.ZoomAxisVert, "Point of View@Select Zoom Axis@Vertical"),
            (EViewGraphMenuItem.EditAxisLabel, "Edit Axis Label"),
            (EViewGraphMenuItem.SwitchAxis, "Switch Axis"),
            (EViewGraphMenuItem.MenuGroup_ViewAndEditExpression, "View && Edit Expression"),
            (EViewGraphMenuItem.EditExpression, "Edit Expression"),
            (EViewGraphMenuItem.AddExpression, "Add Graph@Expression"),
            (EViewGraphMenuItem.AddData, "Add Graph@Data"),
            (EViewGraphMenuItem.AddDataByClick, "Add Graph@Add Data By Click"),
            (EViewGraphMenuItem.SetAxisTickSpacing, "Set Axis Tick Spacing"),
            (EViewGraphMenuItem.SetAxisTickDecimalPlaces, "Set Axis Tick Decimal Places"),
            (EViewGraphMenuItem.MenuGroup_ShowGraph, "Show Graph"),
            (EViewGraphMenuItem.ShowMultipleGraph, "Show Graph@Show Multiple Graph"),
            (EViewGraphMenuItem.ShowGraph, "Show Graph"),
            (EViewGraphMenuItem.MenuGroup_RemoveGraph, "Remove Graph"),
            (EViewGraphMenuItem.RemoveMultipleGraph, "Remove Graph@Remove Multiple Graph"),
            (EViewGraphMenuItem.RemoveGraph, "Remove Graph"),
            (EViewGraphMenuItem.RemoveData, "Remove"),
            (EViewGraphMenuItem.EditData, "Edit"),
            (EViewGraphMenuItem.Panning, "Point of View@Panning Mode"),
            (EViewGraphMenuItem.IndicateMinMax, "Indicate Chart Min Max"),
            (EViewGraphMenuItem.SetAxisRange, "Set Range"),
            (EViewGraphMenuItem.SetOpacityOfLegend, "Set Opacity of Legend"),
            (EViewGraphMenuItem.MenuGroup_ShowLayers, "Layer@Show Layers"),
            (EViewGraphMenuItem.ShowAllLayers, "Layer@Show Layers@Show All Layers"),
            (EViewGraphMenuItem.HideAllLayers, "Layer@Show Layers@Hide All Layers"),
            (EViewGraphMenuItem.ShowLayer_Drawing, "Layer@Show Layers@Layer #"),
            (EViewGraphMenuItem.LayerProperties, "Layer Properties"),
            (EViewGraphMenuItem.MenuGroup_ClearLayers, "Clear Layers"),
            (EViewGraphMenuItem.ClearAllLayers, "Layer@Clear All Layers"),
            (EViewGraphMenuItem.ClearLayer, "Clear Layer"),
            (EViewGraphMenuItem.ClearNamedLayer, "Clear Named Layer"),
            (EViewGraphMenuItem.ShowNamedLayer, "Show Named Layer"),
            (EViewGraphMenuItem.ThemeLightMode, "Show@Theme@Light Mode"),
            (EViewGraphMenuItem.ThemeDarkMode, "Show@Theme@Dark Mode"),
            (EViewGraphMenuItem.MenuGroup_Synchronization, "Synchronization"),
            (EViewGraphMenuItem.MenuGroup_SyncPointOfView, "Synchronization@Point of View"),
            (EViewGraphMenuItem.SyncViewPointOfView, "Synchronization@Point of View"),
            (EViewGraphMenuItem.MenuGroup_SyncWindow, "Synchronization@Window"),
            (EViewGraphMenuItem.SyncWindow, "Synchronization@Window"),
            (EViewGraphMenuItem.ShowAxis_Horz, "Show@Show Axis Components@Horizontal Axis"),
            (EViewGraphMenuItem.ShowAxis_Vert, "Show@Show Axis Components@Vertical Axis"),
            (EViewGraphMenuItem.ShowAxisLabel_Horz, "Show@Show Axis Components@Horizontal Axis Label"),
            (EViewGraphMenuItem.ShowAxisLabel_Vert, "Show@Show Axis Components@Vertical Axis Label"),
            (EViewGraphMenuItem.ShowAxisTick_Horz, "Show@Show Axis Components@Horizontal Axis Tick"),
            (EViewGraphMenuItem.ShowAxisTick_Vert, "Show@Show Axis Components@Vertical Axis Tick"),
            (EViewGraphMenuItem.ShowAxisTickLabel_Horz, "Show@Show Axis Components@Horizontal Axis Tick Labels"),
            (EViewGraphMenuItem.ShowAxisTickLabel_Vert, "Show@Show Axis Components@Vertical Axis Tick Labels"),
            (EViewGraphMenuItem.MenuGroup_ChartSettings, "Chart Settings"),
            (EViewGraphMenuItem.ChangeType_BarChart, "Chart Settings@Change Chart Type@Bar"),
            (EViewGraphMenuItem.ChangeType_LineGraph, "Chart Settings@Change Chart Type@Line"),
            (EViewGraphMenuItem.ChangeType_ScatterChart, "Chart Settings@Change Chart Type@Scatter"),
            (EViewGraphMenuItem.MenuGroup_LineGraphMarkerType, "Line Graph Marker Type"),
            (EViewGraphMenuItem.LineGraphMarker_ZoomInOnly, "Chart Settings@Line Graph Marker Type@Zoom-in Only"),
            (EViewGraphMenuItem.LineGraphMarker_Always, "Chart Settings@Line Graph Marker Type@Always"),
            (EViewGraphMenuItem.LineGraphMarker_Never, "Chart Settings@Line Graph Marker Type@Never"),
            (EViewGraphMenuItem.LineGraphMarkerSettings, "Chart Settings@Marker Settings.."),
            (EViewGraphMenuItem.SetLogBase, "Set Log Base"),
            (EViewGraphMenuItem.MenuGroup_AddGraph, "Add Graph"),
            (EViewGraphMenuItem.MenuGroup_Layer, "Layer"),
            (EViewGraphMenuItem.MenuGroup_CopyAndPaste, "Copy && Paste"),
            (EViewGraphMenuItem.MenuGroup_Show, "Show"),
            (EViewGraphMenuItem.MenuGroup_Theme, "Show@Theme"),
            (EViewGraphMenuItem.MenuGroup_ShowAxisComponents, "Show Axis Components"),
            (EViewGraphMenuItem.MenuGroup_SelectZoomAxis, "Select Zoom Axis")
        ]

        # 폼 로드(초기화) 시퀀스 (C# FormGraphViewLoad 대응)
        self.dock_graph_view_to_this()
        self._create_right_controls()
        self.apply_context_menu()
        self.initialize_controls()
        self.update_controls()

    def dock_graph_view_to_this(self):
        # 그래프 뷰 생성
        self.m_viewGraph = CGUIViewGraph()
        res = self.m_viewGraph.CreateAndFitParent(get_hwnd(self.left_panel))

        if res.IsFail():
            ErrorMessageBox(res, "")

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
        self.select_var = tk.StringVar(value="none")
        tk.Label(frame, text="Available Context Menu").pack(anchor="w", pady=(10, 0))

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
        if self.unavailable_var.get() == "show":
            # 이용 불가능한 메뉴를 디스플레이 // Display unavailable menu
            self.m_viewGraph.ShowUnavailableContextMenu(True)
        elif self.unavailable_var.get() == "hide":
            # 이용 불가능한 메뉴를 숨김 // Hide unavailable menu
            self.m_viewGraph.ShowUnavailableContextMenu(False)

    def apply_context_menu(self):
        # 그래프 뷰 유효성 체크
        if not self.m_viewGraph.IsAvailable():
            return

        # 사용 가능한 그래프 뷰 메뉴 // Available Graph View Context Menu 
        listAvailableMenu = []
        for var, enum_val in self.check_vars:
            # 체크 선택된 메뉴 아이템을 추가
            # Add the checked menu item
            if var.get():
                listAvailableMenu.append(enum_val)

        # 선택된 메뉴 아이템들을 그래프 뷰의 이용 가능한 메뉴에 적용
        # Apply the selected menu items to the available menu in the graph view
        self.m_viewGraph.SetAvailableViewGraphContextMenu(listAvailableMenu)

        ##########################################
        # Whether to execute the "Tip" code below
        # 아래 "팁" 코드를 수행할지 여부
        bTipCodeExecute = False

        if not bTipCodeExecute:
            return

        # 팁: 아래와 같이 기존 메뉴에서 한두 개의 메뉴만 제외 가능
        # Tip: It is possible to exclude only few menus from the existing menu as shown below
        listAvailableMenuToRemove = [
            EViewGraphMenuItem.IndicateMinMax,
            EViewGraphMenuItem.SetOpacityOfLegend
        ]
        self.m_viewGraph.RemoveAvailableViewGraphContextMenu(listAvailableMenuToRemove)

        # 팁: 아래와 같이 기존 메뉴에서 한두 개의 메뉴만 추가 가능
        # Tip: It is possible to add only few menus from the existing menu as shown below
        listAvailableMenuToAdd = [
            EViewGraphMenuItem.IndicateMinMax,
            EViewGraphMenuItem.SetOpacityOfLegend
        ]
        self.m_viewGraph.AddAvailableViewGraphContextMenu(listAvailableMenuToAdd)

    def initialize_controls(self):
        if self.m_viewGraph.IsAvailable():
            # Check whether the unavailable context menu is displayed
            # 이용 불가능한 컨텍스트 메뉴를 디스플레이하는지 여부를 확인
            if self.m_viewGraph.IsUnavailableContextMenuVisible():
                self.unavailable_var.set("show")
            else:
                self.unavailable_var.set("hide")

            listAvailableMenu = self.m_viewGraph.GetAvailableViewGraphContextMenu()

            for var, _ in self.check_vars:
                var.set(False)

            for var, enum_val in self.check_vars:
                # m_viewGraph에서 받은 활성화 리스트에 현재 체크박스의 메뉴가 포함되어 있는지 확인
                if enum_val in listAvailableMenu:
                    var.set(True)
                else:
                    var.set(False)

            if len(listAvailableMenu) == int(EViewGraphMenuItem.Count):
                self.select_var.set("all")
            elif len(listAvailableMenu) == 0:
                self.select_var.set("none")

    def update_controls(self):
        # 그래프 뷰 유효성 체크
        self.apply_button.config(state="normal" if self.m_viewGraph.IsAvailable() else "disabled")
        
        # TimerTick 100ms 반복 호출 (C# m_timer 대응)
        self.after(100, self.update_controls)

    def on_select_toggle(self):
        if self.select_var.get() == "all":
            for var, _ in self.check_vars:
                var.set(True)
        elif self.select_var.get() == "none":
            for var, _ in self.check_vars:
                var.set(False)

if __name__ == "__main__":
    app = GraphViewContextMenu()
    app.mainloop()