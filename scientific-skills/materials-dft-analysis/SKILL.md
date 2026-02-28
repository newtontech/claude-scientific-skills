---
name: materials-dft-analysis
description: Analyze DFT calculation results - band structure, density of states (DOS), charge density, Fermi surface, and electronic structure properties. Visualize and extract insights from quantum mechanical simulations.
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# Materials DFT Analysis

## Overview

A specialized skill for analyzing Density Functional Theory (DFT) calculation results. Extract and visualize electronic structure properties including band structures, density of states (DOS), charge densities, and Fermi surfaces. Compute band gaps, effective masses, and other electronic properties. Perfect for understanding the quantum mechanical behavior of materials.

## When to Use This Skill

This skill should be used when:
- Analyzing electronic band structures from DFT calculations
- Computing and visualizing density of states (total and projected)
- Calculating band gaps (direct and indirect)
- Identifying valence band maximum (VBM) and conduction band minimum (CBM)
- Computing effective masses from band curvatures
- Analyzing charge density distributions
- Generating Fermi surface plots
- Computing work functions and ionization potentials
- Analyzing spin-polarized electronic structure
- Extracting partial density of states (PDOS) by element or orbital

## Quick Start Guide

### Installation

```bash
# Core dependencies
uv pip install pymatgen matplotlib numpy scipy

# For advanced analysis
uv pip install pymatgen[vis] boltztrap2
```

### Band Structure Analysis

```python
from pymatgen.io.vasp import Vasprun
from pymatgen.electronic_structure.plotter import BSPlotter

# Parse VASP band structure
vasprun = Vasprun("vasprun.xml")
bs = vasprun.get_band_structure()

# Get band gap info
band_gap = bs.get_band_gap()
print(f"Band gap: {band_gap['energy']:.3f} eV")
print(f"Direct: {band_gap['direct']}")
print(f"Transition: {band_gap['transition']}")

# Plot band structure
plotter = BSPlotter(bs)
plotter.get_plot()
plt.savefig("band_structure.png", dpi=150)
```

### Density of States Analysis

```python
from pymatgen.electronic_structure.plotter import DosPlotter

# Get complete DOS
dos = vasprun.complete_dos

# Get elemental PDOS
element_dos = dos.get_element_dos()

# Plot
plotter = DosPlotter()
plotter.add_dos("Total", dos)
for element, pdos in element_dos.items():
    plotter.add_dos(str(element), pdos)
plotter.get_plot()
plt.savefig("dos.png", dpi=150)
```

## Core Capabilities

### 1. Band Structure Analysis

Extract and analyze electronic band structures.

```python
from pymatgen.io.vasp import Vasprun, BSVasprun
from pymatgen.electronic_structure.plotter import BSPlotter
from pymatgen.electronic_structure.bandstructure import BandStructure
import matplotlib.pyplot as plt

# Parse band structure
vasprun = BSVasprun("vasprun.xml", parse_projected_eigen=True)
bs = vasprun.get_band_structure()

# Basic properties
print(f"Number of bands: {bs.nb_bands}")
print(f"Number of k-points: {len(bs.kpoints)}")
print(f"Fermi energy: {bs.efermi:.3f} eV")

# Band gap analysis
band_gap = bs.get_band_gap()
print(f"\nBand gap: {band_gap['energy']:.3f} eV")
print(f"Direct gap: {band_gap['direct']}")
print(f"Transition: {band_gap['transition']}")

# VBM and CBM
vbm = bs.get_vbm()
cbm = bs.get_cbm()
print(f"\nVBM: {vbm['energy']:.3f} eV at k-point {vbm['kpoint']}")
print(f"CBM: {cbm['energy']:.3f} eV at k-point {cbm['kpoint']}")

# Check if material is metallic
print(f"\nIs metal: {bs.is_metal()}")

# Visualization
plotter = BSPlotter(bs)
plt = plotter.get_plot()
plt.savefig("band_structure.png", dpi=150, bbox_inches="tight")
```

**Band Structure with Projections:**
```python
# Parse with projections
vasprun = BSVasprun("vasprun.xml", parse_projected_eigen=True)
bs = vasprun.get_band_structure()

# Get projected band structure
proj_bs = vasprun.get_band_structure()

# Plot with element projections
from pymatgen.electronic_structure.plotter import BSPlotterProjected

plotter = BSPlotterProjected(bs)
# Project on specific elements
plt = plotter.get_elt_projected_plots(['Si', 'O'])
plt.savefig("band_structure_projected.png", dpi=150)
```

