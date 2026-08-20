
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
	fliSourceImage1 = CFLImage()
	fliSourceImage2 = CFLImage()
	fliSourceImage3 = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSrc1 = CGUIViewImage()
	viewImageSrc2 = CGUIViewImage()
	viewImageSrc3 = CGUIViewImage()

	while True:
		
		# Source 이미지 로드 # Load the source image
		res = fliSourceImage1.Load("../../ExampleImages/FocusMeasurement/Focus1.flif")

		if res.IsFail():
			ErrorPrint(res, "Failed to load the image file.")
			break

		res = fliSourceImage2.Load("../../ExampleImages/FocusMeasurement/Focus2.flif")

		if res.IsFail():
			ErrorPrint(res, "Failed to load the image file.")
			break

		res = fliSourceImage3.Load("../../ExampleImages/FocusMeasurement/Focus3.flif")

		if res.IsFail():
			ErrorPrint(res, "Failed to load the image file.")
			break

		# Source 이미지 뷰 생성 # Create source image view
		if (res := viewImageSrc1.Create(400, 0, 912, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		if (res := viewImageSrc2.Create(912, 0, 1424, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		if (res := viewImageSrc3.Create(1424, 0, 1936, 512)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc1.SetImagePtr(fliSourceImage1)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		if (res := viewImageSrc2.SetImagePtr(fliSourceImage2)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		if (res := viewImageSrc3.SetImagePtr(fliSourceImage3)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc1.SynchronizePointOfView(viewImageSrc2)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		if (res := viewImageSrc1.SynchronizePointOfView(viewImageSrc3)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc1.SynchronizeWindow(viewImageSrc2)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		if (res := viewImageSrc1.SynchronizeWindow(viewImageSrc3)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# Tenengrad 객체 생성 # Create Tenengrad object
		tenengrad = CTenengrad()
		
		# Source 이미지 1 설정 # Set the source1 image
		tenengrad.SetSourceImage(fliSourceImage1)

		# Threshold 설정 # Set Threshold
		tenengrad.SetThreshold(5.0)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := tenengrad.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Tenengrad.')
			break

		# 결과 점수 획득 # Get Result Score
		f64Score1 = tenengrad.GetResultScore()

		# Source 이미지 2 설정 # Set the source2 image
		tenengrad.SetSourceImage(fliSourceImage2)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := tenengrad.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Tenengrad.')
			break

		# 결과 점수 획득 # Get Result Score
		f64Score2 = tenengrad.GetResultScore()

		# Source 이미지 3 설정 # Set the source3 image
		tenengrad.SetSourceImage(fliSourceImage3)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := tenengrad.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Tenengrad.')
			break

		# 결과 점수 획득 # Get Result Score
		f64Score3 = tenengrad.GetResultScore()

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSource1 = viewImageSrc1.GetLayer(0)
		layerSource2 = viewImageSrc2.GetLayer(0)
		layerSource3 = viewImageSrc3.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSource1.Clear()
		layerSource2.Clear()
		layerSource3.Clear()

		# 점수를 디스플레이 한다. # Display score
		# 아래 함수 DrawTextCanvas은 Screen좌표를 기준으로 하는 String을 Drawing 한다. # The function DrawTextCanvas below draws a String based on the screen coordinates.
		# 색상 파라미터를 EGUIViewImageLayerTransparencyColor 으로 넣어주게되면 배경색으로 처리함으로 불투명도를 0으로 한것과 같은 효과가 있다.
		# If the color parameter is set as EGUIViewImageLayerTransparencyColor, it has the same effect as setting the opacity to 0 by treating it as a background color.
		# 파라미터 순서 : 레이어 -> 기준 좌표 Figure 객체 -> 문자열 -> 폰트 색 -> 면 색 -> 폰트 크기 -> 실제 크기 유무 -> 각도 ->
		#                 얼라인 -> 폰트 이름 -> 폰트 알파값(불투명도) -> 면 알파값 (불투명도) -> 폰트 두께 -> 폰트 이텔릭
		# Parameter order: layer -> reference coordinate Figure object -> string -> font color -> Area color -> font size -> actual size -> angle ->
		#                  Align -> Font Name -> Font Alpha Value (Opaqueness) -> Cotton Alpha Value (Opaqueness) -> Font Thickness -> Font Italic
		flpPoint = CFLPoint[Double](0, 0)

		if (res := layerSource1.DrawTextCanvas(flpPoint, 'Score : ' + str(f64Score1), EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := layerSource2.DrawTextCanvas(flpPoint, 'Score : ' + str(f64Score2), EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		if (res := layerSource3.DrawTextCanvas(flpPoint, 'Score : ' + str(f64Score3), EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 이미지 뷰를 갱신 # Update image view
		viewImageSrc1.Invalidate(True)
		viewImageSrc2.Invalidate(True)
		viewImageSrc3.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImageSrc1.IsAvailable() and viewImageSrc2.IsAvailable() and viewImageSrc3.IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function


if __name__ == '__main__':
    main()