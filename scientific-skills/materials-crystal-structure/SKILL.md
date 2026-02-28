---
name: materials-crystal-structure
description: Crystal structure analysis and manipulation using pymatgen. Parse CIF/POSCAR files, analyze symmetry, generate supercells, visualize structures, and perform structural transformations for computational materials science.
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# Materials Crystal Structure

## Overview

A specialized skill for crystal structure analysis, manipulation, and visualization. Parse and convert between CIF, POSCAR, XYZ, and other formats. Analyze crystal symmetry, space groups, and coordination environments. Generate supercells, slabs, and interfaces. Perfect for preparing structures for DFT calculations and analyzing structural properties.

## When to Use This Skill

This skill should be used when:
- Parsing and analyzing CIF files from crystallographic databases
- Converting between crystal structure formats (CIF ↔ POSCAR ↔ XYZ)
- Analyzing crystal symmetry and determining space groups
- Generating supercells for computational modeling
- Creating surface slabs and interfaces
- Analyzing coordination environments and bond distances
- Preparing structures for VASP, Quantum ESPRESSO, or other DFT codes
- Visualizing crystal structures in 2D and 3D
- Performing structural transformations (substitutions, defects)
- Calculating lattice parameters and unit cell properties

## Quick Start Guide

### Installation

```bash
# Core dependencies
uv pip install pymatgen matplotlib numpy

# For advanced visualization
uv pip install pymatgen[vis] nglview

# For structure matching
uv pip install pymatgen[analysis]
```

### Basic Structure Parsing

```python
from pymatgen.core import Structure, Lattice
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

# Parse CIF file
struct = Structure.from_file("structure.cif")

# Parse VASP POSCAR
struct = Structure.from_file("POSCAR")

# Basic properties
print(f"Formula: {struct.composition.reduced_formula}")
print(f"Lattice: a={struct.lattice.a:.4f} Å")
print(f"Volume: {struct.volume:.2f} Å³")

# Symmetry analysis
sga = SpacegroupAnalyzer(struct)
print(f"Space group: {sga.get_space_group_symbol()}")
print(f"Crystal system: {sga.get_crystal_system()}")
```

### Format Conversion

```python
# CIF to POSCAR
struct = Structure.from_file("input.cif")
struct.to(filename="POSCAR", fmt="poscar")

# POSCAR to CIF
struct = Structure.from_file("POSCAR")
struct.to(filename="output.cif", fmt="cif")

# To XYZ (for molecules)
from pymatgen.core import Molecule
mol = Molecule.from_file("molecule.xyz")
mol.to(filename="molecule.cif")
```

## Core Capabilities

### 1. Structure Parsing and I/O

Read and write crystal structures in multiple formats.

**Supported formats:**
- **Crystallographic**: CIF, CIF2, CFG
- **VASP**: POSCAR, CONTCAR, CHGCAR
- **Quantum ESPRESSO**: PWscf input/output
- **Molecular**: XYZ, PDB, Mol, SDF
- **Other**: CSSR, JSON, VESTA, XTL

```python
# Automatic format detection
struct = Structure.from_file("structure.cif")

# Explicit format specification
struct = Structure.from_file("data.txt", fmt="cif")

# Write to specific format
struct.to(filename="output.vasp", fmt="poscar")
struct.to(filename="output.json", fmt="json")
```

**Batch conversion:**
```python
import os
from pathlib import Path

# Convert all CIF files to POSCAR
cif_dir = Path("./cif_files")
output_dir = Path("./poscar_files")
output_dir.mkdir(exist_ok=True)

for cif_file in cif_dir.glob("*.cif"):
    struct = Structure.from_file(cif_file)
    output_file = output_dir / f"{cif_file.stem}.vasp"
    struct.to(filename=output_file, fmt="poscar")
    print(f"Converted: {cif_file.name}")
```

### 2. Symmetry Analysis

Determine space groups, crystal systems, and symmetry operations.