### 2. Density of States (DOS) Analysis

Compute and visualize total and partial density of states.

```python
from pymatgen.io.vasp import Vasprun
from pymatgen.electronic_structure.plotter import DosPlotter
from pymatgen.electronic_structure.core import OrbitalType

# Parse vasprun.xml
dos_vasprun = Vasprun("vasprun.xml")
dos = dos_vasprun.complete_dos

# Basic DOS properties
print(f"Fermi energy: {dos.efermi:.3f} eV")
print(f"Band gap: {dos.get_gap():.3f} eV")
print(f"CBM: {dos.get_cbm_vbm()[0]:.3f} eV")
print(f"VBM: {dos.get_cbm_vbm()[1]:.3f} eV")

# Element-projected DOS
element_dos = dos.get_element_dos()
for element, pdos in element_dos.items():
    print(f"\n{element}:")
    print(f"  Band gap: {pdos.get_gap():.3f} eV")

# Orbital-projected DOS for specific element
spd_dos = dos.get_element_spd_dos("Si")
print(f"\nSi orbital contributions:")
for orbital, pdos in spd_dos.items():
    print(f"  {orbital}: gap = {pdos.get_gap():.3f} eV")

# Site-projected DOS
site_dos = dos.get_site_dos(struct[0])  # First site

# Visualization
plotter = DosPlotter(sigma=0.05)  # Gaussian smearing
plotter.add_dos("Total", dos)

# Add elemental contributions
for element, pdos in element_dos.items():
    plotter.add_dos(str(element), pdos)

plt = plotter.get_plot()
plt.savefig("dos_elements.png", dpi=150)

# Orbital-resolved DOS for specific element
plotter = DosPlotter(sigma=0.05)
spd_dos = dos.get_element_spd_dos("Si")
for orb, pdos in spd_dos.items():
    plotter.add_dos(f"Si-{orb.name}", pdos)
plt = plotter.get_plot()
plt.savefig("dos_si_orbitals.png", dpi=150)
```

**Spin-Polarized DOS:**
```python
# For spin-polarized calculations
from pymatgen.electronic_structure.core import Spin

# Total DOS for each spin
total_dos_up = dos.densities[Spin.up]
total_dos_down = dos.densities[Spin.down]

# Element spin DOS
fe_spd = dos.get_element_spd_dos("Fe")
for orb, pdos in fe_spd.items():
    up = pdos.densities[Spin.up]
    down = pdos.densities[Spin.down]
    print(f"Fe {orb.name}: up={up.sum():.2f}, down={down.sum():.2f}")

# Plot spin-resolved DOS
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 6))
energies = dos.energies - dos.efermi

ax.plot(energies, dos.densities[Spin.up], label='Spin up', color='blue')
ax.plot(energies, -dos.densities[Spin.down], label='Spin down', color='red')
ax.axvline(0, color='black', linestyle='--', alpha=0.5)
ax.set_xlabel('Energy (eV)')
ax.set_ylabel('DOS (states/eV)')
ax.legend()
plt.savefig("dos_spin_polarized.png", dpi=150)
```

### 3. Effective Mass Calculations

Compute carrier effective masses from band curvatures.

```python
from pymatgen.electronic_structure.bandstructure import BandStructure
from pymatgen.analysis.electronic_structure import get_linear_interpolations
import numpy as np

def calculate_effective_mass(bs, temperature=300):
    """
    Calculate effective masses at band extrema
    """
    from scipy.optimize import curve_fit
    
    # Get VBM and CBM
    vbm = bs.get_vbm()
    cbm = bs.get_cbm()
    
    results = {}
    
    # Analyze VBM (holes)
    vbm_k = vbm['kpoint']
    vbm_band = vbm['band_index']
    
    # Find k-points near VBM
    # (Implementation depends on specific band structure format)
    
    # Analyze CBM (electrons)
    cbm_k = cbm['kpoint']
    cbm_band = cbm['band_index']
    
    # Fit parabolic dispersion: E = E0 + (ħ²k²)/(2m*)
    # m* = ħ² / (d²E/dk²)
    
    hbar = 6.582119569e-16  # eV·s
    ev_to_j = 1.60218e-19
    ang_to_m = 1e-10
    
    results['vbm_energy'] = vbm['energy']
    results['cbm_energy'] = cbm['energy']
    
    # Note: Full implementation requires interpolation along k-paths
    # This is a simplified version
    
    return results

# Usage
em_results = calculate_effective_mass(bs)
print(f"Effective mass analysis:")
for key, value in em_results.items():
    print(f"  {key}: {value}")
```

