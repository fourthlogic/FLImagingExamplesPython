# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# WinForms 관련
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import *
from System.Drawing import Point, Size
from System import EventHandler, Int64, Int32

class FormGraphView(Form):
    def __init__(self):
        Form.__init__(self)
        self.Text = "Form Graph View"
        self.Size = Size(420, 221)

        self.m_bLockControls = False
        
        self.m_viewGraph = CGUIViewGraph()
        
        x1 = 10
        x2 = 207
        y = 10
        cx = 187
        cy = 23

        # Buttons
        self.buttonOpenView = Button()
        self.buttonOpenView.Text = "Open Graph View"
        self.buttonOpenView.Location = Point(x1, y)
        self.buttonOpenView.Size = Size(cx, cy)

        self.buttonTerminateView = Button()
        self.buttonTerminateView.Text = "Terminate View"
        self.buttonTerminateView.Location = Point(x2, y)
        self.buttonTerminateView.Size = Size(cx, cy)

        y += 30
        
        self.buttonLoadGraph = Button()
        self.buttonLoadGraph.Text = "Load Graph"
        self.buttonLoadGraph.Location = Point(x1, y)
        self.buttonLoadGraph.Size = Size(cx, cy)

        self.buttonSaveGraph = Button()
        self.buttonSaveGraph.Text = "Save Graph"
        self.buttonSaveGraph.Location = Point(x2, y)
        self.buttonSaveGraph.Size = Size(cx, cy)
        
        self.Controls.AddRange([self.buttonOpenView, self.buttonTerminateView, self.buttonLoadGraph, self.buttonSaveGraph])

        y += 35
        
        # GroupBox 추가
        self.group = GroupBox()
        self.group.Text = "Chart"
        self.group.Location = Point(x1, y)
        self.group.Size = Size(382, 98)
        self.Controls.Add(self.group)
        
        x1 = 5
        x2 = 197
        y = 23
        cx = 180
        
        # Label : Name
        self.labelName = Label()
        self.labelName.Text = "Name"
        self.labelName.Size = Size(cx, 16)
        self.labelName.Location = Point(x1, y)
        self.group.Controls.Add(self.labelName)
        
        # Label : Type
        self.labelType = Label()
        self.labelType.Text = "Type"
        self.labelType.Size = Size(cx, 16)
        self.labelType.Location = Point(x2, y)
        self.group.Controls.Add(self.labelType)

        y+=18

        # TextBox : Name
        self.textboxName = TextBox()
        self.textboxName.Location = Point(x1, y)
        self.textboxName.Size = Size(cx, cy)
        self.group.Controls.Add(self.textboxName)
        
        # ComboBox : ChartType
        self.comboBoxChartType = ComboBox()
        self.comboBoxChartType.DropDownStyle = ComboBoxStyle.DropDownList
        self.comboBoxChartType.Location = Point(x2, y)
        self.comboBoxChartType.Size = Size(cx, cy)
        self.group.Controls.Add(self.comboBoxChartType)

        self.comboBoxChartType.Items.AddRange(["Bar", "Line", "Scatter"])
        self.comboBoxChartType.SelectedIndex = 0
        
        y+=26
        
        # Button : Add
        self.buttonAdd = Button()
        self.buttonAdd.Text = "Add"
        self.buttonAdd.Location = Point(x1, y)
        self.buttonAdd.Size = Size(cx, cy)
        self.group.Controls.Add(self.buttonAdd)
        
        # Button : Clear
        self.buttonClear = Button()
        self.buttonClear.Text = "Clear"
        self.buttonClear.Location = Point(x2, y)
        self.buttonClear.Size = Size(cx, cy)
        self.group.Controls.Add(self.buttonClear)

        self.buttonOpenView.Click += EventHandler(self.ClickButtonOpenView)
        self.buttonTerminateView.Click += EventHandler(self.ClickButtonTerminateView)
        self.buttonLoadGraph.Click += EventHandler(self.ClickButtonLoadGraph)
        self.buttonSaveGraph.Click += EventHandler(self.ClickButtonSaveGraph)
        self.buttonAdd.Click += EventHandler(self.ClickButtonChartAdd)
        self.buttonClear.Click += EventHandler(self.ClickButtonChartClear)

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
        elif not self.m_viewGraph.IsAvailable():
            enabled = False
        else:
            enabled = True

        self.buttonOpenView.Enabled = not enabled
        self.buttonTerminateView.Enabled = enabled
        self.buttonLoadGraph.Enabled = enabled
        self.buttonSaveGraph.Enabled = self.m_viewGraph.DoesGraphExist() if enabled else False
        self.buttonAdd.Enabled = enabled
        self.buttonClear.Enabled = self.m_viewGraph.DoesGraphExist() if enabled else False
        self.textboxName.Enabled = enabled
        self.comboBoxChartType.Enabled = enabled 

    def ClickButtonOpenView(self, sender, e):
        if self.m_viewGraph.IsAvailable(): 
            return
        
        if (res := self.m_viewGraph.Create(0, 0, 500, 500)).IsFail(): 
            self.ErrorMessageBox(res, "")

        self.m_viewGraph.ZoomFit()

    def ClickButtonTerminateView(self, sender, e):
        if not self.m_viewGraph.IsAvailable(): 
            return
        
        if (res := self.m_viewGraph.Destroy()).IsFail(): 
            self.ErrorMessageBox(res, "")

    def ClickButtonLoadGraph(self, sender, e):
        if not self.m_viewGraph.IsAvailable(): 
            return
        self.LockControls(True)
        self.m_viewGraph.Load("", EViewGraphLoadOption(int(EViewGraphLoadOption.Load) | int(EViewGraphLoadOption.OpenDialog), True))
        self.LockControls(False)

    def ClickButtonSaveGraph(self, sender, e):
        if not self.m_viewGraph.IsAvailable(): 
            return
        if not self.m_viewGraph.DoesGraphExist(): 
            return
        self.LockControls(True)
        self.m_viewGraph.Save()
        self.LockControls(False)

    def ClickButtonChartAdd(self, sender, e):
        import random
        if not self.m_viewGraph.IsAvailable(): 
            return

        # Chart Name
        strChartName = self.textboxName.Text
        if strChartName == "":
            strChartName = "Chart"

        # Chart Type
        eChartType = EChartType(self.comboBoxChartType.SelectedIndex + 1, True)

        # Data Count
        i32DataCount = 30

        # Data Array
        dataX = [float(random.randint(0, 99)) for _ in range(i32DataCount)]
        dataY = [float(random.randint(0, 99)) for _ in range(i32DataCount)]
        arrF64DataX1 = Array[Double](dataX)
        arrF64DataY1 = Array[Double](dataY)

        # Chart Color
        eColor = EColor((random.randint(0, 255)) | (random.randint(0, 255) << 8) | (random.randint(0, 255) << 16), True)

        # Plot
        self.m_viewGraph.Plot(arrF64DataX1, arrF64DataY1, i32DataCount, eChartType, eColor, strChartName)
        self.m_viewGraph.Invalidate()

    def ClickButtonChartClear(self, sender, e):
        if not self.m_viewGraph.IsAvailable(): 
            return
        self.m_viewGraph.Clear()
        self.m_viewGraph.Invalidate()

if __name__ == "__main__":
    Application.EnableVisualStyles()
    Application.Run(FormGraphView())
