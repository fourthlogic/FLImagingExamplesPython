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

		bCalcGeometricMoment = True
		bCalcCentroidMoment = True
		bCalcCentralMoment = True
		bCalcNormalizedCentralMoment = True
		bCalcHuMoment = True

		# 계산 대상에 기하학적 모멘트를 포함합니다. # Include the geometric moment in the computed object.
		moment.EnableGeometricMoment(bCalcGeometricMoment)
		# 계산 대상에 도심 모멘트를 포함합니다. # Include the centroid moment in the calculation target.
		moment.EnableCentroidMoment(bCalcCentroidMoment)
		# 계산 대상에 중심 모멘트를 포함합니다. # Include the central moment in the calculation target.
		moment.EnableCentralMoment(bCalcCentralMoment)
		# 계산 대상에 정규화된 중심 모멘트를 포함합니다. # Include the normalized central moment in the computed target.
		moment.EnableNormalizedCentralMoment(bCalcNormalizedCentralMoment)
		# 계산 대상에 휴(불변) 모멘트를 포함합니다. # Include the idle (invariant) moment in the calculation target.
		moment.EnableHuMoment(bCalcHuMoment)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := moment.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Moment.')
			break

		# 모멘트 결과들을 가져옵니다. # Get the moment results.
		results = CMoment.SMoment()

		moment.GetMoment(results)

		# 모멘트 결과를 Console창에 출력 # Output the moment result to the console window
		if bCalcGeometricMoment:
			print('< Geometric Moment >')
			print(f' Moment 00 : {results.pSGeometricMoments.f64GeometricM00}')
			print(f' Moment 10 : {results.pSGeometricMoments.f64GeometricM10}')
			print(f' Moment 01 : {results.pSGeometricMoments.f64GeometricM01}')
			print(f' Moment 20 : {results.pSGeometricMoments.f64GeometricM20}')
			print(f' Moment 11 : {results.pSGeometricMoments.f64GeometricM11}')
			print(f' Moment 02 : {results.pSGeometricMoments.f64GeometricM02}')
			print(f' Moment 30 : {results.pSGeometricMoments.f64GeometricM30}')
			print(f' Moment 21 : {results.pSGeometricMoments.f64GeometricM21}')
			print(f' Moment 12 : {results.pSGeometricMoments.f64GeometricM12}')
			print(f' Moment 03 : {results.pSGeometricMoments.f64GeometricM03}')
			print('')

		if bCalcCentroidMoment:
			print('< Centroid Moment > ')
			print(f' Moment Centroid X : {results.pSCentroidMoment.f64CentroidX}')
			print(f' Moment Centroid Y : {results.pSCentroidMoment.f64CentroidY}')
			print('')

		if bCalcCentralMoment:
			print('< Central Moment > ')
			print(f' Moment 00 : {results.pSCentralMoments.f64CentralM00}')
			print(f' Moment 10 : {results.pSCentralMoments.f64CentralM10}')
			print(f' Moment 01 : {results.pSCentralMoments.f64CentralM01}')
			print(f' Moment 20 : {results.pSCentralMoments.f64CentralM20}')
			print(f' Moment 11 : {results.pSCentralMoments.f64CentralM11}')
			print(f' Moment 02 : {results.pSCentralMoments.f64CentralM02}')
			print(f' Moment 30 : {results.pSCentralMoments.f64CentralM30}')
			print(f' Moment 21 : {results.pSCentralMoments.f64CentralM21}')
			print(f' Moment 12 : {results.pSCentralMoments.f64CentralM12}')
			print(f' Moment 03 : {results.pSCentralMoments.f64CentralM03}')
			print('')

		if bCalcNormalizedCentralMoment:
			print('< Normalized Central Moment > ')
			print(f' Moment 00 : {results.pSNormalizedCentralMoments.f64NormalizedCentralM00}')
			print(f' Moment 10 : {results.pSNormalizedCentralMoments.f64NormalizedCentralM10}')
			print(f' Moment 01 : {results.pSNormalizedCentralMoments.f64NormalizedCentralM01}')
			print(f' Moment 20 : {results.pSNormalizedCentralMoments.f64NormalizedCentralM20}')
			print(f' Moment 11 : {results.pSNormalizedCentralMoments.f64NormalizedCentralM11}')
			print(f' Moment 02 : {results.pSNormalizedCentralMoments.f64NormalizedCentralM02}')
			print(f' Moment 30 : {results.pSNormalizedCentralMoments.f64NormalizedCentralM30}')
			print(f' Moment 21 : {results.pSNormalizedCentralMoments.f64NormalizedCentralM21}')
			print(f' Moment 12 : {results.pSNormalizedCentralMoments.f64NormalizedCentralM12}')
			print(f' Moment 03 : {results.pSNormalizedCentralMoments.f64NormalizedCentralM03}')
			print('')

		if bCalcHuMoment:
			print('< Hu Moment > ')
			print(f' Hu 0 : {results.pSHuMoments.f64Hu0}')
			print(f' Hu 1 : {results.pSHuMoments.f64Hu1}')
			print(f' Hu 2 : {results.pSHuMoments.f64Hu2}')
			print(f' Hu 3 : {results.pSHuMoments.f64Hu3}')
			print(f' Hu 4 : {results.pSHuMoments.f64Hu4}')
			print(f' Hu 5 : {results.pSHuMoments.f64Hu5}')
			print(f' Hu 6 : {results.pSHuMoments.f64Hu6}')
			print('')

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