### 4. Charge Density Analysis

Analyze charge density distributions from CHGCAR files.

```python
from pymatgen.io.vasp import Chgcar
import numpy as np

# Parse CHGCAR
chgcar = Chgcar.from_file("CHGCAR")

# Get charge density data
data = chgcar.data  # 3D numpy array

# Basic statistics
print(f"Grid shape: {data.shape}")
print(f"Total charge: {data.sum():.2f}")
print(f"Min density: {data.min():.6f}")
print(f"Max density: {data.max():.6f}")

# Integrate along z-axis (for 2D materials)
z_profile = data.mean(axis=(0, 1))
print(f"Z-averaged profile shape: {z_profile.shape}")

# Planar average
planar_avg = chgcar.get_axis_grid(2)  # along z-axis

# Visualization
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 3, figsize=(15, 4))

# XY slice at center
z_mid = data.shape[2] // 2
axes[0].imshow(data[:, :, z_mid].T, origin='lower', cmap='viridis')
axes[0].set_title('XY slice (z=center)')

# XZ slice at center
y_mid = data.shape[1] // 2
axes[1].imshow(data[:, y_mid, :].T, origin='lower', cmap='viridis')
axes[1].set_title('XZ slice (y=center)')

# 1D profile along z
z_grid = np.linspace(0, chgcar.structure.lattice.c, data.shape[2])
axes[2].plot(z_grid, z_profile)
axes[2].set_xlabel('z (Å)')
axes[2].set_ylabel('Average charge density')
axes[2].set_title('Z-averaged charge density')

plt.tight_layout()
plt.savefig("charge_density.png", dpi=150)
```

**Differential Charge Density:**
```python
# Calculate differential charge density
chgcar_total = Chgcar.from_file("CHGCAR")
chgcar_a = Chgcar.from_file("CHGCAR_A")
chgcar_b = Chgcar.from_file("CHGCAR_B")

# Δρ = ρ(AB) - ρ(A) - ρ(B)
diff_density = chgcar_total.data - chgcar_a.data - chgcar_b.data

# Visualize charge transfer
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 6))
im = ax.imshow(diff_density[:, :, diff_density.shape[2]//2].T, 
               origin='lower', cmap='RdBu_r', vmin=-0.1, vmax=0.1)
ax.set_title('Differential Charge Density')
plt.colorbar(im, ax=ax, label='Δρ (e/Å³)')
plt.savefig("diff_charge_density.png", dpi=150)
```

### 5. Work Function Analysis

Calculate work functions from electrostatic potential.

```python
from pymatgen.io.vasp import Locpot
import numpy as np
import matplotlib.pyplot as plt

# Parse LOCPOT (electrostatic potential)
locpot = Locpot.from_file("LOCPOT")

# Get planar-averaged potential along z-axis
z_grid = locpot.get_axis_grid(2)  # z-axis
planar_avg = locpot.get_average_along_axis(2)

# For slab calculations, identify vacuum and slab regions
# Vacuum potential is the plateau region
vacuum_potential = np.max(planar_avg)  # Approximate

# Work function = V_vacuum - E_Fermi
fermi_energy = 5.0  # Get from OUTCAR or vasprun.xml
work_function = vacuum_potential - fermi_energy

print(f"Vacuum potential: {vacuum_potential:.3f} eV")
print(f"Fermi energy: {fermi_energy:.3f} eV")
print(f"Work function: {work_function:.3f} eV")

# Visualization
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(z_grid, planar_avg, 'b-', linewidth=2)
ax.axhline(vacuum_potential, color='r', linestyle='--', label='Vacuum level')
ax.axhline(fermi_energy, color='g', linestyle='--', label='Fermi level')
ax.fill_between(z_grid, planar_avg, alpha=0.3)
ax.set_xlabel('z (Å)')
ax.set_ylabel('Electrostatic potential (eV)')
ax.set_title(f'Work Function = {work_function:.2f} eV')
ax.legend()
plt.savefig("work_function.png", dpi=150)
```

### 6. Spin and Magnetic Analysis

Analyze spin-polarized electronic structure.

