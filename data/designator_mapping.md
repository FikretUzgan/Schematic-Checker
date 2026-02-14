# Altium Designator Prefix Mapping

This document lists the standard designator prefixes used for component categorization in the Auto_Altium project.

| Prefix | Component Type |
| :--- | :--- |
| **R** | Resistor |
| **C** | Capacitor |
| **J** | Connector |
| **CN** | Connector |
| **IC** | Integrated Circuit |
| **U** | Integrated Circuit |
| **D** | Diode |
| **TR** | Transistor |
| **Q** | Transistor |
| **L** | Coil (Inductor) |
| **FL** | Filter |
| **X** | Xtal |

## Usage in Verification Tool

The current version of the Rating Verification Tool filters specifically for **R** and **C** prefixes to perform power and voltage rating checks. Other prefixes are categorized but ignored for the final verdict dashboard to focus on passive components.
