# test python script must be in same location as aurum_pb2.py

import grpc
from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import time

isTabContentPageOpened = False


# Check if notification test1 page is opened or not.
def CheckTabContentTestStart(stub):
    LaunchAppTest(stub)

    global isTabContentPageOpened
    isTabContentPageOpened = FindTCByInputText(stub, "TabContentTest")
    time.sleep(0.3)
    return isTabContentPageOpened


# Check
def CheckTabContentTest1(stub):
    if not isTabContentPageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button', isShowing=True))
    for elem in res.elements:
        if "OnSelect" in elem.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))
            time.sleep(1)

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="TabContent/TabContentTest01.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='TabContent/TabContentTestExpected01.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckTabContentTestEnd(stub):
    global isTabContentPageOpened
    isTabContentPageOpened = False

    # Return to NUI Gallery page.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Exit Gallery.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='XF86Exit'))
    time.sleep(0.3)
    return True


def runTest(stub, testFunc):
    print("Testing started :", testFunc)
    result = testFunc(stub)
    print("Testing result :", result)
    return True


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = BootstrapStub(channel)
        runTest(stub, CheckTabContentTestStart)
        runTest(stub, CheckTabContentTest1)
        runTest(stub, CheckTabContentTestEnd)


if __name__ == '__main__':
    run()
