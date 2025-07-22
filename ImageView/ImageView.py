# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# WinForms 관련
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import *
from System.Drawing import Point, Size
from System import EventHandler, Int64, Int32

class FormImageView(Form):
    def __init__(self):
        Form.__init__(self)
        self.Text = "Form Image View"
        self.Size = Size(420, 276)

        self.m_bLockControls = False
        
        self.m_viewImage = CGUIViewImage()
        
        x1 = 10
        x2 = 207
        y = 10
        cx = 187
        cy = 23

        # Buttons
        self.buttonOpenView = Button()
        self.buttonOpenView.Text = "Open Image View"
        self.buttonOpenView.Location = Point(x1, y)
        self.buttonOpenView.Size = Size(cx, cy)

        self.buttonTerminateView = Button()
        self.buttonTerminateView.Text = "Terminate View"
        self.buttonTerminateView.Location = Point(x2, y)
        self.buttonTerminateView.Size = Size(cx, cy)

        y += 30
        
        self.buttonLoadImage = Button()
        self.buttonLoadImage.Text = "Load Image"
        self.buttonLoadImage.Location = Point(x1, y)
        self.buttonLoadImage.Size = Size(cx, cy)

        self.buttonSaveImage = Button()
        self.buttonSaveImage.Text = "Save Image"
        self.buttonSaveImage.Location = Point(x2, y)
        self.buttonSaveImage.Size = Size(cx, cy)
        
        self.Controls.AddRange([self.buttonOpenView, self.buttonTerminateView, self.buttonLoadImage, self.buttonSaveImage])

        y += 35
        
        # GroupBox 추가
        self.group = GroupBox()
        self.group.Text = "Figure Object"
        self.group.Location = Point(x1, y)
        self.group.Size = Size(382, 150)
        self.Controls.Add(self.group)
        
        x1 = 5
        x2 = 197
        y = 23
        cx = 180
        
        # Label : DeclType
        self.labelDeclType = Label()
        self.labelDeclType.Text = "DeclType"
        self.labelDeclType.Size = Size(cx, 16)
        self.labelDeclType.Location = Point(x1, y)
        self.group.Controls.Add(self.labelDeclType)
        
        # Label : Info
        self.labelInfo = Label()
        self.labelInfo.Text = "Info"
        self.labelInfo.Size = Size(cx, 16)
        self.labelInfo.Location = Point(x2, y)
        self.group.Controls.Add(self.labelInfo)

        y+=18

        # ComboBox : DeclType
        self.comboBoxDeclType = ComboBox()
        self.comboBoxDeclType.DropDownStyle = ComboBoxStyle.DropDownList
        self.comboBoxDeclType.Location = Point(x1, y)
        self.comboBoxDeclType.Size = Size(cx, cy)
        self.group.Controls.Add(self.comboBoxDeclType)
        
        # Info Output
        self.richTextBoxInfo = TextBox()
        self.richTextBoxInfo.Multiline = True
        self.richTextBoxInfo.ReadOnly = True
        self.richTextBoxInfo.ScrollBars = ScrollBars.Vertical
        self.richTextBoxInfo.Location = Point(x2, y)
        self.richTextBoxInfo.Size = Size(cx, 70)
        self.group.Controls.Add(self.richTextBoxInfo)

        y+=30
        
        # Label : TemplateType
        self.labelDeclType = Label()
        self.labelDeclType.Text = "TemplateType"
        self.labelDeclType.Size = Size(cx, 16)
        self.labelDeclType.Location = Point(x1, y)
        self.group.Controls.Add(self.labelDeclType)
        
        y+=18

        # ComboBox : TemplateType
        self.comboBoxTemplateType = ComboBox()
        self.comboBoxTemplateType.DropDownStyle = ComboBoxStyle.DropDownList
        self.comboBoxTemplateType.Location = Point(x1, y)
        self.comboBoxTemplateType.Size = Size(cx, cy)
        self.group.Controls.Add(self.comboBoxTemplateType)

        self.comboBoxDeclType.Items.AddRange(["Point", "Line", "Rect", "Quad", "Circle", "Ellipse", "CubicSpline", "Region", "ComplexRegion", "Doughnut"])
        self.comboBoxTemplateType.Items.AddRange(["Int32", "Int64", "Float", "Double"])
        self.comboBoxDeclType.SelectedIndex = 0
        self.comboBoxTemplateType.SelectedIndex = 0
        
        y+=30
        
        # Button : Create Figure
        self.buttonCreate = Button()
        self.buttonCreate.Text = "Create Figure"
        self.buttonCreate.Location = Point(x1, y)
        self.buttonCreate.Size = Size(cx, cy)
        self.group.Controls.Add(self.buttonCreate)
        
        # Button : Pop Front Figure
        self.buttonPopFront = Button()
        self.buttonPopFront.Text = "Pop Front Figure"
        self.buttonPopFront.Location = Point(x2, y)
        self.buttonPopFront.Size = Size(cx, cy)
        self.group.Controls.Add(self.buttonPopFront)

        self.buttonOpenView.Click += EventHandler(self.ClickButtonOpenView)
        self.buttonTerminateView.Click += EventHandler(self.ClickButtonTerminateView)
        self.buttonLoadImage.Click += EventHandler(self.ClickButtonLoadImage)
        self.buttonSaveImage.Click += EventHandler(self.ClickButtonSaveImage)
        self.buttonCreate.Click += EventHandler(self.ClickButtonCreate)
        self.buttonPopFront.Click += EventHandler(self.ClickButtonPopFront)

        # Timer
        self.m_timer = Timer()
        self.m_timer.Interval = 100
        self.m_timer.Tick += EventHandler(self.TimerTick)
        self.m_timer.Start()

        self.UpdateControls()

    def ErrorMessageBox(self, cResult, msg):
        message = f"Error code : {cResult.GetResultCode()}\nError name : {cResult.GetString()}\n"
        if len(msg) > 1:
            message += msg
        MessageBox.Show(message, "Error")

    def LockControls(self, lock_flag):
        self.m_bLockControls = lock_flag
        self.UpdateControls()

    def TimerTick(self, sender, e):
        self.UpdateControls()

    def UpdateControls(self):
        if self.m_bLockControls:
            enabled = False
        elif not self.m_viewImage.IsAvailable():
            enabled = False
        else:
            enabled = True

        self.buttonOpenView.Enabled = not enabled
        self.buttonTerminateView.Enabled = enabled
        self.buttonLoadImage.Enabled = enabled
        self.buttonSaveImage.Enabled = self.m_viewImage.DoesFLImageBufferExist() if enabled else False
        self.buttonCreate.Enabled = enabled
        self.buttonPopFront.Enabled = self.m_viewImage.GetFigureObjectCount() > 0 if enabled else False
        self.comboBoxDeclType.Enabled = enabled
        self.comboBoxTemplateType.Enabled = enabled and self.SelectedDeclType() not in [
            EFigureDeclType.CubicSpline,
            EFigureDeclType.Region,
            EFigureDeclType.ComplexRegion
        ]

    def ClickButtonOpenView(self, sender, e):
        if self.m_viewImage.IsAvailable(): return
        res = self.m_viewImage.Create(0, 0, 500, 500)
        if res.IsFail(): self.ErrorMessageBox(res, "")

    def ClickButtonTerminateView(self, sender, e):
        if not self.m_viewImage.IsAvailable(): return
        res = self.m_viewImage.Destroy()
        if res.IsFail(): self.ErrorMessageBox(res, "")

    def ClickButtonLoadImage(self, sender, e):
        if not self.m_viewImage.IsAvailable(): return
        self.LockControls(True)
        self.m_viewImage.Load("", EViewImageLoadOption.Load)
        self.LockControls(False)

    def ClickButtonSaveImage(self, sender, e):
        if not self.m_viewImage.IsAvailable(): return
        if not self.m_viewImage.DoesFLImageBufferExist(): return
        self.LockControls(True)
        self.m_viewImage.Save("", False)
        self.LockControls(False)

    def ClickButtonCreate(self, sender, e):
        if not self.m_viewImage.IsAvailable(): return

        eTemplateType = [
            EFigureTemplateType.Int32,
            EFigureTemplateType.Int64,
            EFigureTemplateType.Float,
            EFigureTemplateType.Double
        ][self.comboBoxTemplateType.SelectedIndex]

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
        if flFigure is None: return

        flFigure.Set(flrdFigureShape)
        self.m_viewImage.PushBackFigureObject(flFigure, EAvailableFigureContextMenu.All)

    def ClickButtonPopFront(self, sender, e):
        if not self.m_viewImage.IsAvailable(): return
        flFigure = self.m_viewImage.PopFrontFigureObject()
        if flFigure is None: return
        strFigure = CFigureUtilities.ConvertFigureObjectToString(flFigure)
        self.richTextBoxInfo.Text = strFigure

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
        ][self.comboBoxDeclType.SelectedIndex]

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

if __name__ == "__main__":
    Application.EnableVisualStyles()
    Application.Run(FormImageView())
