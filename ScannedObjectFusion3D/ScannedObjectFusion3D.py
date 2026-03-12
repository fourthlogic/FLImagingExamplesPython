# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():

	# 3D 뷰 선언 # Declare 3D view	
	i32SourceCount = 6
	view3DDst = CGUIView3D()
	arrSourceView = [CGUIView3D() for _ in range(i32SourceCount)]	

	# 3D 객체 선언 # Declare 3D object
	arrSourceObjects = [CFL3DObject() for _ in range(i32SourceCount)]
	floDst = CFL3DObject()
	
	# 알고리즘 동작 결과 # Algorithm execution result
	res = CResult()

	while True:		
		scannedObjectFusion3D = CScannedObjectFusion3D()

		# Source Object 로드 # Load the Source object
		for i in range(6):
			strPath = f'../../ExampleImages/ScannedObjectFusion3D/{i}.fl3do'

			if(res := arrSourceObjects[i].Load(strPath)).IsFail() :
				break

			scannedObjectFusion3D.AddSourceObject(arrSourceObjects[i])

		# Source 3D 뷰 생성
		i32WindowWidth = 300
		i32WindowHeight = 300

		for i in range(i32SourceCount // 3):
			i32Height = i32WindowHeight * i
			
			for j in range(i32SourceCount // 2):
				i32Width = i32WindowWidth * j
				arrSourceView[i * 3 + j].Create(10 + i32Width, 10 + i32Height, 10 + i32Width + i32WindowWidth, 10 + i32Height + i32WindowHeight)

		# Destination Object 3D 뷰 생성 # Create the destination object 3D view
		if(res := view3DDst.Create(910, 10, 1510, 610)).IsFail() :		
			ErrorPrint(res, "Failed to create the Destination 3D view.\n")
			break
		
		for i in range(1, i32SourceCount):
			arrSourceView[0].SynchronizeWindow(arrSourceView[i])

		flpTopLeft = CFLPoint[Double](0, 0)

		for i in range(i32SourceCount):
			arrSourceView[i].PushObject(arrSourceObjects[i])
			arrSourceView[i].ZoomFit()

			strName = f'Scene {i}'
			arrSourceView[i].GetLayer(0).DrawTextCanvas(flpTopLeft, strName, EColor.YELLOW, EColor.BLACK, 20)
		

		# 샘플링 거리 설정 # Set the sampling distance
		scannedObjectFusion3D.SetSamplingDistance(0.03)
		# 기준 좌표계 설정 # Set the base coordinate system
		scannedObjectFusion3D.SetBaseCoordinateFrame(0)
		# 데이터 취득 타입 설정 # Set the data acquisition type
		scannedObjectFusion3D.SetAcquisitionType(CScannedObjectFusion3D.EAcquisitionType.Unordered)
		# Destination object 설정 # Set the destination object
		scannedObjectFusion3D.SetDestinationObject(floDst)

		if(res := scannedObjectFusion3D.Calibrate()).IsFail() :
			ErrorPrint(res, "Failed to Calibrate\n")
			break

		view3DDst.PushObject(floDst)

		if(res := view3DDst.GetLayer(0).DrawTextCanvas(flpTopLeft, "Calibration Result", EColor.YELLOW, EColor.BLACK, 20)).IsFail():		
			ErrorPrint(res, "Failed to draw text.\n")
			break		

		# 뷰를 갱신 # Update view
		for i in range(i32SourceCount):
			arrSourceView[i].Invalidate(True)

		view3DDst.ZoomFit()
		view3DDst.Invalidate(True)

		#이미지 뷰, 3D 뷰가 종료될 때 까지 기다림 # Wait for the image and 3D view to close
		while view3DDst.IsAvailable() :
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