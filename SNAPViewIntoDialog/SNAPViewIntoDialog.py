# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()

import tkinter as tk

def get_hwnd(widget):
    # 윈도우 핸들 얻기 (Tkinter 내부 식별자를 사용)
    widget.update_idletasks()
    hwnd = widget.winfo_id()
    return hwnd

class SNAPViewIntoDialog(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("SNAPViewIntoDialog")
		self.geometry("740x500")

        # 뷰 영역 패널 // View Area Panel
		self.panelView = tk.Frame(self, bd=2, relief="solid")
		self.panelView.pack(side="left", fill="both", expand=True)
		
		# 스냅 뷰 객체 선언 // Declare the SNAP View
		self.m_viewSNAP = CGUIViewSNAP()

		while True:
		
		    # 스냅 뷰 생성 // Create SNAP view
			if (res := self.m_viewSNAP.CreateAndFitParent(get_hwnd(self.panelView))).IsFail():
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
    app = SNAPViewIntoDialog()
    app.mainloop()
