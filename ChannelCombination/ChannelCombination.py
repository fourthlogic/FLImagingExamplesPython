# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *


# 메인 함수 # Main function
def main():

	# 이미지 객체 선언 # Declare the image object
	fliImage = [CFLImage() for i in range(3)]
	fliDstImage = CFLImage()

	# 이미지 뷰 선언 # Declare the image view
	viewSrcImage = [CGUIViewImage() for i in range(3)]
	viewDstImage = CGUIViewImage()

	while True:
		
		# Source 이미지 로드 # Load the source image
		if (res := fliImage[0].Load('../../ExampleImages/ChannelCombination/Valley1.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		if (res := fliImage[1].Load('../../ExampleImages/ChannelCombination/Valley2.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		if (res := fliImage[2].Load('../../ExampleImages/ChannelCombination/Valley3.flif')).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break
		
		# Source 이미지 뷰 생성 # Create source image view
		if (res := viewSrcImage[0].Create(100, 0, 100 + 440, 340)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		if (res := viewSrcImage[1].Create(100 + 440, 0, 100 + 440 * 2, 340)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		if (res := viewSrcImage[2].Create(100 + 440 * 2, 0, 100 + 440 * 3, 340)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
		if (res := viewDstImage.Create(100 + 440 * 3, 0, 100 + 440 * 4, 340)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		
        # 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
        # ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... 형태를 반환한다.
		if (res := viewSrcImage[0].SynchronizePointOfView(viewSrcImage[1])[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize view")
			break
		
        # 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
        # ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... 형태를 반환한다.
		if (res := viewSrcImage[1].SynchronizePointOfView(viewSrcImage[2])[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize view")
			break
		
        # 두 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the two image views
        # ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... 형태를 반환한다.
		if (res := viewSrcImage[2].SynchronizePointOfView(viewDstImage)[0]).IsFail():
			ErrorPrint(res, "Failed to synchronize view")
			break
		
		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewSrcImage[0].SynchronizeWindow(viewSrcImage[1])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break
		
		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewSrcImage[1].SynchronizeWindow(viewSrcImage[2])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break
		
		# 두 이미지 뷰 윈도우의 위치를 맞춤 # Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. # A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewSrcImage[2].SynchronizeWindow(viewDstImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break
		
		# 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
		if (res := viewSrcImage[0].SetImagePtr(fliImage[0])[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		if (res := viewSrcImage[1].SetImagePtr(fliImage[1])[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		if (res := viewSrcImage[2].SetImagePtr(fliImage[2])[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		if (res := viewDstImage.SetImagePtr(fliDstImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break
		
		# Channel Combination 객체 생성 # Create Channel Combination object
		ChannelCombination = CChannelCombination()

		# Source 이미지를 저장할 Array 선언 # Declare an Array to store the source image
		vctSrcImages = List[CFLImage]()

		# 결합할 채널을 저장할 Array 선언 # Declare an Array to store the channels
		vctSrcChannels = List[Int64]()

		# Source 이미지 입력 # source images add
		vctSrcImages.Add(fliImage[0])
		vctSrcImages.Add(fliImage[1])
		vctSrcImages.Add(fliImage[2])

		# 이미지별 결합할 채널을 입력 # channels add
		vctSrcChannels.Add(int(EChannelSelection.Channel_0))
		vctSrcChannels.Add(int(EChannelSelection.Channel_0))
		vctSrcChannels.Add(int(EChannelSelection.Channel_0))

		# 결합할 이미지 및 채널입력 # Set images, channels
		ChannelCombination.SetSourceImage(vctSrcImages, vctSrcChannels)

		# 결합 결과를 저장할 이미지 설정 # Set destination image
		ChannelCombination.SetDestinationImage(fliDstImage)

		# 앞서 설정된 파라미터 대로 알고리즘 수행 # Execute algorithm according to previously set parameters
		if (res := ChannelCombination.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute.')
			break
		
		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
		layer1 = viewSrcImage[0].GetLayer(0)
		layer2 = viewSrcImage[1].GetLayer(0)
		layer3 = viewSrcImage[2].GetLayer(0)
		layer4 = viewDstImage.GetLayer(0)

		flpPoint = CFLPoint[Double](0, 0)
		
		# 기존에 Layer에 그려진 도형들을 삭제 # Delete the shapes drawn on the existing layer
		layer1.Clear()
		layer2.Clear()
		layer3.Clear()
		layer4.Clear()
		
		# View 정보를 디스플레이 합니다. # Display View information.
		if (res := layer1.DrawTextImage(flpPoint, 'Source Image 1', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := layer2.DrawTextImage(flpPoint, 'Source Image 2', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break

		if (res := layer3.DrawTextImage(flpPoint, 'Source Image 3', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		if (res := layer4.DrawTextImage(flpPoint, 'Source Image 1+2+3', EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, 'Failed to draw text.')
			break
		
		# 이미지 뷰를 갱신 합니다. # Update the image view.
		viewSrcImage[0].Invalidate(True);
		viewSrcImage[1].Invalidate(True);
		viewSrcImage[2].Invalidate(True);
		viewDstImage.Invalidate(True);

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until the image view is closed before exiting
		while viewSrcImage[0].IsAvailable() and viewSrcImage[1].IsAvailable() and viewSrcImage[2].IsAvailable() and viewDstImage.IsAvailable():
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