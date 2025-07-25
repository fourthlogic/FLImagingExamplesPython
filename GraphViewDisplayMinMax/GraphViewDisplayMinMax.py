# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

CLibraryUtilities.Initialize()

import clr
import sys
import time
import random

def main():
    # 그래프 뷰 선언
    # Declare graph views
    arrViewGraph = [CGUIViewGraph(), CGUIViewGraph(), CGUIViewGraph()]

    res = CResult()
    
    while True:
        # 첫 번째 그래프 뷰 생성
        # Create the first graph view
        if (res := arrViewGraph[0].Create(100, 0, 100 + 440, 340)).IsFail():
            ErrorPrint(res, "Failed to create the graph view.")
            break

        # 두 번째 그래프 뷰 생성
        # Create the second graph view
        if (res := arrViewGraph[1].Create(100 + 440 * 1, 0, 100 + 440 * 2, 340)).IsFail():
            ErrorPrint(res, "Failed to create the graph view.")
            break

        # 세 번째 그래프 뷰 생성
        # Create the third graph view
        if (res := arrViewGraph[2].Create(100 + 440 * 2, 0, 100 + 440 * 3, 340)).IsFail():
            ErrorPrint(res, "Failed to create the graph view.")
            break

        # 윈도우 동기화
        # Synchronize window positions between views
        if (res := arrViewGraph[0].SynchronizeWindow(arrViewGraph[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.")
            break

        if (res := arrViewGraph[1].SynchronizeWindow(arrViewGraph[2])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.")
            break

        # 차트 3개 생성
        # Generate and plot 3 charts
        for k in range(3):
            rand = random.Random(k * 2 + int(time.time() * 1000))
            i32DataCount = 100
            arrF64DataX = Array[Double]([0.0] * i32DataCount)
            arrF64DataY = Array[Double]([0.0] * i32DataCount)

            f64PrevX = 0
            f64PrevY = 0

            for i in range(i32DataCount):
                arrF64DataX[i] = f64PrevX + ((rand.randint(0, 99)) / 10)
                if rand.randint(0, 1) != 0:
                    arrF64DataY[i] = f64PrevY + ((rand.randint(0, 99)) / 10)
                else:
                    arrF64DataY[i] = f64PrevY - ((rand.randint(0, 99)) / 10)

                f64PrevX = arrF64DataX[i]
                f64PrevY = arrF64DataY[i]

            # EColor 무작위 RGB
            # Generate random RGB color for chart
            r = rand.randint(0, 255)
            g = rand.randint(0, 255)
            b = rand.randint(0, 255)
            eColor = EColor(((r | (g << 8) | (b << 16)) & 0xFFFFFFFF), True)

            strName = f"Chart {k}"

            # 모든 그래프 뷰에 동일 차트 플롯
            # Plot the same chart on all views
            for view in arrViewGraph:
                view.Plot(arrF64DataX, arrF64DataY, i32DataCount, EChartType.Line, eColor, strName)

            # 잠시 대기
            # Short delay between plots
            time.sleep(0.005)

        # 전체 차트에 Y축 최대/최소값 표시
        # Indicate global min/max Y values across all charts
        eIndicateType = int(EViewGraphIndicateType.Value) | int(EViewGraphIndicateType.Name) | int(EViewGraphIndicateType.Arrow)
        arrViewGraph[0].IndicateEntireChart(EViewGraphExtrema.MinY, EViewGraphIndicateType(eIndicateType, True))
        arrViewGraph[0].IndicateEntireChart(EViewGraphExtrema.MaxY, EViewGraphIndicateType(eIndicateType, True))

        # 모든 차트 각각 X, Y 최대/최소
        # Indicate individual min/max X and Y for each chart
        arrViewGraph[1].IndicateEveryIndividualChart(EViewGraphExtrema.MinX, EViewGraphIndicateType.All)
        arrViewGraph[1].IndicateEveryIndividualChart(EViewGraphExtrema.MaxX, EViewGraphIndicateType.All)
        arrViewGraph[1].IndicateEveryIndividualChart(EViewGraphExtrema.MinY, EViewGraphIndicateType.All)
        arrViewGraph[1].IndicateEveryIndividualChart(EViewGraphExtrema.MaxY, EViewGraphIndicateType.All)

        # 특정 차트(인덱스 2)에 표시
        # Indicate only on specific chart (index 2)
        i32ChartIndex = 2
        indicateType = getattr(EViewGraphIndicateType, "None")
        arrViewGraph[2].Indicate(i32ChartIndex, EViewGraphExtrema.MinX, indicateType)
        arrViewGraph[2].Indicate(i32ChartIndex, EViewGraphExtrema.MaxX, indicateType)
        arrViewGraph[2].Indicate(i32ChartIndex, EViewGraphExtrema.MinY, EViewGraphIndicateType.All)
        arrViewGraph[2].Indicate(i32ChartIndex, EViewGraphExtrema.MaxY, EViewGraphIndicateType.All)

        # 십자선 비활성화 및 ZoomFit
        # Disable crosshair and apply ZoomFit
        for view in arrViewGraph:
            view.ShowCrosshair(False)
            view.ZoomFit()

        # 뷰가 닫힐 때까지 대기
        # Wait until all views are closed
        while all(view.IsAvailable() for view in arrViewGraph):
            CThreadUtilities.Sleep(1)

        break




# 에러 출력 함수 # Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}')


if __name__ == '__main__':
    main()