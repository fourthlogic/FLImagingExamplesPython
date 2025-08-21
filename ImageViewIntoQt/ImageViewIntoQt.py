# FLImagingClrPy 선언 # Declare FLImagingClrPy
from FLImagingClrPy import *

# You must call the following function once
# before using any features of the FLImaging(R) library
CLibraryUtilities.Initialize()

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QPushButton, QTextEdit
from PyQt5.QtCore import Qt, QTimer


class ImageViewIntoQt(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ImageViewIntoQt")
        self.resize(740, 500)

        # 메인 레이아웃 생성 # Create the main layout
        self.layoutMain = QHBoxLayout()
        self.setLayout(self.layoutMain)

        # 뷰의 프레임 생성 # Create the view frame
        self.frameView = QFrame()
        self.frameView.setFrameShape(QFrame.StyledPanel)
        self.layoutMain.addWidget(self.frameView, stretch=4)

        # 컨트롤들의 프레임 생성 # Create a frame for the controls
        self.frameControls = QFrame()
        self.frameControls.setFrameShape(QFrame.StyledPanel)
        self.layoutMain.addWidget(self.frameControls, stretch=1)
        
        # 컨트롤들의 레이아웃 생성 # Create a layout for the controls
        self.layoutControls = QVBoxLayout()
        self.frameControls.setLayout(self.layoutControls)

        # 라벨 생성 # Create a label
        self.labelTitle = QLabel("RectFigure Object")
        self.labelTitle.setAlignment(Qt.AlignCenter)
        self.layoutControls.addWidget(self.labelTitle)

        # 생성 버튼 생성 # Create a 'Create' button
        self.buttonCreate = QPushButton("Create")
        self.buttonCreate.clicked.connect(self.OnCreateButtonClick)
        self.layoutControls.addWidget(self.buttonCreate)

        # 제거 버튼 생성 # Create a 'Pop Front' button
        self.buttonPopFront = QPushButton("Pop Front")
        self.buttonPopFront.clicked.connect(self.OnPopFrontButtonClick)
        self.layoutControls.addWidget(self.buttonPopFront)

        # 인포메이션 텍스트 에디트 생성 # Create an information text editor
        self.textInfo = QTextEdit()
        self.textInfo.setReadOnly(True)
        self.layoutControls.addWidget(self.textInfo)

        # 이미지 뷰 생성 # Create an image view
        self.m_viewImage = CGUIViewImage()
        if (res := self.m_viewImage.CreateAndFitParent(int(self.frameView.winId()))).IsFail():
            ErrorPrint(res, 'Failed to create the image view.')

        # 타이머 시작
        self.timerUpdate = QTimer()
        self.timerUpdate.timeout.connect(self.UpdateControls)
        self.timerUpdate.start(100)

    # 컨트롤들의 활성화 여부를 업데이트하는 함수
    # Function to update the enable/disable state of the controls
    def UpdateControls(self):
        enabled = False

        if self.m_viewImage and self.m_viewImage.IsAvailable():
            if self.m_viewImage.GetFigureObjectCount() > 0:
                enabled = True

        self.buttonPopFront.setEnabled(enabled)

    # Create 버튼 클릭에 대한 이벤트 처리기
    # Event handler for Create button click
    def OnCreateButtonClick(self):
         while True:
            # 1. 뷰 유효성 체크
            # 1. Check if the image view is valid
            if not self.m_viewImage.IsAvailable():
                return

            # 2. 캔버스 좌표 얻기
            # 2. Get canvas coordinate region
            flrlCanvas = self.m_viewImage.GetClientRectCanvasRegion()

            # 3. 이미지 좌표계로 변환
            # 3. Convert to image coordinate space
            flrdImage = self.m_viewImage.ConvertCanvasCoordToImageCoord(flrlCanvas) # CFLRect[Double]

            # 4. 사각형 크기 계산
            # 4. Calculate the size of the rectangle
            f64Width = flrdImage.GetWidth() / 10.0
            f64Height = flrdImage.GetHeight() / 10.0
            f64Size = Math.Min(f64Width, f64Height)

            # 5. 중심 좌표 계산
            # 5. Calculate the center point
            flpdCenter = CFLPoint[Double](0.0, 0.0)
            flrdImage.GetCenter(flpdCenter)

            # 6. 중심 기준 사각형 생성
            # 6. Create a rectangle centered at the center point
            flrFigure = CFLRect[Double](
                flpdCenter.x - f64Size,
                flpdCenter.y - f64Size,
                flpdCenter.x + f64Size,
                flpdCenter.y + f64Size
            )

            # 7. 이미지 뷰에 Figure 추가
            # 7. Add the rectangle figure to the image view
            self.m_viewImage.PushBackFigureObject(flrFigure, EAvailableFigureContextMenu.All)
            break

    # PopFront 버튼 클릭에 대한 이벤트 처리기
    # Event handler for Pop Front button click
    def OnPopFrontButtonClick(self):
        flFigure = None
        strFigureInfo = "Error"

        if self.m_viewImage.IsAvailable():
            # PopFrontFigureObject()로 Figure 꺼내기
            # Pop the first (front-most) figure from the image view
            flFigure = self.m_viewImage.PopFrontFigureObject()
    
            if flFigure is not None:
                # Figure를 문자열로 변환
                # Convert the figure object to a string representation
                strFigure = CFigureUtilities.ConvertFigureObjectToString(flFigure)
                strFigureInfo = strFigure
                
        # textInfo에 문자열을 출력
        # Display text in the textInfo
        self.textInfo.setPlainText(strFigureInfo)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageViewIntoQt()
    window.show()
    sys.exit(app.exec_()) 


# 에러 출력 함수 # Error printing function
def ErrorPrint(res: CResult, string: str):
	if len(string) > 1:
		print(string)

	print(f'Error code : {res.GetResultCode()}\nError name : {res.GetString()}\n')
