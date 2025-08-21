# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 메인 함수 # Main function
def main():

	class EType:
		Source = 0
		Destination1 = 1
		Destination2 = 2
		Destination3 = 3
		Destination4 = 4
		ETypeCount = 5

	# 이미지 객체 선언 # Declare the image object
	arrFliImage = [CFLImage() for i in range(EType.ETypeCount)]

	# 이미지 뷰 선언 # Declare the image view
	arrViewImage = [CGUIViewImage() for i in range(EType.ETypeCount)]

	while True:
		
		# Source 이미지 로드 # Load the source image
		if (res := arrFliImage[EType.Source].Load('../../ExampleImages/EdgeDetection/AlphabatColor.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		bError = False

		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 # Create destination image as same as source image
		for i in range(EType.Destination1, EType.ETypeCount) :
			if (res := arrFliImage[i].Assign(arrFliImage[EType.Source])).IsFail():
				ErrorPrint(res, 'Failed to load the image file.')
				break

		if bError :
			break

		for i in range(EType.ETypeCount) :

			x = i % 3
			y = int(i / 3)

			#이미지 뷰 생성 # Create image view
			if (res := arrViewImage[i].Create(x * 400 + 400, y * 400, x * 400 + 400 + 400, y * 400 + 400)).IsFail():
				ErrorPrint(res, 'Failed to create the image view.')
				bError = True
				break

			# 이미지 뷰에 이미지를 디스플레이 # Display an image in an image view
			if (res := arrViewImage[i].SetImagePtr(arrFliImage[i])[0]).IsFail():
				ErrorPrint(res, 'Failed to set image object on the image view.')
				bError = True
				break

			if i == EType.Source :
				continue

			# 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the image views
			if (res := arrViewImage[EType.Source].SynchronizePointOfView(arrViewImage[i])[0]).IsFail():
				ErrorPrint(res, 'Failed to synchronize view.')
				bError = True
				break

			# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
			if (res := arrViewImage[EType.Source].SynchronizeWindow(arrViewImage[i])[0]).IsFail():
				ErrorPrint(res, 'Failed to synchronize window.')
				bError = True
				break

		if bError :
			break

		# ROI 설정을 위한 CFLRect 객체 생성 # Create a CFLRect object for setting ROI
		flrROI = CFLRect[int](150, 150, 300, 300)

		# 객체 생성 # Create object
		laplacianOfGaussianFilter = CLaplacianOfGaussianFilter()

		# Source 이미지 설정 # Set the source image
		laplacianOfGaussianFilter.SetSourceImage(arrFliImage[EType.Source])

		# Source ROI 설정 # Set the Source ROI
		laplacianOfGaussianFilter.SetSourceROI(flrROI)

		# Destination1 이미지 설정 # Set the destination image
		laplacianOfGaussianFilter.SetDestinationImage(arrFliImage[EType.Destination1])

		# Sigma 값 설정 # Set the sigma value
		laplacianOfGaussianFilter.SetSigma(0.5)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := laplacianOfGaussianFilter.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break

		# Destination2 이미지 설정 # Set the destination image
		laplacianOfGaussianFilter.SetDestinationImage(arrFliImage[EType.Destination2])

		# Sigma 값 설정 # Set the sigma value
		laplacianOfGaussianFilter.SetSigma(0.8)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := laplacianOfGaussianFilter.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break

		# Destination3 이미지 설정 # Set the destination image
		laplacianOfGaussianFilter.SetDestinationImage(arrFliImage[EType.Destination3])

		# Sigma 값 설정 # Set the sigma value
		laplacianOfGaussianFilter.SetSigma(1)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := laplacianOfGaussianFilter.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break

		# Destination4 이미지 설정 # Set the destination image
		laplacianOfGaussianFilter.SetDestinationImage(arrFliImage[EType.Destination4])

		# Sigma 값 설정 # Set the sigma value
		laplacianOfGaussianFilter.SetSigma(2)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := laplacianOfGaussianFilter.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break

		
		arrLayer = [CGUIViewImageLayer() for i in range(EType.ETypeCount)]

		for i in range(EType.ETypeCount) :

			# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
			# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
			arrLayer[i] = arrViewImage[i].GetLayer(0)

			# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
			arrLayer[i].Clear()

			# ROI영역이 어디인지 알기 위해 디스플레이 한다 # Display to find out where ROI is
			# FLImaging의 Figure 객체들은 어떤 도형모양이든 상관없이 하나의 함수로 디스플레이가 가능 # FLimaging's Figure objects can be displayed as a function regardless of the shape
			# 아래 함수 DrawFigureImage는 Image좌표를 기준으로 하는 Figure를 Drawing 한다는 것을 의미하며 # The function DrawFigureImage below means drawing a picture based on the image coordinates
			# 맨 마지막 두개의 파라미터는 불투명도 값이고 1일경우 불투명, 0일경우 완전 투명을 의미한다. # The last two parameters are opacity values, which mean opacity for 1 day and complete transparency for 0 day.
			# 파라미터 순서 : 레이어 -> Figure 객체 -> 선 색 -> 선 두께 -> 면 색 -> 펜 스타일 -> 선 알파값(불투명도) -> 면 알파값 (불투명도) # Parameter order: Layer -> Figure object -> Line color -> Line thickness -> Face color -> Pen style -> Line alpha value (opacity) -> Area alpha value (opacity)
			if (res := arrLayer[i].DrawFigureImage(flrROI, EColor.LIME)).IsFail():
				ErrorPrint(res, 'Failed to draw figure.')
				break


		# View 정보를 디스플레이 한다. # Display view information
		# 아래 함수 DrawTextCanvas은 Screen좌표를 기준으로 하는 String을 Drawing 한다. # The function DrawTextCanvas below draws a String based on the screen coordinates.
		# 색상 파라미터를 EGUIViewImageLayerTransparencyColor 으로 넣어주게되면 배경색으로 처리함으로 불투명도를 0으로 한것과 같은 효과가 있다.
		# If the color parameter is set as EGUIViewImageLayerTransparencyColor, it has the same effect as setting the opacity to 0 by treating it as a background color.
		# 파라미터 순서 : 레이어 -> 기준 좌표 Figure 객체 -> 문자열 -> 폰트 색 -> 면 색 -> 폰트 크기 -> 실제 크기 유무 -> 각도 ->
		#                 얼라인 -> 폰트 이름 -> 폰트 알파값(불투명도) -> 면 알파값 (불투명도) -> 폰트 두께 -> 폰트 이텔릭
		# Parameter order: layer -> reference coordinate Figure object -> string -> font color -> Area color -> font size -> actual size -> angle ->
		#                  Align -> Font Name -> Font Alpha Value (Opaqueness) -> Cotton Alpha Value (Opaqueness) -> Font Thickness -> Font Italic

		# 이미지 뷰 정보 표시 # Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if (res := arrLayer[EType.Source].DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := arrLayer[EType.Destination1].DrawTextCanvas(flpPoint, 'Destination1 Image (Sigma 0.5)', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := arrLayer[EType.Destination2].DrawTextCanvas(flpPoint, 'Destination2 Image (Sigma 0.8)', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := arrLayer[EType.Destination3].DrawTextCanvas(flpPoint, 'Destination3 Image (Sigma 1)', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := arrLayer[EType.Destination4].DrawTextCanvas(flpPoint, 'Destination4 Image (Sigma 2)', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 이미지 뷰를 갱신 # Update image view
		for i in range(EType.ETypeCount) :
			arrViewImage[i].Invalidate(True)

		# 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		bAvailable = True

		while bAvailable :
			for i in range(EType.ETypeCount) :
				bAvailable = arrViewImage[i].IsAvailable()

				if bAvailable == False :
					break

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