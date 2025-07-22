# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 # Main function
def main():
	# 이미지 객체 선언 # Declare the image object
	fliSrcImage = CFLImage()
	fliDstImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSrc = CGUIViewImage()
	viewImageDst = CGUIViewImage()

	res = CResult()

	while True:
		# 이미지 로드 # Load image
		if (res := fliSrcImage.Load("../../ExampleImages/ChannelL1Norm/Coord.flif")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break
		
		# 이미지 뷰 생성 # Create image views
		if (res := viewImageSrc.Create(100, 0, 600, 500)).IsFail() or \
			(res := viewImageDst.Create(600, 0, 1100, 500)).IsFail():
			ErrorPrint(res, "Failed to create the image view. \n")
			break
		
		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views. .
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizePointOfView(viewImageDst)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize view. \n")
			break
		
		# 두 이미지 뷰 윈도우의 위치를 동기화 한다 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizeWindow(viewImageDst)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize window. \n")
			break
		
		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SetImagePtr(fliSrcImage)[0]).IsFail() or \
			(res := viewImageDst.SetImagePtr(fliDstImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view. \n")
			break
		

		# 알고리즘 객체 생성 # Create algorithm object
		algObject = CChannelL1Norm()
		
		if (res := algObject.SetSourceImage(fliSrcImage)[0]).IsFail():
			break
		if (res := algObject.SetDestinationImage(fliDstImage)[0]).IsFail():
			break
		
		# 알고리즘 수행 # Execute the algorithm
		if (res := algObject.Execute()).IsFail():
			ErrorPrint(res, "Failed to execute the algorithm.")
			break

		
		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSrc = viewImageSrc.GetLayer(0)
		layerDst = viewImageDst.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSrc.Clear()
		layerDst.Clear()

		# 이미지 뷰 정보 표시 # Display image view information
		flpTemp = CFLPoint[Double](0, 0)
		if ((res := layerSrc.DrawTextCanvas(flpTemp, "Source Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or 
			(res := layerDst.DrawTextCanvas(flpTemp, "Destination Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail()):
			ErrorPrint(res, "Failed to draw text. \n")
			break

		# 이미지 뷰를 갱신 # Update image view
		viewImageSrc.Invalidate(True)
		viewImageDst.Invalidate(True)

		# 이미지 뷰가 종료될 때 까지 기다림 # Wait for the image view to close
		while viewImageSrc.IsAvailable() and viewImageDst.IsAvailable():			
			CThreadUtilities.Sleep(1)

		break
	# End of main function



# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
 main()