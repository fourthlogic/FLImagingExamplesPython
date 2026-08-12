# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


import tkinter as tk
from tkinter import messagebox, LabelFrame, ttk, scrolledtext
import time

def get_hwnd(widget):
    # 윈도우 핸들 얻기 (Tkinter 내부 식별자를 사용)
    # Get window handle (using Tkinter internal identifier)
    widget.update_idletasks()
    hwnd = widget.winfo_id()
    return hwnd

class FigureOperationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("FigureOperation")
        self.geometry("734x511")

        # 왼쪽 패널 (이미지 뷰 영역)
        # Left panel (image view area)
        self.left_panel = tk.Frame(self, bd=2, relief="solid")
        self.left_panel.pack(side="left", fill="both", expand=True)
        
        # 오른쪽 컨트롤 패널
        # Right control panel
        self.right_panel = tk.Frame(self, bd=2, relief="solid", width=170)
        self.right_panel.pack(side="right", fill="y")

        self.CreateRightControls()

        self.comboBoxSrc.bind("<<ComboboxSelected>>", self.SelectedIndexChangedComboBoxSrcFigure)
        self.comboBoxDst.bind("<<ComboboxSelected>>", self.SelectedIndexChangedComboBoxDstFigure)

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

    # 컨트롤들의 활성화 여부를 업데이트하는 함수
    # Function to update the enable/disable state of the controls
    def update_controls(self):
        if not self.m_viewImage.IsAvailable():
            self.comboBoxDeclType.config(state='disabled')
            self.comboBoxTemplateType.config(state='disabled')
            self.buttonCreate.config(state='disabled')
            self.buttonClear.config(state='disabled')
            self.comboBoxSrc.config(state='disabled')
            self.comboBoxDst.config(state='disabled')
            self.comboBoxOperation.config(state='disabled')
            self.buttonExecute.config(state='disabled')
        else:
            self.comboBoxDeclType.config(state='normal')

            selected_decl_type = self.SelectedDeclType()
        
            if selected_decl_type in [EFigureDeclType.CubicSpline, EFigureDeclType.Region, EFigureDeclType.ComplexRegion]:
                if self.comboBoxTemplateType.current() != 3:
                    self.comboBoxTemplateType.current(3)
                
                self.comboBoxTemplateType.config(state='disabled')
            else:
                self.comboBoxTemplateType.config(state='normal')

        self.buttonCreate.config(state='normal')

        i32FigureCount = self.m_viewImage.GetFigureObjectCount()
        self.buttonClear.config(state='normal' if i32FigureCount > 0 else 'disabled')

        self.comboBoxSrc.config(state='normal')
        self.comboBoxDst.config(state='normal')
        self.comboBoxOperation.config(state='normal')
        self.buttonExecute.config(state='normal')

        i32FigureCount = self.m_viewImage.GetFigureObjectCount()
        
        if len(self.comboBoxSrc['values']) != i32FigureCount or len(self.comboBoxDst['values']) != i32FigureCount:
            self.UpdateFigureObjectList()

    # 오른쪽 패널의 컨트롤들을 생성 및 배치하는 함수
    # Function to create and place controls in the right panel
    def CreateRightControls(self):
        self.groupboxFigureObject = tk.LabelFrame(self.right_panel, text="Figure Object", font=("Arial", 9))
        self.groupboxFigureObject.place(x=5, y=5, width=160, height=162)
        
        gx, gy, gcx = 3, 22, 150

        tk.Label(self.groupboxFigureObject, text="Decl Type", font=("Arial", 9)).place(x=2, y=0)
        self.comboBoxDeclType = ttk.Combobox(self.groupboxFigureObject, state="readonly", values=[
            "Point", "Line", "Rect", "Quad", "Circle", "Ellipse", "CubicSpline", "Region", "ComplexRegion", "Doughnut"
        ])
        self.comboBoxDeclType.place(x=gx, y=gy, width=gcx, height=23)
        self.comboBoxDeclType.set("Point")

        gy += 23
        tk.Label(self.groupboxFigureObject, text="Template Type", font=("Arial", 9)).place(x=2, y=gy)
        self.comboBoxTemplateType = ttk.Combobox(self.groupboxFigureObject, state="readonly", values=[
            "Int32", "Int64", "Float", "Double"
        ])
        
        gy += 23
        self.comboBoxTemplateType.place(x=gx, y=gy, width=gcx, height=23)
        self.comboBoxTemplateType.set("Double")

        gy += 23
        self.buttonCreate = tk.Button(self.groupboxFigureObject, text="Create", command=self.ClickButtonCreate)
        self.buttonCreate.place(x=gx, y=gy, width=gcx, height=25)
        
        gy += 25
        self.buttonClear = tk.Button(self.groupboxFigureObject, text="Clear", relief="raised", command=self.ClickButtonClear)
        self.buttonClear.place(x=gx, y=gy, width=gcx, height=25)

        gy += 55
        self.groupboxOperation = tk.LabelFrame(self.right_panel, text="Figure Operation", font=("Arial", 9))
        self.groupboxOperation.place(x=5, y=gy, width=160, height=330)

        gy = 23
        tk.Label(self.groupboxOperation, text="Source Figure", font=("Arial", 9), bg="Salmon").place(x=2, y=0)
        self.comboBoxSrc = ttk.Combobox(self.groupboxOperation, state="readonly")
        self.comboBoxSrc.place(x=gx, y=gy, width=gcx, height=23)
        
        gy += 25
        tk.Label(self.groupboxOperation, text="Destination Figure", font=("Arial", 9), bg="CornflowerBlue").place(x=2, y=gy)
        
        gy += 23
        self.comboBoxDst = ttk.Combobox(self.groupboxOperation, state="readonly")
        self.comboBoxDst.place(x=gx, y=gy, width=gcx, height=23)
        
        gy += 23
        tk.Label(self.groupboxOperation, text="Operation", font=("Arial", 9)).place(x=2, y=gy)
        self.comboBoxOperation = ttk.Combobox(self.groupboxOperation, state="readonly", values=[
            "Intersection", "Union", "Subtraction", "Exclusive Or"
        ])

        gy += 23
        self.comboBoxOperation.place(x=gx, y=gy, width=gcx, height=23)
        self.comboBoxOperation.set("Intersection")
        
        gy += 25
        self.buttonExecute = tk.Button(self.groupboxOperation, text="Execute", relief="raised", command=self.ClickButtonExecute)
        self.buttonExecute.place(x=gx, y=gy, width=gcx, height=25)

        tk.Label(self.groupboxOperation, text="Message", font=("Arial", 9)).place(x=2, y=204)
        self.richTextBoxInfo = scrolledtext.ScrolledText(self.groupboxOperation, wrap="word", state="disabled", height=82, width=150)
        self.richTextBoxInfo.place(x=2, y=225, width=150, height=82)
        
    # Create 버튼 클릭에 대한 이벤트 처리기
    # Event handler for Create button click
    def ClickButtonCreate(self):
        if not self.m_viewImage.IsAvailable(): 
            return

        eTemplateType = [
            EFigureTemplateType.Int32,
            EFigureTemplateType.Int64,
            EFigureTemplateType.Float,
            EFigureTemplateType.Double
        ][self.comboBoxTemplateType.current()]

        declType = self.SelectedDeclType()

        flrlCanvas = self.m_viewImage.GetClientRectCanvasRegion()
        flrdImage = self.m_viewImage.ConvertCanvasCoordToImageCoord(flrlCanvas)
        f64Width = flrdImage.GetWidth() / 10.0
        f64Height = flrdImage.GetHeight() / 10.0
        f64Size = min(f64Width, f64Height)

        flpdCenter = CFLPoint[Double](0.0, 0.0)
        flrdImage.GetCenter(flpdCenter)

        flrdFigureShape = CFLRect[Double](
            flpdCenter.x - f64Size,
            flpdCenter.y - f64Size,
            flpdCenter.x + f64Size,
            flpdCenter.y + f64Size
        )

        flFigure = self.CreateFigure(declType, eTemplateType)
        if flFigure is None: 
            return

        flFigure.Set(flrdFigureShape)

        # 이미지 뷰에 Figure object 를 생성한다.
        # Create a Figure object in the image view.
        self.m_viewImage.PushBackFigureObject(flFigure)

        # 이미지 뷰를 갱신한다. # Update the image view.
        self.m_viewImage.Invalidate(True)

        # 콤보 박스에 Figure Object 항목을 설정한다.
        # Set the Figure Object items in the combo box.
        self.UpdateFigureObjectList()

    # Clear 버튼 클릭에 대한 이벤트 처리기
    # Event handler for Clear button click
    def ClickButtonClear(self):
        if not self.m_viewImage.IsAvailable(): 
            return
        
		# 현재 이미지 뷰에 있는 Figure Objects 를 제거한다.
        # Removes Figure Objects currently in the image view.
        self.m_viewImage.ClearFigureObject()

        layer = self.m_viewImage.GetLayer(0)
        layer.Clear()

        # 이미지 뷰를 갱신한다. # Update the image view.
        self.m_viewImage.Invalidate(True)
        # 콤보 박스에 Figure Object 항목을 설정한다.
        # Sets the Figure Object items in the combo box.
        self.UpdateFigureObjectList()
    
    def SelectedIndexChangedComboBoxSrcFigure(self, event):
        self.DrawSelectedFigure()
        
    def SelectedIndexChangedComboBoxDstFigure(self, event):
        self.DrawSelectedFigure()
        
    # Execute 버튼 클릭에 대한 이벤트 처리기
    # Event handler for Execute button click
    def ClickButtonExecute(self):
        flFigure1 = None
        flFigure2 = None
        res = CResult()

        while True:
            flFigure1 = self.GetSelectedFigure1()
            flFigure2 = self.GetSelectedFigure2()

            if flFigure1 is None or flFigure2 is None:
                res = EResult.InvalidObject
                break
            
            flfaRes = CFLFigureArray()

            selected_index = self.comboBoxOperation.current()

            if selected_index == 0:
                # Intersection Operation 수행 # Execute intersection operation
                res = flFigure1.GetRegionOfIntersection(flFigure2, flfaRes)[0]
            elif selected_index == 1:
                # Union Operation 수행 # Execute union operation
                res = flFigure1.GetRegionOfUnion(flFigure2, flfaRes)[0]
            elif selected_index == 2:
                # Subtraction Operation 수행 # Execute subtraction operation
                res = flFigure1.GetRegionOfSubtraction(flFigure2, flfaRes)[0]
            elif selected_index == 3:
                # Exclusive Or Operation 수행 # Execute exclusive or operation
                res = flFigure1.GetRegionOfExclusiveOr(flFigure2, flfaRes)[0]

            if res.IsFail():
                break

            if flfaRes.GetCount() == 0:
                break

            if flfaRes.GetCount() == 1:
                self.m_viewImage.PushBackFigureObject(flfaRes.GetAt(0))
            else:
                self.m_viewImage.PushBackFigureObject(flfaRes)
                
            self.m_viewImage.Invalidate(True)

            self.UpdateFigureObjectList()

            break
        
        # info_box에 문자열을 출력
        # Display text in the info_box
        self._append_info(res.GetString())

    # EFigureDeclType과 EFigureTemplateType를 지정하여 CFLFigure 객체를 생성하는 함수
    # Creates a CFLFigure object using the specified EFigureDeclType and EFigureTemplateType
    def CreateFigure(self, declType, template_type):
        if declType == EFigureDeclType.Point:
            return {
                EFigureTemplateType.Int32: CFLPoint[Int32](),
                EFigureTemplateType.Int64: CFLPoint[Int64](),
                EFigureTemplateType.Float: CFLPoint[Single](),
                EFigureTemplateType.Double: CFLPoint[Double]()
            }.get(template_type)
        elif declType == EFigureDeclType.Line:
            return {
                EFigureTemplateType.Int32: CFLLine[Int32](),
                EFigureTemplateType.Int64: CFLLine[Int64](),
                EFigureTemplateType.Float: CFLLine[Single](),
                EFigureTemplateType.Double: CFLLine[Double]()
            }.get(template_type)
        elif declType == EFigureDeclType.Rect:
            return {
                EFigureTemplateType.Int32: CFLRect[Int32](),
                EFigureTemplateType.Int64: CFLRect[Int64](),
                EFigureTemplateType.Float: CFLRect[Single](),
                EFigureTemplateType.Double: CFLRect[Double]()
            }.get(template_type)
        elif declType == EFigureDeclType.Quad:
            return {
                EFigureTemplateType.Int32: CFLQuad[Int32](),
                EFigureTemplateType.Int64: CFLQuad[Int64](),
                EFigureTemplateType.Float: CFLQuad[Single](),
                EFigureTemplateType.Double: CFLQuad[Single]()
            }.get(template_type)
        elif declType == EFigureDeclType.Circle:
            return {
                EFigureTemplateType.Int32: CFLCircle[Int32](),
                EFigureTemplateType.Int64: CFLCircle[Int64](),
                EFigureTemplateType.Float: CFLCircle[Single](),
                EFigureTemplateType.Double: CFLCircle[Double]()
            }.get(template_type)
        elif declType == EFigureDeclType.Ellipse:
            return {
                EFigureTemplateType.Int32: CFLEllipse[Int32](),
                EFigureTemplateType.Int64: CFLEllipse[Int64](),
                EFigureTemplateType.Float: CFLEllipse[Single](),
                EFigureTemplateType.Double: CFLEllipse[Double]()
            }.get(template_type)
        elif declType == EFigureDeclType.CubicSpline:
            return CFLCubicSpline()
        elif declType == EFigureDeclType.Region:
            return CFLRegion()
        elif declType == EFigureDeclType.ComplexRegion:
            return CFLComplexRegion()
        elif declType == EFigureDeclType.Doughnut:
            return {
                EFigureTemplateType.Int32: CFLDoughnut[Int32](),
                EFigureTemplateType.Int64: CFLDoughnut[Int64](),
                EFigureTemplateType.Float: CFLDoughnut[Single](),
                EFigureTemplateType.Double: CFLDoughnut[Double]()
            }.get(template_type)
        return None

    def DrawSelectedFigure(self):
        if not self.m_viewImage.IsAvailable(): 
            return

        flFigure1 = self.GetSelectedFigure1()
        flFigure2 = self.GetSelectedFigure2()

        layer = self.m_viewImage.GetLayer(0)
        layer.Clear()

        if (flFigure1 is None) and (flFigure2 is None):
            return

        if flFigure1 is not None:
            layer.DrawFigureImage(flFigure1, EColor.RED, 5, EColor.RED, EGUIViewImagePenStyle.Solid, 0.5, 0.3)
            
        if flFigure2 is not None:
            layer.DrawFigureImage(flFigure2, EColor.BLUE, 5, EColor.BLUE, EGUIViewImagePenStyle.Solid, 0.5, 0.3)

        self.m_viewImage.Invalidate(True)
        
    # 콤보박스에서 선택한 아이템에 대한 EFigureDeclType을 반환하는 함수
    # Returns the selected EFigureDeclType based on the selected item in the combo box
    def SelectedDeclType(self):
        return [
            EFigureDeclType.Point,
            EFigureDeclType.Line,
            EFigureDeclType.Rect,
            EFigureDeclType.Quad,
            EFigureDeclType.Circle,
            EFigureDeclType.Ellipse,
            EFigureDeclType.CubicSpline,
            EFigureDeclType.Region,
            EFigureDeclType.ComplexRegion,
            EFigureDeclType.Doughnut
        ][self.comboBoxDeclType.current()]
    
    def UpdateFigureObjectList(self):
        while True:
            i32Selected1 = max(0, self.comboBoxSrc.current())
            i32Selected2 = max(0, self.comboBoxDst.current())
        
            self.comboBoxSrc['values'] = []
            self.comboBoxDst['values'] = []

            FigureNameList = []

            i32Count = self.m_viewImage.GetFigureObjectCount()

            if i32Count == 0:
                break

            for i in range(i32Count):
                flFigure = self.m_viewImage.GetFigureObject(i)
                if not flFigure:
                    continue

                strFigureName = self.MakeFigureObjectName(i, flFigure)
                if not strFigureName:
                    break

                FigureNameList.append(strFigureName)

            self.comboBoxSrc['values'] = FigureNameList
            self.comboBoxDst['values'] = FigureNameList

            if len(FigureNameList) > i32Selected1:
                self.comboBoxSrc.current(i32Selected1)
                
            if len(FigureNameList) > i32Selected2:
                self.comboBoxDst.current(i32Selected2)

            break
        
    def MakeFigureObjectName(self, index, figure):
        while True:
            if not figure:
                break

            mapDeclType = {
            EFigureDeclType.Point: "Point",
            EFigureDeclType.Line: "Line",
            EFigureDeclType.Rect: "Rect",
            EFigureDeclType.Quad: "Quad",
            EFigureDeclType.Circle: "Circle",
            EFigureDeclType.Ellipse: "Ellipse",
            EFigureDeclType.CubicSpline: "CubicSpline",
            EFigureDeclType.Region: "Region",
            EFigureDeclType.ComplexRegion: "ComplexRegion",
            EFigureDeclType.Doughnut: "Doughnut",
            EFigureDeclType.Array: "Array",
        }

            nameDeclType = mapDeclType.get(figure.GetDeclType(), "Unknown")

            if nameDeclType == "Unknown":
                break

            mapTemplateType = {
            EFigureTemplateType.Int32: "(Int32)",
            EFigureTemplateType.Int64: "(Int64)",
            EFigureTemplateType.Float: "(Float)",
            EFigureTemplateType.Double: "(Double)",
        }

            nameTemplateType = mapTemplateType.get(figure.GetTemplateType(), "")

            break
        return f"[{index}] {nameDeclType}{nameTemplateType}"

    def GetSelectedFigure1(self):
        
        flfReturn = None

        while True:
            if not self.m_viewImage.IsAvailable():
                break

            i32Selected = self.comboBoxSrc.current()

            if i32Selected < 0:
                break

            # 해당 인덱스의 Figure Object 를 얻어온다. # Get the Figure Object of the corresponding index
            flfReturn = self.m_viewImage.GetFigureObject(i32Selected)

            break

        return flfReturn
    
    def GetSelectedFigure2(self):
        
        flfReturn = None

        while True:
            if not self.m_viewImage.IsAvailable():
                break

            i32Selected = self.comboBoxDst.current()

            if i32Selected < 0:
                break

            # 해당 인덱스의 Figure Object 를 얻어온다. # Get the Figure Object of the corresponding index
            flfReturn = self.m_viewImage.GetFigureObject(i32Selected)

            break

        return flfReturn

    # info_box에 문자열을 출력하는 함수
    # Function to display text in the info_box
    def _append_info(self, text):
        self.richTextBoxInfo.config(state="normal")
        self.richTextBoxInfo.delete("1.0", "end")
        self.richTextBoxInfo.insert("end", text + "")
        self.richTextBoxInfo.config(state="disabled")
        
    # 주기적으로 컨트롤들의 활성화 여부를 업데이트하는 타이머 함수
    # Timer function that periodically updates the enable/disable state of controls
    def timer_tick(self):
        self.update_controls()
        self.DrawSelectedFigure()
        self.after(100, self.timer_tick)


if __name__ == "__main__":
    app = FigureOperationApp()
    app.mainloop()
