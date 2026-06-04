# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliSourceImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSrc = CGUIViewImage()

	while True:
		
		# Source 이미지 로드 # Load the source image
		if (res := fliSourceImage.Load('../../ExampleImages/FLLocalExtremaDetection/FLLocalExtremaDetection.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 뷰 생성 # Create source image view
		if (res := viewImageSrc.Create(400, 0, 1168, 540)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 객체 생성 # Create object
		flLocalExtremaDetection = CFLLocalExtremaDetection()

		# ROI 범위 설정 # Set the ROI value
		flrROI = CFLRect[int](100, 50, 450, 450)

		# Source 이미지 설정 # Set the source image
		flLocalExtremaDetection.SetSourceImage(fliSourceImage)

		# Source ROI 설정 # Set the Source ROI
		flLocalExtremaDetection.SetSourceROI(flrROI)

		# 검출을 위한 Suppression Radius 설정 # Set Suppression Radius
		flLocalExtremaDetection.SetSuppressionRadius(11)

		# Reference Surface Check 설정 # Set Reference Surface Check
		flLocalExtremaDetection.EnableReferenceSurfaceCheck(True)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := flLocalExtremaDetection.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break

		# 결과값을 받아올 컨테이너 생성 # Create the object to push the result
		flfaResultPoints = CFLFigureArray()

		# 검출 결과 받아오기 # Get the detection points
		if (res := flLocalExtremaDetection.GetResultPoints(flfaResultPoints)[0]).IsFail():
			ErrorPrint(res, 'Failed to process.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSrc.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSource.Clear()

		# ROI영역이 어디인지 알기 위해 디스플레이 한다 # Display to find out where ROI is
		if (res := layerSource.DrawFigureImage(flrROI, EColor.LIME)).IsFail():
			ErrorPrint(res, 'Failed to draw figure.')
			break

		# 이미지 뷰 정보 표시 # Display image view information
		if (res := layerSource.DrawFigureImage(flfaResultPoints, EColor.RED, 2)).IsFail():
			ErrorPrint(res, 'Failed to draw figure.')
			break

		if (res := layerSource.DrawFigureImage(flrROI, EColor.BLUE)).IsFail():
			ErrorPrint(res, 'Failed to draw figure.')
			break

		# 이미지 뷰를 갱신 # Update image view
		viewImageSrc.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImageSrc.IsAvailable():
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