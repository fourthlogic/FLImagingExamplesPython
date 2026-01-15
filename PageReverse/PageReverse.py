# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliAfterSrcImage = CFLImage()
	fliBeforeSrcImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageAfterSrc = CGUIViewImage()
	viewImageBeforeSrc = CGUIViewImage()

	while True:
		
		# 알고리즘을 수행할 Source 이미지 로드 # Load the source image to execute algorithm
		if (res := fliAfterSrcImage.Load('../../ExampleImages/PageReorder/Landscape.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# 알고리즘 수행 결과와 비교할 Source 이미지 로드 # Load the source image to compare executing result of algorithm
		if (res := fliBeforeSrcImage.Load('../../ExampleImages/PageReorder/Landscape.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# 알고리즘을 수행 할 Source 이미지 뷰 생성 # Create the After Source image view to execute algorithm
		if (res := viewImageAfterSrc.Create(912, 0, 1424, 612)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# 알고리즘 수행 결과와 비교할 Source 이미지 뷰 생성 # Create the source image view to compare executing result of algorithm
		if (res := viewImageBeforeSrc.Create(400, 0, 912, 612)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# 알고리즘을 수행 할 Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view to execute algorithm
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageAfterSrc.SetImagePtr(fliAfterSrcImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 알고리즘 수행 결과와 비교할 Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view to compare executing result of algorithm
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageBeforeSrc.SetImagePtr(fliBeforeSrcImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageAfterSrc.SynchronizeWindow(viewImageBeforeSrc)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageAfterSrc.SynchronizePointOfView(viewImageBeforeSrc)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# 두 이미지 뷰의 페이지 색인을 동기화 한다 # Synchronize the page index of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageAfterSrc.SynchronizePageIndex(viewImageBeforeSrc)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# Image 크기에 맞게 view의 크기를 조정 # Zoom the view to fit the image size
		if (res := viewImageAfterSrc.ZoomFit()).IsFail():
			ErrorPrint(res, "Failed to zoom fit\n")
			return

		# PageReverse 객체 생성 # Create PageReverse object
		pageReverse = CPageReverse()

		# Source 이미지 설정 # Set the source image
		pageReverse.SetSourceImage(fliAfterSrcImage)

		# 순서를 뒤집을 페이지의 시작 인덱스와 페이지 개수 설정 # Set the start page index and  page counts to reverse order
		pageReverse.SetSelection(0, 5);

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := pageReverse.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Page Reverse.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerAfterSrc = viewImageAfterSrc.GetLayer(0)
		layerBeforeSrc = viewImageBeforeSrc.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerAfterSrc.Clear()
		layerBeforeSrc.Clear()

		# 이미지 뷰 정보 표시 # Display image view information
		flpPoint = CFLPoint[Double](0, 0)
		
		if (res := layerAfterSrc.DrawTextCanvas(flpPoint, 'Source Image After Reverse', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := layerBeforeSrc.DrawTextCanvas(flpPoint, 'Source Image Before Reverse', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# 이미지 뷰를 갱신 # Update image view
		viewImageAfterSrc.Invalidate(True)
		viewImageBeforeSrc.Invalidate(True)

		# 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImageAfterSrc.IsAvailable() and viewImageBeforeSrc.IsAvailable():
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
