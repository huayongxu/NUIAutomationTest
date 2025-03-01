# test python script must be in same location as aurum_pb2.py

from aurum_pb2 import *
from aurum_pb2_grpc import BootstrapStub
from NUIGalleryTestUtils import *
import grpc
import time

isAlertDialogOpened = False

# Check if Alert Dialog is opened or not.
def CheckAlertDialogTestStart(stub):
    if not LaunchAppTest(stub):
        return False

    global isAlertDialogOpened
    isAlertDialogOpened = FindTCByInputText(stub, "AlertDialogTest2")
    time.sleep(0.3)
    return isAlertDialogOpened


# Check the first Dialog page.
def CheckAlertDialogTest21(stub):
    if isAlertDialogOpened == False:
        return False

    # Move focus to the button "Click to show Dialog".
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Down'))

    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Down'))
    time.sleep(0.3)

    # Press button to show a dialog.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

    # Take screen shot.
    screenShort = ReadScreenShotFile(stub, fileName="AlertDialog/AlertDialogTest21.png")
    if screenShort is None:
        return False

    # Read image file expected.
    expectedScreenShot = ReadImageFile(fileName='AlertDialog/AlertDialogTestExpected21.png')
    if expectedScreenShot is None:
        return False

    # Check ssim.
    return CheckSSIM(answerImge=expectedScreenShot, testTargetImage=screenShort)


# Check if AlertDialog exit normally.
def CheckAlertDialogTestEnd(stub):
    # Click Button 'Exit'.
    bts = stub.findElements(ReqFindElements(widgetType='Button', isShowing=True))
    for bt in bts.elements:
        if 'Exit' in bt.text:
            stub.click(ReqClick(type="ELEMENTID", elementId=bt.elementId))
            stub.click(ReqClick(type="ELEMENTID", elementId=bt.elementId))
            time.sleep(0.3)

    # Move focus to the back button of DialogPage launcher page.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Up'))

    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Up'))
    time.sleep(0.3)

    # Press to NUI Gallery page.
    stub.sendKey(ReqKey(type='XF86', actionType='STROKE', XF86keyCode='Return'))
    time.sleep(0.3)

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
        runTest(stub, CheckAlertDialogTestStart)
        runTest(stub, CheckAlertDialogTest21)
        runTest(stub, CheckAlertDialogTestEnd)


if __name__ == '__main__':                                         
    run()
