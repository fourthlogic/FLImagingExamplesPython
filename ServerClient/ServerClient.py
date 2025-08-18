# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()

# 서버 소켓 이벤트 핸들러 클래스
# Server socket event class
# 소켓 이벤트를 수신하기 위해 CDeviceEventSocketBase에서 상속받아 구현
# Inherit from CDeviceEventSocketBase to receive socket events
class CDeviceEventSocketServerEx(CDeviceEventSocketBase):
    # 생성자 // Constructor
    def __init__(self, pSocketServer):
        super().__init__()
        self.m_pSocketServer = pSocketServer
        self.RegisterOnReceived(CDeviceEventSocketServerEx.Delegate_OnReceived(self.OnReceived))

    # 수신 이벤트 함수 재정의 // Override receive event function
    def OnReceived(self, pDeviceSocketClient, pSocketPacket):
        # 받은 데이터를 문자열로 출력 // Print received data
        if pSocketPacket is not None:
            buf = pSocketPacket.GetBuffer()
            size = int(pSocketPacket.GetSize())
            fls = bytes([buf[i] for i in range(size)]).decode('ascii', errors='ignore')
            print("[Server] Recv " + fls)

        # 재전송(echo) // Send string(echo)
        if pDeviceSocketClient is not None and pSocketPacket is not None:
            # Obtain Client Manager Objects
            pDeviceSocketClientManager = self.m_pSocketServer.GetSocketClientManager()

            if pDeviceSocketClientManager is not None:
                buf = pSocketPacket.GetBuffer()
                size = int(pSocketPacket.GetSize())
                fls = bytes([buf[i] for i in range(size)]).decode('ascii', errors='ignore')
                print("[Server] Send " + fls)

                # 연결이 살아있고 연결 상태라면 데이터 전송 // Send if connection is alive
                if pDeviceSocketClientManager.IsClientAlive(pDeviceSocketClient):
                    pDeviceSocketClient.Send(pSocketPacket)

                CThreadUtilities.Sleep(500)


# 클라이언트 소켓 이벤트 클래스
# Client socket event class
class CDeviceEventSocketClientEx(CDeviceEventSocketBase):
    # 생성자 // Constructor
    def __init__(self):
        super().__init__()
        self.m_bConnect = False
        self.RegisterOnConnected(CDeviceEventSocketClientEx.Delegate_OnConnected(self.OnConnected))
        self.RegisterOnDisconnected(CDeviceEventSocketClientEx.Delegate_OnDisconnected(self.OnDisconnected))
        self.RegisterOnReceived(CDeviceEventSocketClientEx.Delegate_OnReceived(self.OnReceived))

    # 연결 이벤트 함수 재정의 // Override connection event functions
    def OnConnected(self, pDeviceSocketClient):
        self.m_bConnect = True

    # 연결 해제 이벤트 함수 재정의 // Override disconnection event functions
    def OnDisconnected(self, pDeviceSocketClient):
        self.m_bConnect = False

    # 수신 이벤트 함수 재정의 // Override receive event function
    def OnReceived(self, pDeviceSocketClient, pSocketPacket):
        # 받은 데이터를 문자열로 출력 // Print received data
        if pSocketPacket is not None:
            buf = pSocketPacket.GetBuffer()
            size = int(pSocketPacket.GetSize())
            fls = bytes([buf[i] for i in range(size)]).decode('ascii', errors='ignore')
            print("[Client] Recv " + fls)

        # 재전송(echo) // Send string(echo)
        if self.m_bConnect and pDeviceSocketClient is not None and pSocketPacket is not None:
            buf = pSocketPacket.GetBuffer()
            size = int(pSocketPacket.GetSize())
            fls = bytes([buf[i] for i in range(size)]).decode('ascii', errors='ignore')
            print("[Client] Send " + fls)
            pDeviceSocketClient.Send(pSocketPacket)
            CThreadUtilities.Sleep(500)


# 에러 출력 함수 // Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')

def main():

        # 소켓 서버, 클라이언트 선언 // Declare socket server and client
        deviceSocketServer = CDeviceSocketServer()
        deviceSocketClient = CDeviceSocketClient()

        # 이벤트 객체 생성 및 등록 // Create and register event handlers
        deviceEventSocketServer = CDeviceEventSocketServerEx(deviceSocketServer)
        deviceEventSocketClient = CDeviceEventSocketClientEx()

        deviceSocketServer.RegisterDeviceEvent(deviceEventSocketServer)
        deviceSocketClient.RegisterDeviceEvent(deviceEventSocketClient)

        while True:
            # 소켓 모드 설정 (Passive)
            # Set socket mode (Passive)
            deviceSocketServer.SetSocketMode(ESocketMode.NoProtocol_Passive)
            deviceSocketClient.SetSocketMode(ESocketMode.NoProtocol_Passive)

            # IP 주소와 포트 설정 // Set IP and port
            flsIPAddress = "127.0.0.1"
            u16Port = 4444

            deviceSocketServer.SetConnectionIPAddress(flsIPAddress, u16Port)
            deviceSocketClient.SetConnectionIPAddress(flsIPAddress, u16Port)

            # 소켓 서버 초기화 // Initialize socket server
            if((res := deviceSocketServer.Initialize()).IsFail()):
	            ErrorPrint(res, "Failed to initialize server.")
	            break

            # 소켓 클라이언트 초기화 (서버에 연결) // Initialize client (connect to server)
            if((res := deviceSocketClient.Initialize()).IsFail()):
	            ErrorPrint(res, "Failed to initialize client.")
	            break

            # 테스트용 데이터 생성 // Create test data
            flsData = "Socket echo test. [Enter any key if you want to exit]"
            dataBuf = flsData.encode('ascii')

            socketPacket = CDeviceSocketPacket()
            socketPacket.Assign(dataBuf, len(dataBuf))

            # 클라이언트에서 서버로 데이터 송신 // Send data from client to server
            if (res := deviceSocketClient.Send(socketPacket)).IsFail():
                ErrorPrint(res, "Failed to send.")
                break

            input("Press any key to exit...\n")

            # 소켓 해제 및 이벤트 해제 // Terminate sockets and clear events
            deviceSocketServer.Terminate()
            deviceSocketClient.Terminate()
            break


if __name__ == '__main__':
    main()
