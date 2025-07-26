# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# 메인 함수 // Main function
def main():

	# 이미지 객체 선언 // Declare the image object
	fliSourceImage = CFLImage()
	fliDestinationImage = CFLImage()

	# 이미지 뷰 선언 // Declare the image view
	viewImageSrc = CGUIViewImage()
	viewImageOpr = CGUIViewImage()
	viewImageDst = CGUIViewImage()

	while True:
		
		# Source 이미지 로드 // Load the source image
		if (res := fliSourceImage.Load('../../ExampleImages/Homography/calendar.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 // Create destination image as same as source image
		if (res := fliDestinationImage.Load("../../ExampleImages/Homography/space.flif")).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 뷰 생성 // Create source image view
		if (res := viewImageSrc.Create(100, 0, 550, 480)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰 생성 // Create the destination image view
		if (res := viewImageDst.Create(550, 0, 1050, 480)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizePointOfView(viewImageDst)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 // Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 // Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDst.SetImagePtr(fliDestinationImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizeWindow(viewImageDst)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# 객체 생성 // Create object
		homography = CHomography()

		# Source 이미지 설정 // Set the source image
		homography.SetSourceImage(fliSourceImage)

		# Destination 이미지 설정 // Set the destination image
		homography.SetDestinationImage(fliDestinationImage)

		# Source 이미지의 투영 영역 범위 설정 // Set the range of the projection area of the Source image
		flpaSourceProjection = CFLPointArray();
		flpaSourceProjection.PushBack(CFLPoint[float](564.137931, 316.551724));
		flpaSourceProjection.PushBack(CFLPoint[float](363.448276, 438.620690));
		flpaSourceProjection.PushBack(CFLPoint[float](220.689655, 283.448276));
		flpaSourceProjection.PushBack(CFLPoint[float](363.448276, 192.413793));
		flpaSourceProjection.PushBack(CFLPoint[float](121.379310, 163.448276));
		flpaSourceProjection.PushBack(CFLPoint[float](504.137931, 122.068966));
		flpaSourceProjection.PushBack(CFLPoint[float](80.000000, 120.000000));
		flpaSourceProjection.PushBack(CFLPoint[float](268.275862, 113.793103));
		flpaSourceProjection.PushBack(CFLPoint[float](32.413793, 380.689655));
		flpaSourceProjection.PushBack(CFLPoint[float](53.103448, 74.482759));
		flpaSourceProjection.PushBack(CFLPoint[float](214.482759, 68.275862));
		flpaSourceProjection.PushBack(CFLPoint[float](373.793103, 64.137931));
		flpaSourceProjection.PushBack(CFLPoint[float](160.689655, 28.965517));

		# Source 이미지의 투영 영역 지정 // Set the projection area of the Source image
		homography.SetSourceProjection(flpaSourceProjection);

		# Destination 이미지의 투영 영역 범위 설정 // Set the range of the projection area of the destination image
		flpaDestinationProjection = CFLPointArray();
		flpaDestinationProjection.PushBack(CFLPoint[float](529.223526, 181.280286));
		flpaDestinationProjection.PushBack(CFLPoint[float](528.781754, 301.190422));
		flpaDestinationProjection.PushBack(CFLPoint[float](403.991849, 315.695190));
		flpaDestinationProjection.PushBack(CFLPoint[float](399.088041, 186.290795));
		flpaDestinationProjection.PushBack(CFLPoint[float](262.810194, 316.159206));
		flpaDestinationProjection.PushBack(CFLPoint[float](401.317045, 82.478995));
		flpaDestinationProjection.PushBack(CFLPoint[float](122.572625, 317.202957));
		flpaDestinationProjection.PushBack(CFLPoint[float](268.777064, 182.517166));
		flpaDestinationProjection.PushBack(CFLPoint[float](408.998534, 438.577031));
		flpaDestinationProjection.PushBack(CFLPoint[float](7.275742, 322.207494));
		flpaDestinationProjection.PushBack(CFLPoint[float](131.900147, 180.456139));
		flpaDestinationProjection.PushBack(CFLPoint[float](263.629186, 75.928433));
		flpaDestinationProjection.PushBack(CFLPoint[float](1.266525, 182.189349));

		# Destination 이미지의 투영 영역 지정 // Set the projection area of the destination image
		res = homography.SetDestinationProjection(flpaDestinationProjection);

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := homography.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSrc.GetLayer(0)
		layerDestination = viewImageDst.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layerSource.Clear()
		layerDestination.Clear()

		# 이미지 뷰 정보 표시 // Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if (res := layerSource.DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := layerDestination.DrawTextCanvas(flpPoint, 'Destination Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break	

		# FLImaging의 Figure객체들은 어떤 도형모양이든 상관없이 하나의 함수로 디스플레이가 가능 // FLImaging's figure objects can be displayed with a single function, regardless of the shape of the figure
		# Source Projection 영역이 어디인지 알기 위해 디스플레이 한다 // Display to know where the Source Projection area is
		if (res := layerSource.DrawFigureImage(flpaSourceProjection, EColor.LIME, 3)).IsFail():
			ErrorPrint(res, 'Failed to draw Figure.')
			break		

		# Destination Projection 영역이 어디인지 알기 위해 디스플레이 한다 // Display to know where the Source Projection area is
		if (res := layerDestination.DrawFigureImage(flpaDestinationProjection, EColor.LIME, 3)).IsFail():
			ErrorPrint(res, 'Failed to draw Figure.')
			break	

		# 이미지 뷰를 갱신 // Update image view
		viewImageSrc.Invalidate(True)
		viewImageDst.ZoomFit()
		viewImageDst.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 // Wait until the image view is closed before exiting
		while viewImageSrc.IsAvailable() and viewImageDst.IsAvailable():
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




