# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 메인 함수 # Main function
def main():

    res = CResult()

    # 조명 컨트롤러 LVS_PN_08 선언 // Declare the LVS_PN_08 Light Controller
    lightControllerLVS_PN_08 = CDeviceLightControllerLVS_PN_08()

    bExit = False

    while True:  # do ~ while 구조
        print("\033c", end="")  # Console.Clear() 대체
        portNumber = input("Port Number: ")

        if portNumber.isdigit():
            # 컴포트 번호 설정 // Set the COM port number.
            lightControllerLVS_PN_08.SetComPortNumber(int(portNumber))

        print("\033c", end="")
        baudRate = input("BaudRate(Switch OFF = 9600, ON = 19200]: ")

        if baudRate.isdigit():
            # 보드레이트 설정 // Set the baud rate.
            lightControllerLVS_PN_08.SetBaudRate(int(baudRate))

        if (res := lightControllerLVS_PN_08.Initialize()).IsFail():
            print("Failed to initialize the light controller.")
            break

        while True:
            # 작업 모드를 선택합니다. // Select the operation mode.
            print("1. Light On/Off")
            print("2. Light Value")
            print("0. Exit\n")
            operationMode = input("Select Number: ")

            if not operationMode.isdigit():
                print("\033c", end="")
                print("Invalid input. Try again.\n")
                continue

            operationMode = int(operationMode)
            print("\033c", end="")

            if operationMode == 0:
                bExit = True
                break

            channel = input("Select Channel: ")

            if channel.isdigit():
                channel = int(channel)

                if operationMode == 1:
                    print("\n1. On\n2. Off")
                    onOff = input("Enter On/Off: ")
                    if onOff.isdigit():
                        # 채널별 On/Off 상태를 설정합니다. // Set the On/Off state for the channel.
                        lightControllerLVS_PN_08.SetChannelState(channel, int(onOff) == 1)

                elif operationMode == 2:
                    lightValue = input("Input Light Value (0 ~ 255): ")
                    if lightValue.isdigit():
                        # 조명 값을 설정합니다. // Set the light value.
                        lightControllerLVS_PN_08.SetLightValue(channel, int(lightValue))

            print("\033c", end="")

            # 입력된 파라미터를 적용합니다. // Apply the configured parameters.
            lightControllerLVS_PN_08.Apply()

        if bExit:
            break
        break

    # 조명 컨트롤러에 연결을 종료합니다. // Terminate the connection to the light controller.
    if (res := lightControllerLVS_PN_08.Terminate()).IsFail():
        print("Failed to terminate the motion.\n")

# 에러 출력 함수 # Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')

if __name__ == "__main__":
    main()
