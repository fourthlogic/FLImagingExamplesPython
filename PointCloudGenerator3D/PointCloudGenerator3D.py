# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 // Main function
def main():

	# 3D 뷰 선언 // Declare the 3d view
	view3DDst = CGUIView3D();

	while True:
		
		# 3d 뷰 생성 // Create 3d object view
		if (res := view3DDst.Create(612, 0, 1124, 512)).IsFail():
			ErrorPrint(res, "Failed to create 3D views")
			break

		#알고리즘 객체 생성 // declare algorithm instance
		alg = CPointCloudGenerator3D()
		
		# 3D 뷰와 연결이 유지된 객체 생성 // Declare the object connected to 3D view
		view3DDst.PushObject(CFL3DObject())
		viewObject = view3DDst.GetView3DObject(0)
		floDst = viewObject.Get3DObject()
				
		# 파라미터 설정 // Set parameter
		alg.SetDestinationObject(floDst)
		alg.EnableColorGeneration(True)
		alg.EnableNormalGeneration(False)

		alg.AddPredefinedObject(alg.SCountInfo(True, 0, 0, 0), EPredefinedObject.Regular_DodecaHedron, TPoint3[Byte](255, 255, 255))
		alg.AddPredefinedObject(alg.SCountInfo(False, 4000, 0, 0), EPredefinedObject.Regular_DodecaHedron, TPoint3[Byte](255, 0, 0))
		alg.AddPredefinedObject(alg.SCountInfo(False, 0, 20000, 0), EPredefinedObject.Regular_DodecaHedron, TPoint3[Byte](0, 255, 0))
		alg.AddPredefinedObject(alg.SCountInfo(False, 0, 0, 100000), EPredefinedObject.Regular_DodecaHedron, TPoint3[Byte](0, 0, 255))

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := alg.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break
		
		#출력 뷰의 시점을 계산 // Calculate the viewpoint of destination view
		viewObject.UpdateAll()
		view3DDst.UpdateObject(0)
		view3DDst.ZoomFit()

		while view3DDst.IsAvailable():
			if (res := alg.Execute()).IsFail():
				ErrorPrint(res, "Failed to execute.")
				break;

			if not view3DDst.IsAvailable():
				break

			viewObject.UpdateVertex(True)
			view3DDst.UpdateObject(0)

			view3DDst.UpdateScreen()
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