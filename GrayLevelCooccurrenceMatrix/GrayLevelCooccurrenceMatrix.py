# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

CLibraryUtilities.Initialize()

# Error 출력 함수 import // Import Error Output Function
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Common"))

from ErrorPrint import *


# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliSrcImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImage = CGUIViewImage()

	while True:
		
		# Source 이미지 로드 # Load the source image
		if (res := fliSrcImage.Load('../../ExampleImages/GrayLevelCooccurrenceMatrix/Texture.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 뷰 생성 # Create source image view
		if (res := viewImage.Create(400, 0, 912, 612)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage.SetImagePtr(fliSrcImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# Gray Level Cooccurrence Matrix 객체 생성 # Create Gray Level Cooccurrence Matrix object
		flaGLCM = CGrayLevelCooccurrenceMatrix()
		
		# ROI 지정 # Create ROI
		flfSourceROI = CFLRect[Double](143.508137, 70.054249, 295.117540, 213.562386, 0.000000)

		# Source 이미지 설정 # Set the source image
		flaGLCM.SetSourceImage(fliSrcImage)
		
		# Source ROI 영역 지정 # set Source ROI 
		flaGLCM.SetSourceROI(flfSourceROI)
		
		# grayLevel 설정(2^8 = 256) # Set gray level (2^8 = 256)
		flaGLCM.SetGrayLevel(8)

		# Matrix Direction 0도 설정 # Set Matrix Direction 0 Degree
		flaGLCM.SetDirection(CGrayLevelCooccurrenceMatrix.EDirection.Degree0)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := flaGLCM.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Gray Level Cooccurrence Matrix.')
			break
		
		# 결과값을 받아올 List 컨테이너 생성 # Create the List object to push the result
		listEnergy = List[List[Double]]()
		listCorrelation = List[List[Double]]()
		listHomogeneity = List[List[Double]]()
		listContrast = List[List[Double]]()

		# 이미지 전체(혹은 ROI 영역) 픽셀값의 Energy를 구하는 함수 # Function that calculate Energy of the image(or the region of ROI)
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := flaGLCM.GetResultEnergy(listEnergy)[0]).IsFail():
			ErrorPrint(res, "No Result")
			break

		# 이미지 전체(혹은 ROI 영역) 픽셀값의 Correlation를 구하는 함수 # Function that calculate Correlation of the image(or the region of ROI)
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := flaGLCM.GetResultCorrelation(listCorrelation)[0]).IsFail():
			ErrorPrint(res, "No Result")
			break

		# 이미지 전체(혹은 ROI 영역) 픽셀값의 Homogeneity를 구하는 함수 # Function that calculate Homogeneity of the image(or the region of ROI)
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := flaGLCM.GetResultHomogeneity(listHomogeneity)[0]).IsFail():
			ErrorPrint(res, "No Result")
			break

		# 이미지 전체(혹은 ROI 영역) 픽셀값의 Contrast를 구하는 함수 # Function that calculate Contrast of the image(or the region of ROI)
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := flaGLCM.GetResultContrast(listContrast)[0]).IsFail():
			ErrorPrint(res, "No Result")
			break
		
		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layer = viewImage.GetLayer(0)

		if (res := layer.DrawFigureImage(flfSourceROI, EColor.LIME)).IsFail():
			ErrorPrint(res, 'Failed to draw figure.')
			break


		strText = ""

		for i32PageIdx in range(listEnergy.Count):
			# strText += f"Page.No {i32PageIdx} "

			for i32Ch in range(listEnergy[i32PageIdx].Count):
				# strText += f"\nChannel {i32Ch} "
				strText += f"Energy {listEnergy[i32PageIdx][i32Ch]:.9} "
				strText += f"\nCorrelation {listCorrelation[i32PageIdx][i32Ch]:.9} "
				strText += f"\nHomogeneity {listHomogeneity[i32PageIdx][i32Ch]:.9} "
				strText += f"\nContrast {listContrast[i32PageIdx][i32Ch]:.9} "

			# strText += "\n\n"

		print(strText)

		# 이미지 뷰 정보 표시 # Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if (res := layer.DrawTextCanvas(flpPoint, strText, EColor.YELLOW, EColor.BLACK, 25)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 이미지 뷰를 갱신 # Update image view
		viewImage.Invalidate(True)
		
		# 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImage.IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function


if __name__ == '__main__':
    main()