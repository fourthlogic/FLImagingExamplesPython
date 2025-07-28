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

	# Crevis 카메라 선언 // Declare the Crevis camera
	camCrevis = CDeviceCameraCrevis()

	while True:
		
		strInput = ""

		eDeviceType = CDeviceGenICamTypeBase.EDeviceType.GigE
		bAutoDetect = False
		i32SelectDevice = -1
		eConnectionMethod = CDeviceGenICamTypeBase.EConnectionMethod.SerialNumber
		strConnection = ""
		
		# 장치 타입 선택 // Set Device Type
		while True:
			print("1. GigE")
			print("2. USB")
			strInput = input("Select Device Type: ")

			if(strInput.isdigit()):
				bSelected = True

				if(strInput == "1"):
					eDeviceType = CDeviceGenICamTypeBase.EDeviceType.GigE
				elif(strInput == "2"):
					eDeviceType = CDeviceGenICamTypeBase.EDeviceType.USB
				else:
					bSelected = False

				if(bSelected):
					break

			print("Incorrect input. Please select again.\n")

		print()

		# 카메라 인식 방법 선택 // Select Detection Method
		while True:

			print("1. Auto Detect")
			print("2. Manual")
			strInput = input("Select Detection Method: ")

			if(strInput.isdigit()):
				bSelected = True

				if(strInput == "1"):
					bAutoDetect = True
				elif(strInput == "2"):
					bAutoDetect = False
				else:
					bSelected = False
						
				if(bSelected):
					break

			print("Incorrect input. Please select again.\n")

		print()

		if(bAutoDetect):
			listSerialNumbers = List[String]()

			# 연결되어 있는 카메라의 시리얼 번호를 가져온다. // Get serial numbers of connected cameras
			
			if(eDeviceType == CDeviceGenICamTypeBase.EDeviceType.GigE):
				er = camCrevis.GetAutoDetectGigECameraSerialNumbers(listSerialNumbers)
			elif(eDeviceType == CDeviceGenICamTypeBase.EDeviceType.USB):
				er = camCrevis.GetAutoDetectUSBCameraSerialNumbers(listSerialNumbers)

			if(er[0].IsFail() or listSerialNumbers.Count == 0):
				er = EResult.FailedToRead
				print("Not Found Device.\n")
				break

			# 연결할 카메라를 선택한다. // Select camera to be connected.
			while(True):
				for i in range(listSerialNumbers.Count):
					strElement = String.Format("{0}. ", i + 1)
					strElement += listSerialNumbers[i] + "\n"
					print(strElement)

				strInput = input("Select Device: ")

				if(strInput.isdigit()):
					i32Input = int(strInput)
					i32Input -= 1

					if(i32Input >= 0 and i32Input < listSerialNumbers.Count):
						i32SelectDevice = i32Input
						break

				print("Incorrect input. Please select again.\n\n")
		else:
			# 시리얼 번호를 입력 받는다. // Enter the serial number.
			strConnection = input("Input Serial Number: ")

		# 이벤트를 받을 객체 선언 // Declare the object that receives events
		eventImage = CDeviceEventImageEx()

		# 카메라에 이벤트 객체 설정 // Set event object on Camera 
		camCrevis.RegisterDeviceEvent(eventImage)

		# 카메라에 장치 타입 설정 // Set device type on Camera
		camCrevis.SetDeviceType(eDeviceType)
		
		if(bAutoDetect):
			# 연결할 인덱스에 해당하는 카메라를 설정한다. // Set the camera corresponding to the index to be connected.
			if(eDeviceType == CDeviceGenICamTypeBase.EDeviceType.GigE):
				er = camCrevis.AutoDetectGigECamera(i32SelectDevice)
			elif(eDeviceType == CDeviceGenICamTypeBase.EDeviceType.USB):
				er = camCrevis.AutoDetectUSBCamera(i32SelectDevice)

			if(er.IsFail()):
				print("Failed to Select Device\n")
				break
		else:
			camCrevis.SetConnectionMethod(eConnectionMethod)
			
			if(eConnectionMethod == CDeviceGenICamBase.EConnectionMethod.SerialNumber):
				# 카메라에 연결할 시리얼 번호를 설정한다. // Set the serial number to camera
				camCrevis.SetSerialNumber(strConnection)
			else:
				# 카메라에 연결할 IP 주소를 설정한다. // Set the IP address to camera
				camCrevis.SetIPAddress(strConnection)

		# 카메라 초기화 // Initialize the camera
		if((er := camCrevis.Initialize()).IsFail()):
			print("Failed to initialize the camera.\n")
			break

		# 이미지 뷰 생성 // Create image view
		if((er := viewImage.Create(0,0,1000,1000)).IsFail()):
			er = EResult.FailedToCreateObject
			print("Failed to create the image view.\n")
			break

		eventImage.SetViewImage(viewImage)

		# 카메라 Live // Live the camera
		if((er := camCrevis.Live()).IsFail()):
			print("Failed to live the camera\n")
			break

		# 이미지 뷰가 종료될 때 까지 기다림 // Wait for the image view to close.
		while(viewImage.IsAvailable()):
			CThreadUtilities.Sleep(1)

		break
	
	# 카메라의 초기화를 해제 // Terminate the camera
	camCrevis.Terminate()
	# 카메라에 연결된 이벤트 객체 삭제 // Clear the object that receives events.
	camCrevis.ClearDeviceEvents()

	# End of main function

# 에러 출력 함수 // Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()