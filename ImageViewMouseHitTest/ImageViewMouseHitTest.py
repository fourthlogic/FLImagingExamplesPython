# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

import clr
import time
import threading

# Message Receiver는 CFLBase를 상속 받는다. # Message Receiver inherits from CFLBase
class CMessageReceiver(CFLBase):
    def __init__(self):
        super().__init__()
        # CBroadcastManager 에 구독 등록
        # Register subscription to receive messages from CBroadcastManager
        CBroadcastManager.Subscribe(self, CBroadcastManager.Delegate_OnReceiveBroadcast(self.OnReceiveBroadcast))

    def __del__(self):
        # 객체가 소멸할때 메세지 수신을 중단하기 위해 구독을 해제한다.
        # Unsubscribe from CBroadcastManager when object is destroyed to stop receiving messages
        CBroadcastManager.Unsubscribe(self)
        
	# 메세지가 들어오면 호출되는 함수 OnReceiveBroadcast 오버라이드 하여 구현
    # Override the OnReceiveBroadcast function, which is called when a message arrives
    def OnReceiveBroadcast(self, pMessage):
        while True:
			# message 가 None 인지 확인
            # Check if message is None
            if pMessage is None:
                break
            
            # 이미지 뷰 위에서 마우스가 움직인(MouseMove) 뒤(Post) # After mouse move over image view
            if pMessage.GetChannel() == Convert.ToInt64(EGUIBroadcast.ViewImage_PostMouseMove):
				# message 객체가 CBroadcastMessage_GUI_ViewImage_MouseEvent인지 확인
                # Verify the message is of type CBroadcastMessage_GUI_ViewImage_MouseEvent
                msgMouseEvent = pMessage if isinstance(pMessage, CBroadcastMessage_GUI_ViewImage_MouseEvent) else None
                if msgMouseEvent is None:
                    break
                
                # 메세지를 보낸 객체 얻어 오기
                # Get the sender image view from the message
                viewImage = msgMouseEvent.GetCaller()
                if viewImage is None:
                    break
                
                # 이미지뷰에서 현재 마우스가 닿은 영역 가져오기
                # Get the region currently under the mouse in the image view.
                eHitArea = viewImage.GetHitArea()
                
			    ##  영역을 확인 ## Check which area it is
                if Convert.ToInt64(eHitArea) == 0:
                    # 마우스가 특정 영역 위에 있지 않음
                    # Mouse is not over any specific area
                    strHitArea = "None" 
                else:
                    strHitArea = "Mouse is "
                    str = "on "
                    # 마우스가 이미지 미니맵 위에 있음
                    # Mouse is over the image minimap
                    if eHitArea.HasFlag(EGUIViewImageHitArea.MiniMap):
                        strHitArea += str + "MiniMap"
                        str = " and "

                    # 마우스가 미니맵의 현재 뷰어에 디스플레이 되는 영역을 나타내는 사각형 위에 있음
                    # Mouse is over the rectangle in the minimap that indicates the currently visible area
                    if eHitArea.HasFlag(EGUIViewImageHitArea.MiniMapDisplayingArea):
                        strHitArea += str + "MiniMapDisplayingArea"
                        str = " and "

                    # 마우스가 썸네일 뷰 위에 있음
                    # Mouse is over the thumbnail view
                    if eHitArea.HasFlag(EGUIViewImageHitArea.ThumbnailView):
                        strHitArea += str + "ThumbnailView"
                        str = " and "
                        
                    # 마우스가 썸네일 뷰의 크기 조절 가능한 윗쪽 부분에 있음
                    # Mouse is over the top area of the thumbnail view, where the size can be adjusted
                    if eHitArea.HasFlag(EGUIViewImageHitArea.ThumbnailViewTop):
                        strHitArea += str + "ThumbnailViewTop"
                        str = " and "

                    # 마우스가 도형 객체 위에 있음
                    # Mouse is over a figure object
                    if eHitArea.HasFlag(EGUIViewImageHitArea.Figure):
                        strHitArea += str + "Figure"
                        str = " and "

                    # 마우스가 여러 도형 객체 위에 있음
                    # Mouse is over multiple figure objects
                    if eHitArea.HasFlag(EGUIViewImageHitArea.MultiFigures):
                        strHitArea += str + "MultiFigures"
                        str = " and "

                    # 마우스가 이미지 내에 저장된 도형 객체 위에 있음
                    # Mouse is over a figure object embedded in the image (image ROI)
                    if eHitArea.HasFlag(EGUIViewImageHitArea.ImageFigure):
                        strHitArea += str + "ImageROI"
                        str = " and "

                    # 마우스가 상태 바 위에 있음
                    # Mouse is over the status bar
                    if eHitArea.HasFlag(EGUIViewImageHitArea.StatusBar):
                        strHitArea += str + "StatusBar"
                        str = " and "

                    # 마우스가 페이지 인덱스 영역 위에 있음
                    # Mouse is over the page index area
                    if eHitArea.HasFlag(EGUIViewImageHitArea.PageIndex):
                        strHitArea += str + "PageIndex"
                        str = " and "

                    # 마우스가 페이지를 이전으로 넘기는 화살표 위에 있음
                    # Mouse is over the arrow to navigate to the previous page
                    if eHitArea.HasFlag(EGUIViewImageHitArea.PrevPageArrow):
                        strHitArea += str + "PrevPageArrow"
                        str = " and "

                    # 마우스가 페이지를 다음으로 넘기는 화살표 위에 있음
                    # Mouse is over the arrow to navigate to the next page
                    if eHitArea.HasFlag(EGUIViewImageHitArea.NextPageArrow):
                        strHitArea += str + "NextPageArrow"
                        str = " and "

                    strHitArea += "."
                    
                # 이미지뷰의 0번 레이어 가져오기
                # Get the 0th layer of the image view
                layer = viewImage.GetLayer(0)

                # 기존에 Layer 에 그려진 도형들을 삭제
                # Clear any existing drawings on the layer
                layer.Clear()
                
				# 아래 함수 DrawTextCanvas는 Screen좌표를 기준으로 문자열을 뷰어에 출력한다.
                # Draw the position text to canvas
				# 색상 파라미터를 EColor.TRANSPARENCY 로 넣어주면 투명색으로 처리된다.
				# 파라미터 순서 : 레이어 -> 기준 좌표 Figure 객체 -> 문자열 -> 폰트 색 -> 면 색 -> 폰트 크기 -> 실제 크기 유무 -> 각도 -> 얼라인 -> 폰트 이름 -> 폰트 알파값(불투명도) -> 면 알파값 (불투명도) -> 폰트 두께 -> 폰트 이텔릭
				# Parameter order: layer -> reference coordinate Figure object -> string -> font color -> Area color -> font size -> actual size -> angle -> Align -> Font Name -> Font Alpha Value (Opaqueness) -> Cotton Alpha Value (Opaqueness) -> Font Thickness -> Font Italic
                layer.DrawTextCanvas(CFLPoint[float](80, 10), strHitArea, EColor.LIME, EColor.BLACK)

                # 이미지뷰를 갱신
                # Refresh the image view
                viewImage.Invalidate()
            break

