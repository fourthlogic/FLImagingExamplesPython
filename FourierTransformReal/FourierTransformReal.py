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
	fliISrcImage = CFLImage()
	fliFTImage = CFLImage()
	fliIRFTImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImage = [CGUIViewImage() for i in range(3)]
	
	while True:
		
		# Source 이미지 로드 # Load the source image
		if (res := fliISrcImage.Load('../../ExampleImages/FourierTransform/TempleNoise.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		# 이미지 뷰 생성 # Create source image view
		if (res := viewImage[0].Create(300, 0, 300 + 512, 384)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# 이미지 뷰 생성 # Create source image view
		if (res := viewImage[1].Create(300 + 512, 0, 300 + 512 * 2, 384)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# 이미지 뷰 생성 # Create source image view
		if (res := viewImage[2].Create(300 + 512 * 2, 0, 300 + 512 * 3, 384)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
        # 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
        # ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... 형태를 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage[0].SynchronizePointOfView(viewImage[1])[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize view")
			break
		
        # 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
        # ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... 형태를 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage[0].SynchronizePointOfView(viewImage[2])[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize view")
			break
		
		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage[0].SynchronizeWindow(viewImage[1])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break
		
		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage[0].SynchronizeWindow(viewImage[2])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break
		
		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage[0].SetImagePtr(fliISrcImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage[1].SetImagePtr(fliFTImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage[2].SetImagePtr(fliIRFTImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# Fourier Transform 객체 생성 # Create Fourier Transform object
		fourierTransformReal = CFourierTransformReal()

		# Source 이미지 설정 # Set source image 
		fourierTransformReal.SetSourceImage(fliISrcImage)

		# Destination 이미지 설정 # Set destination image
		fourierTransformReal.SetDestinationImage(fliFTImage)

		# 결과 이미지 포멧 설정 (FFT image, 32/64 bit Floating Point 설정 가능) # Set Result image format(FFT image, 32/64 bit Floating Point) 
		fourierTransformReal.SetResultType(EFloatingPointAccuracy.Bit32)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := fourierTransformReal.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break
		
		# 이미지의 노이즈를 감소하기(Mask 사용) # Reduce the noise in the image (using Mask)
		# Mask 객체 생성 # Create Mask object
		Mask = CMask()

		# 변환 이미지를 설정(FFT) # Set source image(FFT image)
		Mask.SetSourceImage(fliFTImage)

		# CFLFigureArray 객체를 생성 # Create CFLFigureArray object
		flfArray = CFLFigureArray()

		# 미리 그려둔 Mask region Figure Array 불러오기 # Load Pre-drawn Mask Region Figure Array
		if(res := flfArray.Load("../../ExampleImages/FourierTransform/RFTRegion.fig")).IsFail():
			ErrorPrint(res, "Failed to load the figure file.")
			break

		# 지정한 ROI를 입력 # Set mask ROI
		Mask.SetSourceROI(flfArray)

		# 마스크 값을 입력 # set mask value
		Mask.SetMask(0.0)
		
		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := Mask.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break
		
		# Source 이미지 설정(FFT image) # Set source image (FFT image)
		fourierTransformReal.SetSourceImage(fliFTImage)

		# Destination 이미지 설정(IFFT image) # Set destination image(IFFT image)
		fourierTransformReal.SetDestinationImage(fliIRFTImage)
				
		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := fourierTransformReal.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layer1 = viewImage[0].GetLayer(0)
		layer2 = viewImage[1].GetLayer(0)
		layer3 = viewImage[2].GetLayer(0)
		
		flpPoint = CFLPoint[Double](0, 0)
		
		# View 정보를 디스플레이 합니다. # Display View information.
		if (res := layer1.DrawTextImage(flpPoint, 'Spatial Domain', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := layer2.DrawTextImage(flpPoint, 'Frequency Domain', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := layer3.DrawTextImage(flpPoint, 'Inverse RFT Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		# 이미지 뷰를 갱신 합니다. # Update the image view.
		for i in range(3):
			viewImage[i].ZoomFit()
			viewImage[i].Invalidate(True)
			
		# 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImage[0].IsAvailable() and viewImage[1].IsAvailable() and viewImage[2].IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function


if __name__ == '__main__':
    main()