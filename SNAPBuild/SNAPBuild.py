# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():

	# 스냅 빌드 객체 선언 # Declare SNAP Build
	snapBuild = CSNAPBuild()

	while True:

		# 스냅 파일 로드 # Load SNAP file
		if (res := snapBuild.Load('Example.flsf')).IsFail():
			ErrorPrint(res, 'Failed to load the file.')
			break

		# 소스 이미지 노드를 찾습니다. # Finds the source image node.
		nodeSourceImage = snapBuild.FindNode('Image', 'Source Image');

		if nodeSourceImage is None:
			res = CResult(EResult.FailedToFind);
			ErrorPrint(res, 'Failed to find the node.');
			break;
		

		# 임계값 처리 결과 노드를 찾습니다. # Finds the threshold result node.
		nodeThresholdResult = snapBuild.FindNode('MultiVar<Double>', 'Threshold Result');

		if nodeThresholdResult is None:
			res = CResult(EResult.FailedToFind);
			ErrorPrint(res, 'Failed to find the node.');
			break;

		fliSource = CFLImage();

		# 소스 이미지를 로드합니다. # Loads the source image.
		if (res := fliSource.Load('..\\..\\ExampleImages\\Blob\\Ball.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image.');
			break;

		# 노드에 소스 이미지를 설정합니다. # Sets the source image to the node.
		if (res := nodeSourceImage.SetParameter('Image', fliSource)).IsFail():
			ErrorPrint(res, 'Failed to set the parameter.');
			break;

		# 스냅 실행 # Run SNAP
		if (res := snapBuild.Run()).IsFail():
			ErrorPrint(res, 'Failed to run the SNAP.')
			break

		# 스냅 실행이 종료 될때까지 대기합니다. # Waits until the SNAP run is complete.
		snapBuild.WaitStop();

		listThresholdResult = List[Double]();

		res = nodeThresholdResult.GetParameter('Multi Variable', listThresholdResult);

		# 스냅이 종료될 때 까지 기다림 # Wait for the SNAP to close
		while snapBuild.IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function



# 에러 출력 함수 # Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()