def main():
    # 메세지를 전달 받을 CMessageReceiver 객체 생성 
    # Create the CMessageReceiver object to receive messages
    msgReceiver = CMessageReceiver()
    # 이미지 선언 # Declare the image
    fliImage = CFLImage()
    # 이미지 뷰 선언 # Declare the image view
    viewImage = CGUIViewImage()

    while True:     
        # 이미지 로드 # Load the image
        if (res := fliImage.Load("../../ExampleImages/PagePooling/Multiple File_Min.flif")).IsFail():
            ErrorPrint(res, "Failed to load the image file.")
            break
            
        # 이미지 뷰 생성 # Create the image view    
        if (res := viewImage.Create(300, 0, 300 + 520, 430)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break
        
        # 이미지 뷰에 띄울 이미지를 설정
        # Set the image object to be displayed in the image view
        if (res := viewImage.SetImagePtr(fliImage)[0]).IsFail():
            ErrorPrint(res, "Failed to set image object on the image view.")
            break

        # 이미지가 이미지 뷰에 채워지도록 스케일 및 오프셋 조절(ZoomFit)
        # Adjust scale and offset so the image fits the view (ZoomFit)
        if (res := viewImage.ZoomFit()).IsFail():
            ErrorPrint(res, "Failed to zoom fit")
            break

        # 이미지 뷰의 클라이언트 영역 얻어 오기
        # Get the client region of the image view in canvas coordinates
        flrlCanvas = viewImage.GetClientRectCanvasRegion()
        # 이미지 뷰의 클라이언트 영역 사각형을 이미지 좌표 기준으로 변환
        # Convert the canvas rectangle region to image coordinates
        flrdImage = viewImage.ConvertCanvasCoordToImageCoord(flrlCanvas)

        f64Width = flrdImage.GetWidth() / 10.0
        f64Height = flrdImage.GetHeight() / 10.0
        f64Size = min(f64Width, f64Height)
        
        # 사각형의 중심점 구하기
        # Calculate the center point of the image coordinate rectangle
        flpdCenter = CFLPoint[float](0, 0)
        flrdImage.GetCenter(flpdCenter)

        # 화면 중앙에 띄울 사각형 생성
        # Create a rectangle centered on the screen
        flrdFigureShape = CFLRect[float](
            flpdCenter.x - f64Size,
            flpdCenter.y - f64Size,
            flpdCenter.x + f64Size,
            flpdCenter.y + f64Size
        )
        
        # 이미지 뷰에 사각형 객체 추가
        # Add the rectangle figure object to the image view
        viewImage.PushBackFigureObject(flrdFigureShape)
        
        # 이미지 뷰를 갱신
        # Refresh the image view
        viewImage.Invalidate(True)

        # 이미지 뷰의 썸네일 뷰를 고정
        # Lock the thumbnail view of the image view (optional, depends on implementation)
        viewImage.SetFixThumbnailView(True)
        
        # 이미지 뷰가 종료될 때까지 대기
        # Wait until the first image view is closed
        while viewImage.IsAvailable():
            time.sleep(0.01)

        break


# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}')


if __name__ == '__main__':
    main()