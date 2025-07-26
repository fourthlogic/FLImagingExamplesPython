# FLImagingClrPy 선언 // Declare FLImagingClrPy
from asyncio.windows_events import NULL
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')

# 메인 함수 // Main function
def main():
	# 이미지 객체 선언 // Declare the image object
	fliImage = CFLImage()

	# 이미지 뷰 선언 // Declare the image view
	viewImage = CGUIViewImage()

	res = CResult()

	while True:
		# 이미지 로드 // Load the image
		if (res := fliImage.Load('../../ExampleImages/GridOfDotsDetector/GridOfDots.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# 이미지 뷰 생성 // Create the image view
		if (res := viewImage.Create(400, 0, 1040, 480)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# 이미지 뷰에 이미지를 디스플레이 // Display the image in the image view
		if (res := viewImage.SetImagePtr(fliImage))[0].IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# GridOfDots Detector 객체 생성 // Create a GridOfDots Detector object
		gridofDots = CGridOfDotsDetector();

		# 처리할 이미지 설정 // Set the image to process
		gridofDots.SetSourceImage(fliImage)

		# 알고리즘 수행 // Execute the Algoritm
		if (res := gridofDots.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute GridOfDots Detector.\n')
			break

		layer = viewImage.GetLayer(0)
		layer.Clear()

		flqRegion = CFLQuad[Double]()
		flaPoints = List[List[TPoint[Double]]]()
		i64PageIndex = 0
		i64BoardCount = gridofDots.GetResultBoardCount(i64PageIndex)

		for i32BoardIndex in range(i64BoardCount):
			gridofDots.GetResultCenterPoints(i64PageIndex, i64BoardCount, flaPoints)
			gridofDots.GetResultBoardRegion(i64PageIndex, i64BoardCount, flqRegion)
			i64ResultRow = gridofDots.GetResultBoardRows(i64PageIndex, i64BoardCount)
			i64ResultCol = gridofDots.GetResultBoardColumns(i64PageIndex, i64BoardCount)
			f64AverageCellPitch = gridofDots.GetResultBoardAverageCellPitch(i64PageIndex, i64BoardCount)

			flpPoint0 = CFLPoint[Double](flqRegion.flpPoints[0])
			flpPoint1 = CFLPoint[Double](flqRegion.flpPoints[1])

			f64Width = flpPoint0.GetDistance(flpPoint1)
			f64Angle = flpPoint0.GetAngle(flpPoint1)

			if (res := layer.DrawFigureImage(flqRegion, EColor.BLACK, 3)).IsFail():
				ErrorPrint(res, 'Failed to draw figure.')
				break

			if (res := layer.DrawFigureImage(flqRegion, EColor.YELLOW, 1)).IsFail():
				ErrorPrint(res, 'Failed to draw figure.')
				break

			if (res := layer.DrawTextImage(flpPoint0, "({0} X {1}) Pitch [{2}]".format(i64ResultCol, i64ResultRow, f64AverageCellPitch), EColor.YELLOW, EColor.BLACK, int(f64Width / 16), True, f64Angle, EGUIViewImageTextAlignment.LEFT_BOTTOM)).IsFail():
				ErrorPrint(res, 'Failed to draw text.')
				break

			crTable = [EColor.RED, EColor.LIME, EColor.CYAN]
			flpLastPoint = CFLPoint[Double]()
			i32LineTransition = 0
			i32VertexNumber = 0
			f64Pitch = 0.

			for j in range(flaPoints.Count):
				fla2 = flaPoints[j]

				if j > 0:
					fla20 = CFLPoint[Double]()
					fla20.x = fla2[0].x
					fla20.y = fla2[0].y

					fll = CFLLine[Double](flpLastPoint, fla20)

					if (res := layer.DrawFigureImage(fll, EColor.BLACK, 5)).IsFail():
						ErrorPrint(res, 'Failed to draw figure.')
						break

					if (res := layer.DrawFigureImage(fll, EColor.YELLOW, 3)).IsFail():
						ErrorPrint(res, 'Failed to draw figure.')
						break

				for k in range(fla2.Count):
					if k > 0:
						fla2k = CFLPoint[Double]()
						fla2k.x = fla2[k].x
						fla2k.y = fla2[k].y

						fll = CFLLine[Double](flpLastPoint, fla2k)

						if (res := layer.DrawFigureImage(fll, EColor.BLACK, 5)).IsFail():
							ErrorPrint(res, 'Failed to draw figure.')
							break

						if (res := layer.DrawFigureImage(fll, crTable[i32LineTransition % 3], 3)).IsFail():
							ErrorPrint(res, 'Failed to draw figure.')
							break

						i32LineTransition += 1

					fla2kk = CFLPoint[Double]()
					fla2kk.x = fla2[k].x
					fla2kk.y = fla2[k].y
					flpLastPoint = fla2kk

			i32LineTransition = 0

			for j in range(flaPoints.Count):
				fla2 = flaPoints[j];
				fla2Point0 = CFLPoint[Double]();
				fla2Point1 = CFLPoint[Double]();
				fla2Point0.x = fla2[0].x;
				fla2Point0.y = fla2[0].y;
				fla2Point1.x = fla2[1].x;
				fla2Point1.y = fla2[1].y;

				f64Angle = fla2Point0.GetAngle(fla2Point1)

				for k in range(fla2.Count):
					crTextColor = crTable[i32LineTransition % 3]
					i32LineTransition += 1
					i32CheckValue = (i32VertexNumber + 1) % fla2.Count

					if i32CheckValue == 0:
						crTextColor = EColor.YELLOW
					else:
						f64Dx = fla2[k + 1].x - fla2[k].x
						f64Dy = fla2[k + 1].y - fla2[k].y
						f64Pitch = (f64Dx * f64Dx + f64Dy * f64Dy) ** 0.5

					if j == 0:
						f64Dx = flaPoints[1][k].x - flaPoints[0][k].x
						f64Dy = flaPoints[1][k].y - flaPoints[0][k].y
						f64Pitch = min(f64Pitch, (f64Dx * f64Dx + f64Dy * f64Dy) ** 0.5)
					else:
						f64Dx = flaPoints[j][k].x - flaPoints[j - 1][k].x
						f64Dy = flaPoints[j][k].y - flaPoints[j - 1][k].y
						f64Pitch = min(f64Pitch, (f64Dx * f64Dx + f64Dy * f64Dy) ** 0.5)
					
					flpDisPlay = CFLPoint[Double]()
					flpDisPlay.x = fla2[k].x
					flpDisPlay.y = fla2[k].y

					if (res := layer.DrawTextImage(flpDisPlay, "{0}".format(i32VertexNumber), crTextColor, EColor.BLACK, int(f64Pitch / 3), True, f64Angle)).IsFail():
						ErrorPrint(res, 'Failed to draw text.')
						break

					i32VertexNumber += 1

					if k > 0:
						flpAngle0 = CFLPoint[Double](fla2[k].x, fla2[k].y)
						flpAngle1 = CFLPoint[Double](fla2[k - 1].x, fla2[k - 1].y)
						f64Angle = flpAngle1.GetAngle(flpAngle0)

				i32LineTransition -= 1

		viewImage.Invalidate()

		# 이미지 뷰가 종료될 때 까지 기다림 // Wait for the imageview to close
		while viewImage.IsAvailable():
			CThreadUtilities.Sleep(1)

		break

if __name__ == '__main__':
    main()



