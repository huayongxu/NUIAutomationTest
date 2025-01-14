# test python script must be in same location as aurum_pb2.py

from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import grpc
import time

isNavigatorPageOpened = False

# Check if Navigator test page is opened or not.
def CheckNavigatorTestStart(stub):
    global isNavigatorPageOpened
    isNavigatorPageOpened = FindTCByInputText(stub, "NavigatorTest3")
    return isNavigatorPageOpened


# Check the first Navigator page.
def CheckNavigatorTest31(stub):
    if not isNavigatorPageOpened:
        return False

    # Move focus to the button "Click to show Navigator".
    for i in range(3):
        stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Down'))

    # Press button to the first page.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(1)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Navigator/NavigatorTest31.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Navigator/NavigatorTestExpected31.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check the second Navigator page.
def CheckNavigatorTest32(stub):
    if not isNavigatorPageOpened:
        return False

    # Move focus to the button "Click to next".
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Left'))
    time.sleep(0.3)

    # Move focus to the button "Click to insert a page below".
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Right'))
    time.sleep(0.3)

    # Press button.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Navigator/NavigatorTest32.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Navigator/NavigatorTestExpected32.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check the created Navigator page.
def CheckNavigatorTest33(stub):
    if not isNavigatorPageOpened:
        return False

    # Move focus to the button "Click to next".
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Right'))
    time.sleep(0.3)

    # Press button.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="Navigator/NavigatorTest33.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='Navigator/NavigatorTestExpected33.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check if AppBar exit normally.
def CheckNavigatorTestEnd(stub):
    # Press back icon.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Press to NUI Gallery page.
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
        runTest(stub, LaunchAppTest)
        runTest(stub, CheckNavigatorTestStart)
        runTest(stub, CheckNavigatorTest31)
        runTest(stub, CheckNavigatorTest32)
        runTest(stub, CheckNavigatorTest33)
        runTest(stub, CheckNavigatorTestEnd)


if __name__ == '__main__':                                         
    run()
