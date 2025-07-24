# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# WinForms 관련
clr.AddReference("System.Windows.Forms")
from System.Windows.Forms import Application, Form, Panel, DockStyle, BorderStyle
from System.Drawing import Size


class SNAPViewIntoDialog(Form):
	def __init__(self):
		Form.__init__(self)
		self.Text = "SNAPViewIntoDialog"
		self.Size = Size(740, 500)

        # 뷰 영역 패널 // View Area Panel
		self.panelView = Panel()
		self.panelView.Dock = DockStyle.Fill
		self.panelView.BorderStyle = BorderStyle.FixedSingle
		self.Controls.Add(self.panelView)

		# 스냅 뷰 객체 선언 // Declare the SNAP View
		self.m_viewSNAP = CGUIViewSNAP()

		while True:
		
		    # 스냅 뷰 생성 // Create SNAP view
			if (res := self.m_viewSNAP.CreateAndFitParent(self.panelView.Handle.ToInt32())).IsFail():
				ErrorPrint(res, 'Failed to create the SNAP view.')
				break

		    # 스냅 파일 로드 // Load SNAP file
			if (res := self.m_viewSNAP.Load('C:/Users/Public/Documents/FLImaging/FLImagingExamplesSNAP/Advanced Functions/Object/Blob.flsf')).IsFail():
				ErrorPrint(res, 'Failed to load the file.')
				break

		    # 스냅 실행 // Run SNAP
			if (res := self.m_viewSNAP.Run()).IsFail():
				ErrorPrint(res, 'Failed to run the SNAP.')
				break

			break


# 에러 출력 함수 // Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == "__main__":
    form = SNAPViewIntoDialog()
    Application.Run(form)
