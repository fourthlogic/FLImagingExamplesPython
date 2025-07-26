# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# Error 출력 함수 import // Import Error Output Function
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Common"))

from ErrorPrint import *


# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliISrcImage = CFLImage()
	fliIDstImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImage = [CGUIViewImage() for i in range(2)]
	
	while True:
		
		# Source 이미지 로드 # Load the source image
		if (res := fliISrcImage.Load('../../ExampleImages/Integral/Lake.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 # Create destination image as same as source image
		if (res := fliIDstImage.Assign(fliISrcImage)).IsFail():
			ErrorPrint(res, 'Failed to assign the image.')
			break

		# 이미지 뷰 생성 # Create source image view
		if (res := viewImage[0].Create(300, 0, 300 + 520, 430)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# 이미지 뷰 생성 # Create source image view
		if (res := viewImage[1].Create(300 + 520, 0, 300 + 520 * 2, 430)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage[0].SynchronizePointOfView(viewImage[1])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break
		
		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage[0].SynchronizeWindow(viewImage[1])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break
		
		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage[0].SetImagePtr(fliISrcImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage[1].SetImagePtr(fliIDstImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		mvCoefficients = CMultiVar[Double](1.7, 2.1, 1.5)

		# Integral 객체 생성 # Create Integral object
		Integral = CIntegral()

		# Source 이미지 설정 # Set source image 
		Integral.SetSourceImage(fliISrcImage)

		# Destination 이미지 설정 # Set destination image
		Integral.SetDestinationImage(fliIDstImage)

		# 적분합 자료형 타입을 설정합니다. # Set integral data type.
		Integral.SetDataType(CIntegral.EDataType.Uint32)

		# Integral 누적합 연산 모드 설정 # Set integration operation method.
		# ECalculationMode_Polynomial : ax^2 + bx + c 다항식 방식의 합 # ECalculationMode_Polynomial : Polynomial sum
		Integral.SetCalculationMode(CIntegral.ECalculationMode.Polynomial)

		# ax^2 + bx + c 계수 설정(a = 1.7, b = 2.1, c = 1.5) # ax^2 + bx + c Setting the coefficient (a = 1.7, b = 2.1, c = 1.5)
		Integral.SetCoefficients(mvCoefficients)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := Integral.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Integral.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layer1 = viewImage[0].GetLayer(0)
		layer2 = viewImage[1].GetLayer(0)
		
		flpPoint = CFLPoint[Double](0, 0)
		
		# View 정보를 디스플레이 합니다. # Display View information.
		if (res := layer1.DrawTextImage(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := layer2.DrawTextImage(flpPoint, 'Destination Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		# 이미지 뷰를 갱신 합니다. # Update the image view.
		for i in range(2):
			viewImage[i].ZoomFit()
			viewImage[i].Invalidate(True)
			
		# 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImage[0].IsAvailable() and viewImage[1].IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function


if __name__ == '__main__':
    main()