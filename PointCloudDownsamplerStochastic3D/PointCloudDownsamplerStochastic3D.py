# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 // Main function
def main():

	# 3D 뷰 선언 // Declare the 3d view
	view3DSrc = CGUIView3D();
	view3DDst = CGUIView3D();

	while True:
		
		# 3d 뷰 생성 // Create 3d object view
		if (res := view3DSrc.Create(100, 0, 612, 512)).IsFail() or \
			(res := view3DDst.Create(612, 0, 1124, 512)).IsFail():
			ErrorPrint(res, "Failed to create 3D views")
			break

		#알고리즘 객체 생성 // declare algorithm instance
		pointCloudDownsamplerStochastic3D = CPointCloudDownsamplerStochastic3D()
		
		view3DSrc.SetTopologyType(ETopologyType3D.PointCloud)
		view3DDst.SetTopologyType(ETopologyType3D.PointCloud)

		# 3D 뷰와 연결이 유지된 객체 생성 // Declare the object connected to 3D view
		view3DSrc.PushObject(CFL3DObject())
		viewObjectSrc = view3DSrc.GetView3DObject(0)
		floSrc = viewObjectSrc.Get3DObject()
		
		# 3D 뷰와 연결이 유지된 객체 생성 // Declare the object connected to 3D view
		view3DDst.PushObject(CFL3DObject())
		viewObjectDst = view3DDst.GetView3DObject(0)
		floDst = viewObjectDst.Get3DObject()
		
		if (res := floSrc.Load("../../ExampleImages/CoordinateFrameUnification3D/Office_mosaicked(Middle).ply")).IsFail():
			ErrorPrint(res, "Failed to load source object.")
			break

		# 파라미터 설정 // Set parameter
		pointCloudDownsamplerStochastic3D.SetSourceObject(floSrc)
		pointCloudDownsamplerStochastic3D.SetDestinationObject(floDst)
		pointCloudDownsamplerStochastic3D.SetSamplingSize(20000)
		pointCloudDownsamplerStochastic3D.EnableNormalRetainment(True)
		pointCloudDownsamplerStochastic3D.EnableColorRetainment(True)
		pointCloudDownsamplerStochastic3D.EnableFaceRetainment(False)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := pointCloudDownsamplerStochastic3D.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break
		
		viewObjectSrc.UpdateAll()
		viewObjectDst.UpdateAll()

		view3DSrc.SynchronizePointOfView(view3DDst)
		view3DSrc.SynchronizeWindow(view3DDst)
		
		#출력 뷰의 시점을 계산 // Calculate the viewpoint of destination view
		cam = CFL3DCamera()

		cam.SetProjectionType(E3DCameraProjectionType.Perspective)
		cam.SetDirection(CFLPoint3[Single](0.327705, 0.066764, -0.942418))
		cam.SetDirectionUp(CFLPoint3[Single](0.311277, 0.839746, -0.444896))
		cam.SetPosition(CFLPoint3[Single](-1.825832, 0.425620, 1.548716))
		cam.SetAngleOfViewY(45)

		view3DDst.SetCamera(cam)

		view3DSrc.UpdateObject(0)
		view3DDst.UpdateObject(0)

		while view3DSrc.IsAvailable() and view3DDst.IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function



# 에러 출력 함수 // Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()