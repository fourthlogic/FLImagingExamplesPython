# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



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

		# 이미지 뷰 생성 # Create image view
		if ((res := viewImageSrc.Create(100, 0, 600, 500)).IsFail() or
			(res := viewImageDst.Create(600, 0, 1100, 500)).IsFail() or
			(res := viewImageDstSino.Create(100, 500, 600, 1000)).IsFail() or
			(res := view3DDst.Create(600, 500, 1100, 1000)).IsFail()):
			ErrorPrint(res, "Failed to create the image view.\n")
			break

		# 이미지 뷰에 이미지를 디스플레이 # Display an image in an image view
		if ((res := viewImageSrc.SetImagePtr(fliSrcImage)[0]).IsFail() or
			(res := viewImageDst.SetImagePtr(fliDstImage)[0]).IsFail() or
			(res := viewImageDstSino.SetImagePtr(fliDstSinoImage)[0]).IsFail()):
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break
		
		viewImageSrc.SetFixThumbnailView(True)


		# 알고리즘 객체 생성 # Create algorithm object
		stationaryConeBeamTranslateCT3D = CStationaryConeBeamTranslateCT3D()

		if (res := stationaryConeBeamTranslateCT3D.SetSourceImage(fliSrcImage)[0]).IsFail():
			break
		if (res := stationaryConeBeamTranslateCT3D.SetDestinationImage(fliDstImage)[0]).IsFail():
			break
		if (res := stationaryConeBeamTranslateCT3D.SetDestinationSinogramImage(fliDstSinoImage)[0]).IsFail():
			break
		if (res := stationaryConeBeamTranslateCT3D.SetDestinationObject(floDestination)[0]).IsFail():
			break

		if (res := stationaryConeBeamTranslateCT3D.SetDestinationSinogramIndex(15)).IsFail():
			break

		if (res := stationaryConeBeamTranslateCT3D.SetDetectorCellSizeUnit(0.08354)).IsFail():
			break
		if (res := stationaryConeBeamTranslateCT3D.SetObjectTranslateDirection(CStationaryConeBeamTranslateCT3D.EObjectTranslateDirection.RightToLeft)).IsFail():
			break
		if (res := stationaryConeBeamTranslateCT3D.SetSourceObjectDistanceUnit(13.60)).IsFail():
			break
		if (res := stationaryConeBeamTranslateCT3D.SetSourceDetectorDistanceUnit(60.00)).IsFail():
			break
		if (res := stationaryConeBeamTranslateCT3D.SetObjectTranslationDistanceUnit(24.00)).IsFail():
			break
		if (res := stationaryConeBeamTranslateCT3D.SetPrincipalDeltaXPixel(0.00)).IsFail():
			break

		if (res := stationaryConeBeamTranslateCT3D.SetNormalizedAirThreshold(0.60)).IsFail():
			break
		if (res := stationaryConeBeamTranslateCT3D.SetSinogramKeepRatio(0.30)).IsFail():
			break
		if (res := stationaryConeBeamTranslateCT3D.SetInterpolationCoefficient(6)).IsFail():
			break
		if (res := stationaryConeBeamTranslateCT3D.SetMergeCoefficient(21)).IsFail():
			break
		if (res := stationaryConeBeamTranslateCT3D.EnableFrequencyRampFilter(True)).IsFail():
			break
		if (res := stationaryConeBeamTranslateCT3D.SetFrequencyWindow(CStationaryConeBeamTranslateCT3D.EFrequencyWindow.Gaussian)).IsFail():
			break
		if (res := stationaryConeBeamTranslateCT3D.SetSigma(0.50)).IsFail():
			break

		if (res := stationaryConeBeamTranslateCT3D.SetReconstructionPlaneCount(140)).IsFail():
			break
		if (res := stationaryConeBeamTranslateCT3D.EnableNegativeClip(True)).IsFail():
			break
		if (res := stationaryConeBeamTranslateCT3D.EnableCircularMask(True)).IsFail():
			break
		if (res := stationaryConeBeamTranslateCT3D.EnableSigmoid(True)).IsFail():
			break
		if (res := stationaryConeBeamTranslateCT3D.SetSigmoidB(1.00)).IsFail():
			break
		if (res := stationaryConeBeamTranslateCT3D.SetSigmoidM(1.00)).IsFail():
			break
		if (res := stationaryConeBeamTranslateCT3D.SetIntensityThreshold(190)).IsFail():
			break
		
		# 알고리즘 수행 # Execute the algorithm
		if (res := stationaryConeBeamTranslateCT3D.Execute()).IsFail():
			ErrorPrint(res, "Failed to execute the algorithm.")
			break


		# 3D 이미지 뷰에 Destination Object 를 디스플레이
		floDestinationAlg = stationaryConeBeamTranslateCT3D.GetDestinationObject()
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
		
		# 이미지 뷰 정보 표시 # Display image view information
		flp = CFLPoint[Double]()
		if ((res := layerSrc.DrawTextCanvas(flp, "Source Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or
			(res := layerDst.DrawTextCanvas(flp, "Destination Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or
			(res := layerDstSino.DrawTextCanvas(flp, "Destination Sinogram Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or
			(res := layer3D.DrawTextCanvas(flp, "Destination Object", EColor.YELLOW, EColor.BLACK, 20)).IsFail()):
			ErrorPrint(res, "Failed to draw text.\n")
			break
		
		viewImageSrc.SetLayerAutoClearMode(ELayerAutoClearMode.PageChanged, False)
		viewImageDst.SetLayerAutoClearMode(ELayerAutoClearMode.PageChanged, False)

		# Zoom Fit
		if ((res := viewImageSrc.ZoomFit()).IsFail() or
			(res := viewImageDst.ZoomFit()).IsFail() or
			(res := viewImageDstSino.ZoomFit()).IsFail() or
			(res := view3DDst.ZoomFit()).IsFail()):
			ErrorPrint(res, "Failed to zoom fit of the image view.\n")
			break

		# 3D 뷰 카메라 수정 # Modify 3D view camera
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