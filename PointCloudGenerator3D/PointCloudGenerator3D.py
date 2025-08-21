# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():

	# 3D 뷰 선언 # Declare the 3d view
	view3DDst = CGUIView3D()

	while True:
		
		# 3d 뷰 생성 # Create 3d object view
		if (res := view3DDst.Create(612, 0, 1124, 512)).IsFail():
			ErrorPrint(res, "Failed to create 3D views")
			break

		#알고리즘 객체 생성 # declare algorithm instance
		pointCloudGenerator3D = CPointCloudGenerator3D()
		
		floDst = CFL3DObject()
				
		# 파라미터 설정 # Set parameter
		pointCloudGenerator3D.SetDestinationObject(floDst)
		pointCloudGenerator3D.EnableColorGeneration(True)
		pointCloudGenerator3D.EnableNormalGeneration(False)

		pointCloudGenerator3D.AddPredefinedObject(pointCloudGenerator3D.SCountInfo(True, 0, 0, 0), EPredefinedObject.Regular_DodecaHedron, TPoint3[Byte](255, 255, 255))
		pointCloudGenerator3D.AddPredefinedObject(pointCloudGenerator3D.SCountInfo(False, 4000, 0, 0), EPredefinedObject.Regular_DodecaHedron, TPoint3[Byte](255, 0, 0))
		pointCloudGenerator3D.AddPredefinedObject(pointCloudGenerator3D.SCountInfo(False, 0, 20000, 0), EPredefinedObject.Regular_DodecaHedron, TPoint3[Byte](0, 255, 0))
		pointCloudGenerator3D.AddPredefinedObject(pointCloudGenerator3D.SCountInfo(False, 0, 0, 100000), EPredefinedObject.Regular_DodecaHedron, TPoint3[Byte](0, 0, 255))

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := pointCloudGenerator3D.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break
		
		view3DDst.PushObject(floDst)
		#출력 뷰의 시점을 계산 # Calculate the viewpoint of destination view
		view3DDst.ZoomFit()

		while view3DDst.IsAvailable():
			if(res := pointCloudGenerator3D.Execute()).IsFail():
				ErrorPrint(res, "Failed to execute.")
				break

			if not view3DDst.IsAvailable():
				break

			view3DDst.LockUpdate()
			view3DDst.ClearObjects()

			if not view3DDst.IsAvailable():
				break

			view3DDst.PushObject(floDst)
			if not view3DDst.IsAvailable():
				break

			view3DDst.UnlockUpdate()
		break
	
	# End of main function



# 에러 출력 함수 # Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()