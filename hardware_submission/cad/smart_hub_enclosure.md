# Smart Relay Hub CAD Enclosure Design

This document details the mechanical design, 3D printing parameters, and assembly instructions for the **Smart Relay Hub** enclosure.

---

## 1. Mechanical Enclosure Specifications

The Smart Relay Hub housing is designed as a desktop-friendly, wedge-shaped console enclosure. It features distinct cutouts for the user interface components (OLED, LEDs, button) and has mounting slots for the internally-positioned RFID reader and ESP32 board.

* **Dimensions**:
  + **Width**: 110 mm
  + **Depth**: 85 mm
  + **Height (slope range)**: 25 mm (front) to 45 mm (rear)
* **Wall Thickness**: 2.0 mm (provides structural rigidity while saving filament)
* **Material Selection**:
  + **Matte Black or Dark Grey PLA/PETG** (for the main chassis)
  + **Clear Acrylic or Transparent PLA** (0.8mm sheet for the OLED and LED protective window)
* **Mounting Method**: Internal snap-fits for the PCB, with M2.5 self-tapping screws for securing the bottom cover.

---

## 2. Designated Cutouts & Interfaces

1. **OLED Screen Window**: 25.5 mm x 14.5 mm rectangular slot centered on the sloped top face.
2. **LED Indicators**: Two 5.2 mm circular holes spaced 15mm apart below the OLED screen.
3. **RFID Scan Zone**: Engraved symbol on the flat lower face indicating the sweep zone for RFID tags.
4. **Push Button Port**: 6.2 mm circular hole on the right side of the sloped face for the tactile push button.
5. **Power Cable Inlet**: 12.0 mm x 6.5 mm slot on the rear panel aligned with the ESP32’s micro-USB programming port.
6. **Buzzer Vent**: Small grille matrix (six 1.5mm holes) on the side to facilitate clear alarm sound propagation.

---

## 3. 3D Printing Settings (FDM)

To print a high-quality, professional shell on a standard FDM printer (e.g. Ender 3, Bambu Lab), configure the slicer with the following parameters:

* **Layer Height**: 0.2 mm
* **Infill Density**: 15% (Grid or Gyroid pattern)
* **Shells/Perimeters**: 3 (ensures robust screw holes)
* **Support Material**: Required (enable "Tree/Organic supports" for the internal RFID shelf overhangs)
* **Print Orientation**: Place the sloped top face flat on the build plate (face-down) to achieve a smooth textured finish and avoid printing internal supports.

---

## 4. Visual Enclosure CAD Mockup

Below is the 3D CAD render of the Smart Relay Hub enclosure design:

![Smart Relay Hub Enclosure CAD Render](file:///C:/Users/mouli/.gemini/antigravity-ide/brain/d29bc1cd-6a5f-4263-8353-0f507c8aa48f/smart_hub_enclosure_1780932157836.png)