```python
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

sga = SpacegroupAnalyzer(struct, symprec=0.01)

# Space group information
space_group = sga.get_space_group_symbol()
space_group_number = sga.get_space_group_number()
crystal_system = sga.get_crystal_system()

print(f"Space Group: {space_group} ({space_group_number})")
print(f"Crystal System: {crystal_system}")
print(f"Point Group: {sga.get_point_group_symbol()}")

# Get primitive cell
primitive = sga.get_primitive_standard_structure()

# Get conventional cell
conventional = sga.get_conventional_standard_structure()

# Symmetry operations
sym_ops = sga.get_symmetry_operations()
print(f"Number of symmetry operations: {len(sym_ops)}")
```

### 3. Supercell Generation

Create supercells for computational modeling.

```python
from pymatgen.transformations.standard_transformations import SupercellTransformation

# 2x2x2 supercell
trans = SupercellTransformation([[2, 0, 0], [0, 2, 0], [0, 0, 2]])
supercell = trans.apply_transformation(struct)

# Custom supercell (2x2x1)
trans = SupercellTransformation([[2, 0, 0], [0, 2, 0], [0, 0, 1]])
supercell = trans.apply_transformation(struct)

# Write supercell
supercell.to(filename="supercell_222.vasp")

# Get supercell properties
print(f"Original sites: {len(struct)}")
print(f"Supercell sites: {len(supercell)}")
print(f"Volume ratio: {supercell.volume / struct.volume:.1f}x")
```

### 4. Surface and Slab Generation

Create surface slabs for surface science calculations.

```python
from pymatgen.core.surface import SlabGenerator, get_symmetrically_distinct_miller_indices

# Find distinct Miller indices
miller_indices = get_symmetrically_distinct_miller_indices(struct, max_index=2)
print(f"Distinct Miller indices (max=2): {miller_indices}")

# Generate (111) slab
slabgen = SlabGenerator(
    struct,
    miller_index=(1, 1, 1),
    min_slab_size=15.0,      # Minimum slab thickness (Å)
    min_vacuum_size=15.0,    # Minimum vacuum thickness (Å)
    center_slab=True,        # Center the slab
    lll_reduce=True          # Apply LLL reduction
)

# Get all unique terminations
slabs = slabgen.get_slabs()
print(f"Found {len(slabs)} unique slabs")

# Write slabs
for i, slab in enumerate(slabs):
    slab.to(filename=f"slab_111_{i}.vasp")
    print(f"Slab {i}: {len(slab)} sites, surface area: {slab.surface_area:.2f} Å²")
```

### 5. Coordination Environment Analysis

Analyze local coordination environments and bond distances.

```python
from pymatgen.analysis.local_env import CrystalNN, VoronoiNN

# Method 1: CrystalNN (recommended)
cnn = CrystalNN()

# Get coordination for each site
for i, site in enumerate(struct):
    neighbors = cnn.get_nn_info(struct, i)
    coordination = len(neighbors)
    
    print(f"Site {i} ({site.species_string}):")
    print(f"  Coordination number: {coordination}")
    
    for neighbor in neighbors:
        site_idx = neighbor['site_index']
        weight = neighbor['weight']
        distance = struct[i].distance(struct[site_idx])
        print(f"  - {struct[site_idx].species_string}: {distance:.3f} Å (weight: {weight:.3f})")

# Method 2: VoronoiNN (geometric approach)
vnn = VoronoiNN()
coord_numbers = [len(vnn.get_nn(struct, i)) for i in range(len(struct))]
print(f"Coordination numbers: {coord_numbers}")
```

### 6. Structural Transformations

Apply various transformations to structures.

```python
from pymatgen.transformations.standard_transformations import (
    SubstitutionTransformation,
    RemoveSitesTransformation,
    AutoOxiStateDecorationTransformation
)

# Element substitution
trans = SubstitutionTransformation({"Fe": "Mn"})
doped_struct = trans.apply_transformation(struct)

# Create vacancy (remove site 0)
trans = RemoveSitesTransformation([0])
defect_struct = trans.apply_transformation(struct)

# Auto-assign oxidation states
trans = AutoOxiStateDecorationTransformation()
oxi_struct = trans.apply_transformation(struct)

# View oxidation states
for site in oxi_struct:
    print(f"{site.species_string}: {site.specie.oxi_state}")
```

### 7. Structure Visualization

Visualize crystal structures.

