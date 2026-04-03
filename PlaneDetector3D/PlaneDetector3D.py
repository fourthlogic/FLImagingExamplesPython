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
	floDstObject = CFL3DObject()

	# 뷰 선언 # Declare view	
	view3DSrc = CGUIView3D()
	view3DDst = CGUIView3D()

	# 알고리즘 동작 결과 # Algorithm execution result
	res = CResult()

	while True:		
		# Source Object 로드 # Load the Source 3D object
		if(res := floSrcObject.Load("../../ExampleImages/PlaneDetector3D/Source.ply")).IsFail() :		
			ErrorPrint(res, "Failed to load the 3D object file.\n")
			break
		
		# 뷰 생성 # Create view
		if((res := view3DSrc.Create(0, 0, 500, 500)).IsFail() or
		   (res := view3DDst.Create(500, 0, 1000, 500)).IsFail()) :
			ErrorPrint(res, "Failed to create the view.\n")
			break		
		
		# 두 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two views
		if((res := view3DSrc.SynchronizePointOfView(view3DDst)[0]).IsFail()) :
			ErrorPrint(res, "Failed to synchronize the view.\n")
			break

		# View 에 source 3D object 디스플레이 # Display source 3D object on the view
		if(res := view3DSrc.PushObject(floSrcObject)).IsFail() :		
			ErrorPrint(res, "Failed to display the 3D object.\n")
			break
		
		# 알고리즘 객체 생성 # Create algorithm object
		planeDetector3D = CPlaneDetector3D()
		
		if((res := planeDetector3D.SetSourceObject(floSrcObject)[0]).IsFail()) :
			break
		if((res := planeDetector3D.SetDestinationObject(floDstObject)[0]).IsFail()) :
			break

		if((res := planeDetector3D.SetPlaneFittingTarget(CPlaneDetector3D.EPlaneFittingTarget.VertexNormal)).IsFail()) :
			break
		if((res := planeDetector3D.SetMaximumParallelPlaneCount(1)).IsFail()) :
			break
		if((res := planeDetector3D.SetNormalVectorResolution(TPoint3[int](19, 19, 19))).IsFail()) :
			break
		if((res := planeDetector3D.SetInlierDistance(0.5)).IsFail()) :
			break
		if((res := planeDetector3D.SetMinimumInlierCount(500)).IsFail()) :
			break
		if((res := planeDetector3D.SetFitCosineSimilarity(0.995)).IsFail()) :
			break
		if((res := planeDetector3D.SetExpandCosineSimilarity(0.99)).IsFail()) :
			break
		if((res := planeDetector3D.SetMergeCosineSimilarity(0.99)).IsFail()) :
			break

		if((res := planeDetector3D.SetOutliersFilteringMethod(CPlaneDetector3D.EOutliersFilteringMethod.LeastSquare)).IsFail()) :
			break
		if((res := planeDetector3D.SetOutliersThresholdCount(1)).IsFail()) :
			break
		if((res := planeDetector3D.SetOutliersThreshold(3.00)).IsFail()) :
			break
		if((res := planeDetector3D.SetPlaneFittingMethod(CPlaneDetector3D.EPlaneFittingMethod.LeastSquare)).IsFail()) :
			break

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if(res := planeDetector3D.Execute()).IsFail() :	
			ErrorPrint(res, "Failed to execute the algorithm.")
			break
		
		# View 에 3D object 를 디스플레이 # Display the 3D object on the view
		gvoDst = CGUIView3DObject()
		if((res := (gvoDst.Get3DObject()).Swap(floDstObject)[0]).IsFail()) :
			break
		if((res := gvoDst.SetTopologyType(ETopologyType3D(0x1f, True))).IsFail()) :
			break
		if((res := gvoDst.SetPointSize(2)).IsFail()) :
			break
		if((res := view3DDst.PushObject(gvoDst)).IsFail()) :
			ErrorPrint(res, "Failed to set 3D object on the view.\n")
			break
		
		# 화면에 출력하기 위해 View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from view for display
		# 이 객체는 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an view and does not need to be released separately
		layer3DSrc = view3DSrc.GetLayer(0)
		layer3DDst = view3DDst.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
		layer3DSrc.Clear()
		layer3DDst.Clear()

		# 뷰 정보 표시 # Display view information
		i32PlaneCount = planeDetector3D.GetResultPlaneCount()
		flp = CFLPoint[Double](0, 0)
		strDstLayerString = "Plane Count {:d}".format(i32PlaneCount)
		if((res := layer3DSrc.DrawTextCanvas(flp, "Source Object", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or
		   (res := layer3DDst.DrawTextCanvas(flp, "Destination Object", EColor.YELLOW, EColor.BLACK, 20)).IsFail() or
		   (res := layer3DDst.DrawTextCanvas(CFLPoint[Double](0, 30), strDstLayerString, EColor.YELLOW, EColor.BLACK, 12)).IsFail()) :
			ErrorPrint(res, "Failed to draw text.\n")
			break
		
		# text
		bDrawTextIndex = True
		bDrawTextCount = True
		bDrawTextArea = False
		if(bDrawTextIndex or bDrawTextCount or bDrawTextArea) :
			listResultPlaneCentroids = List[TPoint3[Single]]()
			listResultPlaneTargetCounts = List[int]()
			listResultPlaneTargetAreas = List[Single]()
			if((res := planeDetector3D.GetResultPlaneCentroids(listResultPlaneCentroids)).IsFail()) :
				break
			if((res := planeDetector3D.GetResultPlaneTargetCounts(listResultPlaneTargetCounts)).IsFail()) :
				break
			if((res := planeDetector3D.GetResultPlaneAreas(listResultPlaneTargetAreas)).IsFail()) :
				break

			for i32PlaneIndex in range(0, i32PlaneCount) :
				strValueTotal = str()
				strValue = str()
				tp3Centroid = TPoint3[Double]()
				tp3Centroid.x = listResultPlaneCentroids[i32PlaneIndex].x
				tp3Centroid.y = listResultPlaneCentroids[i32PlaneIndex].y
				tp3Centroid.z = listResultPlaneCentroids[i32PlaneIndex].z
				i32PlaneTargetCount = listResultPlaneTargetCounts[i32PlaneIndex]
				f32PlaneArea = listResultPlaneTargetAreas[i32PlaneIndex]
				if(bDrawTextIndex) :
					strValue = "[{:d}]\n".format(i32PlaneIndex)
					strValueTotal += strValue
				if(bDrawTextCount) :
					strValue = "Count {:d}\n".format(i32PlaneTargetCount)
					strValueTotal += strValue
				if(bDrawTextArea) :
					strValue = "Area {:.3f}\n".format(f32PlaneArea)
					strValueTotal += strValue
				layer3DDst.DrawText3D(tp3Centroid, strValueTotal, EColor.YELLOW, EColor.BLACK, 9)

		# Zoom Fit
		view3DSrc.ZoomFit()
		view3DDst.ZoomFit()

		# 뷰를 갱신 합니다. # Update view
		view3DSrc.Invalidate(True)
		view3DDst.Invalidate(True)

		# 뷰가 종료될 때 까지 기다림 # Wait until one of the views is closed
		while(view3DSrc.IsAvailable() and view3DDst.IsAvailable()) :
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