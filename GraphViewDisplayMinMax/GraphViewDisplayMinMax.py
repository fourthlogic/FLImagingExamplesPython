# FLImagingClrPy 선언 // Declare FLImagingClrPy
from FLImagingClrPy import *

import clr
import sys
import time
import random

def main():
    # 그래프 뷰 선언
    arrViewGraph = [CGUIViewGraph(), CGUIViewGraph(), CGUIViewGraph()]

    res = CResult()
    
    while True:
        if (res := arrViewGraph[0].Create(100, 0, 100 + 440, 340)).IsFail():
            ErrorPrint(res, "Failed to create the graph view.\n")
            break

        if (res := arrViewGraph[1].Create(100 + 440 * 1, 0, 100 + 440 * 2, 340)).IsFail():
            ErrorPrint(res, "Failed to create the graph view.\n")
            break

        if (res := arrViewGraph[2].Create(100 + 440 * 2, 0, 100 + 440 * 3, 340)).IsFail():
            ErrorPrint(res, "Failed to create the graph view.\n")
            break

        # 윈도우 동기화
        if (res := arrViewGraph[0].SynchronizeWindow(arrViewGraph[1])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.\n")
            break

        if (res := arrViewGraph[1].SynchronizeWindow(arrViewGraph[2])[0]).IsFail():
            ErrorPrint(res, "Failed to synchronize window.\n")
            break

        # 차트 3개 생성
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
            r = rand.randint(0, 255)
            g = rand.randint(0, 255)
            b = rand.randint(0, 255)
            eColor = EColor(((r | (g << 8) | (b << 16)) & 0xFFFFFFFF), True)

            strName = f"Chart {k}"
            
            for view in arrViewGraph:
                view.Plot(arrF64DataX, arrF64DataY, i32DataCount, EChartType.Line, eColor, strName)

            time.sleep(0.005)

        # 전체 차트에 Y축 최대/최소값 표시
        eIndicateType = int(EViewGraphIndicateType.Value) | int(EViewGraphIndicateType.Name) | int(EViewGraphIndicateType.Arrow)
        arrViewGraph[0].IndicateEntireChart(EViewGraphExtrema.MinY, EViewGraphIndicateType(eIndicateType, True))
        arrViewGraph[0].IndicateEntireChart(EViewGraphExtrema.MaxY, EViewGraphIndicateType(eIndicateType, True))

        # 모든 차트 각각 X, Y 최대/최소
        arrViewGraph[1].IndicateEveryIndividualChart(EViewGraphExtrema.MinX, EViewGraphIndicateType.All)
        arrViewGraph[1].IndicateEveryIndividualChart(EViewGraphExtrema.MaxX, EViewGraphIndicateType.All)
        arrViewGraph[1].IndicateEveryIndividualChart(EViewGraphExtrema.MinY, EViewGraphIndicateType.All)
        arrViewGraph[1].IndicateEveryIndividualChart(EViewGraphExtrema.MaxY, EViewGraphIndicateType.All)

        # 특정 차트(인덱스 2)에 표시
        i32ChartIndex = 2
        indicateType = getattr(EViewGraphIndicateType, "None")
        arrViewGraph[2].Indicate(i32ChartIndex, EViewGraphExtrema.MinX, indicateType)
        arrViewGraph[2].Indicate(i32ChartIndex, EViewGraphExtrema.MaxX, indicateType)
        arrViewGraph[2].Indicate(i32ChartIndex, EViewGraphExtrema.MinY, EViewGraphIndicateType.All)
        arrViewGraph[2].Indicate(i32ChartIndex, EViewGraphExtrema.MaxY, EViewGraphIndicateType.All)

        # 십자선 비활성화
        for view in arrViewGraph:
            view.ShowCrosshair(False)
            view.ZoomFit()

        # 뷰가 닫힐 때까지 대기
        while all(view.IsAvailable() for view in arrViewGraph):
            CThreadUtilities.Sleep(1)

        break



# 에러 출력 함수 // Error printing function
def ErrorPrint(res, str):
	if len(str) > 1:
		print(str)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')


if __name__ == '__main__':
    main()