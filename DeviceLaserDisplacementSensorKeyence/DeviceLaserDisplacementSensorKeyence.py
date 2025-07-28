# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 메인 함수 // Main function
def main():

	# Keyence 레이저 변위 센서 장치를 선언 // Declare keyence laser displacement sensor device
	devLaserDisplacement = CDeviceLaserDisplacementSensorKeyence()

	while True:
		
		# 컴포트 번호를 입력합니다. // Enter the com port number.
		strInput = input("Enter com port number: ")
		i32ComPortNumber = int(strInput)

		devLaserDisplacement.SetComPortNumber(i32ComPortNumber)

		# 보드 레이트를 선택합니다. // Select the baud rate.
		while True:
			print("")
			print("1. 9600")
			print("2. 19200")
			print("3. 38400")
			print("4. 57600")
			print("5. 115200")
			strInput = input("Select baud rate: ")
			i32Select = int(strInput)
			
			i32BaudRate = -1

			if i32Select == 1:
				i32BaudRate = 9600
			elif i32Select == 2:
				i32BaudRate = 19200
			elif i32Select == 3:
				i32BaudRate = 38400
			elif i32Select == 4:
				i32BaudRate = 57600
			elif i32Select == 5:
				i32BaudRate = 115200

			if i32BaudRate != -1:
				devLaserDisplacement.SetBaudRate(i32BaudRate)
				break

			print("Incorrect input. Please select again.\n")

		# 패리티를 선택합니다. // Select the parity.
		while True:
			print("")
			print("1. None")
			print("2. Even")
			print("3. Odd")
			strInput = input("Select parity: ")
			i32Select = int(strInput)

			i32Parity = -1

			if i32Select == 1:
				i32Parity = 0
			elif i32Select == 2:
				i32Parity = 1
			elif i32Select == 3:
				i32Parity = 2

			if i32Parity != -1:
				devLaserDisplacement.SetParity(i32Parity)
				break

			print("Incorrect input. Please select again.\n")

		# 레이저 변위 센서 장치를 초기화 합니다. // Initialize the laser displacement sensor device.
		if((res := devLaserDisplacement.Initialize()).IsFail()):
			ErrorPrint(res, "Failed to initialize the device.")
			break

		while True:
			# 출력 채널을 선택합니다. // Select the output channel.
			print("")
			print("1. Output channel 1")
			print("2. Output channel 2")
			print("0. Exit")
			strInput = input("Select output channel: ")
			i32Select = int(strInput)

			# 측정값을 얻어옵니다. // Retrieve the measured value
			listMeasured = List[Double]()

			if i32Select == 1:
				res = devLaserDisplacement.GetMeasuredValue(CDeviceLaserDisplacementSensorKeyence.EOutputChannel.Channel1, listMeasured)
			elif i32Select == 2:
				res = devLaserDisplacement.GetMeasuredValue(CDeviceLaserDisplacementSensorKeyence.EOutputChannel.Channel2, listMeasured)
			elif i32Select == 0:
				break
			else:
				print.Write("Incorrect input. Please select again.\n")

			if listMeasured.Count == 0:
				continue

			print(f"Output channel {i32Select} measured: {listMeasured[0]}\n")

		break
	
	# 레이저 변위 센서 장치의 초기화를 해제합니다. // Terminate the laser displacement sensor device.
	devLaserDisplacement.Terminate()

	# End of main function

# 에러 출력 함수 // Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()