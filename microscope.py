try:
    _online = True
    from PyJEM import detector
    from PyJEM import TEM3
    print(detector.get_attached_detector())
except ImportError:
    _online = False
    from PyJEM.offline import detector
    from PyJEM.offline import TEM3

stage = TEM3.Stage3()
EOS = TEM3.EOS3()
apt = TEM3.Apt3()
det = TEM3.Detector3()
def3 = TEM3.Def3()
feg = TEM3.FEG3()
gun = TEM3.GUN3()
HT = TEM3.HT3()

# for offline testing:
if not _online:
    HT.SetHtValue(300) # turn off on microsocpe!
    gun.SetFilamentVal(3) # test use the filament, on FEG doesnt work
    # beam valve
    feg.SetBeamValve(1)
    # insert detectors
    det.SetPosition(10,1) # ADF
    det.SetPosition(15,1) # BF
    det.SetPosition(8,1)  # BS
    det.SetPosition(12,1) # FScreen
    det.SetPosition(13,1) # LScreen

    # select mode
    EOS.SelectTemStem(0)
    EOS.SelectFunctionMode(1)
    EOS.SetSelector(36)

    # insert an aperture
    apt.SelectKind(3)
    apt.SetSize(2)


# CL1_Apt = {
#     "Index" : The index used by PyJEM to call the aperture/detector
#     "Name" : A human readable name for the aperture/detector
#     "Size" : A list of sizes available
#     "Image" : the image to be shown on the ui
#     "Xpos"  : the x position of the labels
#     "Ypos"  : the y position of the labels
# }

"""
Aperture Indexes:
0:CL1, 1:CL2, 2:OL(OL Upper), 3:HC(OL Lower), 4:SA, 5:ENT, 
6:HX, 7:BF, 8:AUX1, 9:AUX2, 10:AUX3, 11:AUX4
"""

CL1_Apt = {
    "Index" : 0,
    "Name" : "CL1",
    "Size" : ["Out", "150um", "100um", "70um", "10um"],
    "Image" : "ui/apt.png",
    "Xpos"  : 155,
    "Ypos"  : 100,
}

CL2_Apt = {
    "Index" : 1,
    "Name" : "CL2",
    "Size" : ["Out", "50um", "40um", "30um", "20um"],
    "Image" : "ui/apt.png",
    "Xpos"  : 155,
    "Ypos"  : 150,
}

OL_Apt = {
    "Index" : 3,
    "Name" : "OL",
    "Size" : ["Out", "120um", "60um", "20um", "5um"],
    "Image" : "ui/apt.png",
    "Xpos"  : 155,
    "Ypos"  : 290,
}

SA_Apt = {
    "Index" : 4,
    "Name" : "SA",
    "Size" : ["Out", "100um", "50um", "20um", "10um"],
    "Image" : "ui/apt.png",
    "Xpos"  : 155,
    "Ypos"  : 330,
}

HX_Apt = {
    "Index" : 6,
    "Name" : "HX",
    "Size" : ["Out", "500um", "200um"],
    "Image" : "ui/apt.png",
    "Xpos"  : 155,
    "Ypos"  : 200,
}

BF_Apt = {
    "Index" : 7,
    "Name" : "BF",
    "Size" : ["Out", "5-2.5mm", "3mm", "2mm", "1mm"],
    "Image" : "ui/apt.png",
    "Xpos"  : 155,
    "Ypos"  : 600,
}

aperture_list = [CL1_Apt, CL2_Apt, OL_Apt, SA_Apt, HX_Apt, BF_Apt]

"""
Detector Configurations:
1:SEI, 2:EDS, 3:BI-PRISM, 4:DFI-EF, 5:TVCAM-U, 6:SSCAM-U, 7:FARADAY-CAGE, 8:BS, 9:HRD, 
10:DFI-U, 11:BFI-U, 12:SCR-F, 13:SCR-L, 14:DFI-B, 15:BFI-B, 16:SSCAM-B,17:TVCAM-B, 18:EELS, 19:TVCAM-GIF, 
20:SSCAM-GIF, 21:BEI-TOPO, 22:BEI-COMPO, 23:SEI-TOPO, 24:SEI-COMPO
"""

BS_Det = {
    "Index" : 8,
    "Name" : "BS",
    "State" : ["Out", "In"],
    "Image" : "ui/bs.png",
    "Xpos"  : 155,
    "Ypos"  : 580,
}

ADF_Det = {
    "Index" : 10,
    "Name" : "ADF",
    "State" : ["Retracted", "Inserted"],
    "Image" : "ui/adf.png",
    "Xpos"  : 155,
    "Ypos"  : 400,
}

BF_Det = {
    "Index" : 11,
    "Name" : "BF",
    "State" : ["Retracted", "Inserted"],
    "Image" : "ui/bf.png",
    "Xpos"  : 155,
    "Ypos"  : 640,
}

LScreen_Det = {
    "Index" : 13,
    "Name" : "LScreen",
    "State" : ["Raised", "Lowered"],
    "Image" : "ui/lscreen.png",
    "Xpos"  : 155,
    "Ypos"  : 490,
}

FScreen_Det = {
    "Index" : 12,
    "Name" : "FScreen",
    "State" : ["Retracted", "Inserted"],
    "Image" : "ui/fscreen.png",
    "Xpos"  : 155,
    "Ypos"  : 460,
}

detector_list = [BS_Det, ADF_Det, BF_Det, LScreen_Det, FScreen_Det]
