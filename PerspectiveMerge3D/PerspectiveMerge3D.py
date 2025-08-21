# FLImagingClrPy 선언 # Declare FLImagingClrPy
from pydoc import visiblename
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():

	# 3D 뷰 선언 # Declare the 3d view
	view3DSrc1 = CGUIView3D()
	view3DSrc2 = CGUIView3D()
	view3DDst = CGUIView3D()
	viewTestDescription = CGUIViewImage()

	while True:
		# Source 3D 뷰 생성 # Create the Source 3D view
		if (res := view3DSrc1.Create(100, 0, 600, 500)).IsFail() or \
			(res := view3DSrc2.Create(600, 0, 1100, 500)).IsFail():
			ErrorPrint(res, "Failed to create the 3D view.\n")
			break

		# Destination 3D 뷰 생성 # Create the destination 3D view
		if (res := view3DDst.Create(1100, 0, 1600, 500)).IsFail():
			ErrorPrint(res, "Failed to create the 3D view.\n")
			break

		if (res := viewTestDescription.Create(100, 500, 600, 1000)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break

		#알고리즘 객체 생성 # declare algorithm instance
		perspectiveMerge3D = CPerspectiveMerge3D()
		
		floSrc1 = CFL3DObject()
		floSrc2 = CFL3DObject()
		floDst = CFL3DObject()
		
		if (res := floSrc1.Load("../../ExampleImages/PerspectiveMerge3D/Left Cam.ply")).IsFail() or \
			(res := floSrc2.Load("../../ExampleImages/PerspectiveMerge3D/Right Cam.ply")).IsFail():
			ErrorPrint(res, "Failed to load source object")
			break
		
		tpPosition = TPoint3[Single](-0.152, 0, 0)
		tpRotation = TPoint3[Single](-90, 8, -29)
		tpPosition2 = TPoint3[Single](0.152, 0, 0)
		tpRotation2 = TPoint3[Single](-90, 8, 29)
		# 파라미터 설정 # Set parameter
		
		# 카메라 1, 2의 Source 객체 설정 # Set the source object of camera 1, 2
		perspectiveMerge3D.AddSourceObject(floSrc1, tpPosition, tpRotation)
		perspectiveMerge3D.AddSourceObject(floSrc2, tpPosition2, tpRotation2)
		# Destination 객체 설정 # Set the destination object
		perspectiveMerge3D.SetDestinationObject(floDst)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := perspectiveMerge3D.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break


		# Destination 이미지가 새로 생성됨으로 Zoom fit 을 통해 디스플레이 되는 이미지 배율을 화면에 맞춰준다. # With the newly created Destination image, the image magnification displayed through Zoom fit is adjusted to the screen.
		view3DSrc1.PushObject(floSrc1)
		view3DSrc2.PushObject(floSrc2)
		view3DDst.PushObject(floDst)
		view3DSrc1.ZoomFit()
		view3DSrc2.ZoomFit()
		view3DDst.ZoomFit()
		
		fliTestDescription = CFLImage()
		fliTestDescription.Load("../../ExampleImages/PerspectiveMerge3D/Test Environment.flif")
		viewTestDescription.SetImagePtr(fliTestDescription)


		
		#화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layer3DSrc1 = view3DSrc1.GetLayer(0)
		layer3DSrc2 = view3DSrc2.GetLayer(0)
		layer3DDst = view3DDst.GetLayer(0)
		layerTestDescription = viewTestDescription.GetLayer(0)

		flpTopLeft = CFLPoint[Double]()

		if (res := layer3DSrc1.DrawTextCanvas(flpTopLeft, "Left Camera", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
			(res := layer3DSrc2.DrawTextCanvas(flpTopLeft, "Right Camera", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
			(res := layer3DDst.DrawTextCanvas(flpTopLeft, "Result", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or\
			(res := layerTestDescription.DrawTextCanvas(flpTopLeft, "Test Environment", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break

		# 이미지 뷰를 갱신 합니다. # Update image view
		view3DSrc1.Invalidate(True)
		view3DSrc2.Invalidate(True)
		view3DDst.Invalidate(True)
		viewTestDescription.Invalidate(True)

		#이미지 뷰, 3D 뷰가 종료될 때 까지 기다림 # Wait for the image and 3D view to close
		while view3DSrc1.IsAvailable() and view3DSrc2.IsAvailable() and view3DDst.IsAvailable() and viewTestDescription.IsAvailable():
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