# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()

# 카메라에서 데이터 취득 이벤트를 받기 위해 CDeviceEventImageBase 를 상속 받아서 구현
# Implemented by inheriting CDeviceEventImageBase to receive data acquisition events from the camera
class CDeviceEventImageEx(CDeviceEventImageBase):

	def __init__(self):
		super().__init__()
		self.RegisterOnAcquisition(CDeviceEventImageEx.Delegate_OnAcquisition(self.OnAcquisition))
		self.m_view3D = None

	# 취득한 데이터를 표시할 3D 뷰를 설정하는 함수
	# Function to set the 3D view for displaying the acquired data
	def SetView3D(self, view3D):
		self.m_view3D = view3D

	# 카메라에서 데이터 취득 시 호출 되는 함수
	# Function called when data is acquired from the camera
	def OnAcquisition(self, deviceImage):
		while(True):
			
			if(self.m_view3D is None):
				break

			# 3D 뷰의 유효성을 확인한다.
			# Check whether the 3D view is valid
			if(not self.m_view3D.IsAvailable()):
				break

			if(not isinstance(deviceImage, CDeviceCameraZivid_2_17_1)):
				break

			camera = deviceImage

			# 데이터 객체 선언
			# Declare a data object
			floData = CFL3DObject()

			# 카메라에서 취득 한 데이터를 얻어온다.
			# Retrieve the acquired 3D data from the camera
			camera.GetAcquired3DData(floData)

			if(floData is None):
				break

			# 3D 뷰의 업데이트를 막습니다.
			# Lock the 3D view to prevent updates
			self.m_view3D.LockUpdate()

			# 3D 뷰의 유효성을 확인한다.
			# Check whether the 3D view is valid
			if(not self.m_view3D.IsAvailable()):			
				break

			# 3D 뷰의 객체 개수를 얻어옵니다.
			# Get the number of objects currently in the 3D view
			i32ObjectCount = self.m_view3D.GetObjectCount()

			# 3D 뷰의 객체들을 모두 클리어합니다.
			# Clear all objects in the 3D view
			self.m_view3D.ClearObjects()

			# 3D 뷰의 유효성을 확인한다.
			# Check whether the 3D view is valid
			if(not self.m_view3D.IsAvailable()):			
				break

			# 3D 뷰에 객체를 추가합니다.
			# Add the acquired 3D object to the view
			self.m_view3D.PushObject(floData)

			# 3D 뷰의 유효성을 확인한다.
			# Check whether the 3D view is valid
			if(not self.m_view3D.IsAvailable()):			
				break

			# 3D 뷰의 업데이트 막은 것을 해제합니다.
			# Unlock the 3D view to allow updates again
			self.m_view3D.UnlockUpdate()

			# 3D 뷰의 스케일을 조정합니다.
			# Adjust the 3D view scale if this is the first object
			if(i32ObjectCount == 0):
				self.m_view3D.ZoomFit()

			break

# 메인 함수 # Main function
def main():

	# CResult 객체 선언 # Declare the CRessult object
	er = CResult(EResult.UnknownError)

	# 3D 뷰 선언 # Declare the 3D view
	view3D = CGUIView3D()

	# Zivid 카메라 선언 # Declare the Zivid camera
	camZivid = CDeviceCameraZivid_2_17_1()

	while True:
		
		strInput = ""
		bAutoDetect = False
		i32SelectDevice = -1
		strConnection = ""
		
		# Cam file 의 전체 경로를 입력 # Enter the full path of Cam file.
		strCamFilePath = input("Enter camfile full path (e.g. C:/Sample.yml): ")

		camZivid.SetCamFilePath(strCamFilePath)

		# 카메라 인식 방법 선택 # Select Detection Method
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

			# 연결되어 있는 카메라의 시리얼 번호를 가져온다. # Get serial numbers of connected cameras
			er, listSerialNumbers = camZivid.GetAutoDetectCameraSerialNumbers(listSerialNumbers)

			if(er[0].IsFail() or listSerialNumbers.Count == 0):
				er = EResult.FailedToRead
				print("Not Found Device.\n")
				break

			# 연결할 카메라를 선택한다. # Select camera to be connected.
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
			# 시리얼 번호를 입력 받는다. # Enter the serial number.
			strConnection = input("Input Serial Number: ")

		# 이벤트를 받을 객체 선언 # Declare the object that receives events
		eventImage = CDeviceEventImageEx()

		# 카메라에 이벤트 객체 설정 # Set event object on Camera 
		camZivid.RegisterDeviceEvent(eventImage)

		if(bAutoDetect):
			# 연결할 인덱스에 해당하는 카메라를 설정한다. # Set the camera corresponding to the index to be connected.
			if((er := camZivid.AutoDetectCamera(i32SelectDevice)).IsFail()):
				print("Failed to Select Device.\n")
		else:
			# 카메라에 연결할 시리얼 번호를 설정한다. # Set the serial number to camera
			camZivid.SetSerialNumber(strConnection)

		# 카메라 초기화 # Initialize the camera
		if((er := camZivid.Initialize()).IsFail()):
			print("Failed to initialize the camera.\n")
			break

		# 3D지 뷰 생성 # Create 3D view
		if((er := view3D.Create(0,0,1000,1000)).IsFail()):
			er = EResult.FailedToCreateObject
			print("Failed to create the 3D view.\n")
			break

		eventImage.SetView3D(view3D)

		# 카메라 Live # Live the camera
		if((er := camZivid.Live()).IsFail()):
			print("Failed to live the camera\n")
			break

		# 3D지 뷰가 종료될 때 까지 기다림 # Wait for the 3D view to close.
		while(view3D.IsAvailable()):
			CThreadUtilities.Sleep(1)

		break
	
	# 카메라의 초기화를 해제 # Terminate the camera
	camZivid.Terminate()
	# 카메라에 연결된 이벤트 객체 삭제 # Clear the object that receives events.
	camZivid.ClearDeviceEvents()

	# End of main function

# 에러 출력 함수 # Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()