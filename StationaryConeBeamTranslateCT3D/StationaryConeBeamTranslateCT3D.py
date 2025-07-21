# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 # Main function
def main():
	
	# 이미지 객체 선언 # Declare the image object
	fliSrcImage = CFLImage()
	fliDstImage = CFLImage()
	fliDstSinoImage = CFLImage()
	floDestination = CFL3DObject()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSrc = CGUIViewImage()
	viewImageDst = CGUIViewImage()
	viewImageDstSino = CGUIViewImage()
	view3DDst = CGUIView3D()

	# 알고리즘 동작 결과 # Algorithm execution result
	res = CResult()

	while True:
		# 이미지 로드 # Load image
		if (res := fliSrcImage.Load("../../ExampleImages/StationaryConeBeamTranslateCT3D/")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break

		fliSrcImage.SelectPage(0)

		# 이미지 뷰 생성 # Create image view
		if (res := viewImageSrc.Create(100, 0, 548, 448)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break

		# 이미지 뷰에 이미지를 디스플레이 # Display an image in an image view
		if (res := viewImageSrc.SetImagePtr(fliSrcImage))[0].IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break

		# Destination 이미지 뷰 생성 # Create the destination image view
		if (res := viewImageDst.Create(548, 0, 996, 448)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 # Display the image in the destination image view
		if (res := viewImageDst.SetImagePtr(fliDstImage))[0].IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break

		# Destination 이미지 뷰 생성 # Create the destination image view
		if (res := viewImageDstSino.Create(100, 448, 548, 896)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 # Display the image in the destination image view
		if (res := viewImageDstSino.SetImagePtr(fliDstSinoImage))[0].IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break

		# Destination 3D 이미지 뷰 생성 # Create the destination 3D image view
		if (res := view3DDst.Create(548, 448, 996, 896)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break

		viewImageSrc.SetFixThumbnailView(True)

		# StationaryConeBeamTranslateCT3D 객체 생성 # Create StationaryConeBeamTranslateCT3D object
		algStationaryConeBeamTranslateCT3D = CStationaryConeBeamTranslateCT3D()

		# Source 이미지 설정 # Set the source image
		if (res := algStationaryConeBeamTranslateCT3D.SetSourceImage(fliSrcImage))[0].IsFail():
			break
		# 결과 destination height map 이미지 설정 # Set the destination height map image
		if (res := algStationaryConeBeamTranslateCT3D.SetDestinationImage(fliDstImage))[0].IsFail():
			break
		# 결과 destination texture 이미지 설정 # Set the destination texture image
		if (res := algStationaryConeBeamTranslateCT3D.SetDestinationSinogramImage(fliDstSinoImage))[0].IsFail():
			break
		# Destination 3D object 설정 # Set the Destination 3D object 
		if (res := algStationaryConeBeamTranslateCT3D.SetDestinationObject(floDestination))[0].IsFail():
			break

		if (res := algStationaryConeBeamTranslateCT3D.SetDestinationSinogramIndex(15)).IsFail():
			break

		if (res := algStationaryConeBeamTranslateCT3D.SetDetectorCellSizeUnit(0.08354)).IsFail():
			break
		if (res := algStationaryConeBeamTranslateCT3D.SetObjectTranslateDirection(CStationaryConeBeamTranslateCT3D.EObjectTranslateDirection.RightToLeft)).IsFail():
			break
		if (res := algStationaryConeBeamTranslateCT3D.SetSourceObjectDistanceUnit(13.60)).IsFail():
			break
		if (res := algStationaryConeBeamTranslateCT3D.SetSourceDetectorDistanceUnit(60.00)).IsFail():
			break
		if (res := algStationaryConeBeamTranslateCT3D.SetObjectTranslationDistanceUnit(24.00)).IsFail():
			break
		if (res := algStationaryConeBeamTranslateCT3D.SetPrincipalDeltaXPixel(0.00)).IsFail():
			break

		if (res := algStationaryConeBeamTranslateCT3D.SetNormalizedAirThreshold(0.60)).IsFail():
			break
		if (res := algStationaryConeBeamTranslateCT3D.SetSinogramKeepRatio(0.30)).IsFail():
			break
		if (res := algStationaryConeBeamTranslateCT3D.SetInterpolationCoefficient(6)).IsFail():
			break
		if (res := algStationaryConeBeamTranslateCT3D.SetMergeCoefficient(21)).IsFail():
			break
		if (res := algStationaryConeBeamTranslateCT3D.EnableFrequencyRampFilter(True)).IsFail():
			break
		if (res := algStationaryConeBeamTranslateCT3D.SetFrequencyWindow(CStationaryConeBeamTranslateCT3D.EFrequencyWindow.Gaussian)).IsFail():
			break
		if (res := algStationaryConeBeamTranslateCT3D.SetSigma(0.50)).IsFail():
			break

		if (res := algStationaryConeBeamTranslateCT3D.SetReconstructionPlaneCount(140)).IsFail():
			break
		if (res := algStationaryConeBeamTranslateCT3D.EnableNegativeClip(True)).IsFail():
			break
		if (res := algStationaryConeBeamTranslateCT3D.EnableCircularMask(True)).IsFail():
			break
		if (res := algStationaryConeBeamTranslateCT3D.EnableSigmoid(True)).IsFail():
			break
		if (res := algStationaryConeBeamTranslateCT3D.SetSigmoidB(1.00)).IsFail():
			break
		if (res := algStationaryConeBeamTranslateCT3D.SetSigmoidM(1.00)).IsFail():
			break
		if (res := algStationaryConeBeamTranslateCT3D.SetIntensityThreshold(190)).IsFail():
			break

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := algStationaryConeBeamTranslateCT3D.Execute()).IsFail():
			ErrorPrint(res, "Failed to execute algorithm.\n")
			break


		# 3D 이미지 뷰에 Destination Object 를 디스플레이
		floDestinationAlg = algStationaryConeBeamTranslateCT3D.GetDestinationObject()
		if (res := view3DDst.PushObject(floDestinationAlg)).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break


		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSrc = viewImageSrc.GetLayer(0)
		layerDst = viewImageDst.GetLayer(0)
		layerDstSino = viewImageDstSino.GetLayer(0)
		layer3D = view3DDst.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSrc.Clear()
		layerDst.Clear()
		layerDstSino.Clear()
		layer3D.Clear()

		# View 정보를 디스플레이 합니다. # Display View information.
		# 아래 함수 DrawTextCanvas은 Screen좌표를 기준으로 하는 String을 Drawing 한다.# The function DrawTextCanvas below draws a String based on the screen coordinates.
		# 파라미터 순서 : 레이어 -> 기준 좌표 Figure 객체 -> 문자열 -> 폰트 색 -> 면 색 -> 폰트 크기 -> 실제 크기 유무 -> 각도 ->
		#                 얼라인 -> 폰트 이름 -> 폰트 알파값(불투명도) -> 면 알파값 (불투명도) -> 폰트 두께 -> 폰트 이텔릭
		# Parameter order: layer -> reference coordinate Figure object -> string -> font color -> Area color -> font size -> actual size -> angle ->
		#                  Align -> Font Name -> Font Alpha Value (Opaqueness) -> Cotton Alpha Value (Opaqueness) -> Font Thickness -> Font Italic
		flp = CFLPoint[Double]()
		if (res := layerSrc.DrawTextCanvas(flp, "Source Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break

		if (res := layerDst.DrawTextCanvas(flp, "Destination Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break

		if (res := layerDstSino.DrawTextCanvas(flp, "Destination Sinogram Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break

		if (res := layer3D.DrawTextCanvas(flp, "Destination Object", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break


		# Zoom Fit
		if (res := viewImageSrc.ZoomFit()).IsFail():
			ErrorPrint(res, "Failed to zoom fit of the image view.\n")
			break

		if (res := viewImageDst.ZoomFit()).IsFail():
			ErrorPrint(res, "Failed to zoom fit of the image view.\n")
			break

		if (res := viewImageDstSino.ZoomFit()).IsFail():
			ErrorPrint(res, "Failed to zoom fit of the image view.\n")
			break

		if (res := view3DDst.ZoomFit()).IsFail():
			ErrorPrint(res, "Failed to zoom fit of the image view.\n")
			break


		cameraNew = CGUIView3DCamera()
		cameraNew.Assign(view3DDst.GetCamera())
		flpPositionOld = cameraNew.GetPosition()
		flpPositionOld.y = flpPositionOld.z
		cameraNew.SetPosition(flpPositionOld, False)
		view3DDst.SetCamera(cameraNew)

		# 이미지 뷰를 갱신 합니다. # Update image view
		viewImageSrc.Invalidate(True)
		viewImageDst.Invalidate(True)
		viewImageDstSino.Invalidate(True)
		view3DDst.Invalidate(True)

		# 이미지 뷰, 3D 뷰가 종료될 때 까지 기다림 # Wait for the image and 3D view to close
		while viewImageSrc.IsAvailable() and viewImageDst.IsAvailable() and viewImageDstSino.IsAvailable() and view3DDst.IsAvailable():			
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