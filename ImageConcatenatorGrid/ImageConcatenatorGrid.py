# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()

# 메인 함수 # Main function
def main():
	# 이미지 객체 선언 # Declare the image object
	fliSrcImage = CFLImage()
	fliDstImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSrc = CGUIViewImage()
	viewImageDst = CGUIViewImage()

	while True:
		# Source 이미지 로드 # Load the source image
		if (res := fliSrcImage.Load("../../ExampleImages/ImageConcatenatorGrid/mnist0.flif")).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 # Create destination image as same as source image
		if (res := fliDstImage.Assign(fliSrcImage)).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		# 이미지 뷰 생성 # Create image view
		if ((res := viewImageSrc.Create(400, 0, 800, 400)).IsFail() or 
			(res := viewImageDst.Create(800, 0, 1200, 400)).IsFail()):
			ErrorPrint(res, "Failed to create the image view.\n")
			break

		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if ((res := viewImageSrc.SetImagePtr(fliSrcImage)[0]).IsFail() or 
			(res := viewImageDst.SetImagePtr(fliDstImage)[0]).IsFail()):
			ErrorPrint(res, "Failed to set image object on the image view. \n")
			break
		
		# 알고리즘 객체 생성 # Create algorithm object
		imageConcatenatorGrid = CImageConcatenatorGrid()
		
		# Source 이미지 설정 # Set source image 
		if (res := imageConcatenatorGrid.SetSourceImage(fliSrcImage)[0]).IsFail():
			break
		# Destination 이미지 설정 # Set destination image 
		if (res := imageConcatenatorGrid.SetDestinationImage(fliDstImage)[0]).IsFail():
			break

		# Page scope 설정 # Set page scope
		imageConcatenatorGrid.SetPageScope(CImageConcatenatorGrid.EPageScope.Source_AllPage_Operand_None)
		# Tile Size 설정 # Set Tile Size
		imageConcatenatorGrid.SetTileSize(3, 3)

		# 알고리즘 수행 # Execute the algorithm
		if (res := imageConcatenatorGrid.Execute()).IsFail():
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
		viewImageSrc.ZoomFit()
		viewImageDst.ZoomFit()
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

