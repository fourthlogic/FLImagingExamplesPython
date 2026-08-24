# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()


# Error 출력 함수 import # Import Error Output Function
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'Common'))

from ErrorPrint import *

# 메인 함수 # Main function
def main():
    
    class EViewList:
        Learn = 0
        ModelBaseFind = 1
        NormalFind = 2
        Count = 3
        
    # 이미지 객체 선언 # Declare the image object
    arrFliImage = [CFLImage() for i in range(EViewList.Count)]

    # 이미지 뷰 선언 # Declare the image view
    arrViewImage = [CGUIViewImage() for i in range(EViewList.Count)]
    arrLayer =  [CGUIViewImageLayer() for i in range(EViewList.Count)]
    arrWcsViewText = [
        'Learn View',
        'Model Based Decoder Result View',
        'Decoder Result View'
    ]

    
    # 이미지 로드 # Loads image
    if (res := arrFliImage[EViewList.Learn].Load('../../ExampleImages/DataMatrix/Learn.flif')).IsFail():
        ErrorPrint(res, 'Failed to load the image file.')
        return

    if (res := arrFliImage[EViewList.ModelBaseFind].Load('../../ExampleImages/DataMatrix/Find.flif')).IsFail():
        ErrorPrint(res, 'Failed to load the image file.')
        return

    if (res := arrFliImage[EViewList.NormalFind].Load('../../ExampleImages/DataMatrix/Find.flif')).IsFail():
        ErrorPrint(res, 'Failed to load the image file.')
        return

    
    # 이미지 뷰 생성 # Create image view
    i32ViewSize = 450
    i32Start = 100

    for i in range(EViewList.Count):        
        i32X = i32ViewSize * i
        i32Y = i32Start

        if (res := arrViewImage[i].Create(i32X + i32Start, i32Y, i32X + i32ViewSize + i32Start, i32Y + i32ViewSize)).IsFail():
            ErrorPrint(res, 'Failed to create the image view.\n')
            break

        # 이미지 뷰에 이미지를 디스플레이 # display the image in the imageview
        if (res := arrViewImage[i].SetImagePtr(arrFliImage[i])[0]).IsFail():
            ErrorPrint(res, 'Failed to set image object on the image view.\n')
            break

        # 화면에 출력하기 위해 Image View에서 레이어 0번을 얻어옴 # Obtain layer 0 number from image view for display
        # 이 객체는 이미지 뷰에 속해있기 때문에 따로 해제할 필요가 없음 # This object belongs to an image view and does not need to be released separately
        arrLayer[i] = arrViewImage[i].GetLayer(0)

        if (res := arrLayer[i].DrawTextCanvas(CFLPoint[Double](0, 0), arrWcsViewText[i], EColor.YELLOW, EColor.BLUE, 20)).IsFail():
            ErrorPrint(res, 'Failed to draw figure\n')
            break

    # 이미지 뷰의 시점을 동기화 한다 # Synchronize the viewpoints of the all image views. 
    if (res := arrViewImage[EViewList.ModelBaseFind].SynchronizePointOfView(arrViewImage[EViewList.NormalFind])[0]).IsFail():
        ErrorPrint(res, 'Failed to set image object on the image view.\n')
        return
    
    # Model Based Data Matrix Decoder 객체 생성 # Create Model Based Data Matrix Decoder object
    modelBasedDataMatrixDecoder = CModelBasedDataMatrixDecoder()

    # 학습 이미지 설정 # Sets the learn image.
    modelBasedDataMatrixDecoder.SetLearnImage(arrFliImage[EViewList.Learn])
    # 코드 색상 설정 # Sets the code color.
    modelBasedDataMatrixDecoder.SetColorMode(EDataCodeColor.WhiteOnBlack)

    # 학습 동작 # Learn
    if (res := modelBasedDataMatrixDecoder.Learn()).IsFail():
        ErrorPrint(res, 'Failed to learn data matrix decoder.')
        return

    # 동작 이미지 설정 # Set source image
    modelBasedDataMatrixDecoder.SetSourceImage(arrFliImage[EViewList.ModelBaseFind])
    # 디코딩 결과 개수 설정 # Sets the number of decoding results.
    modelBasedDataMatrixDecoder.SetDetectingCount(EDataCodeDecoderDetectingCount.All)
    modelBasedDataMatrixDecoder.SetMaximumDetectingCount(3)

    # 학습 이미지 기준 탐색 각도 설정 # Sets the search angle relative to the learn data.
    modelBasedDataMatrixDecoder.SetAngleTolerance(30)

    # 동작 # Execute
    if(res := modelBasedDataMatrixDecoder.Execute().IsFail()):
        ErrorPrint(res, 'Failed to execute data matrix decoder.')
        return


    # Learn 동작 결과를 얻어온다 # Gets the result of the learn result.
    datamatrixLearnInfo = CModelBasedDataMatrixDecoder.CDataMatrixLearnInformation()
    modelBasedDataMatrixDecoder.GetLearnResult(datamatrixLearnInfo)
    Console.WriteLine('\n[Model Based Learn Result]')

    flqLearnedCodeRegion = datamatrixLearnInfo.decodedDataMatrixInformation.pFlqRegion
    flsLearnedCode = datamatrixLearnInfo.decodedDataMatrixInformation.pStrCode

    # Learn 동작 결과 영역 및 코드 출력 # Outputs the regions and codes from the learn operation results.
    arrLayer[EViewList.Learn].DrawFigureImage(flqLearnedCodeRegion, EColor.LIME, 2)
    arrLayer[EViewList.Learn].DrawTextImage(flqLearnedCodeRegion.flpPoints[3], flsLearnedCode, EColor.CYAN, EColor.BLACK, 20, False, flqLearnedCodeRegion.flpPoints[3].GetAngle(flqLearnedCodeRegion.flpPoints[2]))

    Console.WriteLine('Code Size : {} x {}'.format(datamatrixLearnInfo.i32Rows, datamatrixLearnInfo.i32Cols))

    flsCodeColor = ''

    if(datamatrixLearnInfo.eColor == EDataCodeColor.BlackOnWhite):
        flsCodeColor = 'Black On White'
    elif(datamatrixLearnInfo.eColor == EDataCodeColor.WhiteOnBlack):
        flsCodeColor = 'White On Black'

    Console.WriteLine('Code Color : {}'.format(flsCodeColor))

    if datamatrixLearnInfo.bFlip == True:
        flsFlip = 'Yes'
    else:
        flsFlip = 'No'

    Console.WriteLine('Flip : {}'.format(flsFlip))
    Console.WriteLine('Code : {}'.format(flsLearnedCode))

    # Data Matrix Decoder 결과 개수를 얻는다. # Gets the number of results from the Data Matrix decoder.
    i64Results = modelBasedDataMatrixDecoder.GetResultCount()

    Console.WriteLine('\n[Model Based Decoded Result]')
    
    for i in range(i64Results):
        flqDecodedCodeRegion = CFLQuad[Double]()
        flsDecodedCode = StringBuilder()

        # Data Matrix Decoder 결과들 중 Data Region 을 얻어옴 # Gets the Data Region from the results of the Data Matrix decoder.
        if(res := modelBasedDataMatrixDecoder.GetResultDataRegion(i, flqDecodedCodeRegion)[0]).IsFail():
            ErrorPrint(res, 'Failed to get data region from the data matrix decoder object.')
            continue

        # Data Matrix Decoder 결과들 중 Decoded String 을 얻어옴 # Gets the decoded string from the results of the Data Matrix decoder.
        if(res := modelBasedDataMatrixDecoder.GetResultDecodedString(i, flsDecodedCode)[0]).IsFail():
            ErrorPrint(res, 'Failed to get decoded string from the data matrix decoder object.')
            continue

        Console.WriteLine('No. {} Code : {}'.format(i, flsDecodedCode))

        arrLayer[EViewList.ModelBaseFind].DrawFigureImage(flqDecodedCodeRegion, EColor.LIME, 2)
        arrLayer[EViewList.ModelBaseFind].DrawTextImage(flqDecodedCodeRegion.flpPoints[3], flsDecodedCode.ToString(), EColor.CYAN, EColor.BLACK, 16, False, flqDecodedCodeRegion.flpPoints[3].GetAngle(flqDecodedCodeRegion.flpPoints[2]))

    # 일반 Data Matrix Decoder 결과와 비교하기 위한 동작 # Operation for comparing with standard Data Matrix decoder results.

    # Data Matrix Decoder 객체 생성 # Create Data Matrix Decoder object
    datamatrixDecoder = CDataMatrixDecoder()

    # 동작 이미지 설정 # Set source image
    datamatrixDecoder.SetSourceImage(arrFliImage[EViewList.NormalFind])
    # 코드 색상 설정 # Sets the code color.
    datamatrixDecoder.SetColorMode(EDataCodeColor.WhiteOnBlack)
    # 디코딩 결과 개수 설정 # Sets the number of decoding results.
    datamatrixDecoder.SetDetectingCount(EDataCodeDecoderDetectingCount.All)
    datamatrixDecoder.SetMaximumDetectingCount(3)

    # 동작 # Execute
    if(res := datamatrixDecoder.Execute()).IsFail():
        ErrorPrint(res, 'Failed to execute data matrix decoder.')
        return

    # Data Matrix Decoder 결과 개수를 얻는다. # Gets the number of results from the Data Matrix decoder.
    i64Results = datamatrixDecoder.GetResultCount()

    Console.WriteLine('\n[Normal Decoded Result]')
    for i in range(i64Results):
        flqDecodedCodeRegion = CFLQuad[Double]()
        flsDecodedCode = StringBuilder()
        
        # Data Matrix Decoder 결과들 중 Data Region 을 얻어옴 # Gets the Data Region from the results of the Data Matrix decoder.
        if(res := datamatrixDecoder.GetResultDataRegion(i, flqDecodedCodeRegion)[0]).IsFail():
            ErrorPrint(res, 'Failed to get data region from the data matrix decoder object.')
            continue

        # Data Matrix Decoder 결과들 중 Decoded String 을 얻어옴 # Gets the decoded string from the results of the Data Matrix decoder.
        if(res := datamatrixDecoder.GetResultDecodedString(i, flsDecodedCode)[0]).IsFail():
            ErrorPrint(res, 'Failed to get decoded string from the data matrix decoder object.')
            continue
        
        Console.WriteLine('No. {} Code : {}'.format(i, flsDecodedCode))

        arrLayer[EViewList.NormalFind].DrawFigureImage(flqDecodedCodeRegion, EColor.LIME, 2)
        arrLayer[EViewList.NormalFind].DrawTextImage(flqDecodedCodeRegion.flpPoints[3], flsDecodedCode.ToString(), EColor.CYAN, EColor.BLACK, 16, False, flqDecodedCodeRegion.flpPoints[3].GetAngle(flqDecodedCodeRegion.flpPoints[2]))

     # 이미지 뷰를 갱신 합니다. # Update the image view.
    for i in range(EViewList.Count):     
        arrViewImage[i].Invalidate()
        
    bAvailable = True

    while bAvailable:
        for i in range(EViewList.Count):
            bAvailable &= arrViewImage[i].IsAvailable()

        CThreadUtilities.Sleep(1)
        
    for i in range(i32ExampleCount):
        arrViewImage[i].Destroy()

        
if __name__ == '__main__':
    main()