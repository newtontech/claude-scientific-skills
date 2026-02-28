---
name: materials-vasp-workflow
description: Complete VASP workflow management - generate inputs (INCAR, KPOINTS, POSCAR), parse outputs (OUTCAR, vasprun.xml), monitor calculations, extract properties, and automate high-throughput DFT workflows.
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# Materials VASP Workflow

## Overview

A comprehensive skill for managing Vienna Ab initio Simulation Package (VASP) calculations. Generate optimized input files (INCAR, KPOINTS, POTCAR), parse output files (OUTCAR, vasprun.xml), extract computed properties, monitor calculation progress, and automate high-throughput DFT workflows. Streamline your computational materials science research with intelligent workflow management.

## When to Use This Skill

This skill should be used when:
- Setting up VASP calculations for materials systems
- Generating optimized INCAR, KPOINTS, and POTCAR files
- Parsing VASP output files and extracting results
- Monitoring running VASP calculations
- Automating relaxation, static, and band structure workflows
- Extracting energies, forces, stresses, and electronic properties
- Managing high-throughput DFT calculations
- Converging k-point grids and plane-wave cutoffs
- Setting up spin-polarized and HSE calculations
- Managing VASP input sets for different calculation types

## Quick Start Guide

### Installation

```bash
# Core dependencies
uv pip install pymatgen custodian

# For advanced workflows
uv pip install atomate fireworks
```

### Basic Input Generation

```python
from pymatgen.io.vasp.sets import MPRelaxSet, MPStaticSet
from pymatgen.core import Structure

# Load structure
struct = Structure.from_file("POSCAR")

# Generate relaxation inputs
relax_set = MPRelaxSet(struct)
relax_set.write_input("./relax_calc")

print("✓ Generated VASP inputs in ./relax_calc")
print(f"  - INCAR: {relax_set.incar}")
print(f"  - KPOINTS: {relax_set.kpoints}")
```

### Parsing VASP Outputs

```python
from pymatgen.io.vasp import Vasprun, Outcar

# Parse vasprun.xml (comprehensive output)
vasprun = Vasprun("vasprun.xml")

# Get final energy
final_energy = vasprun.final_energy
print(f"Final energy: {final_energy:.6f} eV")

# Get structure
final_structure = vasprun.final_structure
print(f"Final volume: {final_structure.volume:.2f} Å³")

# Check convergence
print(f"Converged: {vasprun.converged}")
```

## Core Capabilities

### 1. Input File Generation

Generate optimized VASP input files for different calculation types.

**Standard Input Sets:**
```python
from pymatgen.io.vasp.sets import (
    MPRelaxSet,      # Structure relaxation
    MPStaticSet,     # Static SCF calculation
    MPNonSCFSet,     # Non-self-consistent (bands, DOS)
    MPHSEBSSet,      # HSE06 band structure
    MPNMRSet,        # NMR calculations
    MPMDSet          # Molecular dynamics
)
from pymatgen.core import Structure

struct = Structure.from_file("POSCAR")

# Structure relaxation
relax = MPRelaxSet(struct)
relax.write_input("./1_relax")

# Static calculation (high precision)
static = MPStaticSet(struct)
static.write_input("./2_static")

# Band structure (after static)
bands = MPNonSCFSet(struct, mode="line")
bands.write_input("./3_bands")
```

**Custom Parameters:**
```python
# Override specific INCAR parameters
custom = MPRelaxSet(
    struct,
    user_incar_settings={
        "ENCUT": 600,           # Plane-wave cutoff
        "ISMEAR": 0,            # Gaussian smearing
        "SIGMA": 0.05,          # Smearing width
        "ISPIN": 2,             # Spin-polarized
        "MAGMOM": [5, 5, -5, -5]  # Initial magnetic moments
    },
    user_kpoints_settings={
        "reciprocal_density": 100  # k-point density
    }
)
custom.write_input("./custom_calc")
```

