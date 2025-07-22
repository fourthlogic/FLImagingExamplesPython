# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

import time

class EType:
    Model = 0
    Texture = 1
    Count = 2

# 메인 함수 // Main function
def main():
	# 이미지 객체 선언 // Declare the image object
    arr_image = [CFLImage() for _ in range(EType.Count)]

	# 이미지 뷰 선언 // Declare the image view
    arr_view_image = [CGUIViewImage() for _ in range(EType.Count)]
    view3d = CGUIView3D()

    res = CResult()

    while True:
        # Load Model image        
        if (res := arr_image[EType.Model].Load("../../ExampleImages/View3D/mountain.flif")).IsFail():
            ErrorPrint(res, "Failed to load the image file.\n")
            break

        # Load Texture image        
        if (res := arr_image[EType.Texture].Load("../../ExampleImages/View3D/mountain_texture.flif")).IsFail():
            ErrorPrint(res, "Failed to load the texture image file.\n")
            break

        # Create model view        
        if (res := arr_view_image[EType.Model].Create(100, 0, 612, 512)).IsFail():
            ErrorPrint(res, "Failed to create the image view.\n")
            break

        # Create texture view        
        if (res := arr_view_image[EType.Texture].Create(612, 0, 1124, 512)).IsFail():
            ErrorPrint(res, "Failed to create the image view.\n")
            break

        # Create 3D view        
        if (res := view3d.Create(1124, 0, 1636, 512)).IsFail():
            ErrorPrint(res, "Failed to create the 3D view.\n")
            break

        b_error = False
        for i in range(EType.Count):            
            if (res := arr_view_image[i].SetImagePtr(arr_image[i])[0]).IsFail():
                ErrorPrint(res, "Failed to set image object on the image view.\n")
                b_error = True
                break

        if b_error:
            break

        # Synchronize views        
        if (res := arr_view_image[EType.Model].SynchronizePointOfView(arr_view_image[EType.Texture])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view\n")
            break

        if (res := arr_view_image[EType.Model].SynchronizeWindow(arr_view_image[EType.Texture])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.\n")
            break

        if (res := arr_view_image[EType.Model].SynchronizeWindow(view3d)[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.\n")
            break

        # Create height map object
        fl3d_ohm = CFL3DObjectHeightMap(arr_image[EType.Model], arr_image[EType.Texture])        
        if (res := view3d.PushObject(fl3d_ohm)).IsFail():
            ErrorPrint(res, "Failed to set image object on the 3D view.\n")
            break

        view3d.ZoomFit()

        # Get layers and draw text
        arr_layer = [arr_view_image[i].GetLayer(0) for i in range(2)]
        for layer in arr_layer:
            layer.Clear()
        view3d.GetLayer(0).Clear()

        position = CFLPoint[Double](0, 0)        
        if (res := arr_layer[EType.Model].DrawTextCanvas(position, "Model Image", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text.\n")
            break

        if (res := arr_layer[EType.Texture].DrawTextCanvas(position, "Texture Image", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text.\n")
            break

        if (res := view3d.GetLayer(0).DrawTextCanvas(position, "3D View", EColor.YELLOW, EColor.BLACK, 30)).IsFail():
            ErrorPrint(res, "Failed to draw text.\n")
            break
        
		# 이미지 뷰를 갱신 // Update image view
        arr_view_image[EType.Model].Invalidate(True)
        arr_view_image[EType.Texture].Invalidate(True)
        view3d.Invalidate(True)

		## 이미지 뷰가 닫히기 전까지 종료하지 않고 대기 // Wait until views close
        while (arr_view_image[EType.Model].IsAvailable() and
               arr_view_image[EType.Texture].IsAvailable() and
               view3d.IsAvailable()):
            time.sleep(0.01)
        break
	# End of main function



# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()