```python
from pymatgen.vis.structure_vtk import StructureVis
import matplotlib.pyplot as plt
from pymatgen.electronic_structure.plotter import plot_lattice

# Simple matplotlib visualization
fig, ax = plt.subplots(figsize=(8, 8))

# Plot unit cell
lattice = struct.lattice
ax.plot([0, lattice.a], [0, 0], 'k-', linewidth=2)
ax.plot([0, 0], [0, lattice.b], 'k-', linewidth=2)

# Plot atoms (projected to xy plane)
for site in struct:
    x, y, z = site.frac_coords
    x_cart = x * lattice.a + y * lattice.b * np.cos(np.radians(lattice.gamma))
    y_cart = y * lattice.b * np.sin(np.radians(lattice.gamma))
    
    color = 'red' if site.species_string == 'O' else 'blue' if site.species_string == 'Si' else 'gray'
    ax.scatter(x_cart, y_cart, s=200, c=color, edgecolors='black')

ax.set_aspect('equal')
ax.set_title(f"{struct.composition.reduced_formula} (xy projection)")
plt.savefig("structure_xy.png", dpi=150)
```

### 8. Structure Comparison and Matching

Compare and match crystal structures.

```python
from pymatgen.analysis.structure_matcher import StructureMatcher

# Create matcher with tolerances
matcher = StructureMatcher(
    ltol=0.2,    # Lattice tolerance
    stol=0.3,    # Site tolerance
    angle_tol=5  # Angle tolerance
)

# Compare two structures
struct1 = Structure.from_file("structure1.cif")
struct2 = Structure.from_file("structure2.cif")

# Check if structures match
is_match = matcher.fit(struct1, struct2)
print(f"Structures match: {is_match}")

# Get RMS distance if they match
if is_match:
    rms = matcher.get_rms_dist(struct1, struct2)
    print(f"RMS distance: {rms}")

# Group similar structures
structures = [Structure.from_file(f"struct_{i}.cif") for i in range(10)]
groups = matcher.group_structures(structures)
print(f"Found {len(groups)} unique structure groups")
```

## Common Workflows

### Workflow 1: Database Structure Preprocessing

```python
"""
Process structures from a database for high-throughput calculations.
- Parse CIF files
- Analyze symmetry
- Generate supercells
- Convert to VASP format
"""
from pathlib import Path
from pymatgen.core import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.transformations.standard_transformations import SupercellTransformation

# Setup paths
input_dir = Path("./database_cifs")
output_dir = Path("./processed_structures")
output_dir.mkdir(exist_ok=True)

# Process each CIF
for cif_file in input_dir.glob("*.cif"):
    try:
        # Parse structure
        struct = Structure.from_file(cif_file)
        
        # Analyze symmetry
        sga = SpacegroupAnalyzer(struct)
        sg = sga.get_space_group_symbol()
        
        # Get primitive cell for efficiency
        primitive = sga.get_primitive_standard_structure()
        
        # Generate 2x2x2 supercell if primitive is too small
        if len(primitive) < 10:
            trans = SupercellTransformation([[2, 0, 0], [0, 2, 0], [0, 0, 2]])
            final_struct = trans.apply_transformation(primitive)
        else:
            final_struct = primitive
        
        # Write to VASP format
        formula = final_struct.composition.reduced_formula
        output_file = output_dir / f"{formula}_{sg.replace('/', '_')}.vasp"
        final_struct.to(filename=output_file, fmt="poscar")
        
        print(f"✓ Processed: {cif_file.name} → {output_file.name}")
        
    except Exception as e:
        print(f"✗ Failed: {cif_file.name} - {e}")
```

### Workflow 2: Surface Science Preparation

```python
"""
Generate surface slabs for catalysis calculations.
- Generate multiple Miller index surfaces
- Create symmetric and asymmetric slabs
- Analyze surface terminations
"""
from pymatgen.core import Structure
from pymatgen.core.surface import SlabGenerator, get_symmetrically_distinct_miller_indices

# Load bulk structure
bulk = Structure.from_file("bulk.cif")

# Find distinct Miller indices up to (2,2,2)
miller_indices = get_symmetrically_distinct_miller_indices(bulk, max_index=2)

# Generate slabs for each Miller index
for miller in miller_indices[:5]:  # Top 5 surfaces
    print(f"\nGenerating {miller} surface...")
    
    slabgen = SlabGenerator(
        bulk,
        miller_index=miller,
        min_slab_size=12.0,
        min_vacuum_size=15.0,
        center_slab=True
    )
    
    slabs = slabgen.get_slabs()
    
    for i, slab in enumerate(slabs):
        # Check if symmetric
        is_symmetric = slab.is_symmetric()
        
        filename = f"slab_{miller[0]}{miller[1]}{miller[2]}_{i}.vasp"
        slab.to(filename=filename)
        
        print(f"  {filename}: {len(slab)} atoms, symmetric={is_symmetric}")
```

### Workflow 3: Defect Structure Generation

```python
"""
Generate point defect structures (vacancies, substitutions).
"""
from pymatgen.core import Structure
from pymatgen.transformations.standard_transformations import (
    SubstitutionTransformation, RemoveSitesTransformation
)
import numpy as np

# Load structure
struct = Structure.from_file("structure.cif")

# Generate vacancy structures
vacancy_structs = []
for i, site in enumerate(struct):
    trans = RemoveSitesTransformation([i])
    defect_struct = trans.apply_transformation(struct)
    formula = defect_struct.composition.reduced_formula
    defect_struct.to(filename=f"vacancy_{site.species_string}_{i}.vasp")
    vacancy_structs.append(defect_struct)

# Generate substitution structures (e.g., Si doped with P)
dopants = {"Si": "P", "Si": "B"}  # n-type and p-type
for orig, dopant in dopants.items():
    # Find first occurrence
    for i, site in enumerate(struct):
        if site.species_string == orig:
            trans = SubstitutionTransformation({orig: dopant})
            doped = trans.apply_transformation(struct)
            doped.to(filename=f"doped_{orig}_{dopant}_{i}.vasp")
            break

print(f"Generated {len(vacancy_structs)} vacancy structures and 2 doped structures")
```

## Best Practices

### Structure Parsing
1. **Use automatic format detection**: `Structure.from_file()` handles most formats
2. **Check for parsing errors**: Wrap in try-except for batch processing
3. **Validate structures**: Check for negative volume or overlapping atoms
4. **Preserve metadata**: Use `as_dict()`/`from_dict()` for serialization

### Symmetry Analysis
1. **Choose appropriate symprec**: 0.01 Å for precise structures, 0.1 Å for noisy data
2. **Use primitive cells**: Reduce computation time for periodic calculations
3. **Check space group consistency**: Verify against literature values

### Supercell Generation
1. **Size considerations**: Balance accuracy vs. computational cost
2. **Use primitive cells first**: Generate supercells from primitive structures
3. **Check periodicity**: Ensure supercell maintains original symmetry

### Surface Generation
1. **Check slab polarity**: Avoid polar surfaces unless specifically studying them
2. **Symmetric slabs**: Use for accurate surface energy calculations
3. **Vacuum size**: Minimum 15 Å to avoid spurious interactions

## Units and Conventions

- **Lengths**: Angstroms (Å)
- **Angles**: Degrees (°)
- **Volume**: Cubic angstroms (Å³)
- **Fractional coordinates**: 0 to 1 range
- **Cartesian coordinates**: Å

## Troubleshooting

**CIF parsing errors:**
```python
# Try different parser settings
from pymatgen.io.cif import CifParser
parser = CifParser("problematic.cif", occupancy_tolerance=1.0)
struct = parser.get_structures()[0]
```

**Symmetry detection fails:**
```python
# Adjust tolerance
sga = SpacegroupAnalyzer(struct, symprec=0.1, angle_tolerance=5)
```

**Structure visualization issues:**
```python
# Ensure proper element symbols
print([site.species_string for site in struct])
```

## Additional Resources

- **pymatgen documentation**: https://pymatgen.org/
- **Crystallographic databases**: ICSD, Materials Project, AFLOW
- **CIF format specification**: https://www.iucr.org/resources/cif

## Version Notes

- Requires pymatgen >= 2023.x
- Python 3.10 or higher recommended
- Compatible with VASP 5.x and 6.x
