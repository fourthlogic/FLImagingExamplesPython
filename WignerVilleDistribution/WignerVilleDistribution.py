# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 # Main function
def main():
	# 이미지 객체 선언 # Declare the image object
	fliISrcImage = CFLImage()
	fliIDstImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewImage = List[CGUIViewImage]()
	viewImage.Add(CGUIViewImage())
	viewImage.Add(CGUIViewImage())
	
	res = CResult()

	while True:
		# 이미지 로드 # Load image
		if (res := fliISrcImage.Load("../../ExampleImages/WignerVilleDistribution/chirp.flif")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break

		# 이미지 뷰 생성 # Create image view
		if (res := viewImage[0].Create(300, 0, 300 + 520, 430)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break

		if (res := viewImage[1].Create(300 + 520, 0, 300 + 520 * 2, 430)).IsFail():
			ErrorPrint(res, "Failed to create the image view.\n")
			break

		# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views. 
		if (res := viewImage[0].SynchronizePointOfView(viewImage[1])[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize view\n")
			break

		# 두 이미지 뷰 윈도우의 위치를 동기화 한다 # Synchronize the positions of the two image view windows
		if (res := viewImage[0].SynchronizeWindow(viewImage[1])[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize window\n")
			break

		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		if (res := viewImage[0].SetImagePtr(fliISrcImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break

		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		if (res := viewImage[1].SetImagePtr(fliIDstImage)[0]).IsFail():
			ErrorPrint(res, "Failed to set image object on the image view.\n")
			break

		# Wigner Ville Distribution 객체 생성 # Create Wigner Ville Distribution object
		wvd = CWignerVilleDistribution()
		# Source 이미지 설정 # Set source image 
		if (res := wvd.SetSourceImage(fliISrcImage)[0]).IsFail():
			break
		# Destination 이미지 설정 # Set destination image
		if (res := wvd.SetDestinationImage(fliIDstImage)[0]).IsFail():
			break
		# Scale 설정 # Set Scale
		if (res := wvd.SetScale(0.00004)).IsFail():
			break
		# Self Correlation Half Size 설정 # Set Self Correlation Half Size
		if (res := wvd.SetSelfCorrelationHalfSize(511)).IsFail():
			break
		# Self Correlation Window 설정 # Set Self Correlation Window
		if (res := wvd.SetSelfCorrelationWindow(CWignerVilleDistribution.ESelfCorrelationWindow.Gaussian)).IsFail():
			break
		# Sigma 설정 # Set Sigma
		if (res := wvd.SetSigma(0.3)).IsFail():
			break
		# Output Mode 설정 # Set Output Mode
		if (res := wvd.SetOutputMode(CWignerVilleDistribution.EOutputMode.L2Norm)).IsFail():
			break
		# Output Direction 설정 # Set Output Direction
		if (res := wvd.SetOutputDirection(CWignerVilleDistribution.EOutputDirection.Horizontal)).IsFail():
			break
		# 알고리즘 수행 # Execute the algorithm
		if (res := (wvd.Execute())).IsFail():
			ErrorPrint(res, "Failed to execute algorithm.")
			break

		# 레이어는 따로 해제하지 않아도 View가 해제 될 때 같이 해제된다. # The layer is released together when View is released without releasing it separately.
		layer1 = viewImage[0].GetLayer(0)
		layer2 = viewImage[1].GetLayer(0)
		flpTemp = CFLPoint[Double](0, 0)

		# View 정보를 디스플레이 합니다. # Display View information.
		if (res := layer1.DrawTextImage(flpTemp, "Source Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")

		if (res := layer2.DrawTextImage(flpTemp, "Destination Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")

		viewImage[0].ZoomFit()
		viewImage[1].ZoomFit()

		# 이미지 뷰를 갱신 합니다. # Update image view
		viewImage[0].Invalidate(True)
		viewImage[1].Invalidate(True)

		# 이미지 뷰가 종료될 때 까지 기다림 # Wait for the image view to close
		while viewImage[0].IsAvailable():			
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