**KPOINTS Generation:**
```python
from pymatgen.io.vasp import Kpoints

# Automatic k-point mesh
kpoints = Kpoints.automatic_density(struct, kppa=1000)
kpoints.write_file("KPOINTS")

# Gamma-centered mesh
kpoints = Kpoints.gamma_automatic(kpts=[6, 6, 6])
kpoints.write_file("KPOINTS")

# Band structure path (requires pre-computed static)
from pymatgen.symmetry.bandstructure import HighSymmKpath
kpath = HighSymmKpath(struct)
kpoints = Kpoints.automatic_linemode(divisions=40, ibz=kpath)
kpoints.write_file("KPOINTS")
```

### 2. POTCAR Management

Handle pseudopotential files.

```python
from pymatgen.io.vasp import Potcar

# Generate POTCAR for structure
potcar = Potcar.from_structure(struct)
potcar.write_file("POTCAR")

# Check POTCAR settings
print(f"POTCAR elements: {potcar.symbols}")
print(f"ENMAX values: {potcar.enmax}")

# Use specific POTCAR types
potcar = Potcar(
    symbols=["Si", "O"],
    functional="PBE"  # or "LDA", "PW91"
)
```

### 3. Output Parsing

Extract data from VASP output files.

**Vasprun Parser:**
```python
from pymatgen.io.vasp import Vasprun

vasprun = Vasprun("vasprun.xml")

# Basic properties
print(f"Final energy: {vasprun.final_energy:.6f} eV")
print(f"Converged: {vasprun.converged}")

# Ionic steps (geometry optimization)
for i, step in enumerate(vasprun.ionic_steps):
    print(f"Step {i}: E = {step['e_fr_energy']:.6f} eV")

# Final structure
final_struct = vasprun.final_structure
print(f"Final lattice: {final_struct.lattice.abc}")

# Forces (if available)
if vasprun.forces is not None:
    max_force = np.max(np.abs(vasprun.forces))
    print(f"Max force: {max_force:.4f} eV/Å")

# Stress (if available)
if vasprun.stress is not None:
    print(f"Stress tensor: {vasprun.stress}")

# Electronic properties
band_gap = vasprun.eigenvalue_band_properties[0]
print(f"Band gap: {band_gap:.3f} eV")

# Complete DOS
dos = vasprun.complete_dos
print(f"DOS fermi energy: {dos.efermi:.3f} eV")
```

**OUTCAR Parser:**
```python
from pymatgen.io.vasp import Outcar

outcar = Outcar("OUTCAR")

# Magnetization
if outcar.magnetization:
    total_mag = sum(m['tot'] for m in outcar.magnetization)
    print(f"Total magnetization: {total_mag:.3f} μB")

# NMR chemical shifts (if NMR calculation)
if outcar.chemical_shifts:
    print(f"Chemical shifts: {outcar.chemical_shifts}")

# Born effective charges (if LEPSILON=True)
if outcar.born:
    print(f"Born effective charges: {outcar.born}")

# Piezoelectric tensor
if outcar.piezo_tensor is not None:
    print(f"Piezoelectric tensor:\n{outcar.piezo_tensor}")
```

### 4. Multi-Step Workflows

Automate common VASP workflows.

**Relaxation → Static → Bands:**
```python
"""
Complete band structure workflow:
1. Structure relaxation
2. Static SCF (high precision)
3. Band structure (non-SCF)
"""
from pymatgen.io.vasp.sets import MPRelaxSet, MPStaticSet, MPNonSCFSet
from pymatgen.io.vasp import Vasprun
from pymatgen.core import Structure
import os

struct = Structure.from_file("POSCAR")

# Step 1: Relaxation
print("Step 1: Structure relaxation")
relax_set = MPRelaxSet(struct)
relax_set.write_input("./1_relax")
# ... run VASP here ...

# Step 2: Static (use converged structure)
print("\nStep 2: Static calculation")
relaxed_struct = Vasprun("./1_relax/vasprun.xml").final_structure
static_set = MPStaticSet(relaxed_struct)
static_set.write_input("./2_static")
# ... run VASP here ...

# Step 3: Band structure
print("\nStep 3: Band structure")
bands_set = MPNonSCFSet.from_prev_calc("./2_static", mode="line")
bands_set.write_input("./3_bands")
print("✓ Workflow setup complete")
```

