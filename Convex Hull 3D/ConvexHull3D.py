# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 // Main function
def main():

	# 3D 객체 선언 // Declare the 3D object
	floSrc = CFL3DObject();
	floDst = CFL3DObject();
	
	# 3D 뷰 선언 // Declare the 3d view
	view3DSrc = CGUIView3D();
	view3DDst = CGUIView3D();

	while True:
		
		# Source 이미지 로드 // Load the source image
		if (res := floSrc.Load("../../ExampleImages/ConvexHull3D/RandomPointsOnSphere.ply")).IsFail():
			ErrorPrint(res, "Failed to load the 3D Object.\n")
			break

		# Source 이미지 뷰 생성 // Create source image view
		if (res := view3DSrc.Create(100, 0, 612, 512)).IsFail() or \
			(res := view3DDst.Create(612, 0, 1124, 512)).IsFail():
			ErrorPrint(res, "Failed to create 3D views")
			break

		# 두 3D 뷰의 시점을 동기화한다 // Synchronize the viewpoints of the two 3D views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := view3DSrc.SynchronizePointOfView(view3DDst)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := view3DSrc.SynchronizeWindow(view3DDst)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# Gain Offset 객체 생성 // Create Gain Offset object
		convexhull3D = CConvexHull3D()

		# 처리할 3D 객체 설정 // Set 3D object to process
		convexhull3D.SetSourceObject(floSrc);
		convexhull3D.SetDestinationObject(floDst);

		# 생성될 볼록껍질 객체의 컬러를 설정 // Set color of new 3D object
		convexhull3D.EnableVertexRecoloring(True);
		convexhull3D.SetTargetVertexColor(TPoint3[Byte](255, 125, 0));

		# 3D 뷰에 표시할 3D 객체 추가 // Add 3D object to the 3D view
		view3DSrc.PushObject(floSrc);
		view3DSrc.SetPointSize(3);


		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		
		if (res := convexhull3D.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Convex Hull.')
			break
		
		view3DDst.PushObject(floDst);
		
		# 입력 뷰의 시점을 이동
		view3DSrc.ZoomFit();

		# 입력, 출력 뷰의 시점을 맞춤
		view3DSrc.SynchronizePointOfView(view3DDst);

		# 입력, 출력 뷰를 하나의 창으로 취급
		view3DSrc.SynchronizeWindow(view3DDst);

		view3DSrc.Invalidate();
		view3DDst.Invalidate();


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