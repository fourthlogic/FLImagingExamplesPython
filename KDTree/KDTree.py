# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():
	
    while True:
        # ------------------------------------------------------------------
        # 1단계: 데이터 준비 및 KDTree 구축 (Build)
        # Step 1: Prepare Data and Build KDTree
        # ------------------------------------------------------------------
        print("[Step 1] Prepare Data and Build KDTree")

        list_vertices = List[TPoint[Double]]()
        list_vertices.Add(TPoint[Double](0.0, 0.0))
        list_vertices.Add(TPoint[Double](1.0, 1.0))
        list_vertices.Add(TPoint[Double](2.0, 2.0))
        list_vertices.Add(TPoint[Double](3.0, 1.0))
        list_vertices.Add(TPoint[Double](5.0, 5.0))
        list_vertices.Add(TPoint[Double](10.0, 10.0))

        # 입력받은 정점 목록 및 인덱스 출력 # Output the input list of vertices and indices
        print(" - Input Vertices:")
        for i, pt in enumerate(list_vertices):
            print(f"   Index {i} : ({pt.x:.1f}, {pt.y:.1f})")

        # CKDTree 선언 (2D Point, double 타입) # Declare CKDTree (2D Point, double type)
        kdtree = CKDTree[TPoint[Double]]()
        
        # 트리 구축 # Build tree
        res = kdtree.Build[Double](list_vertices)

        if res.IsFail():
            ErrorPrint(res, "Failed to build KDTree.")
            break

        print(f" - The number of elements in the constructed data : {kdtree.GetCount()}\n")


        # ------------------------------------------------------------------
        # 2단계: 단일 최근접 정점 탐색 (GetNearestPointAndIndex)
        # Step 2: Single Nearest Neighbor Search
        # ------------------------------------------------------------------
        print("[Step 2] Single Nearest Neighbor Search")

        tpQuery1 = TPoint[Double](1.2, 0.9)
        print(f" - Target Query: ({tpQuery1.x:.1f}, {tpQuery1.y:.1f})")

        # 좌표와 인덱스를 동시에 구함
        # Get both coordinates and index
        kvpNearestResult = kdtree.GetNearestPointAndIndex[Double](tpQuery1)
        tpNearestPt = kvpNearestResult.Key
        u64NearestIdx = kvpNearestResult.Value

        print(f" - Nearest Point: ({tpNearestPt.x:.1f}, {tpNearestPt.y:.1f})")
        print(f" - Nearest Index: {u64NearestIdx}\n")


        # ------------------------------------------------------------------
        # 3단계: K-최근접 정점 탐색 (GetNearestNeighborsPointsAndIndices)
        # Step 3: K-Nearest Neighbors Search
        # ------------------------------------------------------------------
        print("[Step 3] K-Nearest Neighbors Search (K = 3)")

        tpQuery2 = TPoint[Double](1.5, 1.5)
        i64K = 3
        print(f" - Target Query: ({tpQuery2.x:.1f}, {tpQuery2.y:.1f})")

        listKNNPoints = List[TPoint[Double]]()
        listKNNIndices = List[UInt64]()
        
        res, listKNNPoints, listKNNIndices = kdtree.GetNearestNeighborsPointsAndIndices[Double](tpQuery2, i64K, listKNNPoints, listKNNIndices)

        for i in range(len(listKNNPoints)):
            print(f"   [{i + 1}] Index: {listKNNIndices[i]} -> ({listKNNPoints[i].x:.1f}, {listKNNPoints[i].y:.1f})")

        print()


        # ------------------------------------------------------------------
        # 4단계: 영역/범위 탐색 (GetPointsAndIndicesInRange)
        # Step 4: Bounding Box Range Search
        # ------------------------------------------------------------------
        print("[Step 4] Bounding Box Range Search")

        tpLowerBound = TPoint[Double](0.5, 0.5)
        tpUpperBound = TPoint[Double](3.5, 2.5)
        print(f" - Range Lower Bound: ({tpLowerBound.x:.1f}, {tpLowerBound.y:.1f})")
        print(f" - Range Upper Bound: ({tpUpperBound.x:.1f}, {tpUpperBound.y:.1f})")

        listRangePoints = List[TPoint[Double]]()
        listRangeIndices = List[UInt64]()

        # 모든 매칭 점을 찾으려면 i64Count에 -1 전달 # Pass -1 to i64Count to find all matching points
        res, listRangePoints, listRangeIndices = kdtree.GetPointsAndIndicesInRange[Double](tpLowerBound, tpUpperBound, listRangePoints, listRangeIndices, -1)

        print(f" - Number of points found in range: {len(listRangePoints)}")

        for i in range(len(listRangePoints)):
            print(f"   - Index: {listRangeIndices[i]} -> ({listRangePoints[i].x:.1f}, {listRangePoints[i].y:.1f})")

        print()


        # ------------------------------------------------------------------
        # 5단계: 반경 탐색 (GetPointsAndIndicesInRadius)
        # Step 5: Radius Search
        # ------------------------------------------------------------------
        print("[Step 5] Radius Search")

        tpCenter = TPoint[Double](0.0, 0.0)
        f64Radius = 3.0
        print(f" - Center Point: ({tpCenter.x:.1f}, {tpCenter.y:.1f})")
        print(f" - Radius: {f64Radius:.1f}")

        listRadiusPoints = List[TPoint[Double]]()
        listRadiusIndices = List[UInt64]()
        
        res, listRadiusPoints, listRadiusIndices = kdtree.GetPointsAndIndicesInRadius[Double](tpCenter, f64Radius, listRadiusPoints, listRadiusIndices, -1)

        print(f" - Number of points found in radius: {len(listRadiusPoints)}")

        for i in range(len(listRadiusPoints)):
            print(f"   - Index: {listRadiusIndices[i]} -> ({listRadiusPoints[i].x:.1f}, {listRadiusPoints[i].y:.1f})")

        print()


        # ------------------------------------------------------------------
        # 6단계: 기하 연산 (OperateAdd)
        # Step 6: Geometric Operation (OperateAdd)
        # ------------------------------------------------------------------
        print("[Step 6] Translate All Nodes (OperateAdd)")

        tpOffset = TPoint[Double](10.0, 10.0)
        print(f" - Offset Vector: ({tpOffset.x:.1f}, {tpOffset.y:.1f})")

        # 모든 점에 (10, 10) 이동 적용 # Apply (10, 10) offset to all points
        kdtree.OperateAdd[Double](tpOffset)

        # 이동 후 동일한 Query 점(1.2, 0.9)으로 다시 탐색해 확인 # Re-query near the same query point (1.2, 0.9) to check result
        print(f" - Re-querying near: ({tpQuery1.x:.1f}, {tpQuery1.y:.1f})")
        
        kvpShiftedResult = kdtree.GetNearestPointAndIndex[Double](tpQuery1)
        tpShiftedPt = kvpShiftedResult.Key
        u64ShiftedIdx = kvpShiftedResult.Value

        print(f" - Shifted Nearest Point: ({tpShiftedPt.x:.1f}, {tpShiftedPt.y:.1f})")
        print(f" - Index: {u64ShiftedIdx}")

        print("\n========================================\n")

        input("Press Enter to exit...")
        break
    
    # End of main function



# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()