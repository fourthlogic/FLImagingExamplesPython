# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()



# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	listFliImage = [CFLImage(), CFLImage(), CFLImage(), CFLImage(), CFLImage()]

	# 이미지 뷰 선언 # Declare the image view
	listViewImage = [CGUIViewImage(), CGUIViewImage(), CGUIViewImage(), CGUIViewImage(), CGUIViewImage()]
	
	bError = False

	while True:
		# Source 이미지 로드 # Load the source image
		if (res := (listFliImage[0].Load("../../ExampleImages/WienerDeconvolutionFilter/bird.flif"))).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break

		for i in range(1, 5) :
		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 # Create destination image as same as source image
			if (res := listFliImage[i].Assign(listFliImage[0])).IsFail():
				ErrorPrint(res, 'Failed to assign the image.')
				break

		for i in range(0, 5) :		
			x = i % 3
			y = i // 3

			# 이미지 뷰 생성 # Create image view
			if(res := listViewImage[i].Create(x * 400 + 400, y * 400, x * 400 + 400 + 400, y * 400 + 400)).IsFail() :
			
				ErrorPrint(res, "Failed to create the image view.\n")
				bError = True
				break
			

			# 이미지 뷰에 이미지를 디스플레이 # Display an image in an image view
			if(res := listViewImage[i].SetImagePtr(listFliImage[i])[0]).IsFail() :
			
				ErrorPrint(res, "Failed to set image object on the image view.\n")
				bError = True
				break
			
			if i == 0:
				continue

			# 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
			if(res := listViewImage[0].SynchronizePointOfView(listViewImage[i])[0]).IsFail() :
			
				ErrorPrint(res, "Failed to synchronize view\n")
				bError = True
				break
			

			# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
			if(res := listViewImage[0].SynchronizeWindow(listViewImage[i])[0]).IsFail() :			
				ErrorPrint(res, "Failed to synchronize window.\n")
				bError = True
				break
			
		if bError:
			break

		# WienerDeconvolution filter 객체 생성 # Create WienerDeconvolution filter object
		wienerDeconvolutionFilter = CWienerDeconvolutionFilter()
		# Source 이미지 설정 # Set the source image
		wienerDeconvolutionFilter.SetSourceImage(listFliImage[0])

		# Destination1 이미지 설정 # Set the destination1 image
		wienerDeconvolutionFilter.SetDestinationImage(listFliImage[1])

		# Destination3 이미지 설정 # Set the destination3 image
		wienerDeconvolutionFilter.SetResultFrequency(listFliImage[3])

		# Angle 값 설정 # Set the Angle value
		wienerDeconvolutionFilter.SetAngle(45)

		# Length 값 설정 # Set the Length value
		wienerDeconvolutionFilter.SetLength(135)

		# SNR 값 설정 # Set the SNR value
		wienerDeconvolutionFilter.SetSNR(0.00001)

		# Motion Blur 값 설정 # Set the Motion Blur value
		wienerDeconvolutionFilter.SetOperationType(CWienerDeconvolutionFilter.EOperationType.Convolution)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := wienerDeconvolutionFilter.Execute()).IsFail() :
		
			ErrorPrint(res, "Failed to execute Wiener Deconvolution Filter.")
			break
		

		# Source 이미지 설정 # Set the source image
		wienerDeconvolutionFilter.SetSourceImage(listFliImage[1])

		# Destination2 이미지 설정 # Set the destination2 image
		wienerDeconvolutionFilter.SetDestinationImage(listFliImage[2])

		# Destination4 이미지 설정 # Set the destination4 image
		wienerDeconvolutionFilter.SetResultFrequency(listFliImage[4])

		# Motion Blur 값 설정 # Set the Motion Blur value
		wienerDeconvolutionFilter.SetOperationType(CWienerDeconvolutionFilter.EOperationType.Deconvolution)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if(res := wienerDeconvolutionFilter.Execute()).IsFail() :
		
			ErrorPrint(res, "Failed to execute Wiener Deconvolution Filter.")
			break
						

		listLayer = [CGUIViewImageLayer(), CGUIViewImageLayer(), CGUIViewImageLayer(), CGUIViewImageLayer(), CGUIViewImageLayer()]
		
		for i in range(0, 5) :
		
			# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
			# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
			listLayer[i] = listViewImage[i].GetLayer(0)

			# 기존에 Layer에 그려진 도형들을 삭제 # Clear the figures drawn on the existing layer
			listLayer[i].Clear()
		

		# View 정보를 디스플레이 한다. # Display view information
		# 아래 함수 DrawTextCanvas은 Screen좌표를 기준으로 하는 String을 Drawing 한다. # The function DrawTextCanvas below draws a String based on the screen coordinates.
		# 색상 파라미터를 EGUIViewImageLayerTransparencyColor 으로 넣어주게되면 배경색으로 처리함으로 불투명도를 0으로 한것과 같은 효과가 있다. # If the color parameter is added as EGUIViewImageLayerTransparencyColor, it has the same effect as setting the opacity to 0 by processing it as a background color.
		# 파라미터 순서 : 레이어 -> 기준 좌표 Figure 객체 -> 문자열 -> 폰트 색 -> 면 색 -> 폰트 크기 -> 실제 크기 유무 -> 각도 ->
		#                 얼라인 -> 폰트 이름 -> 폰트 알파값(불투명도) -> 면 알파값 (불투명도) -> 폰트 두께 -> 폰트 이텔릭
		# Parameter order: layer -> reference coordinate Figure object -> string -> font color -> Area color -> font size -> actual size -> angle ->
		#                  Align -> Font Name -> Font Alpha Value (Opaqueness) -> Cotton Alpha Value (Opaqueness) -> Font Thickness -> Font Italic
		flpZero = CFLPoint[Double](0, 0)

		if(res := listLayer[0].DrawTextCanvas(flpZero, "Source Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail() :
		
			ErrorPrint(res, "Failed to draw text.\n")
			break
		

		if(res := listLayer[1].DrawTextCanvas(flpZero, "Destination1 Image (Motion Blur)", EColor.YELLOW, EColor.BLACK, 20)).IsFail() :
		
			ErrorPrint(res, "Failed to draw text.\n")
			break
		

		if(res := listLayer[2].DrawTextCanvas(flpZero, "Destination2 Image (Deconvolution)", EColor.YELLOW, EColor.BLACK, 20)).IsFail() :
		
			ErrorPrint(res, "Failed to draw text.\n")
			break
		

		if(res := listLayer[3].DrawTextCanvas(flpZero, "Destination3 Image (Blur Frequency)", EColor.YELLOW, EColor.BLACK, 20)).IsFail() :
		
			ErrorPrint(res, "Failed to draw text.\n")
			break
		

		if(res := listLayer[4].DrawTextCanvas(flpZero, "Destination4 Image (Deconv Frequency)", EColor.YELLOW, EColor.BLACK, 20)).IsFail() :
		
			ErrorPrint(res, "Failed to draw text.\n")
			break
		

		# 이미지 뷰를 갱신 합니다. # Update image view
		for i in range(0, 5) :
			listViewImage[i].Invalidate(True)

		# 이미지 뷰가 종료될 때 까지 기다림 # Wait for the image view to close		
		while listViewImage[0].IsAvailable() and listViewImage[1].IsAvailable() and listViewImage[2].IsAvailable() and \
			listViewImage[3].IsAvailable() and listViewImage[4].IsAvailable():
			CThreadUtilities.Sleep(1)
		
		break
	
	# End of main function



# 에러 출력 함수 # Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : res.GetResultCode()\nError name : res.GetString()\n')


if __name__ == '__main__':
    main()