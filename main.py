import sys
from PyQt5.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtTest import QTest
from PyQt5.QtWidgets import QApplication, QMainWindow

import ui.palette
from ui.Scope import Ui_MainWindow


try:
    from PyJEM import detector
    from PyJEM import TEM3
except ImportError:
    from PyJEM.offline import detector
    from PyJEM.offline import TEM3

POLLING = 2000

stage = TEM3.Stage3()
EOS = TEM3.EOS3()
apt = TEM3.Apt3()
det = TEM3.Detector3()
def3 = TEM3.Def3()
feg = TEM3.FEG3()
gun = TEM3.GUN3()
HT = TEM3.HT3()

aperture_list = [0, 1, 3, 4, 6, 7]
apt_list = [["Out", "150um", "100um", "70um", "10um"],  # CL1Apt
            ["Out", "50um", "40um", "30um", "20um"],   # CL2Apt
            [],  # OLUApt
            ["Out", "120um", "60um", "20um", "5um"],  # OLLApt
            ["Out", "100um", "50um", "20um", "10um"],  # SAApt
            [],  # ??
            ["Out", "500um", "200um"],  # HXApt
            ["Out", "5-2.5mm", "3mm", "2mm", "1mm"]]  # BFApt

detector_list = [8, 10, 12, 13, 15]
det_list = [[], [], [], [], [], [], [], [],
            ["Out", "In"], [],
            ["Retracted", "Inserted"], [],
            ["Retracted", "Inserted"],
            ["Retracted", "Inserted"], [],
            ["Retracted", "Inserted"]]


class UpdaterThread(QObject):
    signalExample = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    @pyqtSlot()
    def update(self):
        while True:
            pos = stage.GetPos()
            self.signalExample.emit(1)
            QTest.qWait(POLLING)


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setPalette(ui.palette.PALETTE)
        #self._update()
        #self.statusBar().showMessage("Connected")
        apt.SelectKind(2)
        print(apt.kind)
        apt.SetSize(1)

        self.apt_icons = [self.CL1Apt,
                       self.CL2Apt,
                       None,
                       self.OLApt,
                       self.SAApt,
                       None,
                       self.HXApt,
                       self.BFApt]
        self.det_icons = [None, None, None, None, None, None, None, None,
                          self.BS, None,
                          self.DFDet, None,
                          self.FScreen,
                          self.LScreen, None,
                          self.BFDet]

        self.updater = UpdaterThread()
        self.updaterThread = QThread()
        self.updaterThread.started.connect(self.updater.update)
        self.updater.signalExample.connect(self._update)
        self.updater.moveToThread(self.updaterThread)
        self.updaterThread.start()


    ######################################################################################
    #
    # UI Buttons amd functions etc
    #
    ######################################################################################
    def _update(self):
        # self._get_current_position()
        # QTest.qWait(1000)
        # Background

        if gun.emission_value:
            self.Bkg.setPixmap(QPixmap("ui/bkg-valveclosed.png"))
            if feg.GetBeamValve() == 1:
                self.Bkg.setPixmap(QPixmap("ui/bkg-fscreendown.png"))
                if det.GetPosition(12) == 0:
                    self.Bkg.setPixmap(QPixmap("ui/bkg-lscreendown.png"))
                    if det.GetPosition(13) == 0:
                        self.Bkg.setPixmap(QPixmap("ui/bkg-beam.png"))
        else:
            self.Bkg.setPixmap(QPixmap("ui/bkg.png"))

        # Gun Status
        self.HTLCD.display(HT.GetHtValue())
        self.EmissionLCD.display(gun.emission_value)
        self.A1LCD.display(gun.a1_value)
        self.A2LCD.display(gun.a2_value)

        self.BVButton.setText("Open" if feg.GetBeamValve() else "Closed")
        if feg.GetBeamValve():
            self.BV.setHidden(True)
        else:
            self.BV.setHidden(False)

        self.SampleButton.setText("Inserted" if stage.GetHolderStts() else "Retracted")
        if stage.GetHolderStts():
            self.Sample.setHidden(False)
        else:
            self.Sample.setHidden(True)

        i = 0
        for icon in self.det_icons:
            if icon is not None:
                if det.GetPosition(i):
                    icon.setHidden(False)
                else:
                    icon.setHidden(True)
            i += 1

        self.BSButton.setText(det_list[8][det.GetPosition(8)])

        self.DFButton.setText(det_list[10][det.GetPosition(10)])
        self.FScreenButton.setText(det_list[12][det.GetPosition(12)])
        self.LScreenButton.setText(det_list[13][det.GetPosition(13)])
        self.BFButton.setText(det_list[15][det.GetPosition(15)])
        # Get Aperture Positions
        # GetExpSize:
        # 0:CL1, 1:CL2, 2:OL(OL Upper), 3:HC(OL Lower), 4:SA, 5:ENT, 6:HX, 7:BF, 8:AUX1, 9:AUX2, 10:AUX3, 11:AUX4
        i = 0
        for icon in self.apt_icons:
            if icon is not None:
                if apt.GetSize(i):
                    icon.setHidden(False)
                else:
                    icon.setHidden(True)
            i += 1

        self.CL1Button.setText(apt_list[0][apt.GetSize(0)])
        self.CL2Button.setText(apt_list[1][apt.GetSize(1)])
        self.HXButton.setText(apt_list[6][apt.GetSize(6)])
        self.OLButton.setText(apt_list[3][apt.GetSize(3)])
        self.SAButton.setText(apt_list[4][apt.GetSize(4)])
        self.BFAButton.setText(apt_list[7][apt.GetSize(7)])

        # Get Mag status
        mag_text = str(EOS.GetMagValue()[0])+str(EOS.GetMagValue()[1])
        mod_text = "TEM" if EOS.GetTemStemMode() == 0 else "STEM" if EOS.GetTemStemMode() == 1 else "Unknown"
        smo_text = str(EOS.GetFunctionMode()[1])
        probe_text = EOS.GetProbeMode()
        spt_text = probe_text[1] + "-" + str(EOS.GetSpotSize())
        try:
            cl_text = str(EOS.GetStemCamValue()[0]*10)
            print(cl_text)
        except:
            cl_text = "Unknown"
        self.ModeLabel.setText(mod_text)
        self.subModeLAbel.setText(smo_text)
        self.MagLabel.setText(mag_text)
        self.SpotLabel.setText(spt_text)
        self.CLLabel.setText(cl_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = Window()
    win.show()
    sys.exit(app.exec())
