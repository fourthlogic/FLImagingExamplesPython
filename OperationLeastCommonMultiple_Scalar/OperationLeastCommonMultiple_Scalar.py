# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 // Main function
def main():
	# 이미지 객체 선언 # Declare the image object
	fliSrcImage = CFLImage()
	fliDstImage0 = CFLImage()
	fliDstImage1 = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSrc = CGUIViewImage()
	viewImageDst0 = CGUIViewImage()
	viewImageDst1 = CGUIViewImage()

	while True:
		# Source 이미지 로드 // Load the source image
		if (res := fliSrcImage.Load("../../ExampleImages/OperationLeastCommonMultiple/Gradient.flif")).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 // Create destination image as same as source image
		if ((res := fliDstImage0.Assign(fliSrcImage)).IsFail() or
			(res := fliDstImage1.Assign(fliSrcImage)).IsFail()):
			ErrorPrint(res, 'Failed to assign.')
			break
		
		# 이미지 뷰 생성 # Create image view
		if ((res := viewImageSrc.Create(100, 0, 600, 500)).IsFail() or
			(res := viewImageDst0.Create(600, 0, 1100, 500)).IsFail() or
			(res := viewImageDst1.Create(1100, 0, 1600, 500)).IsFail()):
			ErrorPrint(res, "Failed to create the image view.\n")
			break

		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views. .
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if ((res := viewImageSrc.SynchronizePointOfView(viewImageDst0)[0]).IsFail() or
			(res := viewImageSrc.SynchronizePointOfView(viewImageDst1)[0]).IsFail()):
			ErrorPrint(res, "Failed to synchronize view. \n")
			break

		# 두 이미지 뷰 윈도우의 위치를 동기화 한다 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if ((res := viewImageSrc.SynchronizeWindow(viewImageDst0)[0]).IsFail() or
			(res := viewImageSrc.SynchronizeWindow(viewImageDst1)[0]).IsFail()):
			ErrorPrint(res, "Failed to synchronize window. \n")
			break

		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if ((res := viewImageSrc.SetImagePtr(fliSrcImage)[0]).IsFail() or
			(res := viewImageDst0.SetImagePtr(fliDstImage0)[0]).IsFail() or
			(res := viewImageDst1.SetImagePtr(fliDstImage1)[0]).IsFail()):
			ErrorPrint(res, "Failed to set image object on the image view. \n")
			break
		

		# 알고리즘 객체 생성 # Create algorithm object
		algObject = COperationLeastCommonMultiple()
		
		if (res := algObject.SetSourceImage(fliSrcImage)[0]).IsFail():
			break
		if (res := algObject.SetOperationSource(EOperationSource.Scalar)).IsFail():
			break

		mvScalarValue0 = CMultiVar[Double](5)
		if (res := algObject.SetScalarValue(mvScalarValue0)).IsFail():
			break
		if (res := algObject.SetDestinationImage(fliDstImage0)[0]).IsFail():
			break
		
		# 알고리즘 수행 # Execute the algorithm
		if (res := algObject.Execute()).IsFail():
			ErrorPrint(res, "Failed to execute the algorithm.")
			break
		
		mvScalarValue1 = CMultiVar[Double](17)
		if (res := algObject.SetScalarValue(mvScalarValue1)).IsFail():
			break
		if (res := algObject.SetDestinationImage(fliDstImage1)[0]).IsFail():
			break
		
		# 알고리즘 수행 # Execute the algorithm
		if (res := algObject.Execute()).IsFail():
			ErrorPrint(res, "Failed to execute the algorithm.")
			break
		
		
		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSrc = viewImageSrc.GetLayer(0)
		layerDst0 = viewImageDst0.GetLayer(0)
		layerDst1 = viewImageDst1.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSrc.Clear()
		layerDst0.Clear()
		layerDst1.Clear()

		# 이미지 뷰 정보 표시 # Display image view information
		flpTemp = CFLPoint[Double](0, 0)
		if ((res := layerSrc.DrawTextCanvas(flpTemp, "Source Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or
			(res := layerDst0.DrawTextCanvas(flpTemp, "Destination Image (Opr = 5)", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or
			(res := layerDst1.DrawTextCanvas(flpTemp, "Destination Image (Opr = 17)", EColor.YELLOW, EColor.BLACK, 20)).IsFail()):
			ErrorPrint(res, "Failed to draw text. \n")
			break

		# 이미지 뷰를 갱신 # Update image view
		viewImageSrc.Invalidate(True)
		viewImageDst0.Invalidate(True)
		viewImageDst1.Invalidate(True)

		# 이미지 뷰가 종료될 때 까지 기다림 # Wait for the image view to close
		while viewImageSrc.IsAvailable() and viewImageDst0.IsAvailable() and viewImageDst1.IsAvailable():			
			CThreadUtilities.Sleep(1)

		break
	# End of main function



# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')

if __name__ == '__main__':
    main()