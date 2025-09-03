# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 메인 함수 # Main function
def main():

	# CResult 객체 선언 # Declare the CRessult object
	er = CResult(EResult.UnknownError)

	# 조명 컨트롤러 WordopPD5_6024 선언 # Declare the WordopPD5_6024 Light Controller
	lightController = CDeviceLightControllerWordopPD5_6024()

	bExit = False

	while True:

		strInput = ""
		i32ConnectionType = 0
		
		while True:
			# 조명 컨트롤러 연결 방식을 선택합니다. # Select the connection method for the light controller.
			print("1. RS232C")
			print("2. TCP Server")
			print("3. TCP Client")
			print("4. UDP")
			print("0. Exit")
			strInput = input("Connection Type: ")

			bSelected = True

			if strInput.isdigit():
				i32ConnectionType = int(strInput)

				if i32ConnectionType < 0 or i32ConnectionType > 4:
					bSelected = False

			else:
				bSelected = False

			if bSelected:
				break

			print("Incorrect input. Please select again.")

		if i32ConnectionType == 0:
			break

		eConnectionMethod = CDeviceLightControllerWordopPD5_6024.EConnectionMethod.RS232C

		if i32ConnectionType == 2:
			eConnectionMethod = CDeviceLightControllerWordopPD5_6024.EConnectionMethod.TCPServer
		elif i32ConnectionType == 3:
			eConnectionMethod = CDeviceLightControllerWordopPD5_6024.EConnectionMethod.TCPClient
		elif i32ConnectionType == 4:
			eConnectionMethod = CDeviceLightControllerWordopPD5_6024.EConnectionMethod.UDP

		# 연결 방식을 설정합니다. # Set the connection method.
		lightController.SetConnectionMethod(eConnectionMethod)

		if i32ConnectionType == 1:
			# 컴포트 번호 설정 # Set the COM port number.
			strInput = input("Port Number: ")
	
			if strInput.isdigit():
				lightController.SetConnectionComPortNumber(int(strInput))
		else:
			strIPAddress = input("Input IP Address: ")

			strInput = input("Port Number: ")

			if strInput.isdigit():
				# IP 주소, Port 설정 # Set the IP address and port.
				lightController.SetConnectionIPAddress(strIPAddress)
				lightController.SetConnectionComPortNumber(int(strInput))

		if (er := lightController.Initialize()).IsFail():
			ErrorPrint(er, "Failed to initialize the light controller.")
			break

		i32ChannelCount  = 0

		while True:
			# 채널 갯수를 선택합니다. # Select the number of channels.
			print("1. Channel 4")
			print("2. Channel 8")
			print("0. Exit")
			strInput = input("Input Channel Count: ")

			if strInput.isdigit():
				i32ChannelCount = int(strInput)

				if i32ChannelCount != 0 and i32ChannelCount != 1 and i32ChannelCount != 2:
					print("Incorrect input. Please select again.")
					continue

			if i32ChannelCount == 0:
				bExit = True

			break

		if bExit:
			break

		eLightChannel = CDeviceLightControllerWordopPD5_6024.ELightChannel.Port_4

		if i32ChannelCount == 2 :
			eLightChannel = CDeviceLightControllerWordopPD5_6024.ELightChannel.Port_8

		# 채널 갯수를 설정합니다. # Set the number of channels.
		lightController.SetLightChannel(eLightChannel)

		i32CommunicationType = 0

		while True:
			# 통신 방식을 선택합니다. # Select the communication method.
			print("1. ASCII Code")
			print("2. Hexadecimal")
			print("0. Exit")
			strInput = input("Input Communication Type: ")

			if strInput.isdigit():
				i32CommunicationType = int(strInput)

				if i32CommunicationType != 0 and i32CommunicationType != 1 and i32CommunicationType != 2:
					print("Incorrect input. Please select again.")
					continue

			if i32CommunicationType == 0:
				bExit = True

			break

		if bExit:
			break

		eCommType = CDeviceLightControllerWordopPD5_6024.ECommunicationType.ASCIICode
		
		if i32CommunicationType == 2:
			eCommType = CDeviceLightControllerWordopPD5_6024.ECommunicationType.Hexadecimal

		# 통신 방식을 설정합니다. # Set the communication type.
		lightController.SetCommunicationType(eCommType)

		while True:
			# 작업 모드를 선택합니다. # Select the operation mode.
			print("1. Light On/Off")
			print("2. Light Value")
			print("3. Strobe Time")
			print("4. Trigger Method")
			print("0. Exit")
			strInput = input("Select Number: ")

			if not strInput.isdigit():
				print("Invalid input. Try again.")
				continue
			
			i32OperationMode = int(strInput)

			i32TriggerIndex = 0

			if i32OperationMode == 0:
				bExit = True

			if i32OperationMode == 4:
				i32TriggerMethod = 0

				while True:
					# 트리거 방식을 선택합니다. # Select the trigger method.
					print("1. Low Level")
					print("2. High Level")
					print("3. Falling Edge")
					print("4. Rising Edge")
					print("0. Exit")
					strInput = input("Input Trigger Method: ")

					if strInput.isdigit():
						i32TriggerMethod = int(strInput)

						if not (i32TriggerMethod >= 0 and i32TriggerMethod <= 4):
							print("Incorrect input. Please select again.")
							continue

					if i32TriggerMethod == 0:
						bExit = True

					break

				if bExit:
					break

				eTriggerMethod = CDeviceLightControllerWordopPD5_6024.ETriggerMethod.LowLevel

				if triggerMethod == 2:
					eTriggerMethod = CDeviceLightControllerWordopPD5_6024.ETriggerMethod.HighLevel
				elif triggerMethod == 3:
					eTriggerMethod = CDeviceLightControllerWordopPD5_6024.ETriggerMethod.FallingEdge
				elif triggerMethod == 4:
					eTriggerMethod = CDeviceLightControllerWordopPD5_6024.ETriggerMethod.RisingEdge

				lightController.SetTriggerMethod(eTriggerMethod)

			else:
				strInput = input("Select Channel: ")

				if strInput.isdigit():
					i32Channel = int(strInput)

					if i32OperationMode == 1:
						print("1. On\n2. Off")
						strInput = input("Enter On/Off: ")

						if strInput == '1':
							lightController.SetChannelState(i32Channel, True)
						elif strInput == '2':
							lightController.SetChannelState(i32Channel, False)

					elif i32OperationMode == 2:
						strInput = input("Input Light Value (0 ~ 255): ")

						if strInput.isdigit():
							i32LightValue = int(strInput)
							lightController.SetLightValue(i32Channel, i32LightValue & 0xff)

					elif i32OperationMode == 3:
						strInput = input("Input Strobe Time (1 ~ 999 ms): ")

						if strInput.isdigit():
							i32LightValue = int(strInput)
							lightController.SetLightValue(i32Channel, UInt16(i32LightValue & 0xffff))


			# 입력된 파라미터를 적용합니다. # Apply the configured parameters.
			if (er := lightController.Apply()).IsFail():
				print("Failed to apply the light controller.")
				break

		if bExit:
			break

		break

	# End of main function

# 에러 출력 함수 # Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()