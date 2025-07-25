# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

CLibraryUtilities.Initialize()


# 메인 함수 # Main function
def main():
	# 이미지 객체 선언 # Declare the image object
	fliSrcImage = CFLImage()
	fliDstImage = CFLImage()
	fliTxtImage = CFLImage()
	floDstObject = CFL3DObjectHeightMap()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSrc = CGUIViewImage()
	viewImageDst = CGUIViewImage()
	view3DDst = CGUIView3D()

	res = CResult()

	while True:
		# 이미지 로드 # Load image
		if (res := fliSrcImage.Load("../../ExampleImages/MultiFocusMAPBased3D/")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break
		
		# 이미지 뷰 생성 # Create image view
		if ((res := viewImageSrc.Create(100, 0, 600, 500)).IsFail() or
			(res := viewImageDst.Create(600, 0, 1100, 500)).IsFail() or
			(res := view3DDst.Create(400, 200, 1300, 800)).IsFail()):
			ErrorPrint(res, "Failed to create the image view.\n")
			break
		
		# 이미지 뷰에 이미지를 디스플레이 # Display an image in an image view
		if ((res := viewImageSrc.SetImagePtr(fliSrcImage)[0]).IsFail() or
			(res := viewImageDst.SetImagePtr(fliDstImage)[0]).IsFail()):
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break

		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
		if (res := viewImageSrc.SynchronizePointOfView(viewImageDst)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize view. \n")
			break

		# 두 뷰 윈도우의 위치를 동기화 한다 # Synchronize the position of the two view windows.
		if (res := viewImageSrc.SynchronizeWindow(viewImageDst)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize view. \n")
			break

		viewImageSrc.SetFixThumbnailView(True)

		
		# 알고리즘 객체 생성 # Create algorithm object
		algObject = CMultiFocusMAPBased3D()

		# Source 이미지 설정 # Set the source image
		if (res := algObject.SetSourceImage(fliSrcImage)[0]).IsFail():
			break
		# 결과 destination height map 이미지 설정 # Set the destination height map image
		if (res := algObject.SetDestinationHeightMapImage(fliDstImage)[0]).IsFail():
			break
		# 결과 destination texture 이미지 설정 # Set the destination texture image
		if (res := algObject.SetDestinationTextureImage(fliTxtImage)[0]).IsFail():
			break

		# Focus measure bias page index 설정 # Set the focus measure bias page index
		if (res := algObject.SetFMBiasPageIndex(3)).IsFail():
			break
		# Focus measure bias value 설정 # Set the Focus measure bias value
		if (res := algObject.SetFMBiasValue(0.02)).IsFail():
			break
		# Focus measure method 설정 # Set focus measure method
		if (res := algObject.SetFocusMeasureMethod(CMultiFocusMAPBased3D.EFocusMeasureMethod.DoG)).IsFail():
			break
		# Sigma1 설정 # Set the sigma1
		if (res := algObject.SetSigma1(0.4)).IsFail():
			break
		# Sigma2 설정 # Set the sigma2
		if (res := algObject.SetSigma2(0.8)).IsFail():
			break

		# Local regularization factor 설정 # Set the local regularization factor
		if (res := algObject.SetLocalRegularizationFactor(0.02)).IsFail():
			break
		# Global regularization factor 설정 # Set the global regularization factor
		if (res := algObject.SetGlobalRegularizationFactor(0.00000000001)).IsFail():
			break
		# Conjugate Gradient Method 의 tolerance 설정 # Set the tolerance for Conjugate Gradient Method
		if (res := algObject.SetCGMTolerance(0.00001)).IsFail():
			break
		# Conjugate Gradient Method 의 max iterations 설정 # Set the max iterations for Conjugate Gradient Method
		if (res := algObject.SetCGMMaxIterations(100)).IsFail():
			break

		# Page Direction 설정 # Set the page direction
		if (res := algObject.SetDirection(CMultiFocusMAPBased3D.EDirection.BottomToTop)).IsFail():
			break
		# Pixel Accuracy 설정 # Set the pixel accuracy
		if (res := algObject.SetPixelAccuracy(1.0)).IsFail():
			break
		# Depth Pitch 설정 # Set the depth pitch
		if (res := algObject.SetDepthPitch(2.0)).IsFail():
			break

		# Destination 3D object 생성 활성화 # Enable the Destination 3D object generation
		if (res := algObject.Enable3DObjectGeneration(True)).IsFail():
			break
		# Destination 3D object 설정 # Set the Destination 3D object 
		if (res := algObject.SetDestinationObject(floDstObject)[0]).IsFail():
			break
		
		# 알고리즘 수행 # Execute the algorithm
		if (res := algObject.Execute()).IsFail():
			ErrorPrint(res, "Failed to execute the algorithm.")
			break
		

		# floDstObject.SetTextureImage(fliTxtImage)
		# floDstObject.ActivateVertexColorTexture(True)

		# 3D 이미지 뷰에 Height Map (Destination Image) 이미지를 디스플레이 # Display the Height Map (Destination Image) on the 3D image view
		if view3DDst.PushObject(floDstObject).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSrc = viewImageSrc.GetLayer(0)
		layerDst = viewImageDst.GetLayer(0)
		layer3D = view3DDst.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSrc.Clear()
		layerDst.Clear()
		layer3D.Clear()
		
		# 이미지 뷰 정보 표시 # Display image view information
		flpTemp = CFLPoint[Double](0, 0)
		if ((res := layerSrc.DrawTextCanvas(flpTemp, "Source Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or
			(res := layerDst.DrawTextCanvas(flpTemp, "Destination Height Map Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or
			(res := layer3D.DrawTextCanvas(flpTemp, "Destination Object", EColor.YELLOW, EColor.BLACK, 20)).IsFail()):
			ErrorPrint(res, "Failed to draw text.\n")
			break
				
		viewImageSrc.SetLayerAutoClearMode(ELayerAutoClearMode.PageChanged, False)
		
		# Zoom Fit
		if ((res := viewImageSrc.ZoomFit()).IsFail() or
			(res := viewImageDst.ZoomFit()).IsFail() or
			(res := view3DDst.ZoomFit()).IsFail()):
			ErrorPrint(res, "Failed to zoom fit of the image view.\n")
			break
		
		# 이미지 뷰를 갱신 # Update image view
		viewImageSrc.Invalidate(True)
		viewImageDst.Invalidate(True)
		view3DDst.Invalidate(True)

		# 이미지 뷰, 3D 뷰가 종료될 때 까지 기다림 # Wait for the image and 3D view to close
		while viewImageSrc.IsAvailable() and viewImageDst.IsAvailable() and view3DDst.IsAvailable():			
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