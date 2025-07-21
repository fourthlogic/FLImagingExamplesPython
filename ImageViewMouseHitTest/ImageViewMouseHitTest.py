# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

import clr
import time
import threading

class CMessageReceiver(CFLBase):
    def __init__(self):
        super().__init__()
        CBroadcastManager.Subscribe(self)

    def __del__(self):
        CBroadcastManager.Unsubscribe(self)

    def OnReceiveBroadcast(self, pMessage):
        if pMessage is None:
            return

        if pMessage.GetChannel() == EGUIBroadcast.ViewImage_PostMouseMove:
            msgMouseEvent = pMessage if isinstance(pMessage, CBroadcastMessage_GUI_ViewImage_MouseEvent) else None
            if msgMouseEvent is None:
                return

            viewImage = msgMouseEvent.GetCaller()
            if viewImage is None:
                return

            eHitArea = viewImage.GetHitArea()

            if Convert.ToInt64(eHitArea) == 0:
                strHitArea = "None"
            else:
                strHitArea = "Mouse is "
                str = "on "
                if eHitArea.HasFlag(EGUIViewImageHitArea.MiniMap):
                    strHitArea += str + "MiniMap"
                    str = " and "
                if eHitArea.HasFlag(EGUIViewImageHitArea.MiniMapDisplayingArea):
                    strHitArea += str + "MiniMapDisplayingArea"
                    str = " and "
                if eHitArea.HasFlag(EGUIViewImageHitArea.ThumbnailView):
                    strHitArea += str + "ThumbnailView"
                    str = " and "
                if eHitArea.HasFlag(EGUIViewImageHitArea.ThumbnailViewTop):
                    strHitArea += str + "ThumbnailViewTop"
                    str = " and "
                if eHitArea.HasFlag(EGUIViewImageHitArea.Figure):
                    strHitArea += str + "Figure"
                    str = " and "
                if eHitArea.HasFlag(EGUIViewImageHitArea.MultiFigures):
                    strHitArea += str + "MultiFigures"
                    str = " and "
                if eHitArea.HasFlag(EGUIViewImageHitArea.ImageFigure):
                    strHitArea += str + "ImageROI"
                    str = " and "
                if eHitArea.HasFlag(EGUIViewImageHitArea.StatusBar):
                    strHitArea += str + "StatusBar"
                    str = " and "
                if eHitArea.HasFlag(EGUIViewImageHitArea.PageIndex):
                    strHitArea += str + "PageIndex"
                    str = " and "
                if eHitArea.HasFlag(EGUIViewImageHitArea.PrevPageArrow):
                    strHitArea += str + "PrevPageArrow"
                    str = " and "
                if eHitArea.HasFlag(EGUIViewImageHitArea.NextPageArrow):
                    strHitArea += str + "NextPageArrow"
                    str = " and "

                strHitArea += "."

            layer = viewImage.GetLayer(0)
            layer.Clear()
            layer.DrawTextCanvas(CFLPoint[float](80, 10), strHitArea, EColor.LIME, EColor.BLACK)
            viewImage.Invalidate()


def errorPrint(cResult, str):
    if len(str) > 1:
        print(str)

    print(f"Error code : {cResult.GetResultCode()}\nError name : {cResult.GetString()}\n")
    input("Press any key to continue...")


def main():
    msgReceiver = CMessageReceiver()
    fliImage = CFLImage()
    viewImage = CGUIViewImage()

    while True:
        res = fliImage.Load("../../ExampleImages/PagePooling/Multiple File_Min.flif")
        if res.IsFail():
            errorPrint(res, "Failed to load the image file.\n")
            break

        res = viewImage.Create(300, 0, 300 + 520, 430)
        if res.IsFail():
            errorPrint(res, "Failed to create the image view.\n")
            break

        res = viewImage.SetImagePtr(fliImage)
        if isinstance(res, tuple):
            res = res[0]
        if res.IsFail():
            errorPrint(res, "Failed to set image object on the image view.\n")
            break

        res = viewImage.ZoomFit()
        if res.IsFail():
            errorPrint(res, "Failed to zoom fit\n")
            break

        flrlCanvas = viewImage.GetClientRectCanvasRegion()
        flrdImage = viewImage.ConvertCanvasCoordToImageCoord(flrlCanvas)

        f64Width = flrdImage.GetWidth() / 10.0
        f64Height = flrdImage.GetHeight() / 10.0
        f64Size = min(f64Width, f64Height)

        flpdCenter = CFLPoint[float](0, 0)
        flrdImage.GetCenter(flpdCenter)

        flrdFigureShape = CFLRect[float](
            flpdCenter.x - f64Size,
            flpdCenter.y - f64Size,
            flpdCenter.x + f64Size,
            flpdCenter.y + f64Size
        )
        
        menuFlag = getattr(EAvailableFigureContextMenu, "None")
        viewImage.PushBackFigureObject(flrdFigureShape, menuFlag)
        viewImage.Invalidate(True)
        viewImage.SetFixThumbnailView(True)

        while viewImage.IsAvailable():
            time.sleep(0.01)

        break


# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()