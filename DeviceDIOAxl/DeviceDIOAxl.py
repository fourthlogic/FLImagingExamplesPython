# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()

# 메인 함수 // Main function
def main():

	# CResult 객체 선언 // Declare the CRessult object
	er = CResult(EResult.UnknownError)

	devDIOAxl = CDeviceDIOAxl()

	while True:

		strInput = ""

		 # DIO 장치를 초기화합니다. // Initialize the DIO device.
		if (er := devDIOAxl.Initialize()).IsFail():
			ErrorPrint(er, "Failed to Initialize the device.")
			break

		while True:
			# 사용할 기능을 선택합니다. // Select the features you want to use.
			print("1. Read input")
			print("2. Read output")
			print("3. Write input")
			print("4. Write output")
			strInput = input("Select: ")

			if strInput.isdigit():
				i32Select = int(strInput)

				if i32Select == 1 or i32Select == 2:
					# Bit 를 입력 받습니다. // Enter Bit.
					strInput = input("Bit input: ")

					if(strInput.isdigit()):
						i32Bit = int(strInput)

					# Bit 의 상태를 읽습니다. // Read Bit status.
					if i32Select == 1:
						bReadStatus = devDIOAxl.ReadInBit(i32Bit)
					else:
						bReadStatus = devDIOAxl.ReadOutBit(i32Bit)

					print("Read status: {0}", bReadStatus)

				elif i32Select == 3 or i32Select == 4:
					# Bit 를 입력 받습니다. // Enter Bit.
					strInput = input("Bit input: ")
										
					if strInput.isdigit():
						i32Bit = int(strInput)

					# 상태를 입력 받습니다. // Enter status.
					strInput = input("Stastus input: ")
					
					bWriteStatus = False

					if strInput != '0':
						bWriteStatus = True

					# Bit 에 상태를 기록합니다. // Write the status in Bit.
					if i32Select == 3:
						er = devDIOAxl.WriteInBit(i32Bit, bWriteStatus)
					else:
						er = devDIOAxl.WriteOutBit(i32Bit, bWriteStatus)

					if er.IsOK():
						print("Succeded to write \n")
					else:
						print("Failed to write \n")
				else:
					print("Incorrect input. Please select again.\n")
		break

	devDIOAxl.Terminate()

	# End of main function

# 에러 출력 함수 // Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()