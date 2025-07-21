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

	# 알고리즘 동작 결과 # Algorithm execution result
	res = CResult()

	while True:
		# Learn 이미지 로드 # Load the reference plane image for calibration
		if (res := vctLrnImages[0].Load("../../ExampleImages/Moire3D/Learn0/")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break


		vctLrnImages[0].SelectPage(0)

		# Source 이미지 로드 # Load the source image
		if (res := vctSrcImages[0].Load("../../ExampleImages/Moire3D/Object0/")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break


		vctSrcImages[0].SelectPage(0)

		# Learn 이미지 로드 # Load the reference plane image for calibration
		if (res := vctLrnImages[1].Load("../../ExampleImages/Moire3D/Learn1/")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break


		vctLrnImages[1].SelectPage(0)

		# Source 이미지 로드 # Load the source image
		if (res := vctSrcImages[1].Load("../../ExampleImages/Moire3D/Object1/")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break


		vctSrcImages[1].SelectPage(0)

		# Learn 이미지 뷰 생성 # Create the learn image view
		if (res := viewImageLrn[0].Create(100, 0, 548, 348)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break


		# Learn 이미지 뷰 생성 # Create the destination image view
		if (res := viewImageLrn[1].Create(548, 0, 996, 348)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break


		# Source 이미지 뷰 생성 # Create the Source image view
		if (res := viewImageSrc[0].Create(100, 348, 548, 696)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break


		# Source 이미지 뷰 생성 # Create the destination image view
		if (res := viewImageSrc[1].Create(548, 348, 996, 696)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break


		# Dst 이미지 뷰 생성 # Create the destination image view
		if (res := viewImageDst.Create(996, 348, 1444, 696)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break


		# Learn 이미지 뷰에 이미지를 디스플레이 # Display the image in the Learn image view
		for i32I in range(0, 2):
			if (res := viewImageLrn[i32I].SetImagePtr(fliLrnImage[i32I]))[0].IsFail():
				ErrorPrint(res, "Failed to set image object on the image view.\n")
				break

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the Source image view
		for i32I in range(0, 2):
			if (res := viewImageSrc[i32I].SetImagePtr(fliSrcImage[i32I]))[0].IsFail():
				ErrorPrint(res, "Failed to set image object on the image view.\n")
				break

		# Dst 이미지 뷰에 이미지를 디스플레이 # Display the image in the destination image view
		if (res := viewImageDst.SetImagePtr(fliDstImage))[0].IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break


		# 두 뷰 윈도우의 위치를 동기화 한다 # Synchronize the positions of the two view windows
		if (res := viewImageLrn[1].SynchronizeWindow(viewImageLrn[0]))[0].IsFail():
			ErrorPrint(res, "Failed to synchronize window.\n")
			break


		# 두 뷰 윈도우의 위치를 동기화 한다 # Synchronize the positions of the two view windows
		for i32I in range(0, 2):
			if (res := viewImageSrc[i32I].SynchronizeWindow(viewImageLrn[0]))[0].IsFail():
				ErrorPrint(res, "Failed to synchronize window.\n")
				break

		# 두 뷰 윈도우의 위치를 동기화 한다 # Synchronize the positions of the two view windows
		if (res := viewImageDst.SynchronizeWindow(viewImageLrn[0]))[0].IsFail():
			ErrorPrint(res, "Failed to synchronize window.\n")
			break


		# 두 이미지 뷰의 시점을 동기화 한다. # Synchronize the viewpoints of the two image views. 
		if (res := viewImageLrn[1].SynchronizePointOfView(viewImageLrn[0]))[0].IsFail():
			ErrorPrint(res, "Failed to synchronize view.\n")
			break


		# 두 이미지 뷰의 시점을 동기화 한다. # Synchronize the viewpoints of the two image views. 
		for i32I in range(0, 2):
			if (res := viewImageSrc[i32I].SynchronizePointOfView(viewImageLrn[0]))[0].IsFail():
				ErrorPrint(res, "Failed to synchronize view.\n")
				break

		# 두 이미지 뷰의 페이지를 동기화 한다. # Synchronize the page of the two image views. 
		if (res := viewImageDst.SynchronizePointOfView(viewImageLrn[0]))[0].IsFail():
			ErrorPrint(res, "Failed to synchronize window.\n")
			break


		# 두 이미지 뷰의 페이지를 동기화 한다. # Synchronize the page of the two image views. 
		if (res := viewImageLrn[1].SynchronizePageIndex(viewImageLrn[0]))[0].IsFail():
			ErrorPrint(res, "Failed to synchronize view.\n")
			break


		# 두 이미지 뷰의 페이지를 동기화 한다. # Synchronize the page of the two image views. 
		for i32I in range(0, 2):
			if (res := viewImageSrc[i32I].SynchronizePageIndex(viewImageLrn[0]))[0].IsFail():
				ErrorPrint(res, "Failed to synchronize view.\n")
				break
		# Destination 3D 이미지 뷰 생성 # Create the destination 3D image view
		if (res := view3DDst.Create(400, 200, 1300, 800)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break


		mvF64AngleOfProjector = CMultiVar[Double](73, 105)
		mvF64SmallBinRange = CMultiVar[Double](1, 1)

		# FPP 객체 생성 # Create FPP object
		Moire3D = CMoire3D()

		fl3DOHM = CFL3DObjectHeightMap()

		# Learn 이미지 설정 # Set the learn image
		Moire3D.SetLearnImage(vctLrnImages)
		# Source 이미지 설정 # Set the source image
		Moire3D.SetSourceImage(vctSrcImages)
		# Destination Height Map 이미지 설정 # Set the destination height map image
		Moire3D.SetDestinationHeightMapImage(fliDstImage)
		# Destination 객체 설정 # Set the destination object
		Moire3D.SetDestinationObject(fl3DOHM)
		# 카메라의 working distance 설정 # Set working distance of the camera
		Moire3D.SetWorkingDistance(330)
		# 카메라의 field of view 설정 # Set field of view of the camera
		Moire3D.SetFieldOfView(400)
		# 프로젝터 각도 설정 # Set angle of projector
		Moire3D.SetAngleOfProjector(mvF64AngleOfProjector)
		# Phase Unwrap 히스토그램 bin 범위 설정 # Set histogram bin range for phase unwrapping
		Moire3D.SetBinInterval(mvF64SmallBinRange)
		# 패턴 타입 설정 # Set Pattern Type
		Moire3D.SetPatternType(CMoire3D.EPatternType.SquareWave)
		# Noise 감쇠 모드 활성화 # Enable noise reduction mode
		Moire3D.EnableNoiseReduction(True)

		# 앞서 설정된 파라미터 대로 Calibration 수행 # Calibrate algorithm according to previously set parameters
		if (res := Moire3D.Calibrate()).IsFail():
			ErrorPrint(res, "Failed to calibrate.")
			break


		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := Moire3D.Execute()).IsFail():
			ErrorPrint(res, "Failed to execute algorithm.")
			break


		# Image 크기에 맞게 view의 크기를 조정 # Zoom the view to fit the image size
		if (res := viewImageDst.ZoomFit()).IsFail():
			ErrorPrint(res, "Failed to zoom fit\n")
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

		# View 정보를 디스플레이 합니다. # Display View information.
		# 아래 함수 DrawTextCanvas은 Screen좌표를 기준으로 하는 String을 Drawing 한다.# The function DrawTextCanvas below draws a String based on the screen coordinates.
		# 파라미터 순서 : 레이어 -> 기준 좌표 Figure 객체 -> 문자열 -> 폰트 색 -> 면 색 -> 폰트 크기 -> 실제 크기 유무 -> 각도 ->
		#				 얼라인 -> 폰트 이름 -> 폰트 알파값(불투명도) -> 면 알파값 (불투명도) -> 폰트 두께 -> 폰트 이텔릭
		# Parameter order: layer -> reference coordinate Figure object -> string -> font color -> Area color -> font size -> actual size -> angle ->
		#				  Align -> Font Name -> Font Alpha Value (Opaqueness) -> Cotton Alpha Value (Opaqueness) -> Font Thickness -> Font Italic
		flp = CFLPoint[Double]()

		if (res := layerLrn0.DrawTextCanvas(flp, "Learn Image[0]", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break


		if (res := layerLrn1.DrawTextCanvas(flp, "Learn Image[1]", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break


		if (res := layerSrc0.DrawTextCanvas(flp, "Source Image[0]", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break


		if (res := layerSrc1.DrawTextCanvas(flp, "Source Image[1]", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break


		# Texture 이미지 로드 # Load the texture image
		if (res := fliTxtImage.Load("../../ExampleImages/Moire3D/text.flif")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break


		fl3DObject = Moire3D.GetDestinationObject()
		fl3DObject.SetTextureImage(fliTxtImage)
		fl3DObject.ActivateVertexColorTexture(True)

		# 3D 이미지 뷰에 Height Map (Destination Image) 이미지를 디스플레이 # Display the Height Map (Destination Image) on the 3D image view
		if view3DDst.PushObject(fl3DObject).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break


		view3DDst.ZoomFit()

		if (res := layer3D.DrawTextCanvas(flp, "Destination Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break


		viewImageLrn[0].SetLayerAutoClearMode(ELayerAutoClearMode.PageChanged, False)
		viewImageLrn[1].SetLayerAutoClearMode(ELayerAutoClearMode.PageChanged, False)
		viewImageSrc[0].SetLayerAutoClearMode(ELayerAutoClearMode.PageChanged, False)
		viewImageSrc[1].SetLayerAutoClearMode(ELayerAutoClearMode.PageChanged, False)

		# 이미지 뷰를 갱신 합니다. # Update image view
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