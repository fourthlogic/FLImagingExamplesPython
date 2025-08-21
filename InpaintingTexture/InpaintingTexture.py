# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliSourceImage1 = CFLImage()
	fliSourceImage2 = CFLImage()
	fliDestinationImage1 = CFLImage()
	fliDestinationImage2 = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSrc1 = CGUIViewImage()
	viewImageSrc2 = CGUIViewImage()
	viewImageDst1 = CGUIViewImage()
	viewImageDst2 = CGUIViewImage()

	while True:
		
		# Source 이미지 로드 # Load the source image
		if (res := fliSourceImage1.Load('../../ExampleImages/InpaintingTexture/Seville.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 로드 # Load the source image
		if (res := fliSourceImage2.Load('../../ExampleImages/InpaintingTexture/Wood.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 # Create destination image as same as source image
		if (res := fliDestinationImage1.Assign(fliSourceImage1)).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 # Create destination image as same as source image
		if (res := fliDestinationImage2.Assign(fliSourceImage2)).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 뷰 생성 # Create source image view
		if (res := viewImageSrc1.Create(400, 0, 800, 400)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Source 이미지 뷰 생성 # Create source image view
		if (res := viewImageSrc2.Create(400, 400, 800, 800)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰 생성 # Create the destination image view
		if (res := viewImageDst1.Create(800, 0, 1200, 400)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰 생성 # Create the destination image view
		if (res := viewImageDst2.Create(800, 400, 1200, 800)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc1.SynchronizePointOfView(viewImageDst1)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc2.SynchronizePointOfView(viewImageDst2)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc1.SetImagePtr(fliSourceImage1)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc2.SetImagePtr(fliSourceImage2)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 # Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDst1.SetImagePtr(fliDestinationImage1)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 # Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDst2.SetImagePtr(fliDestinationImage2)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc1.SynchronizeWindow(viewImageSrc2)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc1.SynchronizeWindow(viewImageDst1)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc1.SynchronizeWindow(viewImageDst2)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# InpaintingTexture 객체 생성 # Create InpaintingTexture object
		inpaintingTexture = CInpaintingTexture()

		# Source 이미지 설정 # Set the source image
		inpaintingTexture.SetSourceImage(fliSourceImage1)

		# Destination 이미지 설정 # Set the destination image
		inpaintingTexture.SetDestinationImage(fliDestinationImage1)

		# Patching을 진행할 Mask의 크기 설정 # Set the size of the mask for patching
		inpaintingTexture.SetMaskSize(13)

		# Patching의 Source가 되는 Mask를 찾기 위한 검색 영역의 크기 설정 # Set the size of the search area to find the mask that is the source of the patching
		inpaintingTexture.SetSearchSize(100)

		# Search step size 설정 # Set the search step size
		inpaintingTexture.SetSearchStepSize(1)

		# 매치를 위한 Gradient Value 곱 계수 설정 # Set a coefficient multiplied by gradient value for match
		inpaintingTexture.SetAnisotropy(1)

		flfaPaintingRegion = CFLFigureArray()

		# 미리 그려둔 Painting region Figure Array 불러오기 # Load Pre-drawn Painting region Figure Array
		if (res := flfaPaintingRegion.Load('../../ExampleImages/InpaintingTexture/PaintingRegion.fig')).IsFail():
			ErrorPrint(res, 'Failed to load the figure file.')
			break

		# Inpainting을 위한 Painting region 설정 # Set the painting region for inpainting
		inpaintingTexture.SetPaintingRegion(flfaPaintingRegion)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := inpaintingTexture.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute InpaintingTexture.')
			break

		# Source 이미지 설정 # Set the source image
		inpaintingTexture.SetSourceImage(fliSourceImage2)

		# Destination 이미지 설정 # Set the destination image
		inpaintingTexture.SetDestinationImage(fliDestinationImage2)

		# Patching을 진행할 Mask의 크기 설정 # Set the size of the mask for patching
		inpaintingTexture.SetMaskSize(15)

		# Patching의 Source가 되는 Mask를 찾기 위한 검색 영역의 크기 설정 # Set the size of the search area to find the mask that is the source of the patching
		inpaintingTexture.SetSearchSize(-1)

		# Search step size 설정 # Set the search step size
		inpaintingTexture.SetSearchStepSize(1)

		# 매치를 위한 Gradient Value 곱 계수 설정 # Set a coefficient multiplied by gradient value for match
		inpaintingTexture.SetAnisotropy(0)

		flfaPaintingRegion2 = CFLFigureArray()

		# 미리 그려둔 Painting region Figure Array 불러오기 # Load Pre-drawn Painting region Figure Array
		if (res := flfaPaintingRegion2.Load('../../ExampleImages/InpaintingTexture/PaintingRegion2.fig')).IsFail():
			ErrorPrint(res, 'Failed to load the figure file.')
			break

		# Inpainting을 위한 Painting region 설정 # Set the painting region for inpainting
		inpaintingTexture.SetPaintingRegion(flfaPaintingRegion2)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := inpaintingTexture.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute InpaintingTexture.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSource1 = viewImageSrc1.GetLayer(0)
		layerSource2 = viewImageSrc2.GetLayer(0)
		layerDestination1 = viewImageDst1.GetLayer(0)
		layerDestination2 = viewImageDst2.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSource1.Clear()
		layerSource2.Clear()
		layerDestination1.Clear()
		layerDestination2.Clear()

		# 이미지 뷰 정보 표시 # Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if (res := layerSource1.DrawTextCanvas(flpPoint, 'Source Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail() or \
			(res := layerSource2.DrawTextCanvas(flpPoint, 'Source Image 2', EColor.YELLOW, EColor.BLACK, 30)).IsFail() or \
			(res := layerDestination1.DrawTextCanvas(flpPoint, 'Destination Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail() or \
			(res := layerDestination2.DrawTextCanvas(flpPoint, 'Destination Image', EColor.YELLOW, EColor.BLACK, 30)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		# Painting region을 source image에 디스플레이 # Display painting region on the source image
		if (fliSourceImage1.PushBackFigure(CFigureUtilities.ConvertFigureObjectToString(flfaPaintingRegion)) == -1) or \
			(fliSourceImage2.PushBackFigure(CFigureUtilities.ConvertFigureObjectToString(flfaPaintingRegion2)) == -1):
			ErrorPrint(res, 'Failed to draw figure array.')
			break

		# 이미지 뷰를 갱신 # Update image view
		viewImageSrc1.Invalidate(True)
		viewImageSrc2.Invalidate(True)
		viewImageDst1.Invalidate(True)
		viewImageDst2.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewImageSrc1.IsAvailable() and viewImageDst1.IsAvailable() and viewImageSrc2.IsAvailable() and viewImageDst2.IsAvailable():
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