**Convergence Testing:**
```python
"""
ENCUT convergence test
"""
from pymatgen.io.vasp.sets import MPStaticSet
from pymatgen.core import Structure

struct = Structure.from_file("POSCAR")
encut_values = [300, 400, 500, 600, 700, 800]

for encut in encut_values:
    # Create calculation directory
    calc_dir = f"encut_{encut}"
    os.makedirs(calc_dir, exist_ok=True)
    
    # Generate inputs with custom ENCUT
    static_set = MPStaticSet(
        struct,
        user_incar_settings={"ENCUT": encut}
    )
    static_set.write_input(calc_dir)
    
    print(f"✓ Generated inputs for ENCUT = {encut} eV")

print("\nRun all calculations and analyze convergence")
```

### 5. High-Throughput Workflows

Manage multiple calculations efficiently.

```python
"""
High-throughput screening workflow
"""
from pymatgen.io.vasp.sets import MPRelaxSet
from pymatgen.core import Structure
from pathlib import Path
import json

# Load multiple structures
structures_dir = Path("./structures")
results = {}

for poscar_file in structures_dir.glob("*.vasp"):
    formula = poscar_file.stem
    calc_dir = f"./calcs/{formula}"
    
    try:
        # Generate inputs
        struct = Structure.from_file(poscar_file)
        relax_set = MPRelaxSet(struct)
        relax_set.write_input(calc_dir)
        
        results[formula] = {"status": "input_generated", "path": calc_dir}
        print(f"✓ {formula}: inputs ready")
        
    except Exception as e:
        results[formula] = {"status": "error", "error": str(e)}
        print(f"✗ {formula}: {e}")

# Save status
with open("workflow_status.json", "w") as f:
    json.dump(results, f, indent=2)
```

### 6. Calculation Monitoring

Monitor running VASP calculations.

```python
"""
Monitor VASP calculation progress
"""
import os
import time
from pymatgen.io.vasp import Vasprun

def monitor_vasp(calc_dir, check_interval=60):
    """Monitor a running VASP calculation"""
    vasprun_path = os.path.join(calc_dir, "vasprun.xml")
    
    print(f"Monitoring {calc_dir}...")
    
    while True:
        if os.path.exists(vasprun_path):
            try:
                vasprun = Vasprun(vasprun_path)
                n_ionic = len(vasprun.ionic_steps)
                
                if vasprun.converged:
                    print(f"✓ Calculation converged after {n_ionic} ionic steps")
                    break
                else:
                    print(f"  Step {n_ionic}: E = {vasprun.final_energy:.6f} eV")
                    
            except Exception as e:
                print(f"  Waiting for valid vasprun.xml...")
        
        time.sleep(check_interval)

# Usage
monitor_vasp("./relax_calc")
```

### 7. Property Extraction

Extract computed properties from VASP outputs.

