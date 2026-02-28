---
name: materials-crystal-structure
description: Crystal structure analysis and visualization using pymatgen. Parse CIF files, calculate lattice parameters, and generate structure visualizations for materials science research.
homepage: https://pymatgen.org
metadata: {"clawdbot":{"emoji":"🔮","requires":{"bins":["python3"],"env":["PMG_VASP_PSP_DIR"]},"primaryEnv":"PMG_VASP_PSP_DIR"}}
---

# Materials Crystal Structure

Crystal structure analysis and visualization using pymatgen. Parse CIF files, calculate lattice parameters, and generate structure visualizations.

## Prerequisites

```bash
# Install pymatgen
pip install pymatgen

# Optional: Install additional dependencies for visualization
pip install plotly nglview matplotlib
```

## Quick Start

### Parse CIF File

```python
from pymatgen.core import Structure
from pymatgen.io.cif import CifParser

# Load structure from CIF file
parser = CifParser("structure.cif")
structure = parser.parse_structures()[0]

# Or directly
structure = Structure.from_file("structure.cif")
print(f"Formula: {structure.formula}")
print(f"Lattice: {structure.lattice}")
```

### Calculate Lattice Parameters

```python
from pymatgen.core import Lattice

# Get lattice parameters
lattice = structure.lattice

print(f"a = {lattice.a:.4f} Å")
print(f"b = {lattice.b:.4f} Å")
print(f"c = {lattice.c:.4f} Å")
print(f"α = {lattice.alpha:.2f}°")
print(f"β = {lattice.beta:.2f}°")
print(f"γ = {lattice.gamma:.2f}°")
print(f"Volume = {lattice.volume:.2f} Å³")
print(f"Density = {structure.density:.3f} g/cm³")
```

### Structure Visualization

```python
from pymatgen.vis.structure_vtk import StructureVis
import matplotlib.pyplot as plt
from pymatgen.electronic_structure.plotter import plot_brillouin_zone

# Matplotlib visualization
from pymatgen.analysis.structure_analyzer import get_dimensionality

# Create simple 2D plot
fig, ax = plt.subplots(figsize=(8, 8))
for site in structure:
    ax.scatter(site.frac_coords[0], site.frac_coords[1], 
               s=200, label=site.species_string)
ax.set_xlabel('x (fractional)')
ax.set_ylabel('y (fractional)')
ax.set_title(f'{structure.formula} - Unit Cell')
ax.set_aspect('equal')
ax.legend()
plt.savefig('structure_2d.png', dpi=150)
```

## Common Workflows

### Analyze Crystal System

```python
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

# Get space group information
sga = SpacegroupAnalyzer(structure)
space_group = sga.get_space_group_symbol()
space_group_number = sga.get_space_group_number()
crystal_system = sga.get_crystal_system()

print(f"Space Group: {space_group} ({space_group_number})")
print(f"Crystal System: {crystal_system}")
print(f"Point Group: {sga.get_point_group_symbol()}")

# Get primitive vs conventional cell
primitive = sga.get_primitive_standard_structure()
conventional = sga.get_conventional_standard_structure()
```

### Calculate Atomic Distances and Angles

```python
from pymatgen.analysis.local_env import CrystalNN

# Find nearest neighbors
cnn = CrystalNN()
for i, site in enumerate(structure):
    neighbors = cnn.get_nn_info(structure, i)
    print(f"Site {i} ({site.species_string}):")
    for n in neighbors:
        dist = structure.get_distance(i, n['site_index'])
        print(f"  - {n['site'].species_string} at {dist:.3f} Å")
```

### Supercell Generation

```python
# Create 2x2x2 supercell
supercell = structure * (2, 2, 2)
print(f"Supercell formula: {supercell.formula}")
print(f"Supercell sites: {len(supercell)}")

# Save to file
supercell.to("cif", "supercell.cif")
```

### Batch Process Multiple Structures

```python
import os
import pandas as pd

results = []
for filename in os.listdir("structures/"):
    if filename.endswith(".cif"):
        struct = Structure.from_file(f"structures/{filename}")
        sga = SpacegroupAnalyzer(struct)
        
        results.append({
            'filename': filename,
            'formula': struct.formula,
            'space_group': sga.get_space_group_symbol(),
            'a': struct.lattice.a,
            'b': struct.lattice.b,
            'c': struct.lattice.c,
            'volume': struct.lattice.volume,
            'density': struct.density
        })

df = pd.DataFrame(results)
df.to_csv('structure_analysis.csv', index=False)
```

## Advanced Features

### Structure Matching

```python
from pymatgen.analysis.structure_matcher import StructureMatcher

# Compare two structures
matcher = StructureMatcher()
is_match = matcher.fit(structure1, structure2)
rms_distance = matcher.get_rms_dist(structure1, structure2)
```

### Defect Generation

```python
from pymatgen.analysis.defects.generators import VacancyGenerator

# Generate vacancies
vac_gen = VacancyGenerator(structure)
vacancies = list(vac_gen)

for vac in vacancies:
    print(f"Vacancy at {vac.site.species_string} site")
```

### Diffraction Pattern

```python
from pymatgen.analysis.diffraction.xrd import XRDCalculator

# Calculate XRD pattern
xrd_calc = XRDCalculator()
pattern = xrd_calc.get_pattern(structure)

# Plot XRD
xrd_calc.show_plot(structure)
```

## Best Practices

1. **Always validate CIF files** - Check for parsing errors with `CifParser`
2. **Use SpacegroupAnalyzer** - Get standardized structures for consistent comparisons
3. **Check for warnings** - pymatgen may emit warnings for unusual structures
4. **Save intermediate results** - Structure objects can be serialized with `as_dict()`
5. **Memory management** - Large supercells can consume significant RAM

## References

- [pymatgen Documentation](https://pymatgen.org)
- [Materials Project](https://materialsproject.org)
- [Bilbao Crystallographic Server](https://www.cryst.ehu.es)
