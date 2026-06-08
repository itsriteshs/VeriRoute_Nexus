# Smart Parcel Tag CAD Enclosure Design

This document details the mechanical design, box-mounting mechanisms, and printing parameters for the active **Smart Parcel Tag** enclosure.

---

## 1. Mechanical Enclosure Specifications

The Smart Parcel Tag enclosure is a highly compact, rugged rectangular box. It is designed to be mounted directly onto cardboard cargo boxes or medicine shipping containers.

* **Dimensions**:
  + **Width**: 45 mm
  + **Depth**: 35 mm
  + **Height**: 18 mm (ultra-slim profile to avoid catching during conveyor handoffs)
* **Wall Thickness**: 1.5 mm
* **Material**: Matte Black PLA or Impact-Resistant ABS (to survive drops and shipping impacts)
* **Mounting Method**: Double-sided adhesive tape channel or mounting clips on the bottom base.

---

## 2. Designated Cutouts & Interfaces

1. **Ventilation Slots**: Four 1.0mm wide slots over the DHT22 temperature sensor area to ensure direct airflow and accurate ambient measurements.
2. **Tamper Limit Switch Cutout**: 5.0 mm x 3.0 mm slot on the bottom face allowing the physical limit switch arm to protrude. The switch arm is compressed against the shipping container when mounted. If the tag is removed, the switch triggers.
3. **USB-C Charging Inlet**: 9.0 mm x 4.5 mm side opening for access to the ESP32-C3's charging port.
4. **Onboard LED Lens**: 2.0mm circular guide on top filled with clear hot-glue to act as a lightpipe for the status LED.

---

## 3. 3D Printing Settings (FDM)

Configure the slicer with the following parameters:

* **Layer Height**: 0.15 mm (for finer slot tolerances)
* **Infill Density**: 20%
* **Shells/Perimeters**: 3
* **Support Material**: None required (orient the model flat on its base)
* **Adhesion**: Use a brim (5mm) if printing with ABS to prevent corner warping on the heated bed.

---

## 4. Visual Enclosure CAD Mockup

Below is the 3D CAD render of the Smart Parcel Tag enclosure design:

![Smart Parcel Tag Enclosure CAD Render](file:///C:/Users/mouli/.gemini/antigravity-ide/brain/d29bc1cd-6a5f-4263-8353-0f507c8aa48f/smart_tag_enclosure_1780932174981.png)
