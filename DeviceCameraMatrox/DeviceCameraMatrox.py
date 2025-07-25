# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

CLibraryUtilities.Initialize()

import threading


class CDeviceEventImageEx(CDeviceEventImageBase):

	def __init__(self):
		super().__init__()
		self.RegisterOnAcquisition(CDeviceEventImageEx.Delegate_OnAcquisition(self.OnAcquisition))
		self.m_fliImage = CFLImage()
		self.m_viewImage = None

	def SetViewImage(self, viewImage):
		self.m_viewImage = viewImage
		
	def OnAcquisition(self, deviceImage):
			if(self.m_viewImage is not None and self.m_viewImage.IsAvailable()):
				self.m_fliImage.Lock()
				deviceImage.GetAcquiredImage(self.m_fliImage)
				self.m_fliImage.Unlock()
	
				if(self.m_viewImage.GetImage() != self.m_fliImage):
					self.m_viewImage.SetImagePtr(self.m_fliImage)

				self.m_viewImage.Invalidate()

# 메인 함수 // Main function
def main():

	# CResult 객체 선언 // Declare the CRessult object
	er = CResult(EResult.UnknownError)

	# 이미지 뷰 선언 // Declare the image view
	viewImage = CGUIViewImage()

	# Matrox 카메라 선언 // Declare the Matrox camera
	camMatrox = CDeviceCameraMatrox()

	while True:
		
		strInput = ""
		strCamFilePath = ""

		eDeviceType = CDeviceCameraMatrox.EDeviceType.Unknown
		i32DeviceIndex = 0
		i32ModuleIndex = 0
		
		# Cam file의 전체 경로 입력 // Enter full path of Cam file
		strCamFilePath = input("Enter camfile full path (e.g. C:/Camfile/AnyCamfile.cam): ")

		print()

		while True:
			print("Device type");
			print("1.Clarity UHD\t\t2.Concord POE\t\t3.GenTL");
			print("4.GevIQ\t\t\t5.GigE\t\t\t6.Host");
			print("7.Indio\t\t\t8.Iris GTX\t\t9.Morphis");
			print("10.Radient eV-CXP\t11.Radient eV-CL\t12.Rapixo Pro CL");
			print("13.Rapixo CXP\t\t14.Solios\t\t15.USB3\n");
			strInput = input("Enter device type: ");

			bValid = True

			if(strInput.isdigit()):
				i32DeviceType = int(strInput)

				if(i32DeviceType > 0 and i32DeviceType <= 15):
					eDeviceType = Enum.ToObject(CDeviceCameraMatrox.EDeviceType, i32DeviceType)
				else:
					bValid = False
			else:
				bValid = False
				
			if(bValid):
				break

			print("Incorrect input. Please select again\n")

		print()

		strInput = input("Enter device index: ")

		if(strInput.isdigit()):
			i32DeviceIndex = int(strInput)
		else:
			i32DeviceIndex = 0

		strInput = input("Enter module index: ")

		if(strInput.isdigit()):
			i32ModuleIndex = int(strInput)
		else:
			i32ModuleIndex = 0

		# 이벤트를 받을 객체 선언 // Declare the object that receives events
		eventImage = CDeviceEventImageEx()

		# 카메라에 이벤트 객체 설정 // Set event object on Camera 
		camMatrox.RegisterDeviceEvent(eventImage)

		# 카메라에 파라미터 설정 // Set paramter on Camera
		camMatrox.SetCamFilePath(strCamFilePath)
		camMatrox.SetDeviceType(eDeviceType)
		camMatrox.SetDeviceIndex(i32DeviceIndex)
		camMatrox.SetModuleIndex(i32ModuleIndex)
	
		# 카메라 초기화 // Initialize the camera
		if((er := camMatrox.Initialize()).IsFail()):
			print("Failed to initialize the camera.\n")
			break

		# 이미지 뷰 생성 // Create image view
		if((er := viewImage.Create(0,0,1000,1000)).IsFail()):
			er = EResult.FailedToCreateObject
			print("Failed to create the image view.\n")
			break

		eventImage.SetViewImage(viewImage)

		# 카메라 Live // Live the camera
		if((er := camMatrox.Live()).IsFail()):
			print("Failed to live the camera\n")
			break

		# 이미지 뷰가 종료될 때 까지 기다림 // Wait for the image view to close.
		while(viewImage.IsAvailable()):
			CThreadUtilities.Sleep(1)

		break
	
	# 카메라의 초기화를 해제 // Terminate the camera
	camMatrox.Terminate()
	# 카메라에 연결된 이벤트 객체 삭제 // Clear the object that receives events.
	camMatrox.ClearDeviceEvents()

	# End of main function

# 에러 출력 함수 // Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()