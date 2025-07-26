# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


import time

class EType:
    Model = 0
    Texture = 1
    Count = 2

# 메인 함수 # Main function
def main():
	# 이미지 객체 선언 # Declare the image object
    arr_image = [CFLImage() for _ in range(EType.Count)]

	# 이미지 뷰 선언 # Declare the image view
    arr_view_image = [CGUIViewImage() for _ in range(EType.Count)]
    view3d = CGUIView3D()

    res = CResult()

    while True:
        # Model 이미지 로드 # Load Model image        
        if (res := arr_image[EType.Model].Load("../../ExampleImages/View3D/mountain.flif")).IsFail():
            ErrorPrint(res, "Failed to load the image file.")
            break

        # Texture 이미지 로드 # Load Texture image        
        if (res := arr_image[EType.Texture].Load("../../ExampleImages/View3D/mountain_texture.flif")).IsFail():
            ErrorPrint(res, "Failed to load the texture image file.")
            break

        # Model 이미지 뷰 생성 # Create model view        
        if (res := arr_view_image[EType.Model].Create(100, 0, 612, 512)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # Texture 이미지 뷰 생성 # Create texture view        
        if (res := arr_view_image[EType.Texture].Create(612, 0, 1124, 512)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # 3D 뷰 생성 # Create 3D view        
        if (res := view3d.Create(1124, 0, 1636, 512)).IsFail():
            ErrorPrint(res, "Failed to create the 3D view.")
            break

        b_error = False
        for i in range(EType.Count):
            # 이미지 뷰에 이미지를 디스플레이 # Display the image in the image view
            if (res := arr_view_image[i].SetImagePtr(arr_image[i])[0]).IsFail():
                ErrorPrint(res, "Failed to set image object on the image view.")
                b_error = True
                break

        if b_error:
            break

        # 두 이미지 뷰의 시점을 동기화 # Synchronize views        
        if (res := arr_view_image[EType.Model].SynchronizePointOfView(arr_view_image[EType.Texture])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view")
            break

        # 두 이미지 뷰의 위치를 동기화 # Synchronize the position of the two image view windows.
        if (res := arr_view_image[EType.Model].SynchronizeWindow(arr_view_image[EType.Texture])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.")
            break
        
		# 3D 뷰와 이미지 뷰 윈도우의 위치를 동기화 # Synchronize the position of the image view and the 3D view window
        if (res := arr_view_image[EType.Model].SynchronizeWindow(view3d)[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.")
            break

        # 3D 뷰에 높이 맵과 텍스쳐를 로드하여 디스플레이 # Create height map object
        fl3d_ohm = CFL3DObjectHeightMap(arr_image[EType.Model], arr_image[EType.Texture])        
        if (res := view3d.PushObject(fl3d_ohm)).IsFail():
            ErrorPrint(res, "Failed to set image object on the 3D view.")
            break

        view3d.ZoomFit()

        # 이미지뷰에서 레이어를 얻어 온 뒤 텍스트 출력 # Get layers and draw text
        arr_layer = [arr_view_image[i].GetLayer(0) for i in range(2)]
        for layer in arr_layer:
            layer.Clear()
        view3d.GetLayer(0).Clear()

        # 텍스트 출력 위치 # Text coordinates
        position = CFLPoint[Double](0, 0)    
        
		# 아래 함수 DrawTextCanvas는 스크린 좌표를 기준으로 문자열을 뷰어에 출력한다.
        # The function DrawTextCanvas displays a string on the viewer using screen coordinates.
		# 파라미터 순서 : 기준 좌표 Figure 객체 -> 문자열 -> 텍스트 색 -> 텍스트 테두리 색 -> 폰트 크기 -> 실제 크기로 출력 유무 -> 각도 -> 정렬 -> 폰트 이름 -> 텍스트 알파값(불투명도) -> 텍스트 테두리 알파값 (불투명도) -> 폰트 두께 -> 폰트 이탤릭 여부
		# Parameter order: reference coordinate (Figure object) -> text string -> text color -> text outline color -> font size -> render in real-world size (bool) -> angle -> alignment -> font name -> text alpha (opacity) -> text outline alpha (opacity) -> font thickness -> italic font (bool)
        if (res := arr_layer[EType.Model].DrawTextCanvas(position, "Model Image", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text.")
            break

        if (res := arr_layer[EType.Texture].DrawTextCanvas(position, "Texture Image", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text.")
            break

        if (res := view3d.GetLayer(0).DrawTextCanvas(position, "3D View", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text.")
            break
        
		# 3D 뷰와 이미지 뷰를 갱신 # Update image view
        arr_view_image[EType.Model].Invalidate(True)
        arr_view_image[EType.Texture].Invalidate(True)
        view3d.Invalidate(True)

		# 3D 뷰와 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 # Wait until views close
        while (arr_view_image[EType.Model].IsAvailable() and
               arr_view_image[EType.Texture].IsAvailable() and
               view3d.IsAvailable()):
            time.sleep(0.01)
        break
	# End of main function



# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}')


if __name__ == '__main__':
    main()