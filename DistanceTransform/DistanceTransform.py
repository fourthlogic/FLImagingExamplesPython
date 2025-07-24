# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 // Main function
def main():

	# 이미지 객체 선언 // Declare the image object
	fliSourceImage = CFLImage()
	fliDestinationImage = [CFLImage(), CFLImage(), CFLImage(), CFLImage()]

	# 이미지 뷰 선언 // Declare the image view
	viewImageSrc = CGUIViewImage()
	viewImageDst= [CGUIViewImage(), CGUIViewImage(), CGUIViewImage(), CGUIViewImage()]

	# 연산 방식 선언 // Declare measeure method
	eMeasurementMethod = [CDistanceTransform.EMeasurementMethod.CityBlock, CDistanceTransform.EMeasurementMethod.Chessboard, CDistanceTransform.EMeasurementMethod.Euclid, CDistanceTransform.EMeasurementMethod.QuasiEuclid]

	while True:
		
		# Source 이미지 로드 // Load the source image
		if (res := fliSourceImage.Load('../../ExampleImages/DistanceTransform/circle.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 // Create destination image as same as source image
		if (res := fliDestinationImage[0].Assign(fliSourceImage)).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		if (res := fliDestinationImage[1].Assign(fliSourceImage)).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		if (res := fliDestinationImage[2].Assign(fliSourceImage)).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		if (res := fliDestinationImage[3].Assign(fliSourceImage)).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 뷰 생성 // Create source image view
		if (res := viewImageSrc.Create(100, 0, 612, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# Destination 이미지 뷰 생성 // Create the destination image view
		if (res := viewImageDst[0].Create(612, 0, 1124, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		if (res := viewImageDst[1].Create(100, 512, 612, 1024)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		if (res := viewImageDst[2].Create(612, 512, 1124, 1024)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		if (res := viewImageDst[3].Create(1124, 512, 1636, 1024)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizePointOfView(viewImageDst[0])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		if (res := viewImageSrc.SynchronizePointOfView(viewImageDst[1])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		if (res := viewImageSrc.SynchronizePointOfView(viewImageDst[2])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		if (res := viewImageSrc.SynchronizePointOfView(viewImageDst[3])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 // Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 // Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDst[0].SetImagePtr(fliDestinationImage[0])[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		if (res := viewImageDst[1].SetImagePtr(fliDestinationImage[1])[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		if (res := viewImageDst[2].SetImagePtr(fliDestinationImage[2])[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		if (res := viewImageDst[3].SetImagePtr(fliDestinationImage[3])[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizeWindow(viewImageDst[0])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break
			
		if (res := viewImageSrc.SynchronizeWindow(viewImageDst[1])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break
			
		if (res := viewImageSrc.SynchronizeWindow(viewImageDst[2])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		if (res := viewImageSrc.SynchronizeWindow(viewImageDst[3])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# Distance Transform 객체 생성 // Create Distance Transform object
		distance = CDistanceTransform()

		# Source 이미지 설정 // Set the source image
		distance.SetSourceImage(fliSourceImage)

		for i in range(4):
			# Destination 이미지 설정 // Set the destination image
			distance.SetDestinationImage(fliDestinationImage[i])
	
			# 측정 방식 지정 // Set Measure Method
			distance.SetMeasurementMethod(eMeasurementMethod[i])

			# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
			if (res := distance.Execute()).IsFail():
				ErrorPrint(res, 'Failed to execute Distance Transform.')
				break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSrc.GetLayer(0)
		layerDestination = [viewImageDst[0].GetLayer(0), viewImageDst[1].GetLayer(0), viewImageDst[2].GetLayer(0), viewImageDst[3].GetLayer(0)]

		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layerSource.Clear()
		layerDestination[0].Clear()
		layerDestination[1].Clear()
		layerDestination[2].Clear()
		layerDestination[3].Clear()

		# 이미지 뷰 정보 표시 // Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		res = layerSource.DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 30)

		if res.IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		res = layerDestination[0].DrawTextCanvas(flpPoint, 'Destination Image CityBlock', EColor.YELLOW, EColor.BLACK, 30)

		if res.IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		res = layerDestination[1].DrawTextCanvas(flpPoint, 'Destination Image Chessboard', EColor.YELLOW, EColor.BLACK, 30)

		if res.IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		res = layerDestination[2].DrawTextCanvas(flpPoint, 'Destination Image Euclid', EColor.YELLOW, EColor.BLACK, 30)

		if res.IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		res = layerDestination[3].DrawTextCanvas(flpPoint, 'Destination Image Qusai Euclid', EColor.YELLOW, EColor.BLACK, 30)

		if res.IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 이미지 뷰를 갱신 // Update image view
		viewImageSrc.Invalidate(True)
		viewImageDst[0].Invalidate(True)
		viewImageDst[1].Invalidate(True)
		viewImageDst[2].Invalidate(True)
		viewImageDst[3].Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 // Wait until the image view is closed before exiting
		while viewImageSrc.IsAvailable() and viewImageDst[0].IsAvailable() and viewImageDst[1].IsAvailable() and viewImageDst[2].IsAvailable() and viewImageDst[3].IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function



# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}')


if __name__ == '__main__':
    main()