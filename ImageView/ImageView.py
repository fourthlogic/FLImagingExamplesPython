# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


import tkinter as tk
from tkinter import ttk, scrolledtext

class ImageViewerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image View")
        self.geometry("404x246")

        # 컨트롤 잠금 상태
        # Control lock state
        self.m_bLockControls = False
        
        # 이미지 뷰 객체 인스턴스 생성
        # Create an instance of the image view object
        self.m_viewImage = CGUIViewImage()

        self._create_main_controls()
        self._create_group_box()
        self.update_controls()

        # Timer
        # Start the timer
        self.after(100, self.timer_tick)

    # 메인 컨트롤 생성 및 배치 함수
    # Function to create and position the main control buttons
    def _create_main_controls(self):
        x1, x2, y, cx, cy = 10, 207, 10, 187, 23

        self.buttonOpenView = tk.Button(self, text="Open Image View", width=25, command=self.click_button_open_view)
        self.buttonOpenView.place(x=x1, y=y, width=cx, height=cy)

        self.buttonTerminateView = tk.Button(self, text="Terminate View", width=25, command=self.click_button_terminate_view)
        self.buttonTerminateView.place(x=x2, y=y, width=cx, height=cy)

        y += 30
        self.buttonLoadImage = tk.Button(self, text="Load Image", width=25, command=self.click_button_load_image)
        self.buttonLoadImage.place(x=x1, y=y, width=cx, height=cy)

        self.buttonSaveImage = tk.Button(self, text="Save Image", width=25, command=self.click_button_save_image)
        self.buttonSaveImage.place(x=x2, y=y, width=cx, height=cy)
        
    # 그룹박스 및 그룹박스 내부 컨트롤 생성 및 배치 함수
    # Function to create and position the group box and its internal controls
    def _create_group_box(self):
        self.group = tk.LabelFrame(self, text="Figure Object")
        self.group.place(x=10, y=75, width=382, height=150)

        gx1, gx2, gy, gcx = 5, 197, 3, 175

        tk.Label(self.group, text="DeclType").place(x=gx1, y=gy)
        tk.Label(self.group, text="Info").place(x=gx2, y=gy)

        gy += 22
        self.comboBoxDeclType = ttk.Combobox(self.group, state="readonly", width=23)
        self.comboBoxDeclType['values'] = [
            "Point", "Line", "Rect", "Quad", "Circle",
            "Ellipse", "CubicSpline", "Region", "ComplexRegion", "Doughnut"
        ]
        self.comboBoxDeclType.current(0)
        self.comboBoxDeclType.place(x=gx1, y=gy, width=gcx)

        self.richTextBoxInfo = scrolledtext.ScrolledText(self.group, width=23, height=4, state="disabled")
        self.richTextBoxInfo.place(x=gx2, y=gy, width=gcx, height=70)

        gy += 26
        tk.Label(self.group, text="TemplateType").place(x=gx1, y=gy)

        gy += 22
        self.comboBoxTemplateType = ttk.Combobox(self.group, state="readonly", width=23)
        self.comboBoxTemplateType['values'] = ["Int32", "Int64", "Float", "Double"]
        self.comboBoxTemplateType.current(0)
        self.comboBoxTemplateType.place(x=gx1, y=gy, width=gcx)

        gy += 30
        self.buttonCreate = tk.Button(self.group, text="Create Figure", width=25, command=self.click_button_create_figure)
        self.buttonCreate.place(x=gx1, y=gy, width=gcx, height=23)

        self.buttonPopFront = tk.Button(self.group, text="Pop Front Figure", width=25, command=self.click_button_pop_front)
        self.buttonPopFront.place(x=gx2, y=gy, width=gcx, height=23)

    # 타이머 함수
    # Timer callback function
    def timer_tick(self):
        self.update_controls()
        self.after(100, self.timer_tick)

    # 컨트롤 잠금 함수
    # Function to lock or unlock UI controls
    def LockControls(self, lock_flag):
        self.m_bLockControls = lock_flag
        self.update_controls()

    # 컨트롤 업데이트 함수
    # Function to update the enabled/disabled state of UI controls
    def update_controls(self):
        available = not self.m_bLockControls and self.m_viewImage.IsAvailable()
        has_image = self.m_viewImage.DoesFLImageBufferExist()
        has_figure = self.m_viewImage.GetFigureObjectCount()
        selected_decl_type = self.comboBoxDeclType.get()

        disable_template = selected_decl_type in ["CubicSpline", "Region", "ComplexRegion"]

        self.buttonOpenView.config(state=("normal" if not available else "disabled"))
        self.buttonTerminateView.config(state=("normal" if available else "disabled"))
        self.buttonLoadImage.config(state=("normal" if available else "disabled"))
        self.buttonSaveImage.config(state=("normal" if has_image and available else "disabled"))
        self.buttonCreate.config(state=("normal" if available else "disabled"))
        self.buttonPopFront.config(state=("normal" if has_figure and available else "disabled"))
        self.comboBoxDeclType.config(state=("readonly" if available else "disabled"))
        self.comboBoxTemplateType.config(state=("disabled" if disable_template or not available else "readonly"))

    # Open View 버튼에 대한 이벤트 처리기
    # Event handler for the "Open View" button
    def click_button_open_view(self):
        if self.m_viewImage.IsAvailable(): 
            return
        
        if (res := self.m_viewImage.Create(0, 0, 500, 500)).IsFail(): 
            self.ErrorMessageBox(res, "")

    # Terminate View 버튼에 대한 이벤트 처리기
    # Event handler for the "Terminate View" button
    def click_button_terminate_view(self):
        if not self.m_viewImage.IsAvailable(): 
            return
        
        if (res := self.m_viewImage.Destroy()).IsFail(): 
            self.ErrorMessageBox(res, "")

    # 이미지 로드 버튼에 대한 이벤트 처리기
    # Event handler for the "Load Image" button
    def click_button_load_image(self):
        if not self.m_viewImage.IsAvailable(): 
            return
        self.LockControls(True)
        self.m_viewImage.Load("", EViewImageLoadOption.Load)
        self.LockControls(False)

    # 이미지 저장 버튼에 대한 이벤트 처리기
    # Event handler for the "Save Image" button
    def click_button_save_image(self):
        if not self.m_viewImage.IsAvailable(): 
            return
        if not self.m_viewImage.DoesFLImageBufferExist(): 
            return
        self.LockControls(True)
        self.m_viewImage.Save("", False)
        self.LockControls(False)
        
    # Create Figure 버튼에 대한 이벤트 처리기. Figure 객체를 생성하여 이미지 뷰에 push
    # Event handler for the "Create Figure" button — creates a figure object and pushes it to the image view
    def click_button_create_figure(self):
        if not self.m_viewImage.IsAvailable(): 
            return

        eTemplateType = [
            EFigureTemplateType.Int32,
            EFigureTemplateType.Int64,
            EFigureTemplateType.Float,
            EFigureTemplateType.Double
        ][self.comboBoxTemplateType.current()]

        decl_type = self.SelectedDeclType()

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

        flFigure = self.CreateFigure(decl_type, eTemplateType)
        if flFigure is None: 
            return

        flFigure.Set(flrdFigureShape)

        # 생성한 Figure를 이미지 뷰에 추가
        # Add the created Figure to the image view
        self.m_viewImage.PushBackFigureObject(flFigure, EAvailableFigureContextMenu.All)

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

    # EFigureDeclType과 EFigureTemplateType를 지정하여 CFLFigure 객체를 생성하는 함수
    # Creates a CFLFigure object using the specified EFigureDeclType and EFigureTemplateType
    def CreateFigure(self, decl_type, template_type):
        if decl_type == EFigureDeclType.Point:
            return {
                EFigureTemplateType.Int32: CFLPoint[Int32](),
                EFigureTemplateType.Int64: CFLPoint[Int64](),
                EFigureTemplateType.Float: CFLPoint[Single](),
                EFigureTemplateType.Double: CFLPoint[Double]()
            }.get(template_type)
        elif decl_type == EFigureDeclType.Line:
            return {
                EFigureTemplateType.Int32: CFLLine[Int32](),
                EFigureTemplateType.Int64: CFLLine[Int64](),
                EFigureTemplateType.Float: CFLLine[Single](),
                EFigureTemplateType.Double: CFLLine[Double]()
            }.get(template_type)
        elif decl_type == EFigureDeclType.Rect:
            return {
                EFigureTemplateType.Int32: CFLRect[Int32](),
                EFigureTemplateType.Int64: CFLRect[Int64](),
                EFigureTemplateType.Float: CFLRect[Single](),
                EFigureTemplateType.Double: CFLRect[Double]()
            }.get(template_type)
        elif decl_type == EFigureDeclType.Quad:
            return {
                EFigureTemplateType.Int32: CFLQuad[Int32](),
                EFigureTemplateType.Int64: CFLQuad[Int64](),
                EFigureTemplateType.Float: CFLQuad[Single](),
                EFigureTemplateType.Double: CFLQuad[Single]()
            }.get(template_type)
        elif decl_type == EFigureDeclType.Circle:
            return {
                EFigureTemplateType.Int32: CFLCircle[Int32](),
                EFigureTemplateType.Int64: CFLCircle[Int64](),
                EFigureTemplateType.Float: CFLCircle[Single](),
                EFigureTemplateType.Double: CFLCircle[Double]()
            }.get(template_type)
        elif decl_type == EFigureDeclType.Ellipse:
            return {
                EFigureTemplateType.Int32: CFLEllipse[Int32](),
                EFigureTemplateType.Int64: CFLEllipse[Int64](),
                EFigureTemplateType.Float: CFLEllipse[Single](),
                EFigureTemplateType.Double: CFLEllipse[Double]()
            }.get(template_type)
        elif decl_type == EFigureDeclType.CubicSpline:
            return CFLCubicSpline()
        elif decl_type == EFigureDeclType.Region:
            return CFLRegion()
        elif decl_type == EFigureDeclType.ComplexRegion:
            return CFLComplexRegion()
        elif decl_type == EFigureDeclType.Doughnut:
            return {
                EFigureTemplateType.Int32: CFLDoughnut[Int32](),
                EFigureTemplateType.Int64: CFLDoughnut[Int64](),
                EFigureTemplateType.Float: CFLDoughnut[Single](),
                EFigureTemplateType.Double: CFLDoughnut[Double]()
            }.get(template_type)
        return None

    # PopFront 버튼에 대한 이벤트 처리기. 이미지 뷰에서 맨 앞의 Figure 객체를 pop
    # Event handler for the "Pop Front" button — pops the front-most figure object from the image view
    def click_button_pop_front(self):
        if not self.m_viewImage.IsAvailable(): 
            return

        # 이미지 뷰에서 맨 앞(container의 0번째)의 Figure 객체를 pop 하여 얻어 온다.
        # Pop and retrieve the front-most (index 0) Figure object from the image view
        flFigure = self.m_viewImage.PopFrontFigureObject()
        if flFigure is None: 
            return

        # Figure 객체를 문자열로 변환한다.
        # Convert the Figure object to a string
        strFigure = CFigureUtilities.ConvertFigureObjectToString(flFigure)
        self._set_info_text(strFigure)

    # Info 텍스트 창에 문자열을 출력하는 함수
    # Outputs a string to the Info text area
    def _set_info_text(self, text):
        self.richTextBoxInfo.config(state="normal")
        self.richTextBoxInfo.delete("1.0", "end")
        self.richTextBoxInfo.insert("end", text)
        self.richTextBoxInfo.config(state="disabled")

if __name__ == "__main__":
    app = ImageViewerApp()
    app.mainloop()
