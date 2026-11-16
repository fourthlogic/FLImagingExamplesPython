# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()

from System.Collections.Generic import List


# 메인 함수 # Main function
def main():

	# 3D 객체 선언 # Declare 3D object
	floSrcObject = CFL3DObject()

	# 뷰 선언 # Declare view
	view3DSrc = CGUIView3D()
	view3DResult = CGUIView3D()

	res = CResult(EResult.UnknownError)

	while True:
		# 법선과 색상이 포함된 원본 점군 로드 # Load the source point cloud with normals and colors
		if((res := floSrcObject.Load("../../ExampleImages/SphereDetector3D/Source.fl3do")).IsFail()):
			ErrorPrint(res, "Failed to load ../../ExampleImages/SphereDetector3D/Source.fl3do.\n")
			break

		# 뷰 생성 # Create view
		if((res := view3DSrc.Create(0, 0, 640, 640)).IsFail() or
		   (res := view3DResult.Create(640, 0, 1280, 640)).IsFail()):
			ErrorPrint(res, "Failed to create the source and result 3D views.\n")
			break

		# 원본 장면을 두 뷰에 표시 # Display the source scene on both views
		if((res := view3DSrc.PushObject(floSrcObject)).IsFail() or
		   (res := view3DResult.PushObject(floSrcObject)).IsFail()):
			ErrorPrint(res, "Failed to display the source point cloud on the 3D views.\n")
			break

		# 알고리즘 객체 생성 # Create algorithm object
		sphereDetector3D = CSphereDetector3D()

		# 구의 대략적인 크기와 개수를 설정 # Set the approximate sphere size and count
		# 작은 구의 관측 점도 포함하도록 최소 inlier 개수를 설정
		# Set the minimum inlier count to include the observed points of the small sphere
		if((res := sphereDetector3D.SetSourceObject(floSrcObject)[0]).IsFail() or
		   (res := sphereDetector3D.SetRadiusRange(0.55, 1.65)).IsFail() or
		   (res := sphereDetector3D.SetMaxCount(4)).IsFail() or
		   (res := sphereDetector3D.SetMinimumInlierCount(40)).IsFail() or
		   (res := sphereDetector3D.SetDistanceThreshold(0.03)).IsFail() or
		   (res := sphereDetector3D.SetFitCosineSimilarity(0.98)).IsFail() or
		   (res := sphereDetector3D.SetMinimumSurfaceCoverage(0.25)).IsFail() or
		   (res := sphereDetector3D.SetScoreItem(CSphereDetector3D.EScoreItem.SurfaceCoverage, CSphereDetector3D.ESortOrder.Descending)).IsFail() or
		   (res := sphereDetector3D.SetIterationCount(5000)).IsFail() or
		   (res := sphereDetector3D.SetRefinementIterationCount(10)).IsFail()):
			ErrorPrint(res, "Failed to set the Sphere Detector 3D source object or detection parameters.\n")
			break

		# 알고리즘 수행 # Execute the algorithm
		if((res := sphereDetector3D.Execute()).IsFail()):
			ErrorPrint(res, "Failed to execute Sphere Detector 3D.\n")
			break

		# 결과 개수, inlier 개수 및 구면 Coverage 가져오기
		# Get the result count, inlier counts and surface coverages
		i64SphereCount = sphereDetector3D.GetResultCount()
		listInlierCounts = List[Int64]()
		listSurfaceCoverages = List[Single]()

		if((res := sphereDetector3D.GetResultInlierCounts(listInlierCounts)[0]).IsFail() or
		   (res := sphereDetector3D.GetResultSurfaceCoverages(listSurfaceCoverages)[0]).IsFail()):
			ErrorPrint(res, "Failed to retrieve the result inlier counts or surface coverages.\n")
			break

		# 화면에 출력하기 위해 3D View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from 3D view for display
		# 이 객체는 3D 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to a 3D view and does not need to be released separately
		layer3DSrc = view3DSrc.GetLayer(0)
		layer3DResult = view3DResult.GetLayer(0)
		strCount = "Sphere Count {0:d}".format(i64SphereCount)

		if((res := layer3DSrc.DrawTextCanvas(CFLPoint[Double](0, 0), "Source Object", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or
		   (res := layer3DResult.DrawTextCanvas(CFLPoint[Double](0, 0), "Sphere Detection Result", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or
		   (res := layer3DResult.DrawTextCanvas(CFLPoint[Double](0, 30), strCount, EColor.YELLOW, EColor.BLACK, 12)).IsFail()):
			ErrorPrint(res, "Failed to draw the view titles or sphere count.\n")
			break

		print("Sphere Count: {0:d}".format(i64SphereCount))

		for i in range(i64SphereCount):
			# 결과 구를 3D ROI로 표시 # Display the result sphere as a 3D ROI
			flsp = CFLSphere3[Double]()

			if((res := sphereDetector3D.GetResultSphere(flsp, i)[0]).IsFail() or
			   (res := view3DResult.PushBackROI(flsp)).IsFail()):
				ErrorPrint(res, "Failed to retrieve a result sphere or display it as a 3D ROI.\n")
				break

			flpCenter = flsp.GetCenter3D()
			tpCenter = TPoint3[Double](flpCenter.x, flpCenter.y, flpCenter.z)
			# 구 위에는 번호를, 화면 상단에는 상세 결과를 표시
			# Display the index on the sphere and the detailed results at the top of the view
			strText = "[{0:d}]".format(i)

			if((res := layer3DResult.DrawText3D(tpCenter, strText, EColor.YELLOW, EColor.BLACK, 12)).IsFail()):
				ErrorPrint(res, "Failed to draw the result sphere index in 3D.\n")
				break

			strText = "[{0:d}]  Radius: {1:.3f}  Inliers: {2:d}  Coverage: {3:.1f}%".format(
				i, flsp.GetRadius(), listInlierCounts[i], listSurfaceCoverages[i] * 100.0)

			if((res := layer3DResult.DrawTextCanvas(CFLPoint[Double](0, 50 + 18 * i), strText, EColor.YELLOW, EColor.BLACK, 11)).IsFail()):
				ErrorPrint(res, "Failed to draw the result sphere radius, inlier count and coverage.\n")
				break

			print("[{0:d}] Center: ({1:.3f}, {2:.3f}, {3:.3f}), Radius: {4:.3f}, Inliers: {5:d}, Coverage: {6:.1f}%".format(
				i, tpCenter.x, tpCenter.y, tpCenter.z, flsp.GetRadius(), listInlierCounts[i], listSurfaceCoverages[i] * 100.0))

		if(res.IsFail()):
			break

		# 원본 장면을 관측 방향에서 바라보기 # View the source scene from the observation direction
		cameraSrc = view3DSrc.GetCamera()

		if((res := cameraSrc.SetPosition(CFLPoint3[Single](13.0, -20.0, 39.0))).IsFail() or
		   (res := cameraSrc.SetTarget(CFLPoint3[Single](0.0, 0.0, 0.0))).IsFail() or
		   (res := cameraSrc.SetDirectionUp(CFLPoint3[Single](0.0, 0.0, 1.0))).IsFail() or
		   (res := view3DSrc.SetCamera(cameraSrc)).IsFail() or
		   (res := view3DSrc.ZoomFit()).IsFail()):
			ErrorPrint(res, "Failed to set the source camera viewpoint or fit the source scene.\n")
			break

		# 결과 뷰는 원본 뷰와 동일한 시점으로 표시 # Display the result view from the same viewpoint as the source view
		if((res := view3DResult.SetCamera(view3DSrc.GetCamera())).IsFail() or
		   (res := view3DSrc.SynchronizePointOfView(view3DResult)[0]).IsFail()):
			ErrorPrint(res, "Failed to copy and synchronize the source and result camera viewpoints.\n")
			break

		# 뷰 갱신 # Update view
		view3DSrc.Invalidate(True)
		view3DResult.Invalidate(True)

		# 뷰가 종료될 때까지 기다림 # Wait for the views to close
		while(view3DSrc.IsAvailable() and view3DResult.IsAvailable()):
			CThreadUtilities.Sleep(1)
		break

	# End of main function

# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()