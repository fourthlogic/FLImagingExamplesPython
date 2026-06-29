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

	# 이미지 객체 선언 # Declare image object
	fliSourceImage = CFLImage()
	fliDestinationImage = CFLImage()

	# 이미지 뷰 선언 # Declare image view
	viewSourceImage = CGUIViewImage()
	viewDestinationImage = CGUIViewImage()

	# 수행 결과 객체 선언 # Declare execution result object
	res = CResult(EResult.UnknownError)

	while True:

		# Source 이미지 로드 # Load Source image
		if (res := fliSourceImage.Load('../../ExampleImages/OperationComplexMultiply/ExampleSource.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.\n')
			break
		
		# Destination 이미지를 Source 이미지와 동일하도록 설정 # Assign Source image to Destination image
		if (res := fliDestinationImage.Assign(fliSourceImage)).IsFail():
			ErrorPrint(res, 'Failed to assign the image.\n')
			break
		
		# Source 이미지 뷰 생성 # Create Source image view
		if (res := viewSourceImage.Create(100, 0, 600, 545)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.\n')
			break
		
		# Destination 이미지 뷰 생성 # Create Destination image view
		if (res := viewDestinationImage.Create(600, 0, 1100, 545)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.\n')
			break
		
		# 두 이미지 뷰의 시점을 동기화 # Synchronize viewpoints of two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewSourceImage.SynchronizePointOfView(viewDestinationImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize point of view between image views.\n')
			break
		
		# Source 이미지 뷰에 이미지를 디스플레이 # Display image in Source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewSourceImage.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.\n')
			break
		
		# Destination 이미지 뷰에 이미지를 디스플레이 # Display image in Destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewDestinationImage.SetImagePtr(fliDestinationImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.\n')
			break
		
		# 두 뷰 윈도우의 위치를 동기화 # Synchronize positions of two views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewSourceImage.SynchronizeWindow(viewDestinationImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window between views.\n')
			break
		
		# Operation Complex Multiply 객체 생성 # Create Operation Complex Multiply object
		operationComplexMultiply = COperationComplexMultiply()

		# Source 이미지 설정 # Set Source image
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := operationComplexMultiply.SetSourceImage(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set Source image.\n')
			break
		
		# Destination 이미지 설정 # Set Destination image
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := operationComplexMultiply.SetDestinationImage(fliDestinationImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set Destination image.\n')
			break
		
		# 연산 방식 스칼라로 설정 # Set operation source to image
		if (res := operationComplexMultiply.SetOperationSource(EOperationSource.Scalar)).IsFail():
			ErrorPrint(res, 'Failed to set operation source.\n')
			break
		
		# 오버플로 처리 방법 설정 # Set overflow handling method
		if (res := operationComplexMultiply.SetOverflowMethod(EOverflowMethod.Wrapping)).IsFail():
			ErrorPrint(res, 'Failed to set overflow method.\n')
			break
		
		# 스칼라 값 지정 # Set scalar value
		if (res := operationComplexMultiply.SetScalarValue(CMultiVar[Double](2, 1))).IsFail():
			ErrorPrint(res, 'Failed to set the scalar value.\n')
			break
		
		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := operationComplexMultiply.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Operation Complex Multiply.\n')
			break
		
		# 화면에 출력하기 위해 이미지 뷰에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released
		layerSource = viewSourceImage.GetLayer(0)
		layerDestination = viewDestinationImage.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear figures drawn on existing layer
		layerSource.Clear()
		layerDestination.Clear()

		# 이미지 뷰 정보 표시 # Display image view information
		if (res := layerSource.DrawTextCanvas(CFLPoint[Double](0, 0), 'Source Image', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.\n')
			break
		
		if (res := layerDestination.DrawTextCanvas(CFLPoint[Double](0, 0), 'Destination Image(Multiplied by 2 + 1i)', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.\n')
			break
		
		# 이미지 뷰를 갱신 # Update image view
		viewSourceImage.Invalidate(True)
		viewDestinationImage.Invalidate(True)

		# 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until a view is closed before exiting
		while viewSourceImage.IsAvailable() and viewDestinationImage.IsAvailable():
			CThreadUtilities.Sleep(1)
		
		break
	
	# End of main function


if __name__ == '__main__':
    main()