```python
"""
Extract comprehensive properties from VASP outputs
"""
from pymatgen.io.vasp import Vasprun, Outcar
from pymatgen.electronic_structure.core import Spin
import numpy as np

def extract_properties(calc_dir):
    """Extract all available properties from VASP calculation"""
    properties = {}
    
    # Parse vasprun.xml
    vasprun = Vasprun(os.path.join(calc_dir, "vasprun.xml"))
    
    # Energy
    properties["final_energy"] = vasprun.final_energy
    properties["final_energy_per_atom"] = vasprun.final_energy / len(vasprun.final_structure)
    
    # Structure
    properties["final_structure"] = vasprun.final_structure
    properties["volume"] = vasprun.final_structure.volume
    properties["volume_per_atom"] = vasprun.final_structure.volume / len(vasprun.final_structure)
    
    # Convergence
    properties["converged"] = vasprun.converged
    properties["n_ionic_steps"] = len(vasprun.ionic_steps)
    
    # Electronic properties
    if vasprun.eigenvalues:
        band_gap = vasprun.eigenvalue_band_properties[0]
        cbm = vasprun.eigenvalue_band_properties[1]
        vbm = vasprun.eigenvalue_band_properties[2]
        properties["band_gap"] = band_gap
        properties["cbm"] = cbm
        properties["vbm"] = vbm
    
    # Forces
    if vasprun.forces is not None:
        properties["max_force"] = np.max(np.abs(vasprun.forces))
        properties["rms_force"] = np.sqrt(np.mean(vasprun.forces**2))
    
    # Stress
    if vasprun.stress is not None:
        properties["stress"] = vasprun.stress
        properties["pressure"] = np.trace(vasprun.stress) / 3
    
    # DOS properties
    if vasprun.complete_dos:
        dos = vasprun.complete_dos
        properties["fermi_energy"] = dos.efermi
        properties["dos_gap"] = dos.get_gap()
    
    # Parse OUTCAR for additional properties
    outcar_path = os.path.join(calc_dir, "OUTCAR")
    if os.path.exists(outcar_path):
        outcar = Outcar(outcar_path)
        
        if outcar.magnetization:
            properties["total_magnetization"] = sum(m['tot'] for m in outcar.magnetization)
        
        if outcar.electrostatic_potential:
            properties["avg_electrostatic_potential"] = np.mean(outcar.electrostatic_potential)
    
    return properties

# Usage
props = extract_properties("./relax_calc")
for key, value in props.items():
    if isinstance(value, float):
        print(f"{key}: {value:.6f}")
    else:
        print(f"{key}: {value}")
```

### 8. Error Handling and Validation

Check for common VASP errors and validate inputs.

```python
"""
Validate VASP inputs and check for errors
"""
from pymatgen.io.vasp import Incar, Kpoints, Potcar, Poscar
import os

def validate_vasp_inputs(calc_dir):
    """Validate VASP input files"""
    errors = []
    warnings = []
    
    # Check required files
    required_files = ["INCAR", "KPOINTS", "POSCAR", "POTCAR"]
    for f in required_files:
        if not os.path.exists(os.path.join(calc_dir, f)):
            errors.append(f"Missing required file: {f}")
    
    if errors:
        return errors, warnings
    
    # Validate INCAR
    try:
        incar = Incar.from_file(os.path.join(calc_dir, "INCAR"))
        
        # Check required tags
        if "ENCUT" not in incar:
            warnings.append("ENCUT not set - will use POTCAR ENMAX")
        if "ISMEAR" not in incar:
            warnings.append("ISMEAR not set - using default (1)")
        
        # Check for common mistakes
        if incar.get("ISPIN", 1) == 2 and "MAGMOM" not in incar:
            warnings.append("Spin-polarized calculation without MAGMOM")
            
    except Exception as e:
        errors.append(f"Error parsing INCAR: {e}")
    
    # Validate POSCAR
    try:
        poscar = Poscar.from_file(os.path.join(calc_dir, "POSCAR"))
        struct = poscar.structure
        
        # Check for very small/large volumes
        vol_per_atom = struct.volume / len(struct)
        if vol_per_atom < 5:
            warnings.append(f"Very small volume per atom: {vol_per_atom:.2f} Å³")
        if vol_per_atom > 100:
            warnings.append(f"Very large volume per atom: {vol_per_atom:.2f} Å³")
            
    except Exception as e:
        errors.append(f"Error parsing POSCAR: {e}")
    
    # Validate POTCAR matches POSCAR
    try:
        potcar = Potcar.from_file(os.path.join(calc_dir, "POTCAR"))
        poscar = Poscar.from_file(os.path.join(calc_dir, "POSCAR"))
        
        potcar_elements = set(potcar.symbols)
        poscar_elements = set(poscar.site_symbols)
        
        if potcar_elements != poscar_elements:
            errors.append(f"POTCAR elements {potcar_elements} don't match POSCAR {poscar_elements}")
            
    except Exception as e:
        errors.append(f"Error validating POTCAR: {e}")
    
    return errors, warnings

# Usage
errors, warnings = validate_vasp_inputs("./relax_calc")

if errors:
    print("Errors:")
    for e in errors:
        print(f"  ✗ {e}")

if warnings:
    print("Warnings:")
    for w in warnings:
        print(f"  ⚠ {w}")

if not errors and not warnings:
    print("✓ All inputs validated successfully")
```

