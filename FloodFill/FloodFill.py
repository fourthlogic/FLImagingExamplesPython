
# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *
from enum import IntEnum

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 이미지 타입 열거형 # Image type enum
class EType:
	Source = 0
	Destination1 = 1
	Destination2 = 2
	COUNT = 3


# 메인 함수 # Main function
def main():
    # 이미지 객체 선언 # Declare the image object
	arrFliImage = [CFLImage() for i in range(EType.COUNT)]

	# 이미지 뷰 선언 # Declare the image view
	arrViewImage = [CGUIViewImage() for i in range(EType.COUNT)]

	while True:

		# 이미지 로드 # Load image
		if (res := arrFliImage[EType.Source].Load("../../ExampleImages/FloodFill/Ball.flif")).IsFail() :
			ErrorPrint(res, "Failed to load the image file.")
			break

		# 이미지 뷰 생성 # Create image view
		for i in range(EType.COUNT) :
			if (res := arrViewImage[i].Create(300 + 520 * i, 0, 300 + 520 * (i + 1), 430)).IsFail() :
				ErrorPrint(res, "Failed to create the image view.")
				break

		if res.IsFail() :
			break

		# 이미지 뷰들의 시점을 동기화 한다 # Synchronize the viewpoints of the image views.
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		for i in range(EType.Destination1, EType.COUNT) :
			if (res := arrViewImage[EType.Source].SynchronizePointOfView(arrViewImage[i])[0]).IsFail() :
				ErrorPrint(res, "Failed to synchronize view")
				break

		if res.IsFail() :
			break

		# 이미지 뷰 윈도우들의 위치를 동기화 한다 # Synchronize the positions of the image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		for i in range(EType.Destination1, EType.COUNT) :
			if (res := arrViewImage[EType.Source].SynchronizeWindow(arrViewImage[i])[0]).IsFail() :
				ErrorPrint(res, "Failed to synchronize window")
				break

		if res.IsFail() :
			break

		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		for i in range(EType.COUNT) :
			if (res := arrViewImage[i].SetImagePtr(arrFliImage[i])[0]).IsFail() :
				ErrorPrint(res, "Failed to set image object on the image view.")
				break

		if res.IsFail() :
			break

		# Flood Fill 객체 생성 # Create Flood Fill object
		floodFill = CFloodFill()

		# Source 이미지 설정 # Set source image
		floodFill.SetSourceImage(arrFliImage[EType.Source])

		# 시작 지점 설정 # Set seed point
		flpSeedPoint = CFLPoint[Double](9, 9)
		floodFill.SetSeedPoint(flpSeedPoint)

		# 픽셀 값 차이의 상한 설정 # Set upper bound of pixel value differences
		floodFill.SetUpperDifference(CMultiVar[Double](10))

		# 픽셀 값 차이의 하한 설정 # Set lower bound of pixel value differences
		floodFill.SetLowerDifference(CMultiVar[Double](10))

		# 연결 영역 출력값 설정 # Set output value of connected region
		floodFill.SetRangeValue(CMultiVar[Double](255))

		# 연결 영역이 아닌 영역의 출력값 설정 # Set output value of out of connected region
		floodFill.SetOutOfRangeValue(CMultiVar[Double](0))

		# Destination1 이미지 설정 # Set Destination1 image
		floodFill.SetDestinationImage(arrFliImage[EType.Destination1])

		# Floating Range Mode 설정 # Set Floating Range Mode
		floodFill.SetRangeMode(CFloodFill.ERangeMode.FloatingRange)

		# 알고리즘 수행 # Execute the algorithm
		if (res := (floodFill.Execute())).IsFail() :
			ErrorPrint(res, "Failed to execute Flood Fill (Floating Range).")
			break

		# Destination2 이미지 설정 # Set Destination2 image
		floodFill.SetDestinationImage(arrFliImage[EType.Destination2])

		# Fixed Range Mode 설정 # Set Fixed Range Mode
		floodFill.SetRangeMode(CFloodFill.ERangeMode.FixedRange)

		# 알고리즘 수행 # Execute the algorithm
		if (res := (floodFill.Execute())).IsFail() :
			ErrorPrint(res, "Failed to execute Flood Fill (Fixed Range).")
			break

		# 출력을 위한 이미지 레이어를 얻어옵니다. #  Gets the image layer for output.
		# 따로 해제할 필요 없음 # No need to release separately
		arrLayer = [arrViewImage[i].GetLayer(0) for i in range(EType.COUNT)]
		flpTemp = CFLPoint[Double](0, 0)

		# 시작 지점을 디스플레이 합니다. # Display the seed point.
		if (res := arrLayer[EType.Source].DrawFigureImage(flpSeedPoint, EColor.RED, 3)).IsFail() :
			ErrorPrint(res, "Failed to draw figure.")

		# View 정보를 디스플레이 합니다. # Display View information.
		arrViewText = ["Source Image", "Floating Range", "Fixed Range"]

		for i in range(EType.COUNT) :
			if (res := arrLayer[i].DrawTextImage(flpTemp, arrViewText[i], EColor.YELLOW, EColor.BLACK, 20)).IsFail() :
				ErrorPrint(res, "Failed to draw text.")

		# 이미지 뷰를 갱신 합니다. # Update the image view.
		for i in range(EType.COUNT) :
			arrViewImage[i].Invalidate(True)

		# 이미지 뷰가 종료될 때 까지 기다림 # Wait for the image view to close
		while all(arrViewImage[i].IsAvailable() for i in range(EType.COUNT)) :
			CThreadUtilities.Sleep(1)

		for i in range(EType.COUNT) :
			arrViewImage[i].Destroy()

		break


# 에러 출력 함수 # Error printing function
def ErrorPrint(res: CResult, string: str):
    if len(string) > 1:
        print(string)
    print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}')


if __name__ == '__main__':
    main()