```python
from pymatgen.io.vasp import Vasprun, Outcar
from pymatgen.electronic_structure.core import Spin

# Parse spin-polarized calculation
vasprun = Vasprun("vasprun.xml")

# Check if spin-polarized
is_spin_polarized = vasprun.is_spin
print(f"Spin-polarized: {is_spin_polarized}")

if is_spin_polarized:
    # Get spin-resolved DOS
    dos = vasprun.complete_dos
    
    # Total spin up/down
    total_up = dos.densities[Spin.up].sum()
    total_down = dos.densities[Spin.down].sum()
    
    print(f"Total DOS: up={total_up:.2f}, down={total_down:.2f}")
    print(f"Spin polarization: {(total_up - total_down) / (total_up + total_down):.3f}")
    
    # Get magnetization from OUTCAR
    outcar = Outcar("OUTCAR")
    
    if outcar.magnetization:
        print("\nMagnetization per site:")
        for i, mag in enumerate(outcar.magnetization):
            print(f"  Site {i}: {mag['tot']:.3f} μB")
        
        total_mag = sum(m['tot'] for m in outcar.magnetization)
        print(f"\nTotal magnetization: {total_mag:.3f} μB")
        print(f"Magnetization per atom: {total_mag / len(vasprun.final_structure):.3f} μB")
```

### 7. Band Structure Visualization

Create publication-quality band structure plots.

```python
from pymatgen.electronic_structure.plotter import BSPlotter
from pymatgen.electronic_structure.bandstructure import BandStructure
import matplotlib.pyplot as plt
import numpy as np

def plot_band_structure(bs, output_file="band_structure.png", 
                        ylim=(-5, 5), highlight_gap=True):
    """
    Create publication-quality band structure plot
    """
    plotter = BSPlotter(bs)
    
    # Get plot
    plt.figure(figsize=(10, 6))
    plt_obj = plotter.get_plot()
    
    # Customize
    ax = plt.gca()
    ax.set_ylim(ylim)
    ax.set_ylabel('Energy (eV)')
    ax.axhline(0, color='black', linestyle='-', linewidth=0.5)
    
    # Highlight band gap
    if highlight_gap and not bs.is_metal():
        band_gap = bs.get_band_gap()
        gap = band_gap['energy']
        
        # Add gap annotation
        vbm = bs.get_vbm()['energy']
        cbm = bs.get_cbm()['energy']
        
        # Find position for annotation
        kpoints = bs.kpoints
        mid_k = len(kpoints) // 2
        
        ax.annotate(f'E$_g$ = {gap:.2f} eV',
                   xy=(mid_k, (vbm + cbm) / 2),
                   ha='center', fontsize=12,
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_file}")

# Combined DOS + Band Structure plot
def plot_bs_dos_combined(bs, dos, output_file="bs_dos.png"):
    """
    Combined band structure and DOS plot
    """
    from pymatgen.electronic_structure.plotter import BSDOSPlotter
    
    plotter = BSDOSPlotter(bs_projection=None, dos_projection='elements')
    plt_obj = plotter.get_plot(bs, dos)
    plt_obj.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"Saved: {output_file}")

# Usage
plot_band_structure(bs, "band_structure_detailed.png")
plot_bs_dos_combined(bs, dos, "bs_dos_combined.png")
```

## Common Workflows

### Workflow 1: Complete Electronic Structure Analysis

