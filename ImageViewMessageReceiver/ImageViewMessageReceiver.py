# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()

import time

# Message Receiver는 CFLBase를 상속 받는다. # Message Receiver inherits from CFLBase
class CMessageReceiver(CFLBase):
    def __init__(self, viewImage):
        super().__init__()
        self.m_viewImage = viewImage
        # CBroadcastManager 에 구독 등록
        # Register subscription to receive messages from CBroadcastManager
        CBroadcastManager.Subscribe(self, CBroadcastManager.Delegate_OnReceiveBroadcast(self.OnReceiveBroadcast))

    def __del__(self):
        # 객체가 소멸할때 메세지 수신을 중단하기 위해 구독을 해제한다.
        # Unsubscribe from CBroadcastManager when object is destroyed to stop receiving messages
        CBroadcastManager.Unsubscribe(self)
        
	# 메세지가 들어오면 호출되는 함수 OnReceiveBroadcast 오버라이드 하여 구현
    # Override the OnReceiveBroadcast function, which is called when a message arrives
    def OnReceiveBroadcast(self, message):
        while True:
			# message 가 None 인지 확인
            # Check if message is None
            if message is None:
                break
            
            # 메세지를 보낸 객체가 등록한 이미지뷰인지 확인
            # Check if the sender of the message is the registered image view
            if message.GetCaller() != self.m_viewImage:
                break
            
			# 메세지의 채널을 얻어온다.
            # Get the channel of the message
            channel = message.GetChannel()
            
			##  채널을 확인 ## Check which channel it is
            # 이미지 뷰 위에서 마우스가 움직인(MouseMove) 뒤(Post) # After mouse move over image view
            if channel == int(EGUIBroadcast.ViewImage_PostMouseMove):
				# message 객체가 CBroadcastMessage_GUI_ViewImage_MouseEvent인지 확인
                # Verify the message is of type CBroadcastMessage_GUI_ViewImage_MouseEvent
                msg_mouse_event = message if isinstance(message, CBroadcastMessage_GUI_ViewImage_MouseEvent) else None
                if msg_mouse_event is None:
                    break

                # 메세지를 보낸 객체 얻어 오기
                # Get the sender image view from the message
                viewImage = msg_mouse_event.GetCaller()
                if viewImage is None:
                    break

                # 이미지뷰의 0번 레이어 가져오기
                # Get the 0th layer of the image view
                layer = viewImage.GetLayer(0)

                # 기존에 Layer 에 그려진 도형들을 삭제
                # Clear any existing drawings on the layer
                layer.Clear()

                # 마우스 좌표를 표시할 문자열 생성
                # Generate a string indicating the mouse position
                str_position = f"Move X: {msg_mouse_event.m_i32CursorX}, Y: {msg_mouse_event.m_i32CursorY}"
                
		        # 아래 함수 DrawTextCanvas는 스크린 좌표를 기준으로 문자열을 뷰어에 출력한다.
                # The function DrawTextCanvas displays a string on the viewer using screen coordinates.
		        # 파라미터 순서 : 기준 좌표 Figure 객체 -> 문자열 -> 텍스트 색 -> 텍스트 테두리 색 -> 폰트 크기 -> 실제 크기로 출력 유무 -> 각도 -> 정렬 -> 폰트 이름 -> 텍스트 알파값(불투명도) -> 텍스트 테두리 알파값 (불투명도) -> 폰트 두께 -> 폰트 이탤릭 여부
		        # Parameter order: reference coordinate (Figure object) -> text string -> text color -> text outline color -> font size -> render in real-world size (bool) -> angle -> alignment -> font name -> text alpha (opacity) -> text outline alpha (opacity) -> font thickness -> italic font (bool)
                layer.DrawTextCanvas(CFLPoint[float](10, 10), str_position, EColor.LIME, EColor.BLACK)

                # 이미지뷰를 갱신
                # Refresh the image view
                viewImage.Invalidate()

            # 이미지 뷰 위에서 마우스의 왼쪽 버튼을 누른(LButtonDown) 뒤(Post)
            # After left mouse button is pressed on image view
            elif channel == int(EGUIBroadcast.ViewImage_PostLButtonDown):
				# message 객체가 CBroadcastMessage_GUI_ViewImage_MouseEvent인지 확인
                # Verify the message is of type CBroadcastMessage_GUI_ViewImage_MouseEvent
                msg_mouse_event = message if isinstance(message, CBroadcastMessage_GUI_ViewImage_MouseEvent) else None
                if msg_mouse_event is None:
                    break
                
                # 메세지를 보낸 객체 얻어 오기
                # Get the sender image view from the message
                viewImage = msg_mouse_event.GetCaller()
                if viewImage is None:
                    break
                
                # 이미지뷰의 0번 레이어 가져오기
                # Get the 0th layer of the image view
                layer = viewImage.GetLayer(0)

                # 기존에 Layer 에 그려진 도형들을 삭제
                # Clear any existing drawings on the layer
                layer.Clear()
                
                # 마우스 좌표를 표시할 문자열 생성
                # Generate a string indicating the mouse position
                str_position = f"LButtonDown X: {msg_mouse_event.m_i32CursorX}, Y: {msg_mouse_event.m_i32CursorY}"
                
		        # 아래 함수 DrawTextCanvas는 스크린 좌표를 기준으로 문자열을 뷰어에 출력한다.
                # The function DrawTextCanvas displays a string on the viewer using screen coordinates.
		        # 파라미터 순서 : 기준 좌표 Figure 객체 -> 문자열 -> 텍스트 색 -> 텍스트 테두리 색 -> 폰트 크기 -> 실제 크기로 출력 유무 -> 각도 -> 정렬 -> 폰트 이름 -> 텍스트 알파값(불투명도) -> 텍스트 테두리 알파값 (불투명도) -> 폰트 두께 -> 폰트 이탤릭 여부
		        # Parameter order: reference coordinate (Figure object) -> text string -> text color -> text outline color -> font size -> render in real-world size (bool) -> angle -> alignment -> font name -> text alpha (opacity) -> text outline alpha (opacity) -> font thickness -> italic font (bool)
                layer.DrawTextCanvas(CFLPoint[float](10, 10), str_position, EColor.RED, EColor.BLACK)

                # 이미지뷰를 갱신
                # Refresh the image view
                viewImage.Invalidate()

            # 이미지 뷰 위에서 마우스의 왼쪽 버튼을 올린(LButtonUp) 뒤(Post)
            # After left mouse button is released on image view
            elif channel == int(EGUIBroadcast.ViewImage_PostLButtonUp):
				# message 객체가 CBroadcastMessage_GUI_ViewImage_MouseEvent인지 확인
                # Verify the message is of type CBroadcastMessage_GUI_ViewImage_MouseEvent
                msg_mouse_event = message if isinstance(message, CBroadcastMessage_GUI_ViewImage_MouseEvent) else None
                if msg_mouse_event is None:
                    break
                
                # 메세지를 보낸 객체 얻어 오기
                # Get the sender image view from the message
                viewImage = msg_mouse_event.GetCaller()
                if viewImage is None:
                    break
                
                # 이미지뷰의 0번 레이어 가져오기
                # Get the 0th layer of the image view
                layer = viewImage.GetLayer(0)

                # 기존에 Layer 에 그려진 도형들을 삭제
                # Clear any existing drawings on the layer
                layer.Clear()
                
                # 마우스 좌표를 표시할 문자열 생성
                # Generate a string indicating the mouse position
                str_position = f"LButtonUp X: {msg_mouse_event.m_i32CursorX}, Y: {msg_mouse_event.m_i32CursorY}"
                
		        # 아래 함수 DrawTextCanvas는 스크린 좌표를 기준으로 문자열을 뷰어에 출력한다.
                # The function DrawTextCanvas displays a string on the viewer using screen coordinates.
		        # 파라미터 순서 : 기준 좌표 Figure 객체 -> 문자열 -> 텍스트 색 -> 텍스트 테두리 색 -> 폰트 크기 -> 실제 크기로 출력 유무 -> 각도 -> 정렬 -> 폰트 이름 -> 텍스트 알파값(불투명도) -> 텍스트 테두리 알파값 (불투명도) -> 폰트 두께 -> 폰트 이탤릭 여부
		        # Parameter order: reference coordinate (Figure object) -> text string -> text color -> text outline color -> font size -> render in real-world size (bool) -> angle -> alignment -> font name -> text alpha (opacity) -> text outline alpha (opacity) -> font thickness -> italic font (bool)
                layer.DrawTextCanvas(CFLPoint[float](10, 10), str_position, EColor.BLUE, EColor.BLACK)

                # 이미지뷰를 갱신
                # Refresh the image view
                viewImage.Invalidate()

            break


