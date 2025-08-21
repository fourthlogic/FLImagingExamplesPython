# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


class CDeviceEventProfileEx(CDeviceEventProfileBase):

	def __init__(self):
		super().__init__()
		self.RegisterOnAcquisition(CDeviceEventProfileEx.Delegate_OnAcquisition(self.OnAcquisition))
		self.m_fliHeight = CFLImage()
		self.m_fliLuminance = CFLImage()
		self.m_viewHeightImage = None
		self.m_viewLuminanceImage = None

	def SetViewHeightImage(self, viewHeightImage):
		self.m_viewHeightImage = viewHeightImage
		self.m_viewHeightImage.SetImagePtr(self.m_fliHeight)
		
	def SetViewLuminanceImage(self, viewHeightImage):
		self.m_viewLuminanceImage = viewHeightImage
		self.m_viewLuminanceImage.SetImagePtr(self.m_fliLuminance)

	def OnAcquisition(self, deviceImage):
		if(self.m_viewHeightImage.IsAvailable()):
			self.m_fliHeight.Lock()
			deviceImage.GetAcquiredHeightProfile(self.m_fliHeight)
			self.m_fliHeight.Unlock()

			self.m_viewHeightImage.Invalidate()

		if(self.m_viewLuminanceImage.IsAvailable()):
			self.m_fliLuminance.Lock()
			deviceImage.GetAcquiredLuminanceProfile(self.m_fliLuminance)
			self.m_fliLuminance.Unlock()

			self.m_viewLuminanceImage.Invalidate()