```python
"""
Complete electronic structure analysis pipeline
"""
from pymatgen.io.vasp import Vasprun, BSVasprun
from pymatgen.electronic_structure.plotter import BSPlotter, DosPlotter
import json

def analyze_electronic_structure(calc_dir, output_dir="./analysis"):
    """
    Complete analysis of electronic structure
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    results = {}
    
    # 1. Parse DOS calculation
    print("[1/5] Analyzing DOS...")
    dos_vasprun = Vasprun(os.path.join(calc_dir, "vasprun.xml"))
    dos = dos_vasprun.complete_dos
    
    results['fermi_energy'] = dos.efermi
    results['dos_gap'] = dos.get_gap()
    results['cbm'] = dos.get_cbm_vbm()[0]
    results['vbm'] = dos.get_cbm_vbm()[1]
    
    # 2. Parse Band Structure
    print("[2/5] Analyzing band structure...")
    bs_vasprun = BSVasprun(os.path.join(calc_dir, "vasprun.xml"))
    bs = bs_vasprun.get_band_structure()
    
    band_gap = bs.get_band_gap()
    results['band_gap'] = band_gap['energy']
    results['is_direct'] = band_gap['direct']
    results['is_metal'] = bs.is_metal()
    
    # 3. Generate visualizations
    print("[3/5] Generating plots...")
    
    # DOS plot
    plotter = DosPlotter(sigma=0.05)
    plotter.add_dos("Total", dos)
    for elem, pdos in dos.get_element_dos().items():
        plotter.add_dos(str(elem), pdos)
    plt = plotter.get_plot()
    plt.savefig(os.path.join(output_dir, "dos.png"), dpi=150)
    
    # Band structure plot
    plotter = BSPlotter(bs)
    plt = plotter.get_plot()
    plt.savefig(os.path.join(output_dir, "band_structure.png"), dpi=150)
    
    # 4. Analyze elemental contributions
    print("[4/5] Analyzing orbital contributions...")
    element_contributions = {}
    for element in dos.structure.composition.elements:
        spd_dos = dos.get_element_spd_dos(str(element))
        element_contributions[str(element)] = {
            orb.name: float(pdos.densities[Spin.up].sum())
            for orb, pdos in spd_dos.items()
        }
    results['element_contributions'] = element_contributions
    
    # 5. Save results
    print("[5/5] Saving results...")
    with open(os.path.join(output_dir, "electronic_properties.json"), "w") as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("\n" + "=" * 50)
    print("ELECTRONIC STRUCTURE SUMMARY")
    print("=" * 50)
    print(f"Band gap: {results['band_gap']:.3f} eV")
    print(f"Direct gap: {results['is_direct']}")
    print(f"Is metal: {results['is_metal']}")
    print(f"VBM: {results['vbm']:.3f} eV")
    print(f"CBM: {results['cbm']:.3f} eV")
    print(f"\nResults saved to {output_dir}")
    
    return results

# Usage
results = analyze_electronic_structure("./dft_calc")
```

### Workflow 2: High-Throughput Screening

```python
"""
High-throughput screening of electronic properties
"""
from pymatgen.io.vasp import Vasprun
import os
import json
from pathlib import Path

def screen_materials(calc_dirs, output_file="screening_results.json"):
    """
    Screen multiple materials for electronic properties
    """
    results = []
    
    for calc_dir in calc_dirs:
        try:
            vasprun = Vasprun(os.path.join(calc_dir, "vasprun.xml"))
            
            # Extract key properties
            result = {
                "material": Path(calc_dir).name,
                "formula": vasprun.final_structure.composition.reduced_formula,
                "band_gap": vasprun.eigenvalue_band_properties[0],
                "cbm": vasprun.eigenvalue_band_properties[1],
                "vbm": vasprun.eigenvalue_band_properties[2],
                "is_metal": vasprun.eigenvalue_band_properties[0] == 0,
                "converged": vasprun.converged
            }
            
            # Check for magnetic properties
            if vasprun.is_spin:
                result["spin_polarized"] = True
            
            results.append(result)
            print(f"✓ {result['formula']}: Eg = {result['band_gap']:.2f} eV")
            
        except Exception as e:
            print(f"✗ {calc_dir}: {str(e)[:50]}")
    
    # Save results
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    # Summary statistics
    gaps = [r['band_gap'] for r in results if r['band_gap'] > 0]
    metals = [r for r in results if r['is_metal']]
    
    print(f"\n{'='*50}")
    print("SCREENING SUMMARY")
    print(f"{'='*50}")
    print(f"Total materials: {len(results)}")
    print(f"Metals: {len(metals)}")
    print(f"Semiconductors: {len(gaps)}")
    if gaps:
        print(f"Gap range: {min(gaps):.2f} - {max(gaps):.2f} eV")
        print(f"Mean gap: {sum(gaps)/len(gaps):.2f} eV")
    
    return results

# Usage
calc_dirs = ["./calc_1", "./calc_2", "./calc_3"]
results = screen_materials(calc_dirs)
```

### Workflow 3: Defect State Analysis

