# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


class CDeviceEventImageEx(CDeviceEventImageBase):

	def __init__(self):
		super().__init__()
		self.RegisterOnAcquisition(CDeviceEventImageEx.Delegate_OnAcquisition(self.OnAcquisition))
		self.m_view3D = None

	def SetView3D(self, view3D):
		self.m_view3D = view3D

	def OnAcquisition(self, deviceImage):
		while(True):
			
			if(self.m_view3D is None):
				break

			if(not self.m_view3D.IsAvailable()):
				break

			if(not isinstance(deviceImage, CDeviceCameraPhoXi)):
				break

			camera = deviceImage
			floData = CFL3DObject()

			camera.GetAcquired3DData(floData)

			if(floData is None):
				break

			self.m_view3D.LockUpdate()

			if(not self.m_view3D.IsAvailable()):			
				break

			i32ObjectCount = self.m_view3D.GetObjectCount()

			self.m_view3D.ClearObjects()

			if(not self.m_view3D.IsAvailable()):			
				break

			self.m_view3D.PushObject(floData)

			if(not self.m_view3D.IsAvailable()):			
				break

			self.m_view3D.UnlockUpdate()

			if(i32ObjectCount == 0):
				self.m_view3D.ZoomFit()

			break

# 메인 함수 // Main function
def main():

	# CResult 객체 선언 // Declare the CRessult object
	er = CResult(EResult.UnknownError)

	# 3D 뷰 선언 // Declare the 3D view
	view3D = CGUIView3D()

	# PhoXi 카메라 선언 // Declare the PhoXi camera
	camPhoXi = CDeviceCameraPhoXi()

	while True:
		
		strInput = ""
		bAutoDetect = False
		i32SelectDevice = -1
		strConnection = ""
		
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

			print("Incorrect input. Please select again.\n\n")

		print("")

		if(bAutoDetect):
			listSerialNumbers = List[String]()

			# 연결되어 있는 카메라의 시리얼 번호를 가져온다. // Get serial numbers of connected cameras
			er = camPhoXi.GetAutoDetectCameraSerialNumbers(listSerialNumbers)

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
		camPhoXi.RegisterDeviceEvent(eventImage)

		if(bAutoDetect):
			# 연결할 인덱스에 해당하는 카메라를 설정한다. // Set the camera corresponding to the index to be connected.
			if((er := camPhoXi.AutoDetectCamera(i32SelectDevice)).IsFail()):
				print("Failed to Select Device.\n")
		else:
			# 카메라에 연결할 시리얼 번호를 설정한다. // Set the serial number to camera
			camPhoXi.SetSerialNumber(strConnection)

		# 카메라 초기화 // Initialize the camera
		if((er := camPhoXi.Initialize()).IsFail()):
			print("Failed to initialize the camera.\n")
			break

		# 3D지 뷰 생성 // Create 3D view
		if((er := view3D.Create(0,0,1000,1000)).IsFail()):
			er = EResult.FailedToCreateObject
			print("Failed to create the 3D view.\n")
			break

		eventImage.SetView3D(view3D)

		# 카메라 Live // Live the camera
		if((er := camPhoXi.Live()).IsFail()):
			print("Failed to live the camera\n")
			break

		# 3D지 뷰가 종료될 때 까지 기다림 // Wait for the 3D view to close.
		while(view3D.IsAvailable()):
			CThreadUtilities.Sleep(1)

		break
	
	# 카메라의 초기화를 해제 // Terminate the camera
	camPhoXi.Terminate()
	# 카메라에 연결된 이벤트 객체 삭제 // Clear the object that receives events.
	camPhoXi.ClearDeviceEvents()

	# End of main function

# 에러 출력 함수 // Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()