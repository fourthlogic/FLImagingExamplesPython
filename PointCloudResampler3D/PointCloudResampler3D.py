# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():

	# 3D 뷰 선언 # Declare the 3d view
	view3DSrc = CGUIView3D()
	view3DUpsample = CGUIView3D()
	view3DDownsample = CGUIView3D()

	while True:
		
		# 3d 뷰 생성 # Create 3d object view
		if (res := view3DSrc.Create(100, 0, 612, 512)).IsFail() or \
			(res := view3DUpsample.Create(612, 0, 1124, 512)).IsFail() or \
			(res := view3DDownsample.Create(1124, 0, 1636, 512)).IsFail():
			ErrorPrint(res, "Failed to create 3D views")
			break

		#알고리즘 객체 생성 # declare algorithm instance
		pointCloudResampler3D = CPointCloudResampler3D()

		view3DSrc.SetTopologyType(ETopologyType3D.PointCloud)
		view3DUpsample.SetTopologyType(ETopologyType3D.PointCloud)
		view3DDownsample.SetTopologyType(ETopologyType3D.PointCloud)

		# 3D 뷰와 연결이 유지된 객체 생성 # Declare the object connected to 3D view
		view3DSrc.PushObject(CFL3DObject())
		viewObjectSrc = view3DSrc.GetView3DObject(0)
		floSrc = viewObjectSrc.Get3DObject()
		
		# 3D 뷰와 연결이 유지된 객체 생성 # Declare the object connected to 3D view
		view3DUpsample.PushObject(CFL3DObject())
		viewObjectUpsample = view3DUpsample.GetView3DObject(0)
		floUpsample = viewObjectUpsample.Get3DObject()
		
		# 3D 뷰와 연결이 유지된 객체 생성 # Declare the object connected to 3D view
		view3DDownsample.PushObject(CFL3DObject())
		viewObjectDownsample = view3DDownsample.GetView3DObject(0)
		floDownsample = viewObjectDownsample.Get3DObject()
		

		if (res := floSrc.Load("../../ExampleImages/CoordinateFrameUnification3D/Office_mosaicked(Middle).ply")).IsFail():
			ErrorPrint(res, "Failed to load source object.")
			break

		# 파라미터 설정 # Set parameter
		pointCloudResampler3D.SetSourceObject(floSrc)
		pointCloudResampler3D.SetColoringMode(EColoringMode.Interpolate)
		pointCloudResampler3D.EnableNormalInterpolation(True)
		pointCloudResampler3D.SetSamplingMode(CPointCloudResampler3D.ESamplingMode.Ratio_Strict)
		pointCloudResampler3D.EnableFaceReconstruction(False)
		pointCloudResampler3D.EnableFaceRetainment(False)
		
		pointCloudResampler3D.SetDestinationObject(floUpsample)
		pointCloudResampler3D.SetSampleRatio(20)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := pointCloudResampler3D.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break
		
		pointCloudResampler3D.SetDestinationObject(floDownsample)
		pointCloudResampler3D.SetSampleRatio(0.15)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := pointCloudResampler3D.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break
		
		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
		layer3DSrc = view3DSrc.GetLayer(0)
		layer3DUpsample = view3DUpsample.GetLayer(0)
		layer3DDownsample = view3DDownsample.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layer3DSrc.Clear()
		layer3DUpsample.Clear()
		layer3DDownsample.Clear()

		flpTopLeft = CFLPoint[Double](0, 0)

		if (res := layer3DSrc.DrawTextCanvas(flpTopLeft, "Source Object", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
		   (res := layer3DUpsample.DrawTextCanvas(flpTopLeft, "Destination Object(Upsample)", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
		   (res := layer3DDownsample.DrawTextCanvas(flpTopLeft, "Destination Object(Downsample)", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
		
			ErrorPrint(res, "Failed to draw text.\n")
			break
		
		viewObjectSrc.UpdateAll()
		viewObjectUpsample.UpdateAll()
		viewObjectDownsample.UpdateAll()
		
		view3DSrc.SynchronizePointOfView(view3DUpsample)
		view3DSrc.SynchronizeWindow(view3DUpsample)
		view3DSrc.SynchronizePointOfView(view3DDownsample)
		view3DSrc.SynchronizeWindow(view3DDownsample)
		
		#출력 뷰의 시점을 계산 # Calculate the viewpoint of destination view
		cam = CFL3DCamera()

		cam.SetProjectionType(E3DCameraProjectionType.Perspective)
		cam.SetDirection(CFLPoint3[Single](0.327705, 0.066764, -0.942418))
		cam.SetDirectionUp(CFLPoint3[Single](0.311277, 0.839746, -0.444896))
		cam.SetPosition(CFLPoint3[Single](-1.825832, 0.425620, 1.548716))
		cam.SetAngleOfViewY(45)

		view3DUpsample.SetCamera(cam)

		view3DSrc.UpdateObject(0)
		view3DUpsample.UpdateObject(0)
		view3DDownsample.UpdateObject(0)

		while view3DSrc.IsAvailable() and view3DUpsample.IsAvailable() and view3DDownsample.IsAvailable():
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