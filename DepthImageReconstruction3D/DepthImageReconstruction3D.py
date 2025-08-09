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
	fliTxtImage = CFLImage()
	floDstObject = CFL3DObjectHeightMap()

	# 이미지 뷰 선언 # Declare the image view
	viewImageSrc = CGUIViewImage()
	viewImageDst = CGUIViewImage()
	view3DDst = CGUIView3D()

	res = CResult()

	while True:
		# 이미지 로드 # Load image
		if (res := fliSrcImage.Load("../../ExampleImages/DepthImageReconstruction3D/")).IsFail():
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
		depthImageReconstruction3D = CDepthImageReconstruction3D()

		# Source 이미지 설정 # Set the source image
		if (res := depthImageReconstruction3D.SetSourceImage(fliSrcImage)[0]).IsFail():
			break
		# Destination Height Map 이미지 설정 # Set the destination height map image
		if (res := depthImageReconstruction3D.SetDestinationHeightMapImage(fliDstImage)[0]).IsFail():
			break
		# Destination Texture 이미지 설정 # Set the destination texture image
		if (res := depthImageReconstruction3D.SetDestinationTextureImage(fliTxtImage)[0]).IsFail():
			break
		# Destination 3D Object 설정 # Set the Destination 3D Object 
		if (res := depthImageReconstruction3D.SetDestinationObject(floDstObject)[0]).IsFail():
			break
		# Pixel Accuracy 설정 # Set the pixel accuracy
		if (res := depthImageReconstruction3D.SetPixelAccuracy(0.1)).IsFail():
			break
		# Depth Pitch 설정 # Set the depth pitch
		if (res := depthImageReconstruction3D.SetDepthPitch(0.2)).IsFail():
			break
		# Filter 설정 # Set filter
		if (res := depthImageReconstruction3D.SetFilter(CDepthImageReconstruction3D.EFilter.FLDenoisingType1)).IsFail():
			break
		if (res := depthImageReconstruction3D.SetFLDenoisingKernel(7)).IsFail():
			break
		if (res := depthImageReconstruction3D.SetFLDenoisingSigma(15.00)).IsFail():
			break
		if (res := depthImageReconstruction3D.SetFLDenoisingAmplitude(15.00)).IsFail():
			break
		if (res := depthImageReconstruction3D.EnableGaussianInterpolation(True)).IsFail():
			break
		
		# 알고리즘 수행 # Execute the algorithm
		if (res := depthImageReconstruction3D.Execute()).IsFail():
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
		
		# 이미지 뷰를 갱신 합니다. # Update image view
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