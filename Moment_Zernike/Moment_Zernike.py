# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliSourceImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSrc = CGUIViewImage()

	while True:
		
		# Source 이미지 로드 # Load the source image
		if (res := fliSourceImage.Load('../../ExampleImages/Moment/airEdge.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 뷰 생성 # Create source image view
		if (res := viewImageSrc.Create(400, 0, 1424, 768)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# Moment 객체 생성 # Create Moment object
		moment = CMoment()

		# ROI 설정 # Set the ROI
		flrROI = CFLRect[int](15, 150, 420, 280)

		# Source 이미지 설정 # Set the source image
		moment.SetSourceImage(fliSourceImage)

		# Source ROI 설정 # Set the source ROI
		moment.SetSourceROI(flrROI)

		# 처리할 이미지의 이진화 이미지로 판단 유무 설정 # Set whether to judge the image to be processed as a binarized image
		# 이진화 이미지로 판단할 경우 0이 아닌 모든 화소값은 1로 처리 # When judging as a binarized image, all non-zero pixel values are treated as 1
		moment.EnableBinaryImage(True)

		# 계산 대상에 저니키 모멘트 N, M 파라미터를 추가합니다. # Add Zernike Moment N, M parameters to the calculation target.
		moment.AddZernike(1, -1)
		moment.AddZernike(1, 1)
		moment.AddZernike(3, -3)
		moment.AddZernike(3, -1)
		moment.AddZernike(3, 1)
		moment.AddZernike(3, 3)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := moment.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Moment.')
			break

		# 모멘트 결과들을 가져옵니다. # Get the moment results.
		zernike = CMoment.SZernike()
		i64ZernikeCount = moment.GetZernikeCount()

		for i in range(i64ZernikeCount):
			moment.GetZernike(zernike, i)
			print(f'Zernike N = {zernike.i32N}, M = {zernike.i32M}, RealValue : {zernike.f64ZernikeReal}, Imaginary : {zernike.f64ZernikeImag}')

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSrc.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSource.Clear()

		# ROI 영역 디스플레이 # Display ROI area
		flpPoint = CFLPoint[Double](0, 0)

		if (res := layerSource.DrawFigureImage(flrROI, EColor.BLUE)).IsFail():
			ErrorPrint(res, "Failed to draw figure")
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