# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()

# 프로파일 데이터 취득 이벤트를 받기 위해 CDeviceEventProfileBase 를 상속 받아서 구현
# Inherit and implement CDeviceEventProfileBase to receive profile data acquisition events
class CDeviceEventProfileEx(CDeviceEventProfileBase):

	# CDeviceEventProfileEx 생성자 # CDeviceEventProfileEx Constructor
	def __init__(self):
		super().__init__()
		self.RegisterOnAcquisition(CDeviceEventProfileEx.Delegate_OnAcquisition(self.OnAcquisition))
		self.m_fliImage = CFLImage()
		self.m_viewImage = None
		self.m_view3D = None

	# 취득한 이미지를 표시할 이미지 뷰를 설정하는 함수
	# Function to set the image view to display the acquired image
	def SetViewImage(self, viewImage):
		self.m_viewImage = viewImage
		self.m_viewImage.SetImagePtr(self.m_fliImage)
	
	# 취득한 3D 데이터를 표시할 3D 뷰를 설정하는 함수
	# Function to set the 3D view to display the acquired 3D data
	def SetView3D(self, view3D):
		self.m_view3D = view3D

	# 카메라에서 이미지 취득 시 호출 되는 함수 # Function called when acquiring an image from the camera
	def OnAcquisition(self, deviceProfile):
		while True:
			
			if(self.m_viewImage is None):
				break

			if(self.m_view3D is None):
				break

			if(not isinstance(deviceProfile, CDeviceLaserProfileSensorLMI)):
				break

			deviceProfileLMI = deviceProfile

			# 스캔 모드를 얻어옵니다. # Get the scan mode.
			eScanMode = CDeviceLaserProfileSensorLMI.EScanMode.Image
			res, eScanMode = deviceProfileLMI.GetScanMode(eScanMode)

			if(eScanMode == CDeviceLaserProfileSensorLMI.EScanMode.Image):

				# 이미지 뷰의 유효성을 확인합니다. # Validate the image view.
				if(not self.m_viewImage.IsAvailable()):
					break

				if(self.m_fliImage is None):
					break

				# 기존 이미지 정보를 얻어옵니다. # Retrieve the existing image information.
				i64Width = self.m_fliImage.GetWidth()
				i64Height = self.m_fliImage.GetHeight()
				i32SelectedPageIndex = self.m_fliImage.GetSelectedPageIndex()
				bZoomFit = False

				self.m_fliImage.Lock()

				# 취득 한 이미지를 얻어온다. #Retrieve the acquired image.
				deviceProfileLMI.GetAcquiredImage(self.m_fliImage)

				# 기존 선택된 페이지 인덱스로 선택합니다. # Select the page using the existing selected page index.
				self.m_fliImage.SelectPage(i32SelectedPageIndex)

				# 기존 이미지 정보와 비교합니다. # Compare with the existing image information.
				if(i64Width != self.m_fliImage.GetWidth() or i64Height != self.m_fliImage.GetHeight()):
					bZoomFit = True

				self.m_fliImage.Unlock()

				# 뷰를 Zoom fit 합니다. # Fit the view to the window.
				if(bZoomFit):
					self.m_viewImage.ZoomFit()

				# 이미지 뷰를 재갱신 한다. # Invalidate the image view.
				self.m_viewImage.Invalidate()

			elif(eScanMode == CDeviceLaserProfileSensorLMI.EScanMode.Profile):
				
				# 프로파일 데이터를 얻어올 리스트를 선언합니다. # Declare an list to store profile data.
				listProfile = List[List[List[Double]]]()

				# 취득한 프로파일 데이터를 얻어온다. # Retrieve the acquired profile data.
				res = deviceProfileLMI.GetAcquiredProfile(listProfile)

				# 프로파일 데이터를 표시합니다. # Display the profile data.
				lineProfile = []

				for i in range(len(listProfile)):
					if i != 0:
						lineProfile.append("\n")

					lineProfile.append("[")

					for j in range(len(listProfile[i])):
						if j != 0:
							lineProfile.append("\n")

						x = listProfile[i][j][CDeviceLaserProfileSensorLMI.EProfileDataElement.PositionX.value__]
						z = listProfile[i][j][CDeviceLaserProfileSensorLMI.EProfileDataElement.PositionZ.value__]
						intensity = listProfile[i][j][CDeviceLaserProfileSensorLMI.EProfileDataElement.Intensity.value__]

						lineProfile.append(f"({x}, {z}, {intensity})")

					lineProfile.append("]")

				print("".join(lineProfile))

			elif(eScanMode == CDeviceLaserProfileSensorLMI.EScanMode.Surface):
				
				# 3D 뷰의 유효성을 확인합니다. # Validate the 3D view.
				if(not self.m_view3D.IsAvailable()):
					break

				# 3D 데이터를 얻어올 객체를 선언합니다. # Declare an object to store 3D data.
				flogData = CFL3DObjectGroup()

				# 취득한 3D 데이터를 얻어온다. # Retrieve the acquired 3D data.
				deviceProfileLMI.GetAcquired3DData(flogData)

				# 3D 뷰의 유효성을 확인합니다. # Validate the 3D view.
				if(not self.m_view3D.IsAvailable()):
					break

				# 3D 데이터를 3D 뷰에 표시합니다. # Display the 3D data in the 3D view.
				self.m_view3D.LockUpdate()

				i32ObjectCount = self.m_view3D.GetObjectCount()

				self.m_view3D.ClearObjects()

				for i in range(flogData.GetObjectCount()):
					self.m_view3D.PushObject(flogData.GetObjectByIndex(i))

				self.m_view3D.UnlockUpdate()

				if(i32ObjectCount == 0):
					self.m_view3D.ZoomFit()



