# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():
	fliSrcImage = CFLImage()
	fliDarkFieldImage = CFLImage()
	fliFlatFieldImage = CFLImage()
	fliDstImage = CFLImage()
	floDstObject = CFL3DObject()

	# 이미지 뷰 선언 # Declare image view
	viewImageSrc = CGUIViewImage()
	viewImageDarkField = CGUIViewImage()
	viewImageFlatField = CGUIViewImage()
	viewImageDst = CGUIViewImage()
	view3DDst = CGUIView3D()

	# 알고리즘 동작 결과 # Algorithm execution result
	res = CResult()

	while True:
		# Source 이미지 로드 # Load the source image
		if (res := fliSrcImage.Load("../../ExampleImages/ComputedTomographyGeneralizedCT/Src_Preprocessing.flif")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break
		

		fliSrcImage.SelectPage(0)

		# Source 이미지 뷰 생성 # Create the source image view
		if (res := viewImageSrc.Create(100, 0, 548, 448)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break
		

		# Source 이미지 뷰에 이미지를 디스플레이 # Display the image in the source image view
		if (res := viewImageSrc.SetImagePtr(fliSrcImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break
		

		# Dark Field 이미지 로드 # Load the dark field image
		if (res := fliDarkFieldImage.Load("../../ExampleImages/ComputedTomographyGeneralizedCT/DarkField.flif")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break
		

		# Dark Field 이미지 뷰 생성 # Create the dark field image view
		if (res := viewImageDarkField.Create(548, 0, 996, 448)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break
		

		# Dark Field 이미지 뷰에 이미지를 디스플레이 # Display the image in the dark field image view
		if (res := viewImageDarkField.SetImagePtr(fliDarkFieldImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break
		

		# Flat Field 이미지 로드 # Load the flat field image
		if (res := fliFlatFieldImage.Load("../../ExampleImages/ComputedTomographyGeneralizedCT/FlatField.flif")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break
		

		# Flat Field 이미지 뷰 생성 # Create the flat field image view
		if (res := viewImageFlatField.Create(996, 0, 1444, 448)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break
		

		# Flat Field 이미지 뷰에 이미지를 디스플레이 # Display the image in the flat field image view
		if (res := viewImageFlatField.SetImagePtr(fliFlatFieldImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break
		

		# Destination 이미지 뷰 생성 # Create the destination image view
		if (res := viewImageDst.Create(548, 448, 996, 896)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break
		

		# Destination 이미지 뷰에 이미지를 디스플레이 # Display the image in the destination image view
		if (res := viewImageDst.SetImagePtr(fliDstImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break
		

		# Destination 3D 이미지 뷰 생성 # Create the destination 3D image view
		if (res := view3DDst.Create(996, 448, 1444, 896)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break
		

		viewImageSrc.SetFixThumbnailView(True)

		# 알고리즘 객체 생성 # Create algorithm object
		computedTomographyGeneralizedCT = CComputedTomographyGeneralizedCT()

		if (res := computedTomographyGeneralizedCT.LoadCSV("../../ExampleImages/ComputedTomographyGeneralizedCT/geometry_preprocessing.csv")).IsFail():
			break
		if (res := computedTomographyGeneralizedCT.SetSourceImage(fliSrcImage)).IsFail():
			break
		if (res := computedTomographyGeneralizedCT.SetDestinationImage(fliDstImage)).IsFail():
			break
		if (res := computedTomographyGeneralizedCT.SetDestinationObject(floDstObject)).IsFail():
			break

		if (res := computedTomographyGeneralizedCT.EnablePreprocessing(True)).IsFail():
			break
		if (res := computedTomographyGeneralizedCT.SetDarkFieldImage(fliDarkFieldImage)).IsFail():
			break
		if (res := computedTomographyGeneralizedCT.SetFlatFieldImage(fliFlatFieldImage)).IsFail():
			break
		if (res := computedTomographyGeneralizedCT.SetMedianFilterKernel(3)).IsFail():
			break

		if (res := computedTomographyGeneralizedCT.SetAngleUnit(EAngleUnit.Degree)).IsFail():
			break

		tpObjectVoxelSize = TPoint3[Single]()
		tpObjectVoxelSize.x = 0.02
		tpObjectVoxelSize.y = 0.02
		tpObjectVoxelSize.z = 0.02
		if (res := computedTomographyGeneralizedCT.SetObjectVoxelSize(tpObjectVoxelSize)).IsFail():
			break
		tpObjectVoxelCount = TPoint3[Int32]()
		tpObjectVoxelCount.x = 150
		tpObjectVoxelCount.y = 150
		tpObjectVoxelCount.z = 150
		if (res := computedTomographyGeneralizedCT.SetObjectVoxelCount(tpObjectVoxelCount)).IsFail():
			break
		tpObjectVoxelSubdivisionCount = TPoint3[Int32]()
		tpObjectVoxelSubdivisionCount.x = 1
		tpObjectVoxelSubdivisionCount.y = 1
		tpObjectVoxelSubdivisionCount.z = 1
		if (res := computedTomographyGeneralizedCT.SetObjectVoxelSubdivisionCount(tpObjectVoxelSubdivisionCount)).IsFail():
			break
		tpObjectVoxelOffset = TPoint3[Int32]()
		tpObjectVoxelOffset.x = 0
		tpObjectVoxelOffset.y = 0
		tpObjectVoxelOffset.z = 0
		if (res := computedTomographyGeneralizedCT.SetObjectVoxelOffset(tpObjectVoxelOffset)).IsFail():
			break

		if (res := computedTomographyGeneralizedCT.EnableFrequencyRampFilter(true)).IsFail():
			break
		if (res := computedTomographyGeneralizedCT.SetFrequencyWindow(CComputedTomographyGeneralizedCT.EFrequencyWindow.Gaussian)).IsFail():
			break
		if (res := computedTomographyGeneralizedCT.SetSigma(0.50)).IsFail():
			break

		if (res := computedTomographyGeneralizedCT.SetOutputFormat(CComputedTomographyGeneralizedCT.EOutputFormat.U8)).IsFail():
			break
		if (res := computedTomographyGeneralizedCT.SetSigmoidB(1000.00)).IsFail():
			break
		if (res := computedTomographyGeneralizedCT.SetSigmoidM(0.00)).IsFail():
			break
		if (res := computedTomographyGeneralizedCT.SetIntensityThreshold(200)).IsFail():
			break
		if (res := computedTomographyGeneralizedCT.SetSlicingPlane(CComputedTomographyGeneralizedCT.ESlicingPlane.Coronal)).IsFail():
			break

		# 알고리즘 수행 # Execute the algorithm
		if (res := computedTomographyGeneralizedCT.Execute()).IsFail():
			ErrorPrint(res, "Failed to execute algorithm.")
			break
		


		# 3D 이미지 뷰에 Destination Object 를 디스플레이
		if (res := view3DDst.PushObject(floDstObject)).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break
		

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layerSrc = viewImageSrc.GetLayer(0)
		layerDarkField = viewImageDarkField.GetLayer(0)
		layerFlatField = viewImageFlatField.GetLayer(0)
		layerDst = viewImageDst.GetLayer(0)
		layer3D = view3DDst.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layerSrc.Clear()
		layerDarkField.Clear()
		layerFlatField.Clear()
		layerDst.Clear()
		layer3D.Clear()

		# 이미지 뷰 정보 표시 # Display image view information
		CFLPoint<double> flp = CFLPoint<double>()
		if((res := layerSrc.DrawTextCanvas(flp, "Source Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or
			(res := layerDarkField.DrawTextCanvas(flp, "Dark Field Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or
			(res := layerFlatField.DrawTextCanvas(flp, "Flat Field Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or
			(res := layerDst.DrawTextCanvas(flp, "Destination Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or
			(res := layer3D.DrawTextCanvas(flp, "Destination Object", EColor.YELLOW, EColor.BLACK, 20)).IsFail()):
			ErrorPrint(res, "Failed to draw text.\n")
			break
		

		viewImageSrc.SetLayerAutoClearMode(ELayerAutoClearMode.PageChanged, false)
		viewImageDst.SetLayerAutoClearMode(ELayerAutoClearMode.PageChanged, false)

		# Zoom Fit
		viewImageSrc.ZoomFit()
		viewImageDarkField.ZoomFit()
		viewImageFlatField.ZoomFit()
		viewImageDst.ZoomFit()
		view3DDst.ZoomFit()

		# 이미지 뷰를 갱신 합니다. # Update image view
		viewImageSrc.Invalidate(true)
		viewImageDarkField.Invalidate(true)
		viewImageFlatField.Invalidate(true)
		viewImageDst.Invalidate(true)
		view3DDst.Invalidate(true)

		# 이미지 뷰, 3D 뷰가 종료될 때 까지 기다림
		while viewImageSrc.IsAvailable() and viewImageDarkField.IsAvailable() and viewImageFlatField.IsAvailable() and viewImageDst.IsAvailable() and view3DDst.IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	# End of main function



# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()nError name : {res.GetString()n')


if __name__ == '__main__':
    main()