## Common Workflows

### Workflow 1: Complete DFT Calculation Pipeline

```python
"""
Complete DFT pipeline: relaxation → static → DOS → bands
"""
from pymatgen.io.vasp.sets import MPRelaxSet, MPStaticSet, MPNonSCFSet
from pymatgen.io.vasp import Vasprun
from pymatgen.core import Structure
import shutil

def full_dft_pipeline(structure_file, output_base="./dft_calc"):
    """
    Run complete DFT pipeline for a structure
    """
    struct = Structure.from_file(structure_file)
    formula = struct.composition.reduced_formula
    
    print(f"Starting DFT pipeline for {formula}")
    print("=" * 50)
    
    # Step 1: Relaxation
    print("\n[1/4] Structure Relaxation")
    relax_dir = f"{output_base}/1_relax"
    relax_set = MPRelaxSet(struct)
    relax_set.write_input(relax_dir)
    print(f"  Inputs written to {relax_dir}")
    print(f"  Run: cd {relax_dir} && mpirun vasp_std")
    
    # Step 2: Static (high precision)
    print("\n[2/4] Static Calculation")
    print("  (Run after relaxation completes)")
    static_dir = f"{output_base}/2_static"
    # Note: Use relaxed structure in practice
    static_set = MPStaticSet(struct)
    static_set.write_input(static_dir)
    print(f"  Inputs written to {static_dir}")
    
    # Step 3: DOS
    print("\n[3/4] Density of States")
    dos_dir = f"{output_base}/3_dos"
    dos_set = MPNonSCFSet(struct, mode="uniform")
    dos_set.write_input(dos_dir)
    print(f"  Inputs written to {dos_dir}")
    
    # Step 4: Band Structure
    print("\n[4/4] Band Structure")
    bands_dir = f"{output_base}/4_bands"
    bands_set = MPNonSCFSet(struct, mode="line")
    bands_set.write_input(bands_dir)
    print(f"  Inputs written to {bands_dir}")
    
    print("\n" + "=" * 50)
    print("Pipeline setup complete!")
    print(f"Run calculations in order: 1 → 2 → 3/4")

# Usage
full_dft_pipeline("POSCAR", "./Si_dft")
```

### Workflow 2: High-Throughput Formation Energy

```python
"""
High-throughput formation energy calculations
"""
from pymatgen.io.vasp.sets import MPStaticSet
from pymatgen.core import Structure, Composition
from pymatgen.ext.matproj import MPRester
import os
import json

def calculate_formation_energy(compound_file, elemental_refs):
    """
    Calculate formation energy for a compound
    elemental_refs: dict of {element: energy_per_atom}
    """
    struct = Structure.from_file(compound_file)
    formula = struct.composition.reduced_formula
    
    # Generate calculation inputs
    calc_dir = f"./formations/{formula}"
    os.makedirs(calc_dir, exist_ok=True)
    
    static_set = MPStaticSet(struct)
    static_set.write_input(calc_dir)
    
    print(f"✓ Generated inputs for {formula}")
    
    # Return metadata for later analysis
    return {
        "formula": formula,
        "composition": struct.composition.as_dict(),
        "n_atoms": len(struct),
        "calc_dir": calc_dir,
        "elemental_refs": elemental_refs
    }

# Define elemental reference energies (from separate calculations)
elemental_refs = {
    "Li": -1.908,
    "Fe": -8.336,
    "O": -4.948,
    "Si": -5.424
}

# Process multiple compounds
compounds = ["LiFeO2.vasp", "Li2O.vasp", "Fe2O3.vasp"]
metadata = []

for compound in compounds:
    if os.path.exists(compound):
        meta = calculate_formation_energy(compound, elemental_refs)
        metadata.append(meta)

# Save metadata for post-processing
with open("formation_calculations.json", "w") as f:
    json.dump(metadata, f, indent=2)

print(f"\nGenerated {len(metadata)} calculations")
print("Run all calculations, then use formation_energy_analysis.py")
```

