# test python script must be in same location as aurum_pb2.py

import grpc
from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import time

isPaginationPageOpened = False


# Check if pagination test page is opened or not.
def CheckPaginationTestStart(stub):
    if not LaunchAppTest(stub):
        return False

    global isPaginationPageOpened
    isPaginationPageOpened = FindTCByInputText(stub, "PaginationTest1")
    time.sleep(0.3)
    return isPaginationPageOpened


# Check right
def CheckPaginationTest1(stub):
    if not isPaginationPageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button'))
    for elem in res.elements:
        if "Right" in elem.text:
            for i in range(4):
                stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))
                time.sleep(0.3)

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="Pagination/PaginationTest1.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='Pagination/PaginationTestExpected1.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check left
def CheckPaginationTest2(stub):
    if not isPaginationPageOpened:
        return False

    res = stub.findElements(ReqFindElements(widgetType='Button'))
    for elem in res.elements:
        if "Left" in elem.text:
            for i in range(2):
                stub.click(ReqClick(type="ELEMENTID", elementId=elem.elementId))
                time.sleep(0.3)

            # Take screenshot
            screenShort = ReadScreenShotFile(stub, fileName="Pagination/PaginationTest2.png")
            if screenShort is None:
                return False

            # Read image file expected
            expectedScreenShot = ReadImageFile(fileName='Pagination/PaginationTestExpected2.png')
            if expectedScreenShot is None:
                return False

            # Check ssim
            return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


def CheckPaginationTestEnd(stub):
    global isPaginationPageOpened
    isPaginationPageOpened = False

    # Return to NUI Gallery page.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(1)

    # Exit Gallery.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='XF86Exit'))
    time.sleep(2)
    return True


def runTest(stub, testFunc):
    print("Testing started :", testFunc)
    result = testFunc(stub)
    print("Testing result :", result)
    return True


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = BootstrapStub(channel)
        time.sleep(1)
        runTest(stub, CheckPaginationTestStart)
        runTest(stub, CheckPaginationTest1)
        runTest(stub, CheckPaginationTest2)
        runTest(stub, CheckPaginationTestEnd)


if __name__ == '__main__':
    run()
