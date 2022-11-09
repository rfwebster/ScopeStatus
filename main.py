import sys
from PyQt4 import QtCore
from PyQt4.QtCore import QObject, QThread, pyqtSignal, pyqtSlot
from PyQt4.QtGui import *
from PyQt4.QtTest import QTest
# from PyQt4.QtWidgets import QApplication, QMainWindow

import ui.palette
from ui.Scope import Ui_MainWindow

OFFLINE = False

try:
    from PyJEM import detector
    from PyJEM import TEM3
    detector.get_attached_detector()
except ImportError:
    from PyJEM.offline import detector
    from PyJEM.offline import TEM3
    detector.get_attached_detector()
    OFFLINE = True

UPDATE = 2000


class Microscope:
    def __init__(self):
        self.stage = TEM3.Stage3()
        self.EOS = TEM3.EOS3()
        self.apt = TEM3.Apt3()
        self.det = TEM3.Detector3()
        self.def3 = TEM3.Def3()
        self.feg = TEM3.FEG3()
        self.gun = TEM3.GUN3()
        self.HT = TEM3.HT3()

        # Miroscope Detector/ Aperture Configuration:
        # 0:CL1, 1:CL2, 2:OL(OL Upper), 3:HC(OL Lower), 4:SA, 5:ENT, 6:HX, 7:BF, 8:AUX1, 9:AUX2, 10:AUX3, 11:AUX4

        self.aperture_list = [0, 1, 3, 4, 6, 7]
        self.apt_list = [["Out", "150um", "100um", "70um", "10um"],  # CL1Apt
                         ["Out", "50um", "40um", "30um", "20um"],  # CL2Apt
                         [],  # OLUApt
                         ["Out", "120um", "60um", "20um", "5um"],  # OLLApt
                         ["Out", "100um", "50um", "20um", "10um"],  # SAApt
                         [],  #  ENT
                         ["Out", "500um", "200um"],  # HXApt
                         ["Out", "5-2.5mm", "3mm", "2mm", "1mm"]]  # BFApt
        self.apt_size_list = [0,  # CL1Apt
                              0,  # CL2Apt
                              [],  # OLUApt
                              0,  # OLLApt
                              0,  # SAApt
                              [],  # ENT
                              0,  # HXApt
                              0]  # BFApt


        # 0 – 1 SEI (Second electron detector)
        # 2 EDS (EDS detector)
        # 3 BI-PRISM (electron beam Bi-prism)
        # 4 DFI-EF (Scanning dark field electron detector for FEF)
        # 5 TVCAM-U (TV camera [Diff chamber])
        # 6 SSCAM-U (Slow scan camera [Diff chamber])
        # 7 FARADAY-CAGE (Faraday cage)
        # 8 BS (Beam stopper)
        # 9 HRD (High resolution electron diffraction holder)
        # 10 DFI-U (Scanning dark field electron detector [Observation chamber])
        # 11 BFI-U (Scanning bright field electron detector [Observation chamber])
        # 12 SCR-F (Small screen)
        # 13 SCR-L (Large screen)
        # 14 DFI-B (Scanning dark field electron detector [below camera chamber])
        # 15 BFI-B (Scanning bright field electron detector [below camera chamber])
        # 16 SSCAM-B (Slow scan camera [below camera chamber])
        # 17 TVCAM-B (TV camera [below camera chamber])
        # 18 EELS (Electron energy loss spectrometer)
        # 19 TVCAM-GIF (TV camera [GATAN energy filter])
        # 20 SSCAM-GIF (Slow scan camera [GATAN energy filter])
        # 21 BEI-TOPO 22 BEI-COMPO 23 SEI-TOPO 24 SEI-COMPO

        self.detector_list = [8, 10, 12, 13, 15]
        self.det_list = [[], [], [], [], [], [], [], [],
                         ["Out", "In"],  # Beam Stop
                         [],
                         ["Out", "In"],  # DF
                         [],
                         ["Retracted", "Inserted"],  # Small Screen
                         ["Raised", "Lowered"],  # large Screen
                         [],
                         ["Out", "In"]  # BF
                         ]
        self.det_pos_list = [[], [], [], [], [], [], [], [],
                             0,  # Beam Stop
                             [],
                             0,  # DF
                             [],
                             0,  # Small Screen
                             0,  # large Screen
                             [],
                             0  # BF
                             ]

        self.CL1_Apt_Size = 0
        self.CL2_Apt_Size = 0
        self.OL_Apt_Size = 0
        self.SA_Apt_Size = 0
        self.BF_Apt_Size = 0
        self.HX_Apt_Size = 0

        self.lscreenpos = 0
        self.sscreenpos = 0
        self.ADFpos = 0
        self.BFpos = 0
        self.BSpos = 0

        self.BV = 0

        self.HT_Value = self.HT.GetHtValue()
        self.Emission_Value = self.gun.GetEmissionCurrentValue()
        self.A1_Value = self.gun.GetAnode1CurrentValue()
        self.A2_Value = self.gun.GetAnode2CurrentValue()

        self.Sample_Insert = 0

        # Get Mag status
        self.Mag_Text = "Unknown"
        self.mod_text = "Unknown"
        self.smo_text = "Unknown"
        self.probe_text = "Unknown"
        self.spt_text = "Unknown"
        try:
            self.CL_text = "Unknown"
            self.print(self.CL_text)
        except:
            self.CL_text = "Unknown"

        if OFFLINE:
            self.set_cond()


    def update(self):
        self.BV = self.feg.GetBeamValve()
        if OFFLINE:
            self.CL1_Apt_Size = self.apt.GetSize(0)
            self.CL2_Apt_Size = self.apt.GetSize(1)
            self.OL_Apt_Size = self.apt.GetSize(3)
            self.SA_Apt_Size = self.apt.GetSize(4)
            self.HX_Apt_Size = self.apt.GetSize(6)
            self.BF_Apt_Size = self.apt.GetSize(7)
        else:
            # 0:CL1, 1:CL2, 2:OL(OL Upper), 3:HC(OL Lower), 4:SA, 5:ENT, 6:HX, 7:BF, 8:AUX1, 9:AUX2, 10:AUX3, 11:AUX4
            self.CL1_Apt_Size = self.apt.GetExpSize(0)
            self.CL2_Apt_Size = self.apt.GetExpSize(1)
            self.OL_Apt_Size = self.apt.GetExpSize(3)
            self.SA_Apt_Size = self.apt.GetExpSize(4)
            self.HX_Apt_Size = self.apt.GetExpSize(6)
            self.BF_Apt_Size = self.apt.GetExpSize(7)

        self.apt_size_list = [self.CL1_Apt_Size,  # CL1Apt
                              self.CL2_Apt_Size,  # CL2Apt
                              [],  # OLUApt
                              self.OL_Apt_Size,  # OLLApt
                              self.SA_Apt_Size,  # SAApt
                              [],  # ??
                              self.HX_Apt_Size,  # HXApt
                              self.BF_Apt_Size]  # BFApt

        self.HT_Value = self.HT.GetHtValue()
        self.Emission_Value = self.gun.GetEmissionCurrentValue()
        self.A1_Value = self.gun.GetAnode1CurrentValue()
        self.A2_Value = self.gun.GetAnode2CurrentValue()

        self.lscreenpos = self.det.GetPosition(14)
        self.sscreenpos = self.det.GetPosition(13)
        self.ADFpos = self.det.GetPosition(10)
        self.BFpos = self.det.GetPosition(15)
        self.BSpos = self.det.GetPosition(8)
        self.det_pos_list[8] = self.BSpos  # Beam Stop
        self.det_pos_list[10] = self.ADFpos  # DF
        self.det_pos_list[12] = self.sscreenpos  # Small Screen
        self.det_pos_list[13] = self.lscreenpos  # large Screen
        self.det_pos_list[15] = self.BFpos  # BF

        self.Sample_Insert = TEM.stage.GetHolderStts()

        # Get Mag status
        if self.EOS.GetTemStemMode():
            self.Mag_Text = str(TEM.EOS.GetStemCamValue())
        else:
            self.Mag_Text = str(TEM.EOS.GetMagValue()[0]) + str(TEM.EOS.GetMagValue()[1])
        self.mod_text = "TEM" if TEM.EOS.GetTemStemMode() == 0 else "STEM" if TEM.EOS.GetTemStemMode() == 1 else "Unknown"
        self.smo_text = str(TEM.EOS.GetFunctionMode()[1])
        self.probe_text = TEM.EOS.GetProbeMode()
        if self.EOS.GetTemStemMode():
            self.spt_Text = str(TEM.EOS.GetSpotSize())
        else:
            self.spt_Text = str(TEM.EOS.GetSpotSize())

        try:
            self.CL_text = str(TEM.EOS.GetStemCamValue()[0] * 10)
            print(self.CL_text)
        except:
            self.CL_text = "Unknown"

    def set_cond(self):
        self.feg.SetBeamValve(1)
        self.HT.SetHtValue(300)

        self.apt.SelectKind(2)
        self.apt.SetSize(1)

        self.det.SetPosition(14, 1)
        self.det.SetPosition(15, 1)

        self.EOS.SelectTemStem(1)
        self.EOS.SelectFunctionMode(2)

        self.EOS.SetSelector(11)
        self.EOS.SelectSpotSize(2)