# 메인 함수 # Main function
def main():
	
	# CResult 객체 선언 # Declare the CRessult object
	res = CResult(EResult.UnknownError)

	# 이미지 뷰 선언 # Declare the image view
	viewHeightImage = CGUIViewImage()
	viewLuminanceImage = CGUIViewImage()

	# Laser Profile Sensor 선언 # Laser Profile Sensor Declaration
	devLaserProfile = CDeviceLaserProfileSensorKeyence()
	
	# 이벤트를 받을 객체 선언 # Declare the object that receives events
	eventProfile = CDeviceEventProfileEx()

	# 카메라에 이벤트 객체 설정 # Set event object on Camera 
	devLaserProfile.RegisterDeviceEvent(eventProfile)

	while True:
		
		strConnection = ""
		
		# IP 주소를 입력 받습니다. # Enter the IP address.
		while True:

			strConnection = input("Input IP Address: ")

			if (res := devLaserProfile.SetConnectionIPAddress(strConnection)).IsOK():
				break

			ErrorPrint(res, "Failed to set IP Address.\n")
			
		# 포트 번호를 입력 받습니다. # Enter the port number.
		while True:

			strConnection = input("Input Port Number: ")
			u16Port = int(strConnection)

			if (res := devLaserProfile.SetPortNumber(u16Port)).IsOK():
				break

			ErrorPrint(res, "Failed to set port number.\n")
			
		# 고속 통신용 포트 번호를 입력 받습니다. # Enter the port number for high-speed communication.
		while True:

			strConnection = input("Input High-speed Port Number: ")
			u16Port = int(strConnection)

			if (res := devLaserProfile.SetHighSpeedPort(u16Port)).IsOK():
				break

			ErrorPrint(res, "Failed to set high-speed port number.\n")
			
		# Profile 수를 입력 받습니다. # Enter the profile number.
		while True:

			strConnection = input("Input Profile Count: ")
			i32ProfileCount = int(strConnection)

			if (res := devLaserProfile.SetProfileCount(i32ProfileCount)).IsOK():
				break

			ErrorPrint(res, "Failed to set profile count.\n")


		# 프로파일 센서를 초기화 합니다. # Initialize the profile sensor.
		if((res := devLaserProfile.Initialize()).IsFail()):
			ErrorPrint(res, "Failed to initialize device.\n")
			break
		
		# 높이 이미지 뷰 생성 # Create height image view
		if((res := viewHeightImage.Create(400, 0, 812, 384)).IsFail()):
			ErrorPrint(res, "Failed to create the image view.\n")
			break
		
		# 휘도 이미지 뷰 생성 # Create luminance image view
		if((res := viewLuminanceImage.Create(812, 0, 1224, 384)).IsFail()):
			ErrorPrint(res, "Failed to create the image view.\n")
			break
		
		# 뷰 시점 동기화 # Synchronize view points
		if (res := viewHeightImage.SynchronizePointOfView(viewLuminanceImage)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize view.\n")
			break

		# 윈도우 위치 동기화 # Synchronize window positions
		if (res := viewHeightImage.SynchronizeWindow(viewLuminanceImage)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize window.\n")
			break

		# 이벤트 객체에 View를 설정합니다. # Set a View on the event object.
		eventProfile.SetViewHeightImage(viewHeightImage)
		eventProfile.SetViewLuminanceImage(viewLuminanceImage)
		
		# 활성 프로그램 No. 를 전환합니다. # Change active program number.
		devLaserProfile.SetProgramNumber(0)
		# 설정 함수의 적용 범위를 설정합니다. # Set the setting depth of the setting function.
		devLaserProfile.SetSettingDepth(CDeviceLaserProfileSensorKeyence.ESettingDepth.Running)

		# 파라미터 설정 함수 - Keyence 사의 LJ X Navigator 설치 후 C:\Program Files\KEYENCE\LJ-X Navigator\lib\Manual 경로의 매뉴얼 11.3 참고
		# Parameter setting function - Refer to section 11.3 of the manual located at C:\Program Files\KEYENCE\LJ-X Navigator\lib\Manual after installing Keyence's LJ-X Navigator.
		
		# Trigger 모드 설정(0 : 연속 트리거, 1 : 외부 트리거, 2 : 인코더 트리거)
		# Trigger mode setting (0: continuous trigger, 1: external trigger, 2: encoder trigger)
		i64DataSize = 4
		arrData = [0] * 4
		arrData[0] = 0

		devLaserProfile.SetTriggerSetting(CDeviceLaserProfileSensorKeyence.ETriggerSettingItem.TriggerMode, bytes(arrData))
		
		# 배치 측정 설정(0 : 배치 OFF, 1 : 배치 ON)
		# Batch measurement settings (0: batch OFF, 1: batch ON)
		i64DataSize = 4
		arrData = [0] * 4
		arrData[0] = 0

		devLaserProfile.SetTriggerSetting(CDeviceLaserProfileSensorKeyence.ETriggerSettingItem.BatchMeasurement, bytes(arrData))
		
		# 휘도 출력 설정(0 : 높이 데이터만, 1 : 높이 + 휘도 데이터)
		# Luminance output settings (0: height data only, 1: height + luminance data)
		i64DataSize = 4
		arrData = [0] * 4
		arrData[0] = 1

		devLaserProfile.SetCommonSetting(CDeviceLaserProfileSensorKeyence.ECommonSettingItem.LuminanceOutput, bytes(arrData))

		# 프로파일 센서를 Start 합니다. # Start the profile sensor.
		if((res := devLaserProfile.Start()).IsFail()):
			ErrorPrint(res, "Failed to start the profile sensor.\n")
			break
		
		CThreadUtilities.Sleep(100)
		viewHeightImage.ZoomFit()
		
		# 각각의 image View 에서 0번 레이어 가져오기 # Get Layer 0 from each image view 
		layerHeight = viewHeightImage.GetLayer(0)
		layerLuminance = viewLuminanceImage.GetLayer(0)

		# 각 레이어 캔버스에 텍스트 그리기 # Draw text to each Layer Canvas
		layerHeight.DrawTextCanvas(CFLPoint[Int32](0, 0), "Height", EColor.YELLOW, EColor.BLACK, 30)
		layerLuminance.DrawTextCanvas(CFLPoint[Int32](0, 0), "Luminance", EColor.YELLOW, EColor.BLACK, 30)

		# 이미지 뷰가 종료될 때 까지 기다림 # Wait for the image view to close.
		while(viewHeightImage.IsAvailable()):
			CThreadUtilities.Sleep(1)

		break
	
	# 프로파일 센서의 초기화를 해제합니다. # Uninitialize the profile sensor.
	devLaserProfile.Terminate()
	# 프로파일 센서에 연결된 이벤트 객체 삭제 # Clear the object that receives events.
	devLaserProfile.ClearDeviceEvents()

	# End of main function

# 에러 출력 함수 # Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()