### Workflow 3: Automatic Error Recovery

```python
"""
Automatic error detection and recovery for VASP calculations
"""
from pymatgen.io.vasp import Vasprun
import os
import shutil

def check_and_recover(calc_dir):
    """
    Check calculation status and suggest recovery actions
    """
    vasprun_path = os.path.join(calc_dir, "vasprun.xml")
    
    # Check if calculation exists
    if not os.path.exists(vasprun_path):
        return {"status": "not_started", "action": "Submit calculation"}
    
    try:
        vasprun = Vasprun(vasprun_path)
        
        if vasprun.converged:
            return {"status": "converged", "action": None}
        else:
            # Check if electronic steps are converging
            n_ionic = len(vasprun.ionic_steps)
            
            if n_ionic > 100:
                return {
                    "status": "not_converging",
                    "action": "Increase NELM or check structure",
                    "suggestion": "Edit INCAR: increase NELM, or check initial structure"
                }
            else:
                return {
                    "status": "running",
                    "action": f"Continue monitoring ({n_ionic} steps so far)"
                }
                
    except Exception as e:
        # Corrupted vasprun.xml
        return {
            "status": "corrupted",
            "action": "Restart from last CONTCAR",
            "suggestion": f"Error: {str(e)[:100]}"
        }

# Check multiple calculations
calc_dirs = ["./calc_1", "./calc_2", "./calc_3"]

for calc_dir in calc_dirs:
    result = check_and_recover(calc_dir)
    print(f"{calc_dir}: {result['status']}")
    if result['action']:
        print(f"  → {result['action']}")
```

## Best Practices

### Input Generation
1. **Start with MPRelaxSet**: Uses tested parameters for accurate results
2. **Customize when needed**: Override specific parameters for your system
3. **Check POTCAR compatibility**: Ensure POTCAR matches POSCAR elements
4. **Use appropriate k-point density**: 1000 k-points per atom is a good default

### Calculation Types
1. **Relaxation first**: Always relax structure before static calculations
2. **High precision for properties**: Use MPStaticSet for accurate energies
3. **Converge carefully**: Check convergence with multiple k-point grids
4. **Monitor forces**: Ensure forces are below 0.01 eV/Å for relaxation

### Output Analysis
1. **Check convergence**: Always verify vasprun.converged
2. **Validate energies**: Compare with literature/reference values
3. **Inspect structures**: Visualize final structures for obvious errors
4. **Check magnetic moments**: For spin-polarized calculations

### Workflow Management
1. **Organize directories**: Use clear naming (1_relax, 2_static, etc.)
2. **Save metadata**: Store calculation parameters for reproducibility
3. **Version control**: Track input files with git
4. **Backup important data**: Copy vasprun.xml before re-running

## Troubleshooting

**"Error reading POTCAR"**: Check POTCAR file exists and matches POSCAR elements

**"BRIONS problems"**: Structure may be exploding; check initial structure and ENCUT

**"ZPOTRF failed"**: Cholesky decomposition failed - check for overlapping atoms

**"Sub-Space-Matrix is not hermitian"**: Numerical precision issue - increase ENCUT

**Convergence issues:**
```python
# Try these INCAR settings
user_incar_settings = {
    "ALGO": "Normal",      # or "Fast", "All"
    "NELM": 100,           # More electronic steps
    "NELMIN": 6,           # Minimum electronic steps
    "AMIX": 0.2,           # Charge mixing parameter
    "BMIX": 0.0001,        # Charge mixing parameter
}
```

## Additional Resources

- **VASP wiki**: https://www.vasp.at/wiki/
- **pymatgen VASP docs**: https://pymatgen.org/pymatgen.io.vasp.html
- **Materials Project**: https://materialsproject.org/
- **VASP forum**: https://www.vasp.at/forum/

## Version Notes

- Requires pymatgen >= 2023.x
- Compatible with VASP 5.4+ and 6.x
- Python 3.10 or higher recommended
- Some features require VASP 6.x
