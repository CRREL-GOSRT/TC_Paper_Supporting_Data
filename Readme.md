# Supporting Python Scripts and Data for Cryosphere Article

**A generalized photon tracking approach to simulate spectral snow
albedo and transmittance using X-ray microtomography and
geometric optics**
*Theodore Letcher, Julie Parno, Zoe Courville, Lauren Farnsworth, and Jason Olivier*

## This folder contains code and data to replicate figures
1. Figure 2
2. Figure 3
3. Figure 5
4. Figure 8
5. Figure 9
6. Figure 10
7. Figure 12
8. Figure 13
9. Figure 14
10. Figure 15

---

All code is in python.
In addition to the CRREL-GOSRT model, you will need the following python libraries:
- pandas
- matplotlib
- sklearn

Within the scripts, all paths should be relative to this folder when accessing data.
That is, the data paths should work just fine.  One exception is that you will need to set the MaterialPath in the namelist to
point to the material path in your local GOSRT folder.
---

All supporting data is in the SampleData Folder including model output and observations.

---

Contacts:
- Theodore Letcher: Theodore.W.Letcher@usace.army.mil
- Julie Parno: Julie.T.Parno@erdc.dren.mil   