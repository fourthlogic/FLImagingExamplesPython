# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

CLibraryUtilities.Initialize()

import time

def main():
    # 이미지 뷰 선언 # Declare image view
    viewImage = [CGUIViewImage(), CGUIViewImage(), CGUIViewImage()]
    res = CResult()

    while True:
        # 이미지 뷰 생성 # Create image view
        if (res := viewImage[0].Create(0, 0, 400, 440)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        if (res := viewImage[1].Create(400, 0, 800, 440)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        if (res := viewImage[2].Create(800, 0, 1200, 440)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break
        
		# 윈도우의 위치 동기화 # Synchronize the positions of windows
        viewImage[0].SynchronizeWindow(viewImage[1])
        viewImage[0].SynchronizeWindow(viewImage[2])
        
		# 3D Object 파일 로드 # Load 3D Object file
        pObj3D = CFL3DObject()
        pObj3D.Load("../../ExampleImages/ProjectionUtilities3D/Cylinder.step")

        fliFinal = [CFLImage(), CFLImage(), CFLImage()]
        fliRes = CFLImage()
        figureText = CFLFigureText[Int32]()
        
        # CProjectionUtilities3D 객체 생성 
        # Create CProjectionUtilities3D object
        pu = CProjectionUtilities3D()

        # CProjectionUtilities3D 객체에 3D Object 를 추가
        # Add 3D Object to CProjectionUtilities3D object
        pu.PushBack3DObject(pObj3D)
        # 결과 이미지 크기 설정 
        # Set result image size
        pu.SetResultImageSize(400, 400)
        # 결과 이미지 배경 색상 설정 
        # Set background color of result image
        pu.SetBackgroundColorOfResultImage(21, 21, 21)
        
        # 1-1. 특정 시점의 투영 이미지 얻기 
        # 1-1. Get projection image from specific viewpoint
        # 카메라 시점 설정 # Set camera viewpoint
        camSet1 = CFL3DCamera()
        camSet1.SetProjectionType(E3DCameraProjectionType.Perspective)
        camSet1.SetPosition(CFLPoint3[Single](-1.41, -317.67, 280.92))
        camSet1.SetDirection(CFLPoint3[Single](0.01, 0.87, -0.50))
        camSet1.SetDirectionUp(CFLPoint3[Single](-0.01, 0.50, 0.87))
        camSet1.SetAngleOfViewY(45)
        camSet1.SetTarget(CFLPoint3[Single](2.13, -59.49, 132.75))
        camSet1.SetNearZ(271.84)
        camSet1.SetFarZ(459.30)
        
        # 카메라 설정 # Set camera
        pu.SetCamera(camSet1)
        # 프로젝션 수행 # Perform projection
        res = pu.Execute()
        # 결과 이미지 얻기 # Get result image
        res = pu.GetResult(fliRes)
        # 결과 이미지에 정보 텍스트 추가 
        # Add information text to result image
        figureText.Set(CFLPoint[Int32](10, 10), "1. Projection(Camera Set 1)", int(EColor.YELLOW), int(EColor.BLACK), 20, False, 0.0, EFigureTextAlignment.LEFT_TOP, "", 1, 1, EFigureTextFontWeight.BOLD, False)
        fliRes.PushBackFigure(CFigureUtilities.ConvertFigureObjectToString(figureText))
        # 최종 이미지에 투영 결과 이미지 복사 
        # Copy projection result image to final image
        fliFinal[0].Assign(fliRes)
        
        # 1-2. 특정 시점의 투영 이미지 얻기 
        # 1-2. Get projection image from another specific viewpoint
        # 카메라 시점 설정 # Set camera viewpoint
        camSet2 = CFL3DCamera()
        camSet2.SetProjectionType(E3DCameraProjectionType.Perspective)
        camSet2.SetPosition(CFLPoint3[Single](-80.38, 97.35, 341.92))
        camSet2.SetDirection(CFLPoint3[Single](0.42, -0.27, -0.86))
        camSet2.SetDirectionUp(CFLPoint3[Single](0.77, 0.61, 0.19))
        camSet2.SetAngleOfViewY(45)
        camSet2.SetTarget(CFLPoint3[Single](-5.45, 49.05, 189.72))
        camSet2.SetNearZ(148.33)
        camSet2.SetFarZ(390.77)
        
        # 카메라 설정 # Set camera
        pu.SetCamera(camSet2)
        # 프로젝션 수행 # Perform projection
        res = pu.Execute()
        # 결과 이미지 얻기 # Get result image
        res = pu.GetResult(fliRes)
        # 결과 이미지에 정보 텍스트 추가 
        # Add information text to result image
        figureText.Set(CFLPoint[Int32](10, 10), "1. Projection(Camera Set 2)", int(EColor.YELLOW), int(EColor.BLACK), 20, False, 0.0, EFigureTextAlignment.LEFT_TOP, "", 1, 1, EFigureTextFontWeight.BOLD, False)
        fliRes.PushBackFigure(CFigureUtilities.ConvertFigureObjectToString(figureText))
        # 최종 이미지에 투영 결과 이미지 추가 
        # Add projection result image to final image
        fliFinal[0].PushBackPage(fliRes)
        
        # 결과 이미지를 이미지 뷰에 로드 
        # Load result image into image view
        viewImage[0].SetImagePtr(fliFinal[0])
        viewImage[0].SetFixThumbnailView(True)
        viewImage[0].ShowImageMiniMap(False)
        viewImage[0].ShowPageIndex(False)
        
		# 2. 카메라 1과 카메라 2 사이의 시점에 대한 프로젝션 
		# 2. Projection for viewpoints between Camera 1 and Camera 2		
        pu.SetTopologyType(ETopologyType3D.Wireframe)
        for i in range(11):
            # 카메라 시점 설정 # Set camera viewpoint
            f32T = i * 0.1
            camInterpolation = CFL3DCamera()
            CFL3DCamera.Interpolate(camSet1, camSet2, f32T, camInterpolation)
            # 카메라 설정 # Set camera
            pu.SetCamera(camInterpolation)
            # 프로젝션 수행 # Perform projection
            res = pu.Execute()
            # 결과 이미지 얻기 # Get result image
            res = pu.GetResult(fliRes)
            
            # 결과 이미지에 정보 텍스트 추가 
            # Add information text to result image
            text = f"2. Projection(Camera Interpolation T={f32T:.1f})"
            figureText.Set(CFLPoint[Int32](10, 10), text, int(EColor.YELLOW), int(EColor.BLACK), 17, False, 0.0, EFigureTextAlignment.LEFT_TOP, "", 1, 1, EFigureTextFontWeight.SEMIBOLD, False)
            fliRes.PushBackFigure(CFigureUtilities.ConvertFigureObjectToString(figureText))
            
            # 최종 이미지에 투영 결과 이미지 추가 
            # Add projection result image to final image
            if i == 0:
                fliFinal[1].Assign(fliRes)
            else:
                fliFinal[1].PushBackPage(fliRes)
                
        # 결과 이미지를 이미지 뷰에 로드 
        # Load result image into image view
        viewImage[1].SetImagePtr(fliFinal[1])
        viewImage[1].SetFixThumbnailView(True)
        viewImage[1].ShowImageMiniMap(False)
        viewImage[1].ShowPageIndex(False)

        
		# 3. Zoom Fit 시점의 이미지 얻기 
		# 3. Get image at Zoom Fit viewpoint
        # 포인트 클라우드 형태로 디스플레이하도록 토폴로지 설정 # Set topology to display as a point cloud
        pu.SetTopologyType(ETopologyType3D.PointCloud)
        # 각 포인트의 크기를 5로 설정 # Set the size of each point to 5
        pu.SetPointSize(5.0)
        # 설정한 이미지 안에 3D 객체가 꽉 차도록 시점 설정 
        # Adjust the camera view so the 3D object fits entirely within the image
        pu.ZoomFitCamera()
        # 프로젝션 수행 # Perform projection
        res = pu.Execute()
        # 결과 이미지 얻기 # Get result image
        res = pu.GetResult(fliFinal[2])
        # 결과 이미지에 정보 텍스트 추가 
        # Add information text to result image
        figureText.Set(CFLPoint[Int32](10, 10), "3. Projection(ZoomFit)", int(EColor.YELLOW), int(EColor.BLACK), 20, False, 0.0, EFigureTextAlignment.LEFT_TOP, "", 1, 1, EFigureTextFontWeight.BOLD, False)
        fliFinal[2].PushBackFigure(CFigureUtilities.ConvertFigureObjectToString(figureText))
        
        # 결과 이미지를 이미지 뷰에 로드 
        # Load result image into image view
        viewImage[2].SetImagePtr(fliFinal[2])
        viewImage[2].SetFixThumbnailView(True)
        viewImage[2].ShowImageMiniMap(False)
        viewImage[2].ShowPageIndex(False)
        
        # 이미지 뷰들이 종료될 때까지 대기
        # Wait until image views are closed
        while viewImage[0].IsAvailable() and viewImage[1].IsAvailable() and viewImage[2].IsAvailable():
            time.sleep(0.01)

        break


# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}')


if __name__ == '__main__':
    main()