# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# 메인 함수 // Main function
def main():

	# 이미지 객체 선언 // Declare the image object
	fliSourceImage = CFLImage()
	fliInsertionImage = [CFLImage(), CFLImage()];
	fliDestinationImage = CFLImage()

	# 이미지 뷰 선언 // Declare the image view
	viewImageSrc = CGUIViewImage()
	viewImageInsertion = [ CGUIViewImage(), CGUIViewImage() ]
	viewImageDst = CGUIViewImage()

	while True:
		
		# Source 이미지 로드 // Load the source image
		if (res := fliSourceImage.Load("../../ExampleImages/ChannelInsertion/Valley1.flif")).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Insertion 이미지 1 로드 // Load the source image
		if (res := fliInsertionImage[0].Load("../../ExampleImages/ChannelInsertion/Valley2.flif")).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Insertion 이미지 2 로드 // Load the source image
		if (res := fliInsertionImage[1].Load("../../ExampleImages/ChannelInsertion/Valley3.flif")).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Destination 이미지를 Source 이미지와 동일한 이미지로 생성 // Create destination image as same as source image
		if (res := fliDestinationImage.Assign(fliSourceImage)).IsFail():
			ErrorPrint(res, 'Failed to load the image file.')
			break

		# Source 이미지 뷰 생성 // Create source image view
		if (res := viewImageSrc.Create(100, 0, 100 + 440, 340)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break
		# Insertion 이미지 뷰 생성 // Create source image view
		if (res := viewImageInsertion[0].Create(100 + 440, 0, 100 + 440 * 2, 340)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Insertion 이미지 뷰 생성 // Create source image view
		if (res := viewImageInsertion[1].Create(100 + 440 * 2, 0, 100 + 440 * 3, 340)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# Destination 이미지 뷰 생성 // Create the destination image view
		if (res := viewImageDst.Create(100 + 440 * 3, 0, 100 + 440 * 4, 340)).IsFail():
			ErrorPrint(res, 'Failed to create the image view.')
			break

		# 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizePointOfView(viewImageInsertion[0])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageInsertion[0].SynchronizePointOfView(viewImageInsertion[1])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# 두 이미지 뷰의 시점을 동기화 한다 // Synchronize the viewpoints of the two image views
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageInsertion[1].SynchronizePointOfView(viewImageDst)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize view.')
			break

		# Source 이미지 뷰에 이미지를 디스플레이 // Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SetImagePtr(fliSourceImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Insertion 이미지 뷰에 이미지를 디스플레이 // Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageInsertion[0].SetImagePtr(fliInsertionImage[0])[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Insertion 이미지 뷰에 이미지를 디스플레이 // Display the image in the source image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageInsertion[1].SetImagePtr(fliInsertionImage[1])[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# Destination 이미지 뷰에 이미지를 디스플레이 // Display the image in the destination image view
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageDst.SetImagePtr(fliDestinationImage)[0]).IsFail():
			ErrorPrint(res, 'Failed to set image object on the image view.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageSrc.SynchronizeWindow(viewImageInsertion[0])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageInsertion[0].SynchronizeWindow(viewImageInsertion[1])[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# 두 이미지 뷰 윈도우의 위치를 맞춤 // Synchronize the positions of the two image view windows
		# ref 파라미터를 입력 받는 함수는 리턴이 tuple로 생성되며 [return], [ref 0], ... [ref n-1] 형태로 tuple 을 반환한다. // A function that receives ref parameters returns a tuple structured as [return], [ref 0], ... [ref n-1].
		if (res := viewImageInsertion[1].SynchronizeWindow(viewImageDst)[0]).IsFail():
			ErrorPrint(res, 'Failed to synchronize window.')
			break

		# Channel Insertion 객체 생성 // Create Channel Insertion object
		channelInsertion = CChannelInsertion()

		# 삽입 이미지를 저장할 List 생성 // Declare an Array to store the insertion image
		listInsertionImages = List[CFLImage]();

		# 추출할 채널을 저장할 Array 선언 // Declare an Array to extract the channels
		listInsertionChannels = List[Int64]();

		# 삽입할 색인을 저장할 Array 선언 // Declare an Array to insert the indices
		listInsertionIndices = List[Int64]();

		# 삽입 이미지 입력 // insertion images add
		listInsertionImages.Add(fliInsertionImage[0]);
		listInsertionImages.Add(fliInsertionImage[1]);

		# 이미지별 추출할 채널을 입력 // channels add
		listInsertionChannels.Add(Convert.ToInt64(EChannelSelection.Channel_0));
		listInsertionChannels.Add(Convert.ToInt64(EChannelSelection.Channel_0));

		# 이미지별 삽입할 색인을 입력 // indices add
		listInsertionIndices.Add(0);
		listInsertionIndices.Add(1);

		# 소스 이미지 설정 // Set source image
		channelInsertion.SetSourceImage(fliSourceImage);

		# 결합할 이미지 및 채널입력 // Set images, channels
		channelInsertion.SetInsertionImage(listInsertionImages, listInsertionChannels, listInsertionIndices);

		# 결합 결과를 저장할 이미지 설정 // Set destination image
		channelInsertion.SetDestinationImage(fliDestinationImage);

		# 앞서 설정된 파라미터 대로 알고리즘 수행 // Execute algorithm according to previously set parameters
		if (res := channelInsertion.Execute()).IsFail():
			ErrorPrint(res, 'Failed to execute Channel Insertion.')
			break

		# 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 // Obtain layer 0 number from image view for display
		# 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 // This object belongs to an image view and does not need to be released separately
		layerSource = viewImageSrc.GetLayer(0)
		layerInsertion0 = viewImageInsertion[0].GetLayer(0)
		layerInsertion1 = viewImageInsertion[1].GetLayer(0)
		layerDestination = viewImageDst.GetLayer(0)

		# 기존에 Layer에 그려진 도형들을 삭제 // Clear the figures drawn on the existing layer
		layerSource.Clear()
		layerDestination.Clear()

		# 이미지 뷰 정보 표시 // Display image view information
		flpPoint = CFLPoint[Double](0, 0)

		if (res := layerSource.DrawTextImage(flpPoint, "Source Image", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.");

		if (res := layerInsertion0.DrawTextImage(flpPoint, "Insertion Image 1", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.");

		if (res := layerInsertion1.DrawTextImage(flpPoint, "Insertion Image 2", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.");

		if (res := layerDestination.DrawTextImage(flpPoint, "Insertion Image 1 +\nSource Image +\nInsertion Image 2", EColor.YELLOW, EColor.BLACK, 20)).IsFail():
			ErrorPrint(res, "Failed to draw text.");

		# 이미지 뷰를 갱신 // Update image view
		viewImageSrc.Invalidate(True)
		viewImageInsertion[0].Invalidate(True)
		viewImageInsertion[1].Invalidate(True)
		viewImageDst.Invalidate(True)

		# # 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 // Wait until the image view is closed before exiting
		while viewImageSrc.IsAvailable() and viewImageInsertion[0].IsAvailable() and viewImageInsertion[1].IsAvailable() and viewImageDst.IsAvailable():
			CThreadUtilities.Sleep(1)

		break
	
	# End of main function



# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}')


if __name__ == '__main__':
    main()