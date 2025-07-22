# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 // Main function
def main():

	# 이미지 객체 선언 // Declare the image object
	fliImage = CFLImage()

	# 이미지 뷰 선언 // Declare the image view
	viewImage = CGUIViewImage()

	while True:
		# 이미지 로드 // Load image
		if (res := fliImage.Load("../../ExampleImages/HarrisCornerDetector/Chip.flif")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break

		# 이미지 뷰 생성 // Create image view
		if (res := viewImage.Create(400, 0, 1168, 540)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break
		

		# 이미지 뷰에 이미지를 디스플레이 // Display an image in an image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImage.SetImagePtr(fliImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break
		
		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
		layer = viewImage.GetLayer(0);

		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layer.Clear();

		# Harris Corner Detector 객체 생성 // Create Harris Corner Detector object
		harris = CHarrisCornerDetector();

		# ROI Draw를 위한 CFLRectL 객체 생성 // Create CFLRectL object for ROI Drawing
		flrROI = CFLRect[int](100, 50, 450, 450);

		# 처리할 이미지 설정 // Set the image to process
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := harris.SetSourceImage(fliImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set Source Image.");
			break;

		# 처리할 ROI 설정 // Set the ROI to process
		if (res := (harris.SetSourceROI(flrROI))).IsFail():
			ErrorPrint(res, "Failed to set Source ROI.");
			break;

		# 코너를 검출하는 이미지의 Scale 값을 설정 // Set the Scale value for the image to detect the corner
		if (res := (harris.SetScale(1.0))).IsFail():
			ErrorPrint(res, "Failed to set scale.");
			break;

		# 검출할 최대 점의 개수를 설정 // Set the maximum number of points to detect
		if (res := (harris.SetMaxPoints(500))).IsFail():
			ErrorPrint(res, "Failed to set max points.");
			break;

		# 검출할 점수의 임계값을 설정 //Set the Threshold of score to detect
		if (res := (harris.SetScoreThreshold(0.8))).IsFail():
			ErrorPrint(res, "Failed to set score threshold.");
			break;

		# 해리스 코너 디텍터의 파리미터 K를 설정 //Set the parameter K for the Harris Corner Detector
		if (res := (harris.SetParamK(0.04))).IsFail():
			ErrorPrint(res, "Failed to set param K.");
			break;

		# 해리스 코너 디텍터 알고리즘 실행 // Execute Harris Corner Detector algorithm
		if (res := (harris.Execute())).IsFail():
			ErrorPrint(res, "Failed to execute.");
			break;

		# 실행 결과를 받아오기 위한 컨테이너 // The container to get execution result
		flfaResultPoints = CFLFigureArray();

		# 검출된 점을 가져옴 // Get the detected points 
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := (harris.GetResultPoints(flfaResultPoints))[0]).IsFail():
			ErrorPrint(res, "Failed to get result.");
			break;

		# 검출된 점의 개수를 가져오는 함수 // Get the number of detected points 
		i64Count = harris.GetResultCount();

		for i in range (0, i64Count):
			# 검출된 점을 출력 // Print the detected points 
			pFlpTemp = (CFLPoint[Double])(flfaResultPoints.GetAt(i));
			layer.DrawFigureImage(pFlpTemp, EColor.RED, 1);

		# ROI영역이 어디인지 알기 위해 디스플레이 한다 // Display to find out where ROI is
		# FLImaging의 Figure객체들은 어떤 도형모양이든 상관없이 하나의 함수로 디스플레이가 가능
		if (res := (layer.DrawFigureImage(flrROI, EColor.BLUE))).IsFail():
			ErrorPrint(res, "Failed to draw figures objects on the image view.\n");
			break;

		# 이미지 뷰를 갱신 합니다. // Update image view
		viewImage.Invalidate(True);

		# 이미지 뷰가 종료될 때 까지 기다림 // Wait for the image view to close
		while viewImage.IsAvailable() :
			CThreadUtilities.Sleep(1);

		break
	
	# End of main function



# 에러 출력 함수 // Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : res.GetResultCode()\nError name : res.GetString()\n')


if __name__ == '__main__':
    main()