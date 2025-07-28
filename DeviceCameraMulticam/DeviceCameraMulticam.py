# FLImagingClrPy 선언 // Declare FLImagingClrPy
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

# 메인 함수 // Main function
def main():

	# CResult 객체 선언 // Declare the CRessult object
	er = CResult(EResult.UnknownError)

	# 이미지 뷰 선언 // Declare the image view
	viewImage = CGUIViewImage()

	# Multicam 카메라 선언 // Declare the Multicam camera
	camMulticam = CDeviceCameraMulticam()

	while True:
		
		strInput = ""

		strCamFilePath = ""
		i32BoardIndex = 0
		eBoardTopology = CDeviceCameraMulticam.EBoardTopology.Mono

		# Cam file 의 전체 경로를 입력 // Enter the full path of Cam file.
		strCamFilePath = input("Enter camfile full path (e.g. C:/Camfile/AnyCamfile.cam): ")

		# 보드의 인덱스 입력 // Enter the index of board
		strInput = input("Enter board index: ")

		if(strInput.isdigit()):
			i32BoardIndex = int(strInput)

		# 보드의 Topology를 선택 // Select topology of board
		while True:

			print("1. Mono")
			print("2. Mono deca")
			print("3. Mono slow")
			strInput = input("Select board topology: ")

			if strInput.isdigit():
				bSelected = True

				i32Select = int(strInput)

				if i32Select == 1:
					eBoardTopology = CDeviceCameraMulticam.EBoardTopology.Mono
				elif i32Select == 2:
					eBoardTopology = CDeviceCameraMulticam.EBoardTopology.MonoDeca
				elif i32Select == 3:
					eBoardTopology = CDeviceCameraMulticam.EBoardTopology.MonoSlow
				else:
					bSelected = False

				if bSelected:
					break

			print("Incorrect input. Please select again.\n")

		# 이벤트를 받을 객체 선언 // Declare the object that receives events
		eventImage = CDeviceEventImageEx()

		# 카메라에 이벤트 객체 설정 // Set event object on Camera 
		camMulticam.RegisterDeviceEvent(eventImage)

		# 카메라에 파라미터 설정 // Set paramter on Camera
		camMulticam.SetCamFilePath(strCamFilePath)
		camMulticam.SetBoardIndex(i32BoardIndex)
		camMulticam.SetBoardTopology(eBoardTopology)

		# 카메라 초기화 // Initialize the camera
		if((er := camMulticam.Initialize()).IsFail()):
			print("Failed to initialize the camera.\n")
			break

		# 이미지 뷰 생성 // Create image view
		if((er := viewImage.Create(0,0,1000,1000)).IsFail()):
			er = EResult.FailedToCreateObject
			print("Failed to create the image view.\n")
			break

		eventImage.SetViewImage(viewImage)

		# 카메라 Live // Live the camera
		if((er := camMulticam.Live()).IsFail()):
			print("Failed to live the camera\n")
			break

		# 이미지 뷰가 종료될 때 까지 기다림 // Wait for the image view to close.
		while(viewImage.IsAvailable()):
			CThreadUtilities.Sleep(1)

		break
	
	# 카메라의 초기화를 해제 // Terminate the camera
	camMulticam.Terminate()
	# 카메라에 연결된 이벤트 객체 삭제 // Clear the object that receives events.
	camMulticam.ClearDeviceEvents()

	# End of main function

# 에러 출력 함수 // Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()