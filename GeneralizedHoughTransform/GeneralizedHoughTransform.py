# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliSrcImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImage = CGUIViewImage()

	while True:
		# 이미지 로드 # Load image
		if (res := fliSrcImage.Load("../../ExampleImages/HoughTransform/PatternExample.flif")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break

		# 이미지 뷰 생성 # Create image view
		if (res := viewImage.Create(300, 0, 300 + 600, 600)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break
		

		# 이미지 뷰에 이미지를 디스플레이 # Display an image in an image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage.SetImagePtr(fliSrcImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break
		
		# 객체 생성 # Create object
		generalizedHoughTransform = CGeneralizedHoughTransform()

		# Source 이미지 설정 # Set the source image
		generalizedHoughTransform.SetSourceImage(fliSrcImage)

		flfPatternROI = CFLCircle[int](575, 755, 71, 0, 0, 360, ERadialShapeType.Segment)
		generalizedHoughTransform.SetPatternROI(flfPatternROI)

		# Threshold 값 설정 # Set Threshold value
		generalizedHoughTransform.SetPixelThreshold(128)

		# 신뢰도 설정 # set confidence
		generalizedHoughTransform.SetConfidence(0.5)

		# 탐색할 각도 단위 설정 (degree) # Set the angle unit to search (degree)
		generalizedHoughTransform.SetAngleTolerance(90)

		# 탐색할 크기 설정 (percent) # Set the scale tolerance to search (percent)
		generalizedHoughTransform.SetScaleTolerance(10)

		# 최대 검출 수 설정 # Set the maximum number of detections
		generalizedHoughTransform.SetMaxObjectCount(100)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := (generalizedHoughTransform.Execute())).IsFail():
		
			ErrorPrint(res, "Failed to execute.")
			break
		
		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layer = viewImage.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layer.Clear()

		# Result 갯수 가져오기 # Get the number of results
		i64ResultCount = generalizedHoughTransform.GetDetectedObjectCount()

		Console.WriteLine("Result Count : {0}", i64ResultCount)

		if i64ResultCount > 0:
			flfaDetectedObjects = CFLFigureArray()
			generalizedHoughTransform.GetDetectedObjects(flfaDetectedObjects)

			# 이미지 뷰에 검출된 객체 출력 # Output the detected object to the image view
			if (res := (layer.DrawFigureImage(flfaDetectedObjects, EColor.BRIGHTCYAN, 2))).IsFail():
			
				ErrorPrint(res, "Failed to draw Figure")
				break

		# 이미지 뷰를 갱신 합니다. # Update image view
		viewImage.Invalidate(True)

		# 이미지 뷰가 종료될 때 까지 기다림 # Wait for the image view to close
		while viewImage.IsAvailable():
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