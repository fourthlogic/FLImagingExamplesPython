# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *


class CMessageReceiver(CFLBase):
	
	def __init__(self, viewImage: 'CGUIViewImage'):
		super().__init__()
		self.m_viewImage = viewImage

		# 메세지를 전달 받기 위해 CBroadcastManager 에 구독 등록 # Subscribe to CBroadcastManager to receive messages
		CBroadcastManager.Subscribe(self, BroadcastCallback(self.OnReceiveBroadcast))

		self.m_fliFirstPageAlignment = CFLQuad[float]()
		self.m_fliLastPageAlignment = CFLQuad[float]()
		
	def __del__(self):
		# CMessageReceiver destructor
		# Unsubscribe to stop receiving messages when the object is deleted
		print("CMessageReceiver is deleted")
		CBroadcastManager.Unsubscribe(self)
	
	def OnReceiveBroadcast(self, message: 'CBroadcastMessage'):
		while True:
			# message 가 null 인지 확인 # Verify message is null
			if message is None:
				break

			# GetCaller() 가 등록한 이미지뷰인지 확인 # Verify that GetCaller() is a registered image view
			if message.GetCaller() != self.m_viewImage:
				break

			# 메세지의 채널을 확인 # Check the channel of the message
			if message.GetChannel() == EGUIBroadcast.ViewImage_PostPageChange:
				
				print("CMessageReceiver page changed")
				# 메세지를 호출한 객체를 CGUIViewImage 로 캐스팅 # Casting the object that called the message as CGUIViewImage
				viewImage = message.GetCaller()
				
				# viewImage 가 null 인지 확인 # Verify viewImage is null
				if viewImage is None:
					break

				fliSrc = viewImage.GetImage()

				if fliSrc is None:
					break

				i64CurPage = fliSrc.GetSelectedPageIndex()

				if i64CurPage == 0:
					# 이미지뷰의 3번 레이어 가져오기 # Get layer 3rd of image view
					wrapImageLayer = viewImage.GetLayer(3)
					wrapImageLayer.DrawFigureImage(self.m_fliFirstPageAlignment, EColor.LIME, 1)

					tpPoint = TPoint[float](self.m_fliFirstPageAlignment.flpPoints[0].x,
											self.m_fliFirstPageAlignment.flpPoints[0].y)

					wrapImageLayer.DrawTextImage(tpPoint, "First Page Alignment", EColor.CYAN)

				elif i64CurPage == fliSrc.GetPageCount() - 1:
					# 이미지뷰의 4번 레이어 가져오기 # Get layer 4th of image view
					wrapImageLayer = viewImage.GetLayer(4)
					wrapImageLayer.DrawFigureImage(self.m_fliLastPageAlignment, EColor.LIME, 1)

					tpPoint = TPoint[float](self.m_fliLastPageAlignment.flpPoints[0].x,
											self.m_fliLastPageAlignment.flpPoints[0].y)

					wrapImageLayer.DrawTextImage(tpPoint, "Last Page Alignment", EColor.CYAN)

				# 이미지뷰를 갱신 # Update the image view.
				viewImage.Invalidate()

			break


# 메인 함수 # Main function
def main():
	# 이미지 객체 선언 # Declare the image object
	fliSrcImage = CFLImage()
	fliDstImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSrc = CGUIViewImage()
	viewImageDst = CGUIViewImage()
	
	# Message Reciever 객체 생성 # Create Message Reciever object
	msgReceiver = CMessageReceiver(viewImageSrc)

	res = CResult()

	while True:
		# 이미지 로드 # Load image
		if (res := fliSrcImage.Load("../../ExampleImages/MultiFocus/SourceAlignment.flif")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break

		flqFirstPageAlignment = CFLQuad[Double]()
		flqLastPageAlignment = CFLQuad[Double]()

		if (res := flqFirstPageAlignment.Load("../../ExampleImages/MultiFocus/FirstPageAlignment.fig")).IsFail():
			ErrorPrint(res, "Failed to load Source Projection Figure.")
			break

		if (res := flqLastPageAlignment.Load("../../ExampleImages/MultiFocus/LastPageAlignment.fig")).IsFail():
			ErrorPrint(res, "Failed to load Destination Projection Figure.")
			break
		
		# 메시지 리시버에 Figure Pointer 설정 # Set Figure Point to message receiver
		msgReceiver.m_fliFirstPageAlignment = flqFirstPageAlignment
		msgReceiver.m_fliLastPageAlignment = flqLastPageAlignment

		# 이미지 뷰 생성 # Create image view
		if (res := viewImageSrc.Create(400, 0, 800, 400)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break

		# Destination 이미지 뷰 생성 # Create the destination image view
		if (res := viewImageDst.Create(800, 0, 1200, 400)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break
		
		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizePointOfView(viewImageDst)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize view.\n")
			break

		# 두 이미지 뷰 윈도우의 위치를 동기화 한다 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizeWindow(viewImageDst)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize window\n")
			break
		
		# 이미지 뷰에 이미지를 디스플레이 # Display an image in an image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SetImagePtr(fliSrcImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 # Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDst.SetImagePtr(fliDstImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break

		
		# 알고리즘 객체 생성 # Create algorithm object
		mf = CMultiFocus()

		# Source 이미지 설정 # Set the source image
		if (res := mf.SetSourceImage(fliSrcImage)[0]).IsFail():
			break
		# Destination 이미지 설정 # Set the destination image
		if (res := mf.SetDestinationImage(fliDstImage)[0]).IsFail():
			break
		# Kernel Size 설정 # Set the kernel size
		if (res := mf.SetKernel(23)).IsFail():
			break
		# 첫번째 페이지 Alignment 설정 # Set first page alignment
		if (res := mf.SetFirstPageAlignment(flqFirstPageAlignment)).IsFail():
			break
		# 마지막 페이지 Alignment 설정 # Set last page alignment
		if (res := mf.SetLastPageAlignment(flqLastPageAlignment)).IsFail():
			break
		
		# 알고리즘 수행 # Execute the algorithm
		if (res := mf.Execute()).IsFail():
			ErrorPrint(res, "Failed to execute the algorithm.")
			break


		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSrc = viewImageSrc.GetLayer(0)
		layerDst = viewImageDst.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSrc.Clear()
		layerDst.Clear()

		# View 정보를 디스플레이 합니다. # Display View information.
		layerSrc.SetAutoClearMode(ELayerAutoClearMode.PageChanged, False)
		flpTemp = CFLPoint[Double](0, 0)
		if (res := layerSrc.DrawTextImage(flpTemp, "Source Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break

		if (res := layerDst.DrawTextImage(flpTemp, "Destination Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break
			
		# 이미지 뷰를 Zoom fit # Zoom fit image view
		viewImageSrc.ZoomFit()
		viewImageDst.ZoomFit()

		# 이미지 뷰를 갱신 합니다. # Update image view
		viewImageSrc.Invalidate(True)
		viewImageDst.Invalidate(True)
		
		# 이미지 뷰가 종료될 때 까지 기다림 # Wait for the image view to close
		while viewImageSrc.IsAvailable() and viewImageDst.IsAvailable():
			CThreadUtilities.Sleep(1)

		msgReceiver.__del__()
		break
	# End of main function



# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
	main()