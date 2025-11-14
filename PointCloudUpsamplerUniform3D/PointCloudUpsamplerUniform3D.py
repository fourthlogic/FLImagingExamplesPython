# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():

	# 3D 뷰 선언 # Declare the 3d view
	view3DSrc = CGUIView3D()
	view3DDst = CGUIView3D()

	while True:
		
		# 3d 뷰 생성 # Create 3d object view
		if (res := view3DSrc.Create(100, 0, 612, 512)).IsFail() or \
			(res := view3DDst.Create(612, 0, 1124, 512)).IsFail():
			ErrorPrint(res, "Failed to create 3D views")
			break

		#알고리즘 객체 생성 # declare algorithm instance
		pointCloudUpsamplerUniform3D = CPointCloudUpsamplerUniform3D()

		view3DSrc.SetTopologyType(ETopologyType3D.PointCloud)
		view3DDst.SetTopologyType(ETopologyType3D.PointCloud)

		# 3D 뷰와 연결이 유지된 객체 생성 # Declare the object connected to 3D view
		view3DSrc.PushObject(CFL3DObject())
		viewObjectSrc = view3DSrc.GetView3DObject(0)
		floSrc = viewObjectSrc.Get3DObject()
		
		# 3D 뷰와 연결이 유지된 객체 생성 # Declare the object connected to 3D view
		view3DDst.PushObject(CFL3DObject())
		viewObjectDst = view3DDst.GetView3DObject(0)
		floDst = viewObjectDst.Get3DObject()
		
		if (res := floSrc.Load("../../ExampleImages/CoordinateFrameUnification3D/Office_mosaicked(Middle).ply")).IsFail():
			ErrorPrint(res, "Failed to load source object.")
			break

		# 파라미터 설정 # Set parameter
		pointCloudUpsamplerUniform3D.SetSourceObject(floSrc)
		pointCloudUpsamplerUniform3D.SetDestinationObject(floDst)
		pointCloudUpsamplerUniform3D.SetColoringMode(EColoringMode.Interpolate)
		pointCloudUpsamplerUniform3D.EnableNormalInterpolation(True)
		pointCloudUpsamplerUniform3D.SetSamplingSize(10 ** 7)
		pointCloudUpsamplerUniform3D.EnableCopyVertex(True)
		pointCloudUpsamplerUniform3D.EnableFaceReconstruction(False)
		pointCloudUpsamplerUniform3D.EnableFaceRetainment(False)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := pointCloudUpsamplerUniform3D.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break
		
		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
		layer3DSrc = view3DSrc.GetLayer(0);
		layer3DDst = view3DDst.GetLayer(0);

		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layer3DSrc.Clear();
		layer3DDst.Clear();

		flpTopLeft = CFLPoint[Double](0, 0);

		if (res := layer3DSrc.DrawTextCanvas(flpTopLeft, "Source Object", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
		   (res := layer3DDst.DrawTextCanvas(flpTopLeft, "Destination Object", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
		
			ErrorPrint(res, "Failed to draw text.\n");
			break;
		
		viewObjectSrc.UpdateAll()
		viewObjectDst.UpdateAll()

		view3DSrc.UpdateObject(0)
		view3DDst.UpdateObject(0)

		view3DSrc.SynchronizePointOfView(view3DDst)
		view3DSrc.SynchronizeWindow(view3DDst)

		view3DSrc.ZoomFit()

		while view3DSrc.IsAvailable() and view3DDst.IsAvailable():
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