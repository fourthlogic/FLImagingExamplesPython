# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliISrcImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImage = CGUIViewImage()

	while True:
		# 이미지 로드 # Load image
		if (res := fliISrcImage.Load("../../ExampleImages/Mask/Moon.flif")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break

		# 이미지 뷰 생성 # Create image view
		if (res := viewImage.Create(400, 0, 912, 612)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break
		

		# 이미지 뷰에 이미지를 디스플레이 # Display an image in an image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage.SetImagePtr(fliISrcImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break
		
		# Mask 객체 생성 # Create Mask object
		mask = CMask()

		# ROI 범위 설정 # Set ROI range
		flcROI = CFLCircle[Double](280, 169, 25)

		# Source 이미지 설정 # Set the source image
		mask.SetSourceImage(fliISrcImage)

		# Source ROI 설정 # Set the Source ROI
		mask.SetSourceROI(flcROI)

		# Mask 색상 지정 # Set mask color
		mvMaskValue = CMultiVar[Double](255, 255, 255)
		mask.SetMask(mvMaskValue)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := (mask.Execute())).IsFail():
			ErrorPrint(res, "Failed to execute Mask.")
			break
		
		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layer = viewImage.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layer.Clear()

		# ROI영역이 어디인지 알기 위해 디스플레이 한다 # Display to find out where ROI is
		# FLImaging의 Figure객체들은 어떤 도형모양이든 상관없이 하나의 함수로 디스플레이가 가능
		if (res := (layer.DrawFigureImage(flcROI, EColor.LIME))).IsFail():
			ErrorPrint(res, "Failed to draw figure")

		# 이미지 뷰 정보 표시 # Display image view information
		flpPosition00 = CFLPoint[Double](0, 0)

		if (res := (layer.DrawTextCanvas(flpPosition00, "Source Image", EColor.YELLOW, EColor.BLACK, 30))).IsFail():
			ErrorPrint(res, "Failed to draw text")
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

	print(f'Error code : res.GetResultCode()\nError name : res.GetString()\n')


if __name__ == '__main__':
    main()