def main():
    # 이미지 뷰 선언 # Declare the image view
    viewImage = [None] * 2
    viewImage[0] = CGUIViewImage()
    viewImage[1] = CGUIViewImage()

    # 메세지를 전달 받을 CMessageReceiver 객체 생성 
    # Create the CMessageReceiver object to receive messages
    msg_receiver = CMessageReceiver(viewImage[0])

    res = CResult()

    # 이미지 뷰 생성 # Create the first image view    
    if (res := viewImage[0].Create(300, 0, 300 + 520, 430)).IsFail():
        ErrorPrint(res, "Failed to create the image view.")
        return

    # 이미지 뷰 생성 # Create the second image view
    if (res := viewImage[1].Create(300 + 520, 0, 300 + 520 * 2, 430)).IsFail():
        ErrorPrint(res, "Failed to create the image view.")
        return

    # 뷰의 시점 동기화 # Synchronize the point of view between views
    if (res := viewImage[0].SynchronizePointOfView(viewImage[1])[0]).IsFail():
        ErrorPrint(res, "Failed to synchronize view")
        return

    # 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
    if (res := viewImage[0].SynchronizeWindow(viewImage[1])[0]).IsFail():
        ErrorPrint(res, "Failed to synchronize window")
        return

    # 이미지 뷰가 종료될 때까지 대기
    # Wait until the first image view is closed
    while viewImage[0].IsAvailable():
        time.sleep(0.01)


# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}')


if __name__ == '__main__':
    main()