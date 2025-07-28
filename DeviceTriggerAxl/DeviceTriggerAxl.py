# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 메인 함수 // Main function
def main():

	# Axl Trigger 장치를 선언 // Declare Axl Trigger device
	devTrigger = CDeviceTriggerAxl()

	while True:
		
		# 장치의 모듈 인덱스를 입력합니다. // Enter the module index of the device.
		strInput = input("Enter Module index: ")
		i32ModuleIndex = int(strInput)

		# 장치의 모듈 인덱스를 설정합니다. // Sets the module index for the device.
		if((res := devTrigger.SetModuleIndex(i32ModuleIndex)).IsFail()):
			ErrorPrint(res, "Failed to set module index.")
			break

		# Trigger 장치를 초기화 합니다. // Initialize the Trigger device.
		if((res := devTrigger.Initialize()).IsFail()):
			ErrorPrint(res, "Failed to initialize the device.")
			break

		# 트리거 채널을 입력합니다. // Enter the trigger channel.
		i32Channel = 0

		while True:
			print("")
			strInput = input(f"Enter trigger channel(0 ~ {devTrigger.GetTriggerChannelCount() - 1}):")
			i32Channel = int(strInput)

			if i32Channel < 0 or i32Channel >= devTrigger.GetTriggerChannelCount():
				print("Incorrect input. Please enter again.\n")
			else:
				break

		# 엔코더 소스를 입력합니다. // Enter the encoder source.
		eEncoderSource = CDeviceTriggerAxl.EEncoderSource.ABPhase

		while True:
			print("")
			print("Encoder Source")
			print("1. AB Phase")
			print("2. Z Phase")
			strInput = input("Select: ")
			i32Select = int(strInput)

			if i32Select == 1:
				eEncoderSource = CDeviceTriggerAxl.EEncoderSource.ABPhase
				break
			elif i32Select == 2:
				eEncoderSource = CDeviceTriggerAxl.EEncoderSource.ZPhase
				break

			print("Incorrect input. Please select again.\n")

		# 엔코더 소스를 설정합니다. // Sets the encoder source.
		if((res := devTrigger.SetEncoderSource(i32Channel, eEncoderSource)).IsFail()):
			ErrorPrint(res, "Failed to set encoder source.")
			break


		# 엔코더 방식을 입력합니다. // Enter the encoder method.
		eEncoderMethod = CDeviceTriggerAxl.EEncoderMethod.UpDownSqr1

		while True:
			print("")
			print("Encoder Method")
			print("1. Up/Down Square 1")
			print("2. Up/Down Square 2")
			print("3. AB Phase Square 1")
			print("4. AB Phase Square 2")
			print("5. AB Phase Square 4")
			print("6. Pulse/Direction Square 1")
			print("7. Pulse/Direction Square 2")
			strInput = input("Select: ")
			i32Select = int(strInput)

			if i32Select == 1:
				eEncoderMethod = CDeviceTriggerAxl.EEncoderMethod.UpDownSqr1;
				break;
			elif i32Select == 2:
				eEncoderMethod = CDeviceTriggerAxl.EEncoderMethod.UpDownSqr2;
				break;
			elif i32Select == 3:
				eEncoderMethod = CDeviceTriggerAxl.EEncoderMethod.ABPhaseSqr1;
				break;
			elif i32Select == 4:
				eEncoderMethod = CDeviceTriggerAxl.EEncoderMethod.ABPhaseSqr2;
				break;
			elif i32Select == 5:
				eEncoderMethod = CDeviceTriggerAxl.EEncoderMethod.ABPhaseSqr4;
				break;
			elif i32Select == 6:
				eEncoderMethod = CDeviceTriggerAxl.EEncoderMethod.PulseDirSqr1;
				break;
			elif i32Select == 7:
				eEncoderMethod = CDeviceTriggerAxl.EEncoderMethod.PulseDirSqr2;
				break;

			print("Incorrect input. Please select again.\n");

		# 엔코더 방식을 설정합니다. // Sets the encoder method.
		if((res := devTrigger.SetEncoderMethod(i32Channel, eEncoderMethod)).IsFail()):
			ErrorPrint(res, "Failed to set encoder method.");
			break;

		# 트리거 모드를 설정합니다. // Sets the trigger mode.
		if((res := devTrigger.SetTriggerMode(i32Channel, CDeviceTriggerAxl.ETriggerMode.Position)).IsFail()):
			ErrorPrint(res, "Failed to set trigger mode.");
			break;

		while True:

			# 트리거를 비활성화 합니다. // Disable the trigger.
			if((res := devTrigger.SetTriggerEnable(i32Channel, False)).IsFail()):
				ErrorPrint(res, "Failed to set trigger enable.");
				break;

			# 엔코더 포지션을 0 으로 설정합니다. // Set the encoder position to 0.
			if((res := devTrigger.SetEncoderPosition(i32Channel, 0)).IsFail()):
				ErrorPrint(res, "Failed to set encoder position.");
				break;

			# 포지션 값을 입력합니다. // Enter a position value.
			print("");
			strInput = input("Enter trigger position(10, 20, 30, ...): ")

			# 포지션 값을 담기위해 List 생성 // Create List to hold position values
			listPosition = List[Double]()

			# 입력 받은 문자열을 ',' 으로 구분하여 double 값으로 변환합니다. // Separate the input string with ',' and convert it to a double value.
			arrStrInput = strInput.split(',')

			for item in arrStrInput:
				if item == "\n":
					break

				listPosition.Add(float(item));

			# 트리거 포지션을 설정합니다. // Sets the trigger position.
			if((res := devTrigger.SetTriggerPosition(i32Channel, listPosition)).IsFail()):
				ErrorPrint(res, "Failed to set trigger position.");
				break;

			# 트리거를 활성화 합니다. // Enables the trigger.
			if((res := devTrigger.SetTriggerEnable(i32Channel, True)).IsFail()):
				ErrorPrint(res, "Failed to set trigger enable.");
				break;

			print("\n");
			print("0. Reset the trigger position\n");
			print("Other. Exit\n");
			strInput = input("Enter: ");

			if strInput != "0":
				break;

		break
	
	# Trigger 장치의 초기화를 해제합니다. // Terminate the Trigger device.
	devTrigger.Terminate();

	# End of main function

# 에러 출력 함수 // Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()