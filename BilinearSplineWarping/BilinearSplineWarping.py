# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

CLibraryUtilities.Initialize()


# 메인 함수 // Main function
def main():

	# 이미지 객체 선언 // Declare the image object
	fliSourceImage =  [CFLImage(), CFLImage()]
	fliDestinationImage = [CFLImage(), CFLImage()]

	# 이미지 뷰 선언 // Declare the image view
	viewImageSrc= [CGUIViewImage(), CGUIViewImage()]
	viewImageDst= [CGUIViewImage(), CGUIViewImage()]

	while True:
		
		# Source 이미지 로드 // Load the source image
		if (res := fliSourceImage[0].Load('../../ExampleImages/BilinearSplineWarping/chess.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 뷰 생성 // Create source image view
		if (res := viewImageSrc[0].Create(100, 0, 612, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		if (res := viewImageSrc[1].Create(100, 512, 612, 1024)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰 생성 // Create the destination image view
		if (res := viewImageDst[0].Create(612, 0, 1124, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		if (res := viewImageDst[1].Create(612, 512, 1124, 1024)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDst[0].SynchronizePointOfView(viewImageSrc[0]))[0].IsFail():
			ErrorPrint(res[0], 'Failed to synchronize view.')
			break

		if (res := viewImageDst[1].SynchronizePointOfView(viewImageSrc[1]))[0].IsFail():
			ErrorPrint(res[0], 'Failed to synchronize view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 // Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc[0].SetImagePtr(fliSourceImage[0]))[0].IsFail():
			ErrorPrint(res[0], 'Failed to set image object on the image view.')
			break

		if (res := viewImageSrc[1].SetImagePtr(fliSourceImage[1]))[0].IsFail():
			ErrorPrint(res[0], 'Failed to set image object on the image view.')
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 // Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDst[0].SetImagePtr(fliDestinationImage[0]))[0].IsFail():
			ErrorPrint(res[0], 'Failed to set image object on the image view.')
			break

		if (res := viewImageDst[1].SetImagePtr(fliDestinationImage[1]))[0].IsFail():
			ErrorPrint(res[0], 'Failed to set image object on the image view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDst[0].SynchronizeWindow(viewImageSrc[0]))[0].IsFail():
			ErrorPrint(res[0], 'Failed to synchronize window.')
			break
			
		if (res := viewImageDst[1].SynchronizeWindow(viewImageSrc[1]))[0].IsFail():
			ErrorPrint(res[0], 'Failed to synchronize window.')
			break

		# Bilinear Spline Warping 객체 생성 // Create Bilinear Spline Warping object
		bilinearSplineWarping = CBilinearSplineWarping()

		# Source 이미지 설정 // Set the source image
		bilinearSplineWarping.SetSourceImage(fliSourceImage[0])

		# Destination 이미지 설정 // Set the destination image
		bilinearSplineWarping.SetDestinationImage(fliDestinationImage[0])
	
		# Interpolation Method 설정 // Set the interpolation method
		bilinearSplineWarping.SetInterpolationMethod(EInterpolationMethod.Bilinear)
		
		# 그리드를 (5,5)로 초기화 // Initialize the grid to (5,5)
		flpGridSize =CFLPoint[int](5, 5)
		flpGridIndex = CFLPoint[int]()
		flpaSource = CFLPointArray()
		flpaDestination = CFLPointArray()

		f64ScaleX = fliSourceImage[0].GetWidth() / 4.0
		f64ScaleY = fliSourceImage[0].GetHeight() / 4.0

		for y in range(flpGridSize.y):
			flpGridIndex.y = y

			for x in range(flpGridSize.x):
				flpGridIndex.x = x

				# Grid Index와 같은 좌표로 Source 좌표를 설정 // Set Source coordinates to the same coordinates as Grid Index
				flpSource = CFLPoint[Double](flpGridIndex.x * f64ScaleX, flpGridIndex.y * f64ScaleY)

				f64RandomX = CRandomGenerator.Double(-0.2, 0.2)
				f64RandomY = CRandomGenerator.Double(-0.2, 0.2)

				# 외곽의 좌표는 안쪽으로 변형 되도록 설정 // Set the outer coordinates to be Warpinged inward
				if y == 0:
					f64RandomY = -f64RandomY if f64RandomY < 0 else f64RandomY
				
				if x == 0:
					f64RandomX = -f64RandomX if f64RandomX < 0 else f64RandomX
				
				if y == flpGridSize.y - 1:
					f64RandomY = -f64RandomY if  f64RandomY > 0 else f64RandomY
				
				if x == flpGridSize.x - 1:
					f64RandomX = -f64RandomX if f64RandomX < 0 else f64RandomX
				
				# Grid Index와 같은 좌표에서 미세한 랜덤 값을 부여해서 좌표를 왜곡 // Distort coordinates by giving fine random values at the same coordinates as Grid Index
				flpDistortion = CFLPoint[Double]((flpGridIndex.x + f64RandomX) * f64ScaleX, (flpGridIndex.y + f64RandomY) * f64ScaleY)
				
				flpaSource.PushBack(flpSource)
				flpaDestination.PushBack(flpDistortion)
                  

		# 위에서 설정한 좌표들을 바탕으로 BilinearSplineWarping 클래스에 Point 배열 설정 // Set the Point array in the BilinearSplineWarping class based on the coordinates set above
		bilinearSplineWarping.SetCalibrationPointArray(flpaSource, flpaDestination)

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSrc[0].GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layerSource.Clear()

		# BilinearSplineWarping 클래스에 설정된 Vertex 정보를 화면에 Display // Display the vertex information set in the BilinearSplineWarping class on the screen.
		for k in range(flpaSource.GetCount()):
			flpSource = CFLPoint[Double]()
			flpDestination = CFLPoint[Double]()
			
			flpSource = flpaSource.GetAt(k)
			flpDestination = flpaDestination.GetAt(k)
			
			fllLine = CFLLine[Double](flpSource, flpDestination)
			flfaArrow = CFLFigureArray()
			
			flfaArrow = fllLine.MakeArrowWithRatio(0.25, True, 20)
			
			# Destination Vertex를 각 View Layer에 Drawing // Drawing the destination vertex on each view layer
			if(res := layerSource.DrawFigureImage(flpDestination, EColor.BLUE, 1).IsFail()):
				ErrorPrint(res,"Failed to draw figure objects on the image view.\n")
				break
			
			# Source Vertex를 각 View Layer에 Drawing // Drawing the source vertex on each view layer
			if(res := layerSource.DrawFigureImage(flpSource, EColor.RED, 1).IsFail()):
				ErrorPrint(res,"Failed to draw figure objects on the image view.\n")
				break
			
			# Source Vertex를 각 View Layer에 Drawing // Drawing the source vertex on each view layer
			if(res := layerSource.DrawFigureImage(flfaArrow, EColor.YELLOW, 1).IsFail()):
				ErrorPrint(res,"Failed to draw figure objects on the image view.\n")
				break

			# 앞서 설정된 이미지, Calibration Point Array로 Calibrate 수행 // Calibrate with previously set image, Calibration Point Array
			if((res := bilinearSplineWarping.Calibrate()).IsFail()):
				ErrorPrint(res, "Failed to calibrate BilinearSplineWarping.")
				ErrorPrint(res,res.GetString())
				break

			# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
			if ((res := bilinearSplineWarping.Execute()).IsFail()):
				ErrorPrint(res, "Failed to execute BilinearSplineWarping.")
				ErrorPrint(res,res.GetString())
				break

		# 두번째 Source 이미지 설정 // set the second source image
		fliSourceImage[1].Assign(fliDestinationImage[0])
		
		# Source 이미지 설정 // Set the source image
		bilinearSplineWarping.SetSourceImage(fliSourceImage[1])
		# Destination 이미지 설정 // Set the destination image
		bilinearSplineWarping.SetDestinationImage(fliDestinationImage[1])
		# Interpolation Method 설정 // Set the interpolation method
		bilinearSplineWarping.SetInterpolationMethod(EInterpolationMethod.Bilinear)
		# Calibration Src, Destination Points 바꿔서 셋팅 // Set Calibration Src, Destination Points by changing
		bilinearSplineWarping.SetCalibrationPointArray(flpaDestination, flpaSource)

		# 앞서 설정된 이미지, Calibration Point Array로 Calibrate 수행 // Calibrate with previously set image, Calibration Point Array
		if((res := bilinearSplineWarping.Calibrate()).IsFail()):
			ErrorPrint(res, "Failed to calibrate BilinearSplineWarping.")
			ErrorPrint(res,res.GetString())
			break

               # 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if ((res := bilinearSplineWarping.Execute()).IsFail()):
			ErrorPrint(res, "Failed to execute BilinearSplineWarping.")
			ErrorPrint(res,res.GetString())
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSrc[1].GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layerSource.Clear()

		# BilinearSplineWarping 클래스에 설정된 Vertex 정보를 화면에 Display // Display the vertex information set in the BilinearSplineWarping class on the screen
		for k in range(flpaSource.GetCount()):
			flpSource = CFLPoint[Double]()
			flpDestination = CFLPoint[Double]()

			flpSource = flpaDestination.GetAt(k)
			flpDestination = flpaSource.GetAt(k)

			fllLine = CFLLine[Double](flpSource, flpDestination)
			flfaArrow = CFLFigureArray()

			flfaArrow = fllLine.MakeArrowWithRatio(0.25, True, 20)

			# Destination Vertex를 각 View Layer에 Drawing // Drawing the destination vertex on each view layer
			if(res := layerSource.DrawFigureImage(flpDestination, EColor.BLUE, 1).IsFail()):
				ErrorPrint(res,"Failed to draw figure objects on the image view.\n")
				break

			# Source Vertex를 각 View Layer에 Drawing // Drawing the source vertex on each view layer
			if(res := layerSource.DrawFigureImage(flpSource, EColor.RED, 1).IsFail()):
				ErrorPrint(res,"Failed to draw figure objects on the image view.\n")
				break

			# Source Vertex를 각 View Layer에 Drawing // Drawing the source vertex on each view layer
			if(res := layerSource.DrawFigureImage(flfaArrow, EColor.YELLOW, 1).IsFail()):
				ErrorPrint(res,"Failed to draw figure objects on the image view.\n")
				break

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := bilinearSplineWarping.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Flip.')
			break
		
		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
		layerSource = [viewImageSrc[0].GetLayer(0), viewImageSrc[1].GetLayer(0)]
		layerDestination = [viewImageDst[0].GetLayer(0), viewImageDst[1].GetLayer(0)]

		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layerDestination[0].Clear()
		layerDestination[1].Clear()

		# 이미지 뷰 정보 표시 // Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		res = layerSource[0].DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 30)

		if res.IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		res = layerDestination[0].DrawTextCanvas(flpPoint, 'Destination Image', EColor.YELLOW, EColor.BLACK, 30)

		if res.IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		res = layerSource[1].DrawTextCanvas(flpPoint, 'Source Image 2', EColor.YELLOW, EColor.BLACK, 30)

		if res.IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		res = layerDestination[1].DrawTextCanvas(flpPoint, 'Destination Image 2', EColor.YELLOW, EColor.BLACK, 30)

		if res.IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		viewImageSrc[0].ZoomFit()
		viewImageSrc[1].ZoomFit()

		# 이미지 뷰를 갱신 // Update image view
		viewImageSrc[0].Invalidate(True)
		viewImageSrc[1].Invalidate(True)
		viewImageDst[0].Invalidate(True)
		viewImageDst[1].Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 // Wait until the image view is closed before exiting
		while viewImageSrc[0].IsAvailable() and viewImageSrc[1].IsAvailable() and viewImageDst[0].IsAvailable() and viewImageDst[1].IsAvailable():
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