class UpdaterThread(QObject):
    signalExample = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    @pyqtSlot()
    def update(self):
        while True:
            TEM.update()
            print("Update")
            QTest.qWait(UPDATE)
            self.signalExample.emit(1)


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setPalette(ui.palette.PALETTE)
        # self._update()
        # self.statusBar().showMessage("Connected")

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
                          self.BFDet
                          ]

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

        if TEM.Emission_Value:
            self.Bkg.setPixmap(QPixmap("ui/bkg-valveclosed.png"))
            if TEM.BV:
                self.Bkg.setPixmap(QPixmap("ui/bkg-fscreendown.png"))
                if TEM.sscreenpos == 0:
                    self.Bkg.setPixmap(QPixmap("ui/bkg-lscreendown.png"))
                    if TEM.lscreenpos == 0:
                        self.Bkg.setPixmap(QPixmap("ui/bkg-beam.png"))
        else:
            self.Bkg.setPixmap(QPixmap("ui/bkg.png"))

        # Gun Status
        self.HTLCD.display(TEM.HT_Value)
        self.EmissionLCD.display(TEM.Emission_Value)
        self.A1LCD.display(TEM.A1_Value)
        self.A2LCD.display(TEM.A2_Value)

        self.BVButton.setText("Open" if TEM.BV else "Closed")
        if TEM.BV:
            self.BV.setHidden(True)
        else:
            self.BV.setHidden(False)

        self.SampleButton.setText("Inserted" if TEM.Sample_Insert else "Retracted")
        if TEM.Sample_Insert:
            self.Sample.setHidden(False)
        else:
            self.Sample.setHidden(True)

        i = 0
        for icon in self.det_icons:
            if icon is not None:
                if TEM.det_pos_list[i]:
                    icon.setHidden(False)
                else:
                    print(i)
                    icon.setHidden(True)
            i += 1

        self.BSButton.setText(TEM.det_list[8][TEM.BSpos])

        self.DFButton.setText(TEM.det_list[10][TEM.ADFpos])
        self.BFButton.setText(TEM.det_list[15][TEM.BFpos])

        self.FScreenButton.setText(TEM.det_list[12][TEM.sscreenpos])
        self.LScreenButton.setText(TEM.det_list[13][TEM.lscreenpos])
        # TODO: inconsistant names!!
        # Get Aperture Positions
        # GetExpSize:
        # 0:CL1, 1:CL2, 2:OL(OL Upper), 3:HC(OL Lower), 4:SA, 5:ENT, 6:HX, 7:BF, 8:AUX1, 9:AUX2, 10:AUX3, 11:AUX4
        i = 0
        for icon in self.apt_icons:
            if icon is not None:
                if TEM.apt_size_list[i]:
                    icon.setHidden(False)
                else:
                    icon.setHidden(True)
            i += 1

        self.CL1Button.setText(TEM.apt_list[0][TEM.CL1_Apt_Size])  # GetExpSize? difference?
        self.CL2Button.setText(TEM.apt_list[1][TEM.CL2_Apt_Size])
        self.HXButton.setText(TEM.apt_list[6][TEM.HX_Apt_Size])
        self.OLButton.setText(TEM.apt_list[3][TEM.OL_Apt_Size])
        self.SAButton.setText(TEM.apt_list[4][TEM.SA_Apt_Size])
        self.BFAButton.setText(TEM.apt_list[7][TEM.BF_Apt_Size])

        self.ModeLabel.setText(TEM.mod_text)
        self.subModeLAbel.setText(TEM.smo_text)
        self.MagLabel.setText(TEM.Mag_Text)
        self.SpotLabel.setText(TEM.spt_text)
        self.CLLabel.setText(TEM.CL_text)


if __name__ == "__main__":
    TEM = Microscope()
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = Window()
    win.show()
    sys.exit(app.exec())