```python
"""
Analyze defect states in semiconductors
"""
from pymatgen.io.vasp import Vasprun
from pymatgen.electronic_structure.plotter import DosPlotter
import matplotlib.pyplot as plt
import numpy as np

def analyze_defect_states(bulk_vasprun, defect_vasprun, output_dir="./defect_analysis"):
    """
    Compare electronic structure of bulk and defect systems
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # Parse calculations
    bulk_dos = bulk_vasprun.complete_dos
    defect_dos = defect_vasprun.complete_dos
    
    # Get band gaps
    bulk_gap = bulk_dos.get_gap()
    defect_gap = defect_dos.get_gap()
    
    # Align Fermi levels (assuming bulk VBM reference)
    vbm_shift = defect_dos.get_cbm_vbm()[1] - bulk_dos.get_cbm_vbm()[1]
    
    print(f"Bulk band gap: {bulk_gap:.3f} eV")
    print(f"Defect band gap: {defect_gap:.3f} eV")
    print(f"VBM shift: {vbm_shift:.3f} eV")
    
    # Plot comparison
    fig, axes = plt.subplots(2, 1, figsize=(8, 10))
    
    energies = bulk_dos.energies - bulk_dos.efermi
    axes[0].fill_between(energies, bulk_dos.densities[Spin.up], alpha=0.5, label='Bulk')
    axes[0].axvline(0, color='k', linestyle='--')
    axes[0].set_ylabel('DOS (states/eV)')
    axes[0].set_title('Bulk DOS')
    axes[0].legend()
    
    energies = defect_dos.energies - defect_dos.efermi
    axes[1].fill_between(energies, defect_dos.densities[Spin.up], alpha=0.5, label='Defect', color='red')
    axes[1].axvline(0, color='k', linestyle='--')
    axes[1].set_xlabel('Energy (eV)')
    axes[1].set_ylabel('DOS (states/eV)')
    axes[1].set_title('Defect DOS')
    axes[1].legend()
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "defect_comparison.png"), dpi=150)
    
    # Identify defect states
    defect_states = []
    for i, (E, dos_val) in enumerate(zip(defect_dos.energies, defect_dos.densities[Spin.up])):
        E_relative = E - defect_dos.efermi
        # Check if in band gap region
        if -defect_gap/2 < E_relative < defect_gap/2 and dos_val > 0.1:
            defect_states.append({
                'energy': E_relative,
                'dos': dos_val
            })
    
    print(f"\nPotential defect states: {len(defect_states)}")
    for state in defect_states[:5]:  # Top 5
        print(f"  E = {state['energy']:.3f} eV, DOS = {state['dos']:.2f}")
    
    return {
        'bulk_gap': bulk_gap,
        'defect_gap': defect_gap,
        'vbm_shift': vbm_shift,
        'defect_states': defect_states
    }

# Usage
# bulk_vasprun = Vasprun("./bulk/vasprun.xml")
# defect_vasprun = Vasprun("./defect/vasprun.xml")
# results = analyze_defect_states(bulk_vasprun, defect_vasprun)
```

## Best Practices

### DOS Analysis
1. **Use Gaussian smearing**: Apply σ = 0.05-0.1 eV for smooth plots
2. **Check convergence**: Ensure k-point grid is converged for DOS
3. **Verify gap**: Compare DOS gap with band structure gap
4. **Analyze orbital character**: Use PDOS to understand bonding

### Band Structure Analysis
1. **High-symmetry paths**: Use standard paths for your crystal system
2. **Dense k-points**: Use at least 40 points between high-symmetry points
3. **Check for dispersion**: Flat bands indicate localized states
4. **Compare methods**: Cross-check with experimental values when available

### Charge Density
1. **Check normalization**: Ensure total charge equals number of electrons
2. **Use appropriate grid**: Finer grids for detailed analysis
3. **Differential density**: Always calculate for interface/bonding analysis
4. **Visualization**: Use logarithmic scale for small features

### Convergence
1. **k-points**: Converge with respect to total energy and forces
2. **ENCUT**: Converge to 1 meV/atom accuracy
3. **Vacuum**: Use at least 15 Å for slab calculations
4. **Validation**: Compare with literature or experimental values

## Troubleshooting

**Band gap is zero when it shouldn't be:**
- Check if calculation is metallic (is_metal())
- Verify k-point density is sufficient
- Check for smearing (ISMEAR) - use ISMEAR = 0 or -5 for insulators

**DOS doesn't match band structure:**
- Ensure calculations use same k-point mesh density
- Check Fermi level alignment
- Verify same functional used

**Charge density looks wrong:**
- Check CHGCAR is from converged calculation
- Verify correct structure file used
- Ensure normalization is correct

## Additional Resources

- **pymatgen electronic structure**: https://pymatgen.org/pymatgen.electronic_structure.html
- **Materials Project**: https://materialsproject.org/
- **VASP manual**: https://www.vasp.at/wiki/
- **DFT best practices**: https://wiki.fysik.dtu.dk/gpaw/

## Version Notes

- Requires pymatgen >= 2023.x
- Compatible with VASP 5.4+ and 6.x
- Python 3.10 or higher recommended
- Some features require additional dependencies (boltztrap2)
