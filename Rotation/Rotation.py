# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# Error 출력 함수 import # Import Error Output Function
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "Common"))

from ErrorPrint import *


# 메인 함수 # Main function
def main():
	# 이미지 객체 선언 # Declare the image object
	fliSrcImage = CFLImage()
	fliDstImage = [CFLImage() for i in range(3)]

	# 이미지 뷰 선언 # Declare the image view
	viewSrcImage = CGUIViewImage()
	viewDstImage = [CGUIViewImage() for i in range(3)]
	
	while True:
		
		# Source 이미지 로드 # Load the source image
		if (res := fliSrcImage.Load('../../ExampleImages/Affine/Sunset.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 # Create destination image as same as source image
		if (res := fliDstImage[0].Assign(fliSrcImage)).IsFail():
			ErrorPrint(res, 'Failed to assign the image.')
			break
		
		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 # Create destination image as same as source image
		if (res := fliDstImage[1].Assign(fliSrcImage)).IsFail():
			ErrorPrint(res, 'Failed to assign the image.')
			break
		
		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 # Create destination image as same as source image
		if (res := fliDstImage[2].Assign(fliSrcImage)).IsFail():
			ErrorPrint(res, 'Failed to assign the image.')
			break
		
		# 이미지 뷰 생성 # Create source image view
		if (res := viewSrcImage.Create(400, 0, 800, 400)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# 이미지 뷰 생성 # Create source image view
		if (res := viewDstImage[0].Create(800, 0, 1200, 400)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# 이미지 뷰 생성 # Create source image view
		if (res := viewDstImage[1].Create(400, 400, 800, 800)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# 이미지 뷰 생성 # Create source image view
		if (res := viewDstImage[2].Create(800, 400, 1200, 800)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewSrcImage.SetImagePtr(fliSrcImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewDstImage[0].SetImagePtr(fliDstImage[0])[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewDstImage[1].SetImagePtr(fliDstImage[1])[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewDstImage[2].SetImagePtr(fliDstImage[2])[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewSrcImage.SynchronizeWindow(viewDstImage[0])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break
		
		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewSrcImage.SynchronizeWindow(viewDstImage[1])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break
		
		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewSrcImage.SynchronizeWindow(viewDstImage[2])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break
		
		# rotation 객체 생성 # Create rotation object
		rotation = CRotation()
		# Source 이미지 설정 # set source image
		rotation.SetSourceImage(fliDstImage[0])
		# rotation 각도 설정 # Set Angle
		rotation.SetAngle(30.0)
		
		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := rotation.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute rotation.')
			break

		mvBlankColor = CMultiVar[Double](0, 0, 0)

		# Source 이미지 설정 # set source image
		rotation.SetSourceImage(fliSrcImage)
		# Destination 이미지 설정 # set destination image
		rotation.SetDestinationImage(fliDstImage[1])
		# 공백 영역을 지정한 색으로 채우도록 설정 # Set fill blank color mode
		rotation.EnableFillBlankColorMode(True)
		# 공백 영역 색상 지정 # Set blank color value
		rotation.SetBlankColor(mvBlankColor)
		
		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := rotation.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute rotation.')
			break

		# Destination 이미지 설정 # set destination image
		rotation.SetDestinationImage(fliDstImage[2])
		# rotation 변환 방식 픽셀로 설정 # Set Resize mode
		rotation.SetResizeMethod(EResizeMethod.Resize)
		
		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := rotation.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute rotation.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSrc1 = viewSrcImage.GetLayer(0)
		layerDst1 = viewDstImage[0].GetLayer(0)
		layerDst2 = viewDstImage[1].GetLayer(0)
		layerDst3 = viewDstImage[2].GetLayer(0)
		
		flpPoint = CFLPoint[Double](0, 0)
		
		# View 정보를 디스플레이 합니다. # Display View information.
		if (res := layerSrc1.DrawTextImage(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := layerDst1.DrawTextImage(flpPoint, 'Destination Image1', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		if (res := layerDst2.DrawTextImage(flpPoint, 'Destination Image2', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := layerDst3.DrawTextImage(flpPoint, 'Destination Image3', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 이미지 뷰를 갱신 합니다. # Update the image view.
		viewSrcImage.ZoomFit()
		viewSrcImage.Invalidate(True)

		for i in range(3):
			viewDstImage[i].ZoomFit()
			viewDstImage[i].Invalidate(True)
			
		# 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewSrcImage.IsAvailable() and viewDstImage[0].IsAvailable() and viewDstImage[1].IsAvailable() and viewDstImage[2].IsAvailable():
			CThreadUtilities.Sleep(1)
			
		viewSrcImage.Destroy()

		for i in range(3):
			viewDstImage[i].Destroy()

		break
	
	# End of main function


if __name__ == '__main__':
    main()