# 메인 함수 # Main function
def main():
	
	# CResult 객체 선언 # Declare the CRessult object
	res = CResult(EResult.UnknownError)

	# 이미지 뷰 선언 # Declare image view
	viewImage = CGUIViewImage()

	# 3D 뷰 선언 # Declare 3D view
	view3D = CGUIView3D()

	# Laser Profile Sensor 선언 # Laser Profile Sensor Declaration
	devLaserProfile = CDeviceLaserProfileSensorLMI()
	
	# 이벤트를 받을 객체 선언 # Declare the object that receives events
	eventProfile = CDeviceEventProfileEx()

	# 카메라에 이벤트 객체 설정 # Set event object on Camera 
	devLaserProfile.RegisterDeviceEvent(eventProfile)

	while True:
		
		strConnection = ""
		
		# IP 주소를 입력 받습니다. # Enter the IP address.
		while True:

			strConnection = input("Input IP Address: ")

			if (res := devLaserProfile.SetIPAddress(strConnection)).IsOK():
				break

			ErrorPrint(res, "Failed to set IP Address.\n")
			
		# 포트 번호를 입력 받습니다. # Enter the port number.
		while True:

			strConnection = input("Input Port Number: ")
			u16Port = int(strConnection)

			if (res := devLaserProfile.SetPortNumber(u16Port)).IsOK():
				break

			ErrorPrint(res, "Failed to set port number.\n")
			
		# 프로파일 센서를 초기화 합니다. # Initialize the profile sensor.
		if((res := devLaserProfile.Initialize()).IsFail()):
			ErrorPrint(res, "Failed to initialize device.\n")
			break
		
		# 이미지 뷰 생성 # Create image view
		if((res := viewImage.Create(400, 0, 812, 384)).IsFail()):
			ErrorPrint(res, "Failed to create the image view.\n")
			break
		
		# 3D 뷰 생성 # Create 3D view
		if((res := view3D.Create(812, 0, 1224, 384)).IsFail()):
			ErrorPrint(res, "Failed to create the 3D view.\n")
			break
		
		# 윈도우 위치 동기화 # Synchronize window positions
		if (res := viewImage.SynchronizeWindow(view3D)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize window.\n")
			break

		# 이벤트 객체에 View를 설정합니다. # Set a View on the event object.
		eventProfile.SetViewImage(viewImage)
		eventProfile.SetView3D(view3D)

		# 서피스 컬러라이제이션 기능을 설정합니다. # Set the surface colorization feature.
		devLaserProfile.EnableSurfaceColorization(True)
		devLaserProfile.SetSurfaceColorizationRange(-5, 5)
		
		# 프로파일 센서를 Start 합니다. # Start the profile sensor.
		if((res := devLaserProfile.Start()).IsFail()):
			ErrorPrint(res, "Failed to start the profile sensor.\n")
			break

		# 이미지 뷰가 종료될 때 까지 기다림 # Wait for the image view to close.
		while(viewImage.IsAvailable()):
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