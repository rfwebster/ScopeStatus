import sys
import tkinter as tk
from PIL import ImageTk, Image
import microscope

try:
    _online = True
    from PyJEM import detector
    from PyJEM import TEM3
except ImportError:
    _online = False
    from PyJEM.offline import detector
    from PyJEM.offline import TEM3

POLLING = 2000




class ScopeStatus:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("500x710")
        self.root.title("ScopeStatus")
        self.root.resizable(False, False)
        self.root.configure(bg="black")
        # Load the default background image
        self.bg_image = ImageTk.PhotoImage(Image.open("ui/bkg-beam.png").convert("RGBA"))
        self.beamvalve_image = ImageTk.PhotoImage(Image.open("ui/bv.png").convert("RGBA"))
        self.sample_image = ImageTk.PhotoImage(Image.open("ui/sample.png").convert("RGBA"))
        self.setup_ui()
        self.setup_canvas()

        self.update()
    
    def setup_ui(self):
        self.status_frame = tk.Frame(self.root, bg="black")
        self.status_frame.pack(padx=10, pady=20, anchor="nw")
        
        self.status_frame.grid_columnconfigure(0, minsize=75)
        self.status_frame.grid_columnconfigure(1, minsize=75)

        self.ht_value  = tk.Label(self.status_frame, text="0 KV", bg="black", fg="light green", font=("Comic Sans MS", 20, "bold"))
        self.ht_value.grid(row=1, columnspan=2, sticky="nsew")

        self.a1_label = tk.Label(self.status_frame, text="A1: ", bg="black", fg="light green", font=("Comic Sans MS", 10, "bold"))
        self.a1_label.grid(row=2, column=0, sticky="w")
        self.a1_value  = tk.Label(self.status_frame, text="0 kV", bg="black", fg="light green", font=("Comic Sans MS", 10))
        self.a1_value.grid(row=2, column=1, sticky="e")

        self.a2_label = tk.Label(self.status_frame, text="A2: ", bg="black", fg="light green", font=("Comic Sans MS", 10, "bold"))
        self.a2_label.grid(row=3, column=0, sticky="w")
        self.a2_value =  tk.Label(self.status_frame, text="0 kV", bg="black", fg="light green", font=("Comic Sans MS", 10))  
        self.a2_value.grid(row=3, column=1, sticky="e")
        
        self.emission_label = tk.Label(self.status_frame, text="Emission: ", bg="black", fg="light green", font=("Comic Sans MS", 10, "bold"))
        self.emission_label.grid(row=4, column=0, sticky="w")
        self.emission_value = tk.Label(self.status_frame, text="0 uA", bg="black", fg="light green", font=("Comic Sans MS", 10))
        self.emission_value.grid(row=4, column=1, sticky="e")

        # blank row
        self.status_frame.grid_rowconfigure(5, minsize=40)

        # self.vacready_label = tk.Label(self.status_frame, text="Vacuum Ready", bg="black", fg="light green", font=("Comic Sans MS", 10, "bold"))
        # self.vacready_label.grid(row=6, columnspan=2, sticky="nsew")

        # blank row
        # self.status_frame.grid_rowconfigure(7, minsize=40)

        self.mode_label = tk.Label(self.status_frame, text="STEM", bg="black", fg="light green", font=("Comic Sans MS", 20, "bold"))
        self.mode_label.grid(row=8, columnspan=2, sticky="nsew")

        self.mag_label = tk.Label(self.status_frame, text="100 kx", bg="black", fg="light green", font=("Comic Sans MS", 14, "bold"))
        self.mag_label.grid(row=9, columnspan=2, sticky="nsew")

        self.camlength_label = tk.Label(self.status_frame, text="30 cm", bg="black", fg="light green", font=("Comic Sans MS", 10))
        self.camlength_label.grid(row=10, column=0, sticky="w")
        self.probesize_label = tk.Label(self.status_frame, text="Probe: 10", bg="black", fg="light green", font=("Comic Sans MS", 10))
        self.probesize_label.grid(row=10, column=1, sticky="e")
             

        # Stage ##############################################################
        self.stage_frame = tk.Frame(self.root, bg="black")
        self.stage_frame.pack(padx=10, pady=20, anchor="sw")
        
        self.stage_frame.grid_columnconfigure(0, minsize=75)
        self.stage_frame.grid_columnconfigure(1, minsize=75)

        self.title_value  = tk.Label(self.stage_frame, text="Stage", bg="black", fg="light green", font=("Comic Sans MS", 20, "bold"))
        self.title_value.grid(row=1, columnspan=2, sticky="nsew")

        self.xy_label = tk.Label(self.stage_frame, text="Pos = ", bg="black", fg="light green", font=("Comic Sans MS", 10))
        self.xy_label.grid(row=2, columnspan=2, sticky="nsew")

        self.z_label = tk.Label(self.stage_frame, text="Z = ", bg="black", fg="light green", font=("Comic Sans MS", 10))
        self.z_label.grid(row=3, columnspan=2, sticky="nsew")

        self.sf_label = tk.Label(self.stage_frame, text="SF-Z = ", bg="black", fg="light green", font=("Comic Sans MS", 10))
        self.sf_label.grid(row=5, columnspan=2, sticky="nsew")
        
        # blank row
        self.status_frame.grid_rowconfigure(6, minsize=40)

        self.tx_label = tk.Label(self.stage_frame, text="TX = ", bg="black", fg="light green", font=("Comic Sans MS", 10))
        self.tx_label.grid(row=7, column=0, sticky="w")
        self.ty_value = tk.Label(self.stage_frame, text="TY = ", bg="black", fg="light green", font=("Comic Sans MS", 10))
        self.ty_value.grid(row=7, column=1, sticky="e")


    def setup_canvas(self):
        self.canvas = tk.Canvas(self.root, width=300, height=670, bg="black", highlightthickness=0)
        self.canvas.place(x=200, y=20)       
        # Load the background image
        self.bg_item = self.canvas.create_image(75, 0, image=self.bg_image, anchor="nw")

        # Move the background image to the back of the canvas
        self.canvas.lower(self.bg_item)

        # Add the beam valve image 
        self.beamvalve_item = self.canvas.create_image(80, 60, image=self.beamvalve_image, anchor="nw")
        self.beamvalve_text_item = self.canvas.create_text(82, 60, text="Beam Valve", anchor="nw",
                                                           fill="white", font=("Comic Sans MS", 9, "bold"))

        # Add the sample image 
        self.sample_text_item = self.canvas.create_text(40, 225, text="Sample", fill="white", font=("Comic Sans MS", 10, "bold"))
        self.sample_state_item = self.canvas.create_text(40, 240, text="In", fill="white")
        self.sample_item = self.canvas.create_image(55, 250, image=self.sample_image, anchor="nw")


        for apt in microscope.aperture_list:
            text_item = self.canvas.create_text(apt["Xpos"]+110, apt["Ypos"]-10, text=apt["Name"], fill="white", font=("Comic Sans MS", 10, "bold"))
            size_item = self.canvas.create_text(apt["Xpos"]+110, apt["Ypos"]+5, text=apt["Size"][0], fill="white")
            img = ImageTk.PhotoImage(Image.open(apt["Image"]).convert("RGBA"))
            image_item = self.canvas.create_image(apt["Xpos"], apt["Ypos"], image=img)

            apt.update({"text_item": text_item, 
                        "size_item": size_item,
                        "image_item": image_item,
                        "img": img})

        for det in microscope.detector_list:
            text_item = self.canvas.create_text(det["Xpos"]-110, det["Ypos"]-10, text=det["Name"], fill="white", font=("Comic Sans MS", 10, "bold"))
            size_item = self.canvas.create_text(det["Xpos"]-110, det["Ypos"]+5, text=det["State"][0], fill="white")
            img = ImageTk.PhotoImage(Image.open(det["Image"]).convert("RGBA"))
            image_item = self.canvas.create_image(det["Xpos"], det["Ypos"], image=img)

            det.update({"text_item": text_item,
                        "size_item": size_item,
                        "image_item": image_item,
                        "img": img})
         


    def update(self):

        # Background

        if (microscope.gun.GetEmissionCurrentValue() and _online) or microscope.gun.GetFilamentVal():
            self.bg_image = ImageTk.PhotoImage(Image.open("ui/bkg-bv.png").convert("RGBA"))
            if microscope.feg.GetBeamValve():
                self.bg_image = ImageTk.PhotoImage(Image.open("ui/bkg-fscreen.png").convert("RGBA"))
                if microscope.det.GetPosition(12) == 0:
                    self.bg_image = ImageTk.PhotoImage(Image.open("ui/bkg-lscreen.png").convert("RGBA"))
                    if microscope.det.GetPosition(13) == 0:
                        self.bg_image = ImageTk.PhotoImage(Image.open("ui/bkg-beam.png").convert("RGBA"))
        else:
            self.bg_image = ImageTk.PhotoImage(Image.open("ui/bkg.png").convert("RGBA"))

        # Update the background image
        self.canvas.itemconfig(self.bg_item, image=self.bg_image)
        


        pos = microscope.stage.GetPos()
        self.xy_label.config(text=f"X, Y = [{pos[0]}, {pos[1]}]")
        self.z_label.config(text=f"Z = {pos[2]}")
        self.tx_label.config(text=f"TX = {pos[3]}")
        self.ty_value.config(text=f"TY = {pos[4]}")

        sf_pos = microscope.stage.GetPiezoPosi()
        self.sf_label.config(text=f"Super Fine = {sf_pos}")


        # update the HT label
        self.ht_value.config(text=f"{microscope.HT.GetHtValue()} kV")
        self.a1_value.config(text=f"{microscope.gun.GetAnode1CurrentValue()} kV")
        self.a2_value.config(text=f"{microscope.gun.GetAnode2CurrentValue()} kV")
        emission = microscope.gun.GetEmissionCurrentValue()
        self.emission_value.config(text=f"{emission} uA")
        if 0 < emission < 12:
            self.emission_label.config(fg="orange") # orange indicates do a flash


        mode = "TEM" if microscope.EOS.GetTemStemMode() == 0 else "STEM"
        self.mode_label.config(text=f"{mode}")
        

        if mode == "STEM":
            self.mag_label.config(text=f"{microscope.EOS.GetFunctionMode()[1]} - {microscope.EOS.GetMagValue()}") # need to test on microscope
            self.camlength_label.config(text=f"{microscope.EOS.GetStemCamValue()}")
            self.probesize_label.config(text=f"Probe: {microscope.EOS.GetSpotSize()+1}") # need to test on microscope
        if mode == "TEM":
            self.mag_label.config(text=f"{microscope.EOS.GetFunctionMode()[1]} - {microscope.EOS.GetMagValue()[2]}")
            self.camlength_label.config(text=f"{microscope.EOS.GetAlphaSelectorEx()[1]}")
            self.probesize_label.config(text=f"Spot: {microscope.EOS.GetSpotSize()+1}") # need to test on microscope
        
        
        # update the beam valve state
        if microscope.feg.GetBeamValve():
            self.canvas.itemconfig(self.beamvalve_item, state="hidden")
        else:
            self.canvas.itemconfig(self.beamvalve_item, state="normal")
        
        # update the sample insertion state
        if _online:
            if microscope.stage.GetHolderStts() == 1:
                self.canvas.itemconfig(self.sample_state_item, text="In")
                self.canvas.itemconfig(self.sample_item, state="normal")
            else:
                self.canvas.itemconfig(self.sample_state_item, text="Out")
                self.canvas.itemconfig(self.sample_item, state="hidden")
        

        # update aperture states
        for apt in microscope.aperture_list:
            if _online:
                microscope.apt.SelectExpKind(apt["Index"])
                size = microscope.apt.GetExpSize(apt["Index"])
            else:
                microscope.apt.SelectKind(apt["Index"])
                size = microscope.apt.GetSize(apt["Index"])
            if size == 0:
                self.canvas.itemconfig(apt["image_item"], state="hidden")
            else: 
                self.canvas.itemconfig(apt["size_item"], text=apt["Size"][size])
                self.canvas.itemconfig(apt["image_item"], state="normal")

        # update detector states
        for det in microscope.detector_list:
            if _online:
                state = microscope.det.GetPosition(det["Index"])
            else:
                state = microscope.det.GetPosition(det["Index"])
            if state == 0:
                self.canvas.itemconfig(det["image_item"], state="hidden")
            else: 
                self.canvas.itemconfig(det["size_item"], text=det["State"][state])
                self.canvas.itemconfig(det["image_item"], state="normal")

        # wait and update!
        self.root.after(POLLING, self.update)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    scope = ScopeStatus()
    scope.run()