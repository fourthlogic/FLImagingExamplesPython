# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

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
		if(res := fliImage.Load('../../ExampleImages/Blob/AlignBall.flif')).IsFail():
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

		# Blob 객체 생성 // Create Blob object
		algBlob = CBlob()

		# 처리할 이미지 설정 // Set the image to process
		algBlob.SetSourceImage(fliImage)
		# 논리 조건 설정 // Set logical condition
		algBlob.SetLogicalCondition(ELogicalCondition.Less)
		# 임계값 설정,  위의 조건과 아래의 조건이 합쳐지면 127보다 작은 객체를 검출 // Detect objects less than 127 when both the upper and lower logical conditions are met.
		algBlob.SetThreshold(127)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if(res := algBlob.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Blob.')
			break

		# 면적이 500 보다 작거나 같은 객체들을 제거 // Filter out objects whose area is less equal 500.
		if(res := algBlob.Filter(CBlob.EFilterItem.Area, 500, ELogicalCondition.LessEqual)).IsFail():
			ErrorPrint(res, 'Blob filtering algorithm error occurred.')
			break

		# Blob 결과를 얻어오기 위해 FigureArray 선언 // Declare a FigureArray to obtain blob detection results.
		flfaBoundaryRects = CFLFigureArray()

		# Blob 결과들 중 Boundary Rectangle 을 얻어옴 // Obtain the boundary rectangles from the blob results.
		if(res := algBlob.GetResultBoundaryRects(flfaBoundaryRects)[0]).IsFail():
			ErrorPrint(res, 'Failed to get boundary rects from the Blob object.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어를 얻어옴 // Obtain layer from image view for display
		layer1 = viewImageSrc.GetLayer(0)
		layer2 = viewImageSrc.GetLayer(1)
		layer3 = viewImageSrc.GetLayer(2)

		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layer1.Clear()
		layer2.Clear()
		layer3.Clear()

		# 이미지 뷰 정보 표시 // Display image view information
		if(res := layer3.DrawTextCanvas(CFLPoint[Double](0, 0), 'Source Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text\n')
			break

		# flfaBoundaryRects 는 Figure들의 배열이기 때문에 Layer에 넣기만 해도 모두 드로윙이 가능하다.
		# 아래 함수 DrawFigureImage는 Image좌표를 기준으로 하는 Figure를 Drawing 한다는 것을 의미하며 // The function DrawFigureImage below means drawing a picture based on the image coordinates
		# 맨 마지막 두개의 파라미터는 불투명도 값이고 1일경우 불투명, 0일경우 완전 투명을 의미한다. // The last two parameters are opacity values, which mean opacity for 1 day and complete transparency for 0 day.
		# 여기서 0.25이므로 옅은 반투명 상태라고 볼 수 있다.
		# 파라미터 순서 : 레이어 -> Figure 객체 -> 선 색 -> 선 두께 -> 면 색 -> 펜 스타일 -> 선 알파값(불투명도) -> 면 알파값 (불투명도) // Parameter order: Layer -> Figure object -> Line color -> Line thickness -> Face color -> Pen style -> Line alpha value (opacity) -> Area alpha value (opacity)
		if(res := layer1.DrawFigureImage(flfaBoundaryRects, EColor.RED, 1, EColor.RED, EGUIViewImagePenStyle.Solid, 1, 0.25)).IsFail():
			ErrorPrint(res, 'Failed to draw figure objects on the image view.\n')
			break

		# Rect 정보값을 각각 확인하는 코드
		for i in range(flfaBoundaryRects.GetCount()):
			flrRect = flfaBoundaryRects.GetAt(i)

			if flrRect != None:
				print(f'No. {i}')
				print(f'LeftTop     : ({flrRect.left},{flrRect.top})')
				print(f'RightBottom : ({flrRect.right},{flrRect.bottom})')
				print(f'Width  : {flrRect.GetWidth()}')
				print(f'Height : {flrRect.GetHeight()}')
				print(f'Center : ({flrRect.GetCenter().x},{flrRect.GetCenter().y})\n')

				strNumber = "[{}]".format(i)
				strLeftTop = "(LT :{}, {})".format(flrRect.left, flrRect.top)
				strRightBottom = "(RB :{}, {})".format(flrRect.right, flrRect.bottom)
				strInfo = "Width : {}\nHeight : {}\nCenter : ({}, {})".format(flrRect.GetWidth(), flrRect.GetHeight(), flrRect.GetCenter().x, flrRect.GetCenter().y)

				flpLeftTop = CFLPoint[Double](flrRect.left, flrRect.top)
				flpRightBottom = CFLPoint[Double](flrRect.right, flrRect.bottom)
				flpRightTop = CFLPoint[Double](flrRect.right, flrRect.top)

				# 아래 함수 DrawTextImage는 Image좌표를 기준으로 하는 Text를 Drawing 한다는 것을 의미한다.
				# 파라미터 순서 : 레이어 -> 문자열 좌표 -> 문자열 지정 -> 문자열 색 -> 면 색 -> 폰트 크기 -> 실제 크기로 그릴지의 여부 -> 각도 -> 문자열의 위치 기준
				layer2.DrawTextImage(flrRect.GetCenter(), strNumber, EColor.CYAN, EColor.BLACK, 12, False, 0, EGUIViewImageTextAlignment.CENTER_CENTER)
				layer2.DrawTextImage(flpLeftTop, strLeftTop, EColor.YELLOW, EColor.BLACK, 12, False, 0, EGUIViewImageTextAlignment.RIGHT_BOTTOM)
				layer2.DrawTextImage(flpRightBottom, strRightBottom, EColor.YELLOW, EColor.BLACK)
				layer2.DrawTextImage(flpRightTop, strInfo, EColor.LIME, EColor.BLACK, 12, False, 0, EGUIViewImageTextAlignment.LEFT_BOTTOM)

		# 이미지에 출력하기 위해 이미지 드로잉 객채에서 레이어를 얻어옴 // Gets layers from image drawing object for output to image
		layer = fliImageDrawing.GetLayer()

		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layer.Clear()

		# 기존 레이어에 드로잉된 원소들을 해당 레이어 뒤쪽에 추가합니다. // Add elements drawn from an existing layer to the back of that layer.
		if(res := layer.PushBack(layer1)).IsFail():
			ErrorPrint(res, 'Failed to push back.\n')
			break

		if(res := layer.PushBack(layer2)).IsFail():
			ErrorPrint(res, 'Failed to push back.\n')
			break

		# 이미지 뷰 정보 표시 // Display image view information
		if(res := layer.DrawTextImage(CFLPoint[Double](0, 0), 'Destination Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text\n')
			break

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