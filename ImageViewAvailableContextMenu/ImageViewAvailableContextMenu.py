# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

import clr
import sys
import time
import random

def main():
    # 이미지 뷰 선언 # Declare the image view
    viewImage = [CGUIViewImage(), CGUIViewImage()]

    while True:
        res = CResult()

        # 이미지 뷰 생성 # Create image views        
        if (res := viewImage[0].Create(300, 0, 300 + 520, 430)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        if (res := viewImage[1].Create(300 + 520, 0, 300 + 520 * 2, 430)).IsFail():
            ErrorPrint(res, "Failed to create the image view.")
            break

        # 뷰의 시점 동기화 # Synchronize the view point        
        if (res := viewImage[0].SynchronizePointOfView(viewImage[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view")
            break

        # 윈도우 위치 동기화 # Synchronize window positions        
        if (res := viewImage[0].SynchronizeWindow(viewImage[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window")
            break

        # 첫 번째 이미지 뷰에 모든 컨텍스트 메뉴 비활성화 설정
        # Disable all context menu options on the first image view
        menuFlag = getattr(EAvailableViewImageContextMenu, "None")
        viewImage[0].SetAvailableViewImageContextMenu(menuFlag)
        
        # 이미지뷰의 0번 레이어 가져오기
        # Get the 0th layer of the image view
        layer = viewImage[0].GetLayer(0)

        # 기존에 Layer 에 그려진 도형들을 삭제
        # Clear any existing drawings on the layer
        layer.Clear()

        strInformation = "RIGHT BUTTON CLICK ON MOUSE AND SEE THE CONTEXT MENU"
        strInformation2 = "Option : EAvailableViewImageContextMenu.None"
        
		# 아래 함수 DrawTextCanvas는 Screen좌표를 기준으로 문자열을 뷰어에 출력한다.
        # Draw the position text to canvas
		# 색상 파라미터를 EColor.TRANSPARENCY 로 넣어주면 투명색으로 처리된다.
		# 파라미터 순서 : 레이어 -> 기준 좌표 Figure 객체 -> 문자열 -> 폰트 색 -> 면 색 -> 폰트 크기 -> 실제 크기 유무 -> 각도 -> 얼라인 -> 폰트 이름 -> 폰트 알파값(불투명도) -> 면 알파값 (불투명도) -> 폰트 두께 -> 폰트 이텔릭
		# Parameter order: layer -> reference coordinate Figure object -> string -> font color -> Area color -> font size -> actual size -> angle -> Align -> Font Name -> Font Alpha Value (Opaqueness) -> Cotton Alpha Value (Opaqueness) -> Font Thickness -> Font Italic
        layer.DrawTextCanvas(CFLPoint[Double](10, 10), strInformation, EColor.LIME, EColor.BLACK, 15)
        layer.DrawTextCanvas(CFLPoint[Double](10, 30), strInformation2, EColor.CYAN, EColor.BLACK, 15)

        # 두 번째 이미지 뷰에서 특정 메뉴 비활성화
        # Disable specific context menu options on the second image view
        ctxMenuOption = int(EAvailableViewImageContextMenu.All) & ~int(
            int(EAvailableViewImageContextMenu.Load) |
            int(EAvailableViewImageContextMenu.ClearFile) |
            int(EAvailableViewImageContextMenu.Save) |
            int(EAvailableViewImageContextMenu.CreateImage)
        )

        # 두 번째 이미지 뷰에 컨텍스트 메뉴 설정
        # Apply the customized context menu to the second image view
        viewImage[1].SetAvailableViewImageContextMenu(EAvailableViewImageContextMenu(ctxMenuOption, True))
        
        # 이미지뷰의 0번 레이어 가져오기
        # Get the 0th layer of the image view
        layer = viewImage[1].GetLayer(0)

        # 기존에 Layer 에 그려진 도형들을 삭제
        # Clear any existing drawings on the layer
        layer.Clear()

        strInformation = "RIGHT BUTTON CLICK ON MOUSE AND SEE THE CONTEXT MENU"
        strInformation2 = ("Option: EAvailableViewImageContextMenu.All & "
                           "           ~(EAvailableViewImageContextMenu.Load | "
                           "              EAvailableViewImageContextMenu.ClearFile | "
                           "              EAvailableViewImageContextMenu.Save | "
                           "              EAvailableViewImageContextMenu.CreateImage)")
        
		# 아래 함수 DrawTextCanvas는 Screen좌표를 기준으로 문자열을 뷰어에 출력한다.
        # Draw the position text to canvas
		# 색상 파라미터를 EColor.TRANSPARENCY 로 넣어주면 투명색으로 처리된다.
		# 파라미터 순서 : 레이어 -> 기준 좌표 Figure 객체 -> 문자열 -> 폰트 색 -> 면 색 -> 폰트 크기 -> 실제 크기 유무 -> 각도 -> 얼라인 -> 폰트 이름 -> 폰트 알파값(불투명도) -> 면 알파값 (불투명도) -> 폰트 두께 -> 폰트 이텔릭
		# Parameter order: layer -> reference coordinate Figure object -> string -> font color -> Area color -> font size -> actual size -> angle -> Align -> Font Name -> Font Alpha Value (Opaqueness) -> Cotton Alpha Value (Opaqueness) -> Font Thickness -> Font Italic
        layer.DrawTextCanvas(CFLPoint[Double](10, 10), strInformation, EColor.LIME, EColor.BLACK, 15)
        layer.DrawTextCanvas(CFLPoint[Double](10, 30), strInformation2, EColor.CYAN, EColor.BLACK, 15)
        
        # 이미지뷰를 갱신
        # Refresh the image view
        for i in range(2):
            viewImage[i].Invalidate()

        # 이미지 뷰가 종료될 때까지 대기 
        # Wait until image view is closed
        while viewImage[0].IsAvailable():
            time.sleep(0.01)

        break


# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}')


if __name__ == '__main__':
    main()