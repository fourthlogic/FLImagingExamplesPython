# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 // Main function
def main():

	# 이미지 객체 선언 // Declare image object
	fliImage = CFLImage()

	# 이미지 드로잉 객체 선언 // Declare image drawing object
	fliImageDrawing = CFLImageDrawing()

	# 이미지 뷰 선언 // Declare image view
	viewImageSrc = CGUIViewImage()
	viewImageDst = CGUIViewImage()

	while True:

		# 이미지 로드 // Load image
		if (res := fliImage.Load('../../ExampleImages/Blob/AlignBall.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.\n')
			break

		# Drawing 이미지를 Source 이미지와 동일한 이미지로 생성 // Create drawing image as same as source image
		if(res := fliImageDrawing.Assign(fliImage)).IsFail():
			ErrorPrint(res, 'Failed to assign the image file.\n')
			break		

		# 이미지 뷰 생성 // Create image view
		if(res := viewImageSrc.Create(400, 0, 800, 400)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.\n')
			break		

		# 이미지 뷰 생성 // Create image view
		if(res := viewImageDst.Create(800, 0, 1200, 400)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.\n')
			break		

		# 두 이미지 뷰의 시점을 동기화 한다. // Synchronize the viewpoints of the two image views.
		if(res := viewImageSrc.SynchronizePointOfView(viewImageDst)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view\n')
			break		

		# 두 이미지 뷰 윈도우의 위치를 동기화 한다 // Synchronize the positions of the two image view windows
		if(res := viewImageSrc.SynchronizeWindow(viewImageDst)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.\n')
			break		

		# 이미지 뷰에 이미지를 디스플레이 // Display an image in an image view
		if(res := viewImageSrc.SetImagePtr(fliImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.\n')
			break		

        # 레이어 가져오기 // Get image layers
		layerSrc = viewImageSrc.GetLayer(0)

        # 레이어 가져오기 // Get image layers
		layerDst = fliImageDrawing.GetLayer()

        # 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layerSrc.Clear()
		layerDst.Clear()

        # 이미지에 정보 표시 // Display image information
		layerSrc.DrawTextImage(CFLPoint[Double](0, 0), 'Source Image', EColor.YELLOW, EColor.BLACK, 30)
		layerDst.DrawTextImage(CFLPoint[Double](0, 0), 'Destination Image', EColor.YELLOW, EColor.BLACK, 30)

		flpDraw = CFLPoint[Double](10.0, 10.0)

		layerSrc.DrawFigureImage(flpDraw, EColor.RED, 3)
		layerDst.DrawFigureImage(flpDraw, EColor.RED, 3)

		fllDraw = CFLLine[Double](15.0, 15.0, 80.0, 30.0)

		layerSrc.DrawFigureImage(fllDraw, EColor.ORANGE, 3)
		layerDst.DrawFigureImage(fllDraw, EColor.ORANGE, 3)

		flrDraw = CFLRect[Double](80.0, 80.0, 150.0, 150.0)

		layerSrc.DrawFigureImage(flrDraw, EColor.YELLOW, 3)
		layerDst.DrawFigureImage(flrDraw, EColor.YELLOW, 3)

		flqDraw = CFLQuad[Double](170.0, 170.0, 200.0, 180.0, 220.0, 210.0, 180.0, 230.0)

		layerSrc.DrawFigureImage(flqDraw, EColor.GREEN, 3)
		layerDst.DrawFigureImage(flqDraw, EColor.GREEN, 3)

		flcDraw = CFLCircle[Double](250.0, 250.0, 50.0)
  
		layerSrc.DrawFigureImage(flcDraw, EColor.BLUE, 3)
		layerDst.DrawFigureImage(flcDraw, EColor.BLUE, 3)

		fleDraw = CFLEllipse[Double](350.0, 350.0, 50.0, 80.0, 25.0)

		layerSrc.DrawFigureImage(fleDraw, EColor.VIOLET, 3)
		layerDst.DrawFigureImage(fleDraw, EColor.VIOLET, 3)

		# 이미지에 그립니다. // Draw in the image.
		if(res := fliImageDrawing.Draw()).IsFail():
			ErrorPrint(res, 'Failed to draw.\n')
			break
		
		# 이미지 뷰에 이미지를 디스플레이 // Display an image in an image view
		if(res := viewImageDst.SetImagePtr(fliImageDrawing)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.\n')
			break
		
		# 이미지 뷰를 갱신 합니다. // Update image view
		viewImageSrc.Invalidate()
		viewImageDst.Invalidate()

		# 이미지 뷰가 종료될 때 까지 기다림 // Wait for the image view to close
		while viewImageSrc.IsAvailable() and viewImageDst.IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function



# 에러 출력 함수 // Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()