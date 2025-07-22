# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

import clr
import sys
import time
import random

def main():
    # 이미지 뷰 선언 // Declare the image view
    viewImage = [CGUIViewImage(), CGUIViewImage()]

    while True:
        res = CResult()

        # 이미지 뷰 생성 // Create image views        
        if (res := viewImage[0].Create(300, 0, 300 + 520, 430)).IsFail():
            ErrorPrint(res, "Failed to create the image view.\n")
            break

        if (res := viewImage[1].Create(300 + 520, 0, 300 + 520 * 2, 430)).IsFail():
            ErrorPrint(res, "Failed to create the image view.\n")
            break

        # 뷰의 시점 동기화 // Synchronize the view point        
        if (res := viewImage[0].SynchronizePointOfView(viewImage[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize view\n")
            break

        # 윈도우 위치 동기화 // Synchronize window positions        
        if (res := viewImage[0].SynchronizeWindow(viewImage[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window\n")
            break

        # 첫 번째 이미지 뷰에 컨텍스트 메뉴 비활성화 설정
        menuFlag = getattr(EAvailableViewImageContextMenu, "None")
        viewImage[0].SetAvailableViewImageContextMenu(menuFlag)

        layer = viewImage[0].GetLayer(0)
        layer.Clear()

        strInformation = "RIGHT BUTTON CLICK ON MOUSE AND SEE THE CONTEXT MENU\n"
        strInformation2 = "Option : EAvailableViewImageContextMenu.None"

        layer.DrawTextCanvas(CFLPoint[Double](10, 10), strInformation, EColor.LIME, EColor.BLACK, 15)
        layer.DrawTextCanvas(CFLPoint[Double](10, 30), strInformation2, EColor.CYAN, EColor.BLACK, 15)

        # 두 번째 이미지 뷰에서 특정 메뉴 비활성화
        ctxMenuOption = int(EAvailableViewImageContextMenu.All) & ~int(
            int(EAvailableViewImageContextMenu.Load) |
            int(EAvailableViewImageContextMenu.ClearFile) |
            int(EAvailableViewImageContextMenu.Save) |
            int(EAvailableViewImageContextMenu.CreateImage)
        )
        viewImage[1].SetAvailableViewImageContextMenu(EAvailableViewImageContextMenu(ctxMenuOption, True))

        layer = viewImage[1].GetLayer(0)
        layer.Clear()

        strInformation = "RIGHT BUTTON CLICK ON MOUSE AND SEE THE CONTEXT MENU\n"
        strInformation2 = ("Option: EAvailableViewImageContextMenu.All & \n"
                           "           ~(EAvailableViewImageContextMenu.Load | \n"
                           "              EAvailableViewImageContextMenu.ClearFile | \n"
                           "              EAvailableViewImageContextMenu.Save | \n"
                           "              EAvailableViewImageContextMenu.CreateImage)")

        layer.DrawTextCanvas(CFLPoint[Double](10, 10), strInformation, EColor.LIME, EColor.BLACK, 15)
        layer.DrawTextCanvas(CFLPoint[Double](10, 30), strInformation2, EColor.CYAN, EColor.BLACK, 15)

        for i in range(2):
            viewImage[i].Invalidate()

        # 이미지 뷰가 종료될 때까지 대기 // Wait until image view is closed
        while viewImage[0].IsAvailable():
            time.sleep(0.01)

        break


# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()