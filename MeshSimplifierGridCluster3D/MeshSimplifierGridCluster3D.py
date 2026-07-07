# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


# 메인 함수 # Main function
def main():

	# 3D 뷰 선언 # Declare 3D view
	view3DDst = [CGUIView3D() for _ in range(4)]
	view3DSource = CGUIView3D()

	# 알고리즘 동작 결과 # Algorithm execution result
	res = CResult()

	while True:
		if (res := view3DSource.Create(0, 0, 500, 500)).IsFail() or \
		   (res := view3DDst[0].Create(500, 0, 1000, 500)).IsFail() or \
		   (res := view3DDst[1].Create(500, 500, 1000, 1000)).IsFail() or \
		   (res := view3DDst[2].Create(1000, 0, 1500, 500)).IsFail() or \
		   (res := view3DDst[3].Create(1000, 500, 1500, 1000)).IsFail():
			ErrorPrint(res, "Failed To Create Views")
			break

		for i in range(4):
			view3DDst[i].SynchronizePointOfView(view3DSource)
			view3DDst[i].SynchronizeWindow(view3DSource)

		# 소스 오브젝트 생성 # Make Source Object
		floPointCloud = CFL3DObject()
		i32Count = int(1e6)

		rng = CXorshiroRandomGenerator()
		rng.Seed(42)

		listVertices = List[TPoint3[Single]]()

		for i in range(i32Count):
			tp = rng.GenerateUniformRandomPointOnUnitSphereF32()
			listVertices.Add(TPoint3[Single](tp.x * 2.0, tp.y * 3.0, tp.z * -3.5))

		floPointCloud.SetVertices(listVertices)

		floMesh = CFL3DObject()
		convexHull3D = CConvexHull3D()
		convexHull3D.SetSourceObject(floPointCloud)
		convexHull3D.SetDestinationObject(floMesh)
		convexHull3D.EnableNormalRecalculation(True)
		convexHull3D.EnablePreserveVertex(False)

		if (res := convexHull3D.Execute()).IsFail():
			ErrorPrint(res, "Failed To Execute Convex Hull.")
			break

		view3DSource.PushObject(floMesh)
		view3DSource.ZoomFit()

		# 소스 뷰에 메시지 출력 # Display message on the source view
		layer3DSource = view3DSource.GetLayer(0)
		layer3DSource.Clear()
		layer3DSource.DrawTextCanvas(CFLPoint[Double](0, 0), "Source View", EColor.YELLOW, EColor.BLACK, 20)

		# CMeshSimplifierGridCluster3D 실행 # Execute CMeshSimplifierGridCluster3D
		meshSimplifierGridCluster3D = CMeshSimplifierGridCluster3D()

		arrI32SampleSize = [3333, 1000, 350, 100]

		for i in range(4):
			floResult = CFL3DObject()

			meshSimplifierGridCluster3D.SetSourceObject(floMesh)
			meshSimplifierGridCluster3D.SetDestinationObject(floResult)
			meshSimplifierGridCluster3D.SetSamplingSize(arrI32SampleSize[i])
			meshSimplifierGridCluster3D.SetClusteringMethod(CMeshSimplifierGridCluster3D.EClusteringMethod.FastGrid)

			if (res := meshSimplifierGridCluster3D.Execute()).IsFail():
				ErrorPrint(res, "Failed To Execute Mesh Simplifier Grid Cluster.")
				break

			view3DDst[i].PushObject(floResult)

			# 목적지 뷰에 메시지 출력 # Display message on the destination view
			layer3DDst = view3DDst[i].GetLayer(0)
			layer3DDst.Clear()
			layer3DDst.DrawTextCanvas(CFLPoint[Double](0, 0), f"Destination(Count: {arrI32SampleSize[i]})", EColor.YELLOW, EColor.BLACK, 20)

		while view3DSource.IsAvailable() and view3DDst[0].IsAvailable() and view3DDst[1].IsAvailable() and view3DDst[2].IsAvailable() and view3DDst[3].IsAvailable():
			CThreadUtilities.Sleep(1)

		break


if __name__ == '__main__':
    main()
