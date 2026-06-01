# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 메인 함수 # Main function
def main():

    # CResult 객체 선언 # Declare the CRessult object
    res = CResult(EResult.UnknownError)

    # RS232C ASCII 선언 // Declare the RS232C ASCII
    rs232CASCII = CDeviceRS232CASCII()
    
    while True:
        bExit = False

        # 페시브 모드 설정 false // Set passive mode to false
        rs232CASCII.SetPassive(False)

        # 컴포트 번호를 입력합니다. // Enter the COM port number.
        i32ComPortNumber = 0

        try:
            i32ComPortNumber = int(input("Port Number: "))
        except:
            i32ComPortNumber = 0

        # 컴포트 번호 설정 // Set the COM port number.
        rs232CASCII.SetComPortNumber(i32ComPortNumber)

        i32BaudRate = 0
        bValidInput = False

        # 보드레이트를 입력합니다. // Enter the Baud Rate.
        while not bValidInput:
            print("=== Select Baud Rate ===")
            print("1. 9600")
            print("2. 19200")
            print("3. 38400")
            print("4. 57600")
            print("5. 115200")

            try:
                i32MenuSelection = int(input("Select Number: "))
            except:
                i32MenuSelection = 0

            # 선택한 번호에 따라 보드 레이트 매핑 // Map the Baud Rate according to the selected number
            if i32MenuSelection == 1:
                i32BaudRate = 9600
                bValidInput = True

            elif i32MenuSelection == 2:
                i32BaudRate = 19200
                bValidInput = True

            elif i32MenuSelection == 3:
                i32BaudRate = 38400
                bValidInput = True

            elif i32MenuSelection == 4:
                i32BaudRate = 57600
                bValidInput = True

            elif i32MenuSelection == 5:
                i32BaudRate = 115200
                bValidInput = True

            else:
                print("[Error] Invalid selection. Please try again.\n")

        # 보드 레이트 설정 // Set the Baud Rate.
        rs232CASCII.SetBaudRate(i32BaudRate)

        if (res := rs232CASCII.Initialize()).IsFail():
            ErrorPrint(res, "Failed to initialize the light controller.\n")
            break

        while True:
            # 작업 모드를 선택합니다. // Select the operation mode.
            print("1. Send")
            print("2. Recv")
            print("0. Exit")
            print()

            try:
                i32SelectMode = int(input("Select Number: "))
            except:
                i32SelectMode = -1

            print()

            if i32SelectMode == 0:
                bExit = True
                break

            elif i32SelectMode == 1:
                # 텍스트를 입력합니다. // Input text.
                strInput = input("Input Text: ")

                # 개행 제거 // Remove CR/LF
                strInput = strInput.rstrip("\r\n")

                # ASCII 인코딩 // ASCII encoding
                arrData = bytearray(strInput.encode("ascii"))

                # 데이터 전송 // Send data
                rs232CASCII.Send(arrData)

            elif i32SelectMode == 2:
                packet = StringBuilder()

                # 데이터 수신 // Receive data
                rs232CASCII.Recv(packet)

                # 수신 데이터 출력 // Print the received data
                if packet.Length > 0:
                    try:
                        strRecv = bytes(packet.GetBuffer()).decode("ascii")
                    except:
                        strRecv = str(bytes(packet.GetBuffer()))

                    print(f"Recv Text: {strRecv}\n")
                else:
                    print("No Recv Data.\n")

        if bExit:
            break

        break

    # RS232C 연결을 종료합니다. // Terminate the connection to the RS232C.
    if (res := rs232CASCII.Terminate()).IsFail():
        # [오류 수정] 기존 "Failed to terminate the motion." 주석 및 문자열을 통신 종료에 맞게 변경
        ErrorPrint(res, "Failed to terminate the communication.\n")

	# End of main function

# 에러 출력 함수 # Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()
