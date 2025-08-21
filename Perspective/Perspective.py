# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliSourceImage = CFLImage()
	fliDestinationImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSrc = CGUIViewImage()
	viewImageDst = CGUIViewImage()

	while True:
		
		# Source 이미지 로드 # Load the source image
		if (res := fliSourceImage.Load('../../ExampleImages/Perspective/calendar.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Destination 이미지 로드 # Load the destination image
		if (res := fliDestinationImage.Load('../../ExampleImages/Perspective/space.flif')).IsFail():
			ErrorPrint(res, 'Failed to assign the image.')
			break

		# Source 이미지 뷰 생성 # Create source image view
		if (res := viewImageSrc.Create(400, 0, 912, 384)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰 생성 # Create the destination image view
		if (res := viewImageDst.Create(912, 0, 1424, 384)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizePointOfView(viewImageDst)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 # Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDst.SetImagePtr(fliDestinationImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizeWindow(viewImageDst)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# Perspective 객체 생성 # Create Perspective object
		perspective = CPerspective()

		# Source 이미지 설정 # Set the source image
		perspective.SetSourceImage(fliSourceImage)
		
		# Source 이미지의 투영 영역 범위 설정 # Set the range of the projection area of the Source image
		flqSourceProjection = CFLQuad[Double](290.87, 65.73, 531.69, 192.5, 169.68, 406.66, 34.59, 170.22)
		
		# Source 이미지의 투영 영역 지정 # Set the projection area of the Source image
		perspective.SetSourceProjection(flqSourceProjection)

		# Destination 이미지 설정 # Set the destination image
		perspective.SetDestinationImage(fliDestinationImage)

		# Destination 이미지의 출력 대상 영역 범위 설정 # Set the output destination area range of Destination image
		flcDestinationROI = CFLCircle[Double](243, 261, 188, 0, 0, 360, EArcClosingMethod.EachOther)

		# Destination 이미지의 출력 대상 영역 지정 # Destination Specify the output target area of the image
		perspective.SetDestinationROI(flcDestinationROI)
		
		# Destination 이미지의 투영 영역 범위 설정 # Set the range of the projection area of the destination image
		flrDestinationProjection = CFLRect[Double](192, 208, 332, 346)
		
		# Destination 이미지의 투영 영역 지정 # Set the projection area of the destination image
		perspective.SetDestinationProjection(flrDestinationProjection)
		
		# 보간법 설정 (Bicubic / Bilinear / NearestNeighbor) # Set interpolation method (Bicubic / Bilinear / NearestNeighbor)
		perspective.SetInterpolationMethod(EInterpolationMethod.Bicubic)
		
		# 공백 영역 색상 값 설정 # Set blank area color value
		mvBlankColor = CMultiVar[Double](10, 160, 20)
		
		# 공백 영역 색상 지정
		perspective.SetBlankColor(mvBlankColor)
		
		# 항상 공백 영역을 지정한 색으로 채우도록 설정 # Always set blank areas to be filled with the specified color
		perspective.EnableFillBlankColorMode(True)
		
		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := perspective.Execute()).IsFail():
			ErrorPrint(res, "Failed to execute perspective.")
			break


		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSrc.GetLayer(0)
		layerDestination = viewImageDst.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSource.Clear()
		layerDestination.Clear()

        # FLImaging의 Figure객체들은 어떤 도형모양이든 상관없이 하나의 함수로 디스플레이가 가능 # FLImaging's figure objects can be displayed with a single function, regardless of the shape of the figure
        # Source Projection 영역이 어디인지 알기 위해 디스플레이 한다 # Display to know where the Source Projection area is
		if (res := layerSource.DrawFigureImage(flqSourceProjection, EColor.LIME, 3)).IsFail():
			ErrorPrint(res, "Failed to draw figure.")
			break

        # Destination Projection 영역이 어디인지 알기 위해 디스플레이한다. # Display to know where the Destination Projection area is.
		if (res := layerDestination.DrawFigureImage(flrDestinationProjection, EColor.LIME, 3)).IsFail():
			ErrorPrint(res, "Failed to draw figure.")
			break

        # Destination ROI 영역이 어디인지 알기 위해 디스플레이한다. # Display to know where the Destination ROI area is.
		if (res := layerDestination.DrawFigureImage(flcDestinationROI, EColor.RED, 3)).IsFail():
			ErrorPrint(res, "Failed to draw figure.")
			break

		# 이미지 뷰 정보 표시 # Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if (res := layerSource.DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail() or \
			(res := layerDestination.DrawTextCanvas(flpPoint, 'Destination Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 이미지 뷰를 갱신 # Update image view
		viewImageSrc.Invalidate(True)
		viewImageDst.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImageSrc.IsAvailable() and viewImageDst.IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function



# 에러 출력 함수 # Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()