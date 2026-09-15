# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


class CDeviceEventProfileEx(CDeviceEventProfileBase):

	def __init__(self):
		super().__init__()
		self.RegisterOnAcquisition(CDeviceEventProfileEx.Delegate_OnAcquisition(self.OnAcquisition))
		self.m_view3D = None

	def SetView3D(self, view3D):
		self.m_view3D = view3D

	def OnAcquisition(self, deviceProfile):
		while(True):
			
			if(self.m_view3D is None):
				break

			if(not self.m_view3D.IsAvailable()):
				break

			if(not isinstance(deviceProfile, CDeviceLaserProfileSensorMechEyeBase)):
				break

			sensor = deviceProfile
			floData = CFL3DObject()

			sensor.GetAcquired3DData(floData)

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

# 메인 함수 # Main function
def main():

	# CResult 객체 선언 # Declare the CRessult object
	er = CResult(EResult.UnknownError)

	# 3D 뷰 선언 # Declare the 3D view
	view3D = CGUIView3D()

	# MechEye 프로파일 센서 선언 # Declare the MechEye profile sensor
	sensor = CDeviceLaserProfileSensorMechEye_2_6_0()

	while True:
		
		strInput = ""
		bAutoDetect = False
		i32SelectDevice = -1
		strConnection = ""
		
		# 프로파일 센서 인식 방법 선택 # Select Detection Method
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

			# 연결되어 있는 프로파일 센서의 시리얼 번호를 가져온다. # Get serial numbers of connected profile sensors
			er = sensor.GetAutoDetectSerialNumbers(listSerialNumbers)

			if(er[0].IsFail() or listSerialNumbers.Count == 0):
				er = EResult.FailedToRead
				print("Not Found Device.\n")
				break

			# 연결할 프로파일 센서를 선택한다. # Select profile sensor to be connected.
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
		eventProfile = CDeviceEventProfileEx()

		# 프로파일 센서에 이벤트 객체 설정 # Set event object on profile sensor 
		sensor.RegisterDeviceEvent(eventProfile)

		if(bAutoDetect):
			# 연결할 인덱스에 해당하는 프로파일 센서를 설정한다. # Set the profile sensor corresponding to the index to be connected.
			if((er := sensor.AutoDetect(i32SelectDevice)).IsFail()):
				print("Failed to Select Device.\n")
		else:
			# 프로파일 센서에 연결할 시리얼 번호를 설정한다. # Set the serial number to profile sensor
			sensor.SetSerialNumber(strConnection)

		# 프로파일 센서 초기화 # Initialize the profile sensor
		if((er := sensor.Initialize()).IsFail()):
			print("Failed to initialize the profile sensor.\n")
			break

		# 3D지 뷰 생성 # Create 3D view
		if((er := view3D.Create(0,0,1000,1000)).IsFail()):
			er = EResult.FailedToCreateObject
			print("Failed to create the 3D view.\n")
			break

		eventProfile.SetView3D(view3D)

		# 프로파일 센서 Start # Start the profile sensor
		if((er := sensor.Start()).IsFail()):
			print("Failed to start the profile sensor\n")
			break
            
        # 프로파일 센서에 소프트웨어 트리거를 발생합니다. # Triggers the profile sensor using a software trigger.
		if((er := sensor.Trigger()).IsFail()):
			print("Failed to trigger the profile sensor\n")
			break

		# 3D지 뷰가 종료될 때 까지 기다림 # Wait for the 3D view to close.
		while(view3D.IsAvailable()):
			CThreadUtilities.Sleep(1)

		break
	
	# 프로파일 센서의 초기화를 해제 # Terminate the profile sensor
	sensor.Terminate()
	# 프로파일 센서에 연결된 이벤트 객체 삭제 # Clear the object that receives events.
	sensor.ClearDeviceEvents()

	# End of main function

# 에러 출력 함수 # Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()