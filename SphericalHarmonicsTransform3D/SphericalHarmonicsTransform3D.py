# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():

	# 3D 뷰 선언 # Declare the 3d view
	view3DSrc = CGUIView3D()
	view3DDst1 = CGUIView3D()
	view3DDst2 = CGUIView3D()

	while True:
		
		# Source 3D 뷰 생성 # Create the Source 3D view
		if (res := view3DSrc.Create(100, 0, 600, 500)).IsFail():
			ErrorPrint(res, "Failed to create the 3D view.\n")
			break

		# Destination 1 3D 뷰 생성 # Create the destination 3D view
		if (res := view3DDst1.Create(600, 0, 1100, 500)).IsFail():
			ErrorPrint(res, "Failed to create the 3D view.\n")
			break

		# Destination 2 3D 뷰 생성 # Create the destination 3D view
		if (res := view3DDst2.Create(1100, 0, 1600, 500)).IsFail():
			ErrorPrint(res, "Failed to create the 3D view.\n")
			break

		#알고리즘 객체 생성 # declare algorithm instance
		sphericalHarmonicsTransform3D = CSphericalHarmonicsTransform3D()
		
		floSrc = CFL3DObject()
		floDst1 = CFL3DObject()
		floDst2 = CFL3DObject()
		
		if (res := floSrc.Load("../../ExampleImages/SphericalHarmonicsTransform3D/Airplane.fl3do")).IsFail():
			ErrorPrint(res, "Failed to load source object")
			break

		# 파라미터 설정 # Set parameter
		sphericalHarmonicsTransform3D.SetSourceObject(floSrc)
		sphericalHarmonicsTransform3D.SetDestinationObject(floDst1)
		sphericalHarmonicsTransform3D.SetDirectionType(CSphericalHarmonicsTransform3D.ETransformDirection.Forward)
		sphericalHarmonicsTransform3D.SetMaxDegree(15)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := sphericalHarmonicsTransform3D.Execute()).IsFail():
			ErrorPrint(res, 'Failed to Forward.')
			break

		# 파라미터 설정 # Set parameter
		sphericalHarmonicsTransform3D.SetSourceObject(floDst1)
		sphericalHarmonicsTransform3D.SetDestinationObject(floDst2)
		sphericalHarmonicsTransform3D.SetDirectionType(CSphericalHarmonicsTransform3D.ETransformDirection.Inverse)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := sphericalHarmonicsTransform3D.Execute()).IsFail():
			ErrorPrint(res, 'Failed to Inverse.')
			break

		#화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layer3DSrc = view3DSrc.GetLayer(0)
		layer3DDst1 = view3DDst1.GetLayer(0)
		layer3DDst2 = view3DDst2.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layer3DSrc.Clear()
		layer3DDst1.Clear()
		layer3DDst2.Clear()

		# Destination 이미지가 새로 생성됨으로 Zoom fit 을 통해 디스플레이 되는 이미지 배율을 화면에 맞춰준다. # With the newly created Destination image, the image magnification displayed through Zoom fit is adjusted to the screen.
		view3DSrc.PushObject(floSrc)
		view3DDst1.PushObject(floDst1)
		view3DDst1.SetPointSize(10)
		view3DDst2.PushObject(floDst2)
		view3DDst2.SetPointSize(2);
		view3DDst2.SetShadingType(EShadingType3D.Shadeless);
		view3DDst2.SynchronizePointOfView(view3DSrc);

		view3DSrc.ZoomFit()
		view3DDst1.ZoomFit()
		view3DDst2.ZoomFit()

		flpTopLeft = CFLPoint[Double]()

		if (res := layer3DSrc.DrawTextCanvas(flpTopLeft, "Source Object", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
		   (res := layer3DDst1.DrawTextCanvas(flpTopLeft, "Forward Result", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
		   (res := layer3DDst2.DrawTextCanvas(flpTopLeft, "Inverse Result", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break

		# 이미지 뷰를 갱신 합니다. # Update image view
		view3DSrc.Invalidate(True)
		view3DDst1.Invalidate(True)
		view3DDst2.Invalidate(True)

		#이미지 뷰, 3D 뷰가 종료될 때 까지 기다림 # Wait for the image and 3D view to close
		while (view3DSrc.IsAvailable() and view3DDst1.IsAvailable() and view3DDst2.IsAvailable()):
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