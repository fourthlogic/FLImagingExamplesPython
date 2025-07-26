# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 메인 함수 // Main function
def main():

	view3DSrc0 = CGUIView3D()
	view3DSrc1 = CGUIView3D()
	view3DWorld = CGUIView3D()
	view3DDst = CGUIView3D()
	floSource0 = CFL3DObject()
	floSource1 = CFL3DObject()
	floWorld = CFL3DObject()
	fl3DObjectDst = CFL3DObject()

	while True:
		# 데이터 로드 // Load data
		floSource0.Load("../../ExampleImages/CoordinateFrameUnification3D/Office_mosaicked(Left).ply")
		floWorld.Load("../../ExampleImages/CoordinateFrameUnification3D/Office_mosaicked(Middle).ply")
		floSource1.Load("../../ExampleImages/CoordinateFrameUnification3D/Office_mosaicked(Right).ply")

		cfu = CCoordinateFrameUnification3D()

		# Scene 0와 World 좌표 간 점 대응을 추가
		# Add point correpondence between Scene 0 & World
		flaWorld0 = List[TPoint3[Single]](4)
		flaScene0 = List[TPoint3[Single]](4)

		flaWorld0.Add(TPoint3[Single](0.316194, 0.089235, -0.955000))
		flaScene0.Add(TPoint3[Single](0.048920, 0.131229, -0.824725))
		flaWorld0.Add(TPoint3[Single](0.328092, 0.086743, -0.952000))
		flaScene0.Add(TPoint3[Single](0.062442, 0.128631, -0.826201))
		flaWorld0.Add(TPoint3[Single](0.465690, 0.065212, -0.920000))
		flaScene0.Add(TPoint3[Single](0.202130, 0.117711, -0.854954))
		flaWorld0.Add(TPoint3[Single](0.339934, -0.020669, -0.646000))
		flaScene0.Add(TPoint3[Single](0.189541, -0.046209, -0.589000))

		cfu.AddSourceObject(floSource0, flaWorld0, flaScene0)

		# Scene 1과 World 좌표 간 점 대응을 추가
		# Add point correpondence between Scene 1 & World
		flaWorld1 = List[TPoint3[Single]](6)
		flaScene1 = List[TPoint3[Single]](6)

		flaWorld1.Add(TPoint3[Single](-0.553926, 0.204508, -1.155000))
		flaScene1.Add(TPoint3[Single](0.202496, 0.448916, -0.853000))
		flaWorld1.Add(TPoint3[Single](-0.552240, 0.189193, -1.160931))
		flaScene1.Add(TPoint3[Single](0.208646, 0.434687, -0.859625))
		flaWorld1.Add(TPoint3[Single](-0.479978, 0.192098, -1.145000))
		flaScene1.Add(TPoint3[Single](0.251620, 0.415887, -0.796545))
		flaWorld1.Add(TPoint3[Single](-0.477483, 0.173172, -1.146783))
		flaScene1.Add(TPoint3[Single](0.258778, 0.401190, -0.810000))
		flaWorld1.Add(TPoint3[Single](-0.406276, -0.267226, -0.835000))
		flaScene1.Add(TPoint3[Single](0.138451, -0.120545, -0.677569))
		flaWorld1.Add(TPoint3[Single](-0.016503, -0.275241, -1.050700))
		flaScene1.Add(TPoint3[Single](0.568925, -0.122618, -0.588000))

		cfu.AddSourceObject(floSource1, flaWorld1, flaScene1)

		floDestination = CFL3DObject()
		cfu.SetDestinationObject(floDestination)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := cfu.Execute()).IsFail():
			ErrorPrint(res, "Failed to execute.\n")
			break

		# 3D 뷰 생성 // Create the 3D views
		if (res := view3DSrc0.Create(100, 250, 600, 750)).IsFail() or \
			(res := view3DWorld.Create(600, 0, 1100, 500)).IsFail() or \
			(res := view3DSrc1.Create(1100, 250, 1600, 750)).IsFail() or \
			(res := view3DDst.Create(600, 500, 1100, 1000)).IsFail():
			ErrorPrint(res, "Failed to create the 3d view.\n")
			break

		view3DDst.SynchronizeWindow(view3DSrc0);
		view3DDst.SynchronizeWindow(view3DWorld);
		view3DDst.SynchronizeWindow(view3DSrc1);

		view3DSrc0.PushObject(floSource0)
		view3DWorld.PushObject(floWorld)
		view3DSrc1.PushObject(floSource1)
		view3DDst.PushObject(floDestination)

		view3DDst.SynchronizePointOfView(view3DSrc0)
		view3DDst.SynchronizePointOfView(view3DWorld)
		view3DDst.SynchronizePointOfView(view3DSrc1)


		# 3D 뷰에 카메라 위치 직접 세팅 // Set 3d view camera pose manually
		cam = CFL3DCamera()

		if (res := cam.SetProjectionType(E3DCameraProjectionType.Perspective)).IsFail() or \
			(res := cam.SetDirection(CFLPoint3[Single](0.337466, -0.125061, -0.932993))).IsFail() or \
			(res := cam.SetDirectionUp(CFLPoint3[Single](0.139977, 0.986837, -0.080987))).IsFail() or \
			(res := cam.SetPosition(CFLPoint3[Single](-0.70, 0.16, 1.0))).IsFail() or \
			(res := cam.SetAngleOfViewY(45)).IsFail() or \
			(res := view3DWorld.SetCamera(cam)).IsFail():
			ErrorPrint(res, "Failed to set camera.\n")
			break

		layer3DSrc0 = view3DSrc0.GetLayer(0)
		layer3DSrc1 = view3DSrc1.GetLayer(0)
		layer3DWorld = view3DWorld.GetLayer(0)
		layer3DDst = view3DDst.GetLayer(0)

		flpTopLeft =  CFLPoint[Double](0, 0);

		if (res := layer3DSrc0.DrawTextCanvas(flpTopLeft, "Scene 0", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
			(res := layer3DWorld.DrawTextCanvas(flpTopLeft, "World(Reference)", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
			(res := layer3DSrc1.DrawTextCanvas(flpTopLeft, "Scene 1", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or \
			(res := layer3DDst.DrawTextCanvas(flpTopLeft, "Result", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break

		# 뷰를 갱신 // Update view
		view3DSrc0.Invalidate(True)
		view3DWorld.Invalidate(True)
		view3DSrc1.Invalidate(True)
		view3DDst.Invalidate(True)

		# 뷰가 종료될 때까지 기다림 // Wait for the view to close
		while(view3DSrc0.IsAvailable() and view3DSrc1.IsAvailable() and view3DWorld.IsAvailable() and view3DDst.IsAvailable()):
			CThreadUtilities.Sleep(1)

		break



# 에러 출력 함수 // Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()