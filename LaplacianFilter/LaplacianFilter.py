# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *
from enum import IntEnum

class EType(IntEnum):
	Source = 0,
	Destination1 = 1,
	Destination2 = 2,
	Destination3 = 3,
	Destination4 = 4,
	ETypeCount = 5,
		

# 메인 함수 // Main function
def main():

	# 이미지 객체 선언 // Declare the image object
	listFliImage = List[CFLImage]()

	for i in range (0, int(EType.ETypeCount)):
		listFliImage.Add(CFLImage())

	# 이미지 뷰 선언 // Declare the image view
	listViewImage = List[CGUIViewImage]()

	for i in range (0, int(EType.ETypeCount)):
		listViewImage.Add(CGUIViewImage())

	while True:

		# 이미지 로드 // Load image
		if (res := listFliImage[int(EType.Source)].Load("../../ExampleImages/EdgeDetection/Alphabat.flif")).IsFail():
			ErrorPrint(res, "Failed to load the image file.\n")
			break

		bError = False

		for i in range(int(EType.Destination1), int(EType.ETypeCount)):
		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 // Create destination image as same as source image
			if (res := (listFliImage[i].Assign(listFliImage[int(EType.Source)]))).IsFail():
				ErrorPrint(res, "Failed to assign the image file.\n")
				bError = True
				break

		if bError:
			break

		for i in range (0, int(EType.ETypeCount)):
			x = int(i % 3)
			y = int(i / 3)

			# 이미지 뷰 생성 // Create image view
			if (res := (listViewImage[i].Create(x * 400 + 400, y * 400, x * 400 + 400 + 400, y * 400 + 400))).IsFail():
				ErrorPrint(res, "Failed to create the image view.\n")
				bError = True
				break

			# 이미지 뷰에 이미지를 디스플레이 // Display an image in an image view
			# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
			if (res := (listViewImage[i].SetImagePtr(listFliImage[i]))[0]).IsFail():
				ErrorPrint(res, "Failed to set image object on the image view.\n")
				bError = True
				break

			if i == int(EType.Source):
				continue

			# 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views
			# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
			if (res := (listViewImage[int(EType.Source)].SynchronizePointOfView(listViewImage[i]))[0]).IsFail():
				ErrorPrint(res, "Failed to synchronize view\n")
				bError = True
				break

			# 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
			# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
			if (res := (listViewImage[int(EType.Source)].SynchronizeWindow(listViewImage[i]))[0]).IsFail():
				ErrorPrint(res, "Failed to synchronize window.\n")
				bError = True
				break

		if bError:
			break

		# ROI 설정을 위한 CFLRect 객체 생성 // Create a CFLRect object for setting ROI
		flrROI = CFLRect[int](200, 200, 500, 500)

		# Laplacian Filter 객체 생성 // Create Laplacian Filter object
		laplacianFilter = CLaplacianFilter()
		# Source 이미지 설정 // Set the source image
		laplacianFilter.SetSourceImage(listFliImage[int(EType.Source)])
		# Source ROI 설정 // Set the Source ROI
		laplacianFilter.SetSourceROI(flrROI)

		# Destination1 이미지 설정 // Set the destination1 image
		laplacianFilter.SetDestinationImage(listFliImage[int(EType.Destination1)])
		# Destination1 ROI 설정 // Set the destination1 ROI
		laplacianFilter.SetDestinationROI(flrROI)

		# 커널 연산 방법 설정 // Set kernel operation method
		laplacianFilter.SetKernelMethod(CLaplacianFilter.EKernel.LaplacianX);

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := (laplacianFilter.Execute())).IsFail():
			ErrorPrint(res, "Failed to execute Laplacian Filter.")
			break

		# Destination2 이미지 설정 // Set the destination2 image
		laplacianFilter.SetDestinationImage(listFliImage[int(EType.Destination2)])
		# Destination2 ROI 설정 // Set the destination2 ROI
		laplacianFilter.SetDestinationROI(flrROI)

		# 커널 연산 방법 설정 // Set kernel operation method
		laplacianFilter.SetKernelMethod(CLaplacianFilter.EKernel.LaplacianY);

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := (laplacianFilter.Execute())).IsFail():
			ErrorPrint(res, "Failed to execute Laplacian Filter.")
			break

		# Destination3 이미지 설정 // Set the destination3 image
		laplacianFilter.SetDestinationImage(listFliImage[int(EType.Destination3)])
		# Destination3 ROI 설정 // Set the destination3 ROI
		laplacianFilter.SetDestinationROI(flrROI)

		# 커널 연산 방법 설정 // Set kernel operation method
		laplacianFilter.SetKernelMethod(CLaplacianFilter.EKernel.Laplacian4);

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := (laplacianFilter.Execute())).IsFail():
			ErrorPrint(res, "Failed to execute Laplacian Filter.")
			break

		# Destination4 이미지 설정 // Set the destination4 image
		laplacianFilter.SetDestinationImage(listFliImage[int(EType.Destination4)])
		# Destination4 ROI 설정 // Set the destination4 ROI
		laplacianFilter.SetDestinationROI(flrROI)

		# 커널 연산 방법 설정 // Set kernel operation method
		laplacianFilter.SetKernelMethod(CLaplacianFilter.EKernel.Laplacian8);

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := (laplacianFilter.Execute())).IsFail():
			ErrorPrint(res, "Failed to execute Laplacian Filter.")
			break

		listLayer = List[CGUIViewImageLayer]()

		for i in range (0, int(EType.ETypeCount)):
			# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
			# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
			listLayer.Add(listViewImage[i].GetLayer(0))

			# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
			listLayer[i].Clear()

			# ROI영역이 어디인지 알기 위해 디스플레이 한다 // Display to find out where ROI is
			# FLImaging의 Figure 객체들은 어떤 도형모양이든 상관없이 하나의 함수로 디스플레이가 가능 // FLimaging's Figure objects can be displayed as a function regardless of the shape
			# 아래 함수 DrawFigureImage는 Image좌표를 기준으로 하는 Figure를 Drawing 한다는 것을 의미하며 // The function DrawFigureImage below means drawing a picture based on the image coordinates
			# 맨 마지막 두개의 파라미터는 불투명도 값이고 1일경우 불투명, 0일경우 완전 투명을 의미한다. // The last two parameters are opacity values, which mean opacity for 1 day and complete transparency for 0 day.
			# 파라미터 순서 : 레이어 -> Figure 객체 -> 선 색 -> 선 두께 -> 면 색 -> 펜 스타일 -> 선 알파값(불투명도) -> 면 알파값 (불투명도) // Parameter order: Layer -> Figure object -> Line color -> Line thickness -> Face color -> Pen style -> Line alpha value (opacity) -> Area alpha value (opacity)
			if (res := (listLayer[i].DrawFigureImage(flrROI, EColor.LIME))).IsFail():
				ErrorPrint(res, "Failed to draw figure.\n")

		# View 정보를 디스플레이 한다. // Display view information
		# 아래 함수 DrawTextCanvas은 Screen좌표를 기준으로 하는 String을 Drawing 한다. // The function DrawTextCanvas below draws a String based on the screen coordinates.
		# 색상 파라미터를 EGUIViewImageLayerTransparencyColor 으로 넣어주게되면 배경색으로 처리함으로 불투명도를 0으로 한것과 같은 효과가 있다. // If the color parameter is added as EGUIViewImageLayerTransparencyColor, it has the same effect as setting the opacity to 0 by processing it as a background color.
		# 파라미터 순서 : 레이어 -> 기준 좌표 Figure 객체 -> 문자열 -> 폰트 색 -> 면 색 -> 폰트 크기 -> 실제 크기 유무 -> 각도 ->
		#                 얼라인 -> 폰트 이름 -> 폰트 알파값(불투명도) -> 면 알파값 (불투명도) -> 폰트 두께 -> 폰트 이텔릭
		# Parameter order: layer -> reference coordinate Figure object -> string -> font color -> Area color -> font size -> actual size -> angle ->
		#                  Align -> Font Name -> Font Alpha Value (Opaqueness) -> Cotton Alpha Value (Opaqueness) -> Font Thickness -> Font Italic
		flpZero = CFLPoint[Double](0, 0)

		if (res := (listLayer[int(EType.Source)].DrawTextCanvas(flpZero, "Source Image", EColor.YELLOW, EColor.BLACK, 20))).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break

		if (res := (listLayer[int(EType.Destination1)].DrawTextCanvas(flpZero, "Destination1 Image (LaplacianX)", EColor.YELLOW, EColor.BLACK, 20))).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break

		if (res := (listLayer[int(EType.Destination2)].DrawTextCanvas(flpZero, "Destination2 Image (LaplacianY)", EColor.YELLOW, EColor.BLACK, 20))).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break

		if (res := (listLayer[int(EType.Destination3)].DrawTextCanvas(flpZero, "Destination3 Image (Laplacian4)", EColor.YELLOW, EColor.BLACK, 20))).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break

		if (res := (listLayer[int(EType.Destination4)].DrawTextCanvas(flpZero, "Destination4 Image (Laplacian8)", EColor.YELLOW, EColor.BLACK, 20))).IsFail():
			ErrorPrint(res, "Failed to draw text.\n")
			break

		# 이미지 뷰를 갱신 합니다. // Update image view
		for i in range (0, int(EType.ETypeCount)):
			listViewImage[i].Invalidate(True)

		# 이미지 뷰가 종료될 때 까지 기다림 // Wait for the image view to close
		bAvailable = True

		while bAvailable:
			for i in range (0, int(EType.ETypeCount)):
				bAvailable = listViewImage[i].IsAvailable()

				if not bAvailable:
					break

			CThreadUtilities.Sleep(1)

		break
	
	# End of main function



# 에러 출력 함수 // Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : res.GetResultCode()\nError name : res.GetString()\n')


if __name__ == '__main__':
    main()