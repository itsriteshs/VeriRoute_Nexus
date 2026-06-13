# Smart Parcel Tag CAD Enclosure Design

This document details the mechanical design, box-mounting mechanisms, and printing parameters for the active **Smart Parcel Tag** enclosure.

---

## 1. Mechanical Enclosure Specifications

The Smart Parcel Tag enclosure is a highly compact, rugged rectangular box. The physical design files are provided as a high-fidelity 3D STEP model: [Smart_Parcel_Tag_closed.step](file:///c:/Users/lakshanya/OneDrive/Desktop/veri/VeriRoute_Nexus/hardware_submission/cad/Smart_Parcel_Tag_closed.step) (migrated from the legacy STL format). It is designed to be mounted directly onto cardboard cargo boxes or medicine shipping containers.

* **Dimensions**:
  + **Width (Body)**: 45.0 mm
  + **Width (with Mounting Ears)**: 62.0 mm
  + **Depth**: 35.0 mm
  + **Height**: 18.0 mm (ultra-slim profile to avoid catching during conveyor handoffs)
* **Wall Thickness**: 1.5 mm
* **Material**: Matte Black ABS / Polycarbonate (to survive drops and shipping impacts)
* **Mounting Method**: 4x M3 screw brackets (ears) at the bottom corners.

---

## 2. Designated Cutouts & Interfaces

1. **Ventilation Slits**: 5x $12.0\text{ mm} \times 1.0\text{ mm}$ slits on the top cover directly over the DHT22 sensor to ensure direct airflow.
2. **Tamper Limit Switch Cutout**: $5.0\text{ mm} \times 3.0\text{ mm}$ opening on the bottom face for the physical limit switch arm. The switch arm is compressed against the container surface when mounted.
3. **USB-C Charging Inlet**: $9.0\text{ mm} \times 4.5\text{ mm}$ opening on the front wall with a protective rubber flap.
4. **Reset Button Cutout**: 3.0 mm circular hole on the front wall.
5. **Status LED Guide**: 2.0 mm circular lightpipe hole on the top cover.
6. **Top Lid Fasteners**: 4x M2.5 threaded screw holes positioned at the top corners to secure the enclosure lid.

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

![Smart Parcel Tag Enclosure CAD Render](../documentation/images/tag_overview_render.png)
