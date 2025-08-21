# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


class CDeviceEventImageEx(CDeviceEventImageBase):

	def __init__(self):
		super().__init__()
		self.RegisterOnAcquisition(CDeviceEventImageEx.Delegate_OnAcquisition(self.OnAcquisition))
		self.m_fliImage = CFLImage()
		self.m_viewImage = None
		
	def SetViewImage(self, viewImage):
		self.m_viewImage = viewImage
		self.m_viewImage.SetImagePtr(self.m_fliImage)

	def OnAcquisition(self, pDeviceImage):
		if self.m_viewImage is not None and self.m_viewImage.IsAvailable():
			self.m_fliImage.Lock()
			pDeviceImage.GetAcquiredImage(self.m_fliImage)
			self.m_fliImage.Unlock()

			self.m_viewImage.Invalidate()

# 메인 함수 # Main function
def main():

	# CResult 객체 선언 # Declare the CRessult object
	er = CResult(EResult.UnknownError)

	# 이미지 뷰 선언 # Declare the image view
	viewImage = CGUIViewImage()

	# EGrabber 카메라 선언 # Declare the EGrabber camera
	camEGrabber = CDeviceCameraEGrabber()

	while True:
		
		strInput = ""

		i32BoardIndex = 0
		i32ModuleIndex = 0

		# 보드의 인덱스 입력 # Enter the index of board
		strInput = input("Enter board index: ")

		if(strInput.isdigit()):
			i32BoardIndex = int(strInput)
		
		# 모듈의 인덱스 입력 # Enter the index of module
		strInput = input("Enter module index: ")

		if(strInput.isdigit()):
			i32ModuleIndex = int(strInput)

		# 이벤트를 받을 객체 선언 # Declare the object that receives events
		eventImage = CDeviceEventImageEx()

		# 카메라에 이벤트 객체 설정 # Set event object on Camera 
		camEGrabber.RegisterDeviceEvent(eventImage)

		# 카메라에 파라미터 설정 # Set paramter on Camera
		camEGrabber.SetBoardIndex(i32BoardIndex)
		camEGrabber.SetModuleIndex(i32ModuleIndex)

		# 카메라 초기화 # Initialize the camera
		if((er := camEGrabber.Initialize()).IsFail()):
			print("Failed to initialize the camera.\n")
			break

		# 이미지 뷰 생성 # Create image view
		if((er := viewImage.Create(0,0,1000,1000)).IsFail()):
			er = EResult.FailedToCreateObject
			print("Failed to create the image view.\n")
			break

		eventImage.SetViewImage(viewImage)

		# 카메라 Live # Live the camera
		if((er := camEGrabber.Live()).IsFail()):
			print("Failed to live the camera\n")
			break

		# 이미지 뷰가 종료될 때 까지 기다림 # Wait for the image view to close.
		while(viewImage.IsAvailable()):
			CThreadUtilities.Sleep(1)

		break
	
	# 카메라의 초기화를 해제 # Terminate the camera
	camEGrabber.Terminate()
	# 카메라에 연결된 이벤트 객체 삭제 # Clear the object that receives events.
	camEGrabber.ClearDeviceEvents()

	# End of main function

# 에러 출력 함수 # Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()