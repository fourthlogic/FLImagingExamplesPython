# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 메인 함수 # Main function
def main():

	# CResult 객체 선언 # Declare the CRessult object
	er = CResult(EResult.UnknownError)

	# 조명 컨트롤러 ProtecPSC_CH03 선언 # Declare the ProtecPSC_CH03 Light Controller
	lightController = CDeviceLightControllerProtecPSC_CH03()

	bExit = False

	while True:

		strInput = ""

		# 컴포트 번호 설정 # Set the COM port number.
		strInput = input("Port Number: ")

		if strInput.isdigit():
			lightController.SetComPortNumber(int(strInput))

		if (er := lightController.Initialize()).IsFail():
			ErrorPrint(er, "Failed to initialize the light controller.")
			break

		while True:
			# 작업 모드를 선택합니다. # Select the operation mode.
			print("1. Live Mode")
			print("2. Strobe Mode")
			print("0. Exit")
			strInput = input("Select Number: ")

			if not strInput.isdigit():
				print("Invalid input. Try again.")
				continue
			
			i32OperationMode = int(strInput)

			i32TriggerIndex = 0

			if i32OperationMode == 0:
				bExit = True
				break

			if i32OperationMode == 1:
				lightController.SetOperationMode(CDeviceLightControllerProtecPSC_CH03.EOperationMode.Live)

				# On/Off 상태를 설정합니다. # Set the On/Off state.
				print("1. Live On\n2. Live Off")
				strInput = input("Select Number: ")

				if strInput == '1':
					lightController.EnableLiveTurnOn(True)

					# 채널 인덱스를 설정합니다. # Select the channel index.
					strInput = input("Select channel index: ")

					if strInput.isdigit():
						i32ChannelIndex = int(strInput)

						# 조명 값을 설정합니다. # Set the light value.
						strInput = input("Input light value (0 ~ 255): ")

						if strInput.isdigit():
							i32Value = int(strInput)

							lightController.SetLightValue(i32ChannelIndex, Byte(i32Value & 0xff))

				elif strInput == '2':
					lightController.EnableLiveTurnOn(False)

			elif i32OperationMode == 2:
				lightController.SetOperationMode(CDeviceLightControllerProtecPSC_CH03.EOperationMode.Strobe)

				# 트리거 인덱스를 설정합니다. # Select the trigger index.
				strInput = input("Select trigger index: ")

				if strInput.isdigit():
					i32TriggerIndex = int(strInput)

					lightController.EnableLiveTurnOn(True)

					# 채널 인덱스를 설정합니다. # Select the channel index.
					strInput = input("Select channel index: ")

					if strInput.isdigit():
						i32ChannelIndex = int(strInput)

						# 스트로브 값을 설정합니다. # Set the strobe value.
						strInput = input("Input strobe value (0 ~ 4000us): ")

						if strInput.isdigit():
							i32StrobeValue = int(strInput)
							
							lightController.SetStrobe(i32TriggerIndex, i32ChannelIndex, UInt16(i32StrobeValue & 0xffff))

			# 입력된 파라미터를 적용합니다. # Apply the configured parameters.
			if lightController.Apply(i32TriggerIndex).IsFail():
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