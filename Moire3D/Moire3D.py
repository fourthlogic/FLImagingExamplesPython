# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *
from System.Collections.Generic import List

# 메인 함수 # Main function
def main():
	# 이미지 객체 선언 # Declare the image object
	fliLrnImage = List[CFLImage]()
	fliLrnImage.Add(CFLImage())
	fliLrnImage.Add(CFLImage())
	fliSrcImage = List[CFLImage]()
	fliSrcImage.Add(CFLImage())
	fliSrcImage.Add(CFLImage())
	fliDstImage = CFLImage()
	fliTxtImage = CFLImage()
	floDstObject = CFL3DObjectHeightMap()

	# 이미지 뷰 선언 # Declare the image view
	viewImageLrn = List[CGUIViewImage]()
	viewImageLrn.Add(CGUIViewImage())
	viewImageLrn.Add(CGUIViewImage())
	viewImageSrc = List[CGUIViewImage]()
	viewImageSrc.Add(CGUIViewImage())
	viewImageSrc.Add(CGUIViewImage())
	viewImageDst = CGUIViewImage()
	view3DDst = CGUIView3D()

	# Source 이미지를 저장할 Array 선언 # Declare an Array to store the source image
	vctLrnImages = List[CFLImage]()
	# Source 이미지 입력 # source images add
	vctLrnImages.Add(fliLrnImage[0])
	vctLrnImages.Add(fliLrnImage[1])

	# Source 이미지를 저장할 Array 선언 # Declare an Array to store the source image
	vctSrcImages = List[CFLImage]()
	# Source 이미지 입력 # source images add
	vctSrcImages.Add(fliSrcImage[0])
	vctSrcImages.Add(fliSrcImage[1])

	res = CResult()

	while True:
		# Learn 이미지 로드 # Load the reference plane image for calibration
		if (res := vctLrnImages[0].Load("../../ExampleImages/Moire3D/Learn0/")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break

		# Source 이미지 로드 # Load the source image
		if (res := vctSrcImages[0].Load("../../ExampleImages/Moire3D/Object0/")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break

		# Learn 이미지 로드 # Load the reference plane image for calibration
		if (res := vctLrnImages[1].Load("../../ExampleImages/Moire3D/Learn1/")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break

		# Source 이미지 로드 # Load the source image
		if (res := vctSrcImages[1].Load("../../ExampleImages/Moire3D/Object1/")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break

		# Texture 이미지 로드 # Load the texture image
		if (res := fliTxtImage.Load("../../ExampleImages/Moire3D/text.flif")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break
		
		# 이미지 뷰 생성 # Create image views
		if ((res := viewImageLrn[0].Create(100, 0, 600, 400)).IsFail() or
			(res := viewImageLrn[1].Create(600, 0, 1100, 400)).IsFail() or
			(res := viewImageSrc[0].Create(100, 400, 600, 800)).IsFail() or
			(res := viewImageSrc[1].Create(600, 400, 1100, 800)).IsFail() or
			(res := viewImageDst.Create(200, 200, 700, 600)).IsFail()):
			ErrorPrint(res, "Failed to create the image view.\n")
			break
		
		# Destination 3D 이미지 뷰 생성 # Create the destination 3D image view
		if (res := view3DDst.Create(400, 100, 1150, 550)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break

		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views. .
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if ((res := viewImageSrc[0].SynchronizePointOfView(viewImageSrc[1])[0]).IsFail() or
			(res := viewImageSrc[0].SynchronizePointOfView(viewImageLrn[0])[0]).IsFail() or
			(res := viewImageSrc[0].SynchronizePointOfView(viewImageLrn[1])[0]).IsFail() or
			(res := viewImageSrc[0].SynchronizePointOfView(viewImageDst)[0]).IsFail()):
			ErrorPrint(res, "Failed to synchronize window.\n")
			break
		
		# 두 이미지 뷰의 페이지 인덱스를 동기화 한다 # Synchronize the page index of the two image views. .
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if ((res := viewImageSrc[0].SynchronizePageIndex(viewImageSrc[1])[0]).IsFail() or
			(res := viewImageSrc[0].SynchronizePageIndex(viewImageLrn[0])[0]).IsFail() or
			(res := viewImageSrc[0].SynchronizePageIndex(viewImageLrn[1])[0]).IsFail()):
			ErrorPrint(res, "Failed to synchronize window.\n")
			break

		# 두 이미지 뷰 윈도우의 위치를 동기화 한다 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if ((res := viewImageSrc[0].SynchronizeWindow(viewImageSrc[1])[0]).IsFail() or
			(res := viewImageSrc[0].SynchronizeWindow(viewImageLrn[0])[0]).IsFail() or
			(res := viewImageSrc[0].SynchronizeWindow(viewImageLrn[1])[0]).IsFail()):
			ErrorPrint(res, "Failed to synchronize window.\n")
			break
				
		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if ((res := viewImageLrn[0].SetImagePtr(fliLrnImage[0])[0]).IsFail() or
			(res := viewImageLrn[1].SetImagePtr(fliLrnImage[1])[0]).IsFail() or
			(res := viewImageSrc[0].SetImagePtr(fliSrcImage[0])[0]).IsFail() or
			(res := viewImageSrc[1].SetImagePtr(fliSrcImage[1])[0]).IsFail() or
			(res := viewImageDst.SetImagePtr(fliDstImage)[0]).IsFail()):
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break


		# 알고리즘 객체 생성 # Create algorithm object
		algObject = CMoire3D()

		# 카메라의 working distance 설정 # Set working distance of the camera
		if (res := algObject.SetWorkingDistance(330)).IsFail():
			break
		# 카메라의 field of view 설정 # Set field of view of the camera
		if (res := algObject.SetFieldOfView(400)).IsFail():
			break
		# 프로젝터 각도 설정 # Set angle of projector
		mvF64AngleOfProjector = CMultiVar[Double](73, 105)
		if (res := algObject.SetAngleOfProjector(mvF64AngleOfProjector)).IsFail():
			break
		# Phase Unwrap 히스토그램 bin 범위 설정 # Set histogram bin range for phase unwrapping
		mvF64SmallBinRange = CMultiVar[Double](1, 1)
		if (res := algObject.SetBinInterval(mvF64SmallBinRange)).IsFail():
			break
		# 패턴 타입 설정 # Set Pattern Type
		if (res := algObject.SetPatternType(CMoire3D.EPatternType.SquareWave)).IsFail():
			break
		# Noise 감쇠 모드 활성화 # Enable noise reduction mode
		if (res := algObject.EnableNoiseReduction(True)).IsFail():
			break

		# Learn 이미지 설정 # Set the learn image
		if (res := algObject.SetLearnImage(vctLrnImages)[0]).IsFail():
			break
		
		# 알고리즘 Calibrate 수행 # Calibrate the algorithm
		if (res := algObject.Calibrate()).IsFail():
			ErrorPrint(res, "Failed to calibrate.")
			break
		
		# Source 이미지 설정 # Set the source image
		if (res := algObject.SetSourceImage(vctSrcImages)[0]).IsFail():
			break
		# Destination Height Map 이미지 설정 # Set the destination height map image
		if (res := algObject.SetDestinationHeightMapImage(fliDstImage)[0]).IsFail():
			break
		# Destination 객체 설정 # Set the destination object
		if (res := algObject.SetDestinationObject(floDstObject)[0]).IsFail():
			break

		# 알고리즘 수행 # Execute the algorithm
		if (res := algObject.Execute()).IsFail():
			ErrorPrint(res, "Failed to execute algorithm.")
			break


		floDstObject.SetTextureImage(fliTxtImage)
		floDstObject.ActivateVertexColorTexture(True)

		# 3D 이미지 뷰에 Height Map (Destination Image) 이미지를 디스플레이 # Display the Height Map (Destination Image) on the 3D image view
		if view3DDst.PushObject(floDstObject).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerLrn0 = viewImageLrn[0].GetLayer(0)
		layerLrn1 = viewImageLrn[1].GetLayer(0)
		layerSrc0 = viewImageSrc[0].GetLayer(0)
		layerSrc1 = viewImageSrc[1].GetLayer(0)
		layerDst = viewImageDst.GetLayer(0)
		layer3D = view3DDst.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerLrn0.Clear()
		layerLrn1.Clear()
		layerSrc0.Clear()
		layerSrc1.Clear()
		layerDst.Clear()
		layer3D.Clear()
		
		# 이미지 뷰 정보 표시 # Display image view information
		flpTemp = CFLPoint[Double](0, 0)
		if ((res := layerLrn0.DrawTextCanvas(flpTemp, "Learn Image[0]", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or
			(res := layerLrn1.DrawTextCanvas(flpTemp, "Learn Image[1]", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or
			(res := layerSrc0.DrawTextCanvas(flpTemp, "Source Image[0]", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or
			(res := layerSrc1.DrawTextCanvas(flpTemp, "Source Image[1]", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or
			(res := layerDst.DrawTextCanvas(flpTemp, "Destination Height Map Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or
			(res := layer3D.DrawTextCanvas(flpTemp, "Destination Object", EColor.YELLOW, EColor.BLACK, 20)).IsFail()):
			ErrorPrint(res, "Failed to draw text.\n")
			break

		viewImageLrn[0].SetLayerAutoClearMode(ELayerAutoClearMode.PageChanged, False)
		viewImageLrn[1].SetLayerAutoClearMode(ELayerAutoClearMode.PageChanged, False)
		viewImageSrc[0].SetLayerAutoClearMode(ELayerAutoClearMode.PageChanged, False)
		viewImageSrc[1].SetLayerAutoClearMode(ELayerAutoClearMode.PageChanged, False)
		
		# Zoom Fit
		if ((res := viewImageLrn[0].ZoomFit()).IsFail() or
			(res := viewImageLrn[1].ZoomFit()).IsFail() or
			(res := viewImageSrc[0].ZoomFit()).IsFail() or
			(res := viewImageSrc[1].ZoomFit()).IsFail() or
			(res := viewImageDst.ZoomFit()).IsFail() or
			(res := view3DDst.ZoomFit()).IsFail()):
			ErrorPrint(res, "Failed to zoom fit of the image view.\n")
			break

		# 이미지 뷰를 갱신 # Update image view
		viewImageLrn[0].Invalidate(True)
		viewImageLrn[1].Invalidate(True)
		viewImageSrc[0].Invalidate(True)
		viewImageSrc[1].Invalidate(True)
		viewImageDst.Invalidate(True)
		view3DDst.Invalidate(True)

		# 이미지 뷰, 3D 뷰가 종료될 때 까지 기다림 # Wait for the image and 3D view to close
		while viewImageLrn[0].IsAvailable() and viewImageLrn[0].IsAvailable() and viewImageSrc[0].IsAvailable() and viewImageSrc[1].IsAvailable() and viewImageDst.IsAvailable() and view3DDst.IsAvailable():			
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