---
name: materials-dft-analysis
description: DFT calculation result analysis. Process band structures, density of states (DOS), Fermi energy calculations, and electronic structure analysis.
homepage: https://pymatgen.org/pymatgen.electronic_structure.html
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["python3"]},"primaryEnv":"None"}}
---

# Materials DFT Analysis

DFT calculation result analysis. Process band structures, density of states (DOS), Fermi energy, and electronic structure properties.

## Prerequisites

```bash
# Install required packages
pip install pymatgen matplotlib plotly scipy

# Optional for advanced plotting
pip install seaborn
```

## Band Structure Analysis

### Load and Plot Band Structure

```python
from pymatgen.io.vasp import Vasprun, BSVasprun
from pymatgen.electronic_structure.plotter import BSPlotter

# Load band structure calculation
bs_vasprun = BSVasprun("band_calc/vasprun.xml")
band_structure = bs_vasprun.get_band_structure()

# Plot band structure
plotter = BSPlotter(band_structure)
plotter.get_plot(vbm_cbm_marker=True)
plt.savefig('band_structure.png', dpi=150)

# Get band gap info
band_gap = band_structure.get_band_gap()
print(f"Band gap: {band_gap['energy']:.3f} eV")
print(f"Direct gap: {band_gap['direct']}")
print(f"Transition: {band_gap['transition']}")
```

### Extract VBM and CBM

```python
# Valence band maximum
vbm = band_structure.get_vbm()
print(f"VBM energy: {vbm['energy']:.4f} eV")
print(f"VBM k-point: {vbm['kpoint'].frac_coords}")

# Conduction band minimum
cbm = band_structure.get_cbm()
print(f"CBM energy: {cbm['energy']:.4f} eV")
print(f"CBM k-point: {cbm['kpoint'].frac_coords}")
```

### Effective Mass Calculation

```python
from pymatgen.electronic_structure.core import Spin
import numpy as np

# Calculate effective mass near band edges
# (Simplified - requires careful k-point sampling)
bands = band_structure.bands[Spin.up]
kpoints = band_structure.kpoints

# Fit parabola near VBM/CBM for effective mass
# m* = ℏ² / (d²E/dk²)
```

## Density of States (DOS) Analysis

### Total and Projected DOS

```python
from pymatgen.io.vasp import Vasprun
from pymatgen.electronic_structure.plotter import DosPlotter

# Load DOS data
vasprun = Vasprun("vasprun.xml", parse_dos=True)
cdos = vasprun.complete_dos

# Get Fermi energy
efermi = cdos.efermi
print(f"Fermi energy: {efermi:.4f} eV")

# Plot total DOS
plotter = DosPlotter()
plotter.add_dos("Total DOS", cdos)
plotter.get_plot().savefig('total_dos.png')

# Get element-projected DOS
pdos = cdos.get_element_dos()
plotter = DosPlotter()
for element, dos in pdos.items():
    plotter.add_dos(str(element), dos)
plotter.get_plot().savefig('element_dos.png')

# Get orbital-projected DOS
spd_dos = cdos.get_spd_dos()
plotter = DosPlotter()
for orbital, dos in spd_dos.items():
    plotter.add_dos(str(orbital), dos)
plotter.get_plot().savefig('orbital_dos.png')
```

### Calculate DOS Properties

```python
from scipy.integrate import simpson

# Energy grid
energies = cdos.energies - efermi  # Shift to Fermi level
densities = cdos.densities[Spin.up]

# DOS at Fermi level
dos_fermi = cdos.get_interpolated_value(efermi)
print(f"DOS at Fermi level: {dos_fermi:.4f} states/eV")

# Integrated DOS up to Fermi level
# (Number of states below Fermi energy)
mask = energies <= 0
integrated_dos = simpson(densities[mask], energies[mask])
print(f"Integrated DOS: {integrated_dos:.2f} states")

# Find band centers
def find_band_center(energies, dos, energy_range):
    mask = (energies >= energy_range[0]) & (energies <= energy_range[1])
    numerator = simpson(energies[mask] * dos[mask], energies[mask])
    denominator = simpson(dos[mask], energies[mask])
    return numerator / denominator if denominator != 0 else None

# d-band center (example for transition metals)
dband_center = find_band_center(energies, densities, (-8, -2))
print(f"d-band center: {dband_center:.2f} eV")
```

## Fermi Surface Analysis

```python
from pymatgen.electronic_structure.plotter import plot_fermi_surface

# Requires Fermi surface calculation (ISMEAR = -5, dense k-mesh)
# This is a simplified example

# Get eigenvalues at k-points
eigenvalues = band_structure.bands[Spin.up]
kpoints = [k.frac_coords for k in band_structure.kpoints]

# Identify states at Fermi level (within some tolerance)
tol = 0.1  # eV
fermi_states = np.abs(eigenvalues - efermi) < tol
```

## Combined Band Structure + DOS Plot

```python
import matplotlib.pyplot as plt
from pymatgen.electronic_structure.plotter import BSPlotter, DosPlotter

# Create figure with subplots
fig = plt.figure(figsize=(12, 6))
gs = fig.add_gridspec(1, 2, width_ratios=[2, 1], wspace=0.1)

# Band structure
ax1 = fig.add_subplot(gs[0])
bs_plotter = BSPlotter(band_structure)
bs_plotter.get_plot(ax=ax1)
ax1.set_xlabel('k-point')
ax1.set_ylabel('Energy (eV)')

# DOS
ax2 = fig.add_subplot(gs[1], sharey=ax1)
dos_plotter = DosPlotter()
dos_plotter.add_dos("Total", cdos)
# Custom DOS plot on ax2
energies = cdos.energies - efermi
densities = cdos.densities[Spin.up]
ax2.plot(densities, energies, 'b-', linewidth=1.5)
ax2.fill_betweenx(energies, 0, densities, alpha=0.3)
ax2.axhline(y=0, color='k', linestyle='--', linewidth=0.5)
ax2.set_xlabel('DOS (states/eV)')
ax2.set_ylabel('')
plt.setp(ax2.get_yticklabels(), visible=False)

plt.tight_layout()
plt.savefig('band_dos_combined.png', dpi=150)
```

## Charge Density Analysis

```python
from pymatgen.io.vasp import Chgcar

# Load CHGCAR
chgcar = Chgcar.from_file("CHGCAR")

# Get charge density data
data = chgcar.data['total']

# Analyze charge density
print(f"Grid shape: {data.shape}")
print(f"Max charge density: {np.max(data):.4f}")
print(f"Total electrons: {np.sum(data) * chgcar.ngridpts / len(chgcar.structure):.2f}")

# Planar average along z-axis
planar_avg = np.mean(data, axis=(0, 1))
z_coords = np.linspace(0, chgcar.structure.lattice.c, len(planar_avg))

plt.plot(z_coords, planar_avg)
plt.xlabel('z (Å)')
plt.ylabel('Charge density')
plt.savefig('planar_avg_charge.png')
```

## Work Function Calculation

```python
# For slab calculations
from pymatgen.io.vasp import Locpot

locpot = Locpot.from_file("LOCPOT")

# Get electrostatic potential
potential = locpot.data['total']

# Average in xy plane
planar_potential = np.mean(potential, axis=(0, 1))

# Work function = V(vacuum) - E_fermi
# Identify vacuum potential (plateau in planar potential)
vacuum_potential = np.max(planar_potential)  # Simplified
work_function = vacuum_potential - efermi
print(f"Work function: {work_function:.3f} eV")
```

## Electronic Structure Database

```python
import json

def analyze_electronic_structure(vasprun_path):
    """Extract key electronic properties from vasprun.xml."""
    vasprun = Vasprun(vasprun_path, parse_dos=True)
    
    bs = vasprun.get_band_structure()
    cdos = vasprun.complete_dos
    
    results = {
        'band_gap': bs.get_band_gap()['energy'],
        'is_direct': bs.get_band_gap()['direct'],
        'fermi_energy': cdos.efermi,
        'dos_at_fermi': cdos.get_interpolated_value(cdos.efermi),
        'vbm': bs.get_vbm()['energy'],
        'cbm': bs.get_cbm()['energy'],
        'is_metal': bs.is_metal(),
    }
    
    return results

# Batch analysis
results = {}
for calc_dir in ['calc1', 'calc2', 'calc3']:
    try:
        results[calc_dir] = analyze_electronic_structure(
            f"{calc_dir}/vasprun.xml"
        )
    except Exception as e:
        print(f"Error in {calc_dir}: {e}")

# Save results
with open('electronic_properties.json', 'w') as f:
    json.dump(results, f, indent=2)
```

## Visualization Best Practices

```python
# High-quality band structure plot
from pymatgen.electronic_structure.plotter import BSPlotterProjected

# With projections
bs_plotter = BSPlotterProjected(band_structure)
plt = bs_plotter.get_elt_projected_plots()
plt.savefig('band_structure_projected.png', dpi=300, bbox_inches='tight')

# Interactive plot with plotly
from pymatgen.electronic_structure.plotter import plotly_bs_plotter

# (Requires additional setup)
```

## References

- [pymatgen electronic_structure](https://pymatgen.org/pymatgen.electronic_structure.html)
- [Materials Project](https://materialsproject.org)
- [VASP Band Structure](https://www.vasp.at/wiki/index.php/Band-structure)
- [Kohn-Sham DFT](https://en.wikipedia.org/wiki/Kohn%E2%80%93Sham_equations)
