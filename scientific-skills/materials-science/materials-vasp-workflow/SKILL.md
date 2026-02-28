---
name: materials-vasp-workflow
description: VASP calculation workflow management. Generate input files (INCAR, POSCAR, KPOINTS), parse output files (OUTCAR, vasprun.xml), and automate DFT calculation workflows.
homepage: https://www.vasp.at
metadata: {"clawdbot":{"emoji":"⚡","requires":{"bins":["python3"],"env":["VASP_PP_PATH"]},"primaryEnv":"VASP_PP_PATH"}}
---

# Materials VASP Workflow

VASP (Vienna Ab initio Simulation Package) workflow management. Generate input files, parse outputs, and automate DFT calculations.

## Prerequisites

```bash
# Install pymatgen with VASP support
pip install pymatgen

# Set VASP pseudopotential directory
export VASP_PP_PATH="/path/to/pseudopotentials"

# Optional: Install custodian for automated error handling
pip install custodian
```

## Input File Generation

### INCAR Generator

```python
from pymatgen.io.vasp.inputs import Incar, Kpoints, Poscar, Potcar
from pymatgen.core import Structure

# Create INCAR for relaxation
incar = Incar({
    'ENCUT': 520,
    'ISMEAR': 0,
    'SIGMA': 0.05,
    'EDIFF': 1E-6,
    'EDIFFG': -0.01,
    'IBRION': 2,
    'ISIF': 3,
    'NSW': 100,
    'NELM': 100,
    'PREC': 'Accurate',
    'ALGO': 'Normal',
    'LREAL': False,
    'LWAVE': False,
    'LCHARG': True,
})

incar.write_file('INCAR')
```

### POSCAR from Structure

```python
from pymatgen.io.vasp import Poscar

# Load structure
structure = Structure.from_file("structure.cif")

# Create POSCAR
poscar = Poscar(structure)
poscar.write_file('POSCAR')

# With selective dynamics
from pymatgen.io.vasp.inputs import Poscar

sd = [[True, True, True] for _ in structure]
# Fix bottom layer
for i, site in enumerate(structure):
    if site.z < 0.5:
        sd[i] = [False, False, False]

poscar_sd = Poscar(structure, selective_dynamics=sd)
poscar_sd.write_file('POSCAR_sd')
```

### KPOINTS Generator

```python
from pymatgen.io.vasp.inputs import Kpoints

# Automatic k-point generation
kpoints = Kpoints.automatic_density(structure, kppa=1000)
kpoints.write_file('KPOINTS')

# Gamma-centered mesh
kpoints_gamma = Kpoints.gamma_automatic(kpts=(8, 8, 8))
kpoints_gamma.write_file('KPOINTS_gamma')

# Custom k-point path for band structure
from pymatgen.symmetry.bandstructure import HighSymmKpath

kpath = HighSymmKpath(structure)
kpoints_line = Kpoints.automatic_linemode(divisions=20, 
                                           ibz=kpath)
kpoints_line.write_file('KPOINTS_band')
```

### POTCAR Generation

```python
from pymatgen.io.vasp import Potcar

# Generate POTCAR from structure
potcar = Potcar.from_structure(structure)
potcar.write_file('POTCAR')

# Or specify symbols manually
potcar = Potcar(['Li_sv', 'Fe_pv', 'P', 'O'])
potcar.write_file('POTCAR')
```

## Output File Parsing

### Parse vasprun.xml

```python
from pymatgen.io.vasp import Vasprun

# Load calculation results
vasprun = Vasprun('vasprun.xml')

# Get final structure
final_structure = vasprun.final_structure

# Get energy
final_energy = vasprun.final_energy
print(f"Final energy: {final_energy:.4f} eV")

# Get forces
forces = vasprun.ionic_steps[-1]['forces']
print(f"Max force: {np.max(np.abs(forces)):.4f} eV/Å")

# Check convergence
print(f"Converged: {vasprun.converged}")
```

### Parse OUTCAR

```python
from pymatgen.io.vasp import Outcar

outcar = Outcar('OUTCAR')

# Get magnetization
magnetization = outcar.magnetization
print(f"Total magnetization: {outcar.total_mag:.4f} μB")

# Get CPU time
print(f"Elapsed time: {outcar.run_stats['Elapsed time (sec)']} s")

# Get stress tensor
stress = outcar.stress
```

### Parse DOSCAR

```python
from pymatgen.io.vasp import Vasprun
from pymatgen.electronic_structure.plotter import DosPlotter

# Get DOS data
vasprun = Vasprun('vasprun.xml', parse_dos=True)
cdos = vasprun.complete_dos

# Get DOS at specific energy
efermi = cdos.efermi
dos_at_fermi = cdos.get_interpolated_value(efermi)
print(f"DOS at Fermi level: {dos_at_fermi:.4f} states/eV")
```

## Workflow Automation

### Standard Relaxation Workflow

```python
import os
from pymatgen.io.vasp.sets import MPRelaxSet

# Load structure
structure = Structure.from_file("input.cif")

# Create relaxation input set
relax_set = MPRelaxSet(structure)
relax_set.write_input('relax_calc')

# Run VASP (example command)
# os.system('cd relax_calc && mpirun -np 4 vasp_std')
```

### Static Calculation after Relaxation

```python
from pymatgen.io.vasp.sets import MPStaticSet

# Load relaxed structure
relaxed_structure = Structure.from_file('relax_calc/CONTCAR')

# Create static calculation input
static_set = MPStaticSet.from_prev_calc('relax_calc')
static_set.write_input('static_calc')
```

### Band Structure Workflow

```python
from pymatgen.io.vasp.sets import MPNonSCFSet

# Create band structure calculation
band_set = MPNonSCFSet.from_prev_calc(
    'static_calc',
    mode='Uniform',
    reciprocal_density=200
)
band_set.write_input('band_calc')
```

### Batch Calculation Submission

```python
import os
import glob
from pymatgen.core import Structure
from pymatgen.io.vasp.sets import MPRelaxSet

# Process all structures
for cif_file in glob.glob("structures/*.cif"):
    basename = os.path.basename(cif_file).replace('.cif', '')
    output_dir = f"calculations/{basename}"
    
    structure = Structure.from_file(cif_file)
    
    # Create input files
    relax_set = MPRelaxSet(structure)
    relax_set.write_input(output_dir)
    
    # Create job script
    with open(f"{output_dir}/job.sh", 'w') as f:
        f.write(f"""#!/bin/bash
#SBATCH --job-name={basename}
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=4
#SBATCH --time=24:00:00

module load vasp
mpirun -np 4 vasp_std
""")
    
    print(f"Prepared: {output_dir}")
```

## Error Handling with Custodian

```python
from custodian.custodian import Custodian
from custodian.vasp.jobs import VaspJob
from custodian.vasp.handlers import (
    VaspErrorHandler, 
    NonConvergingErrorHandler,
    FrozenJobErrorHandler
)

# Setup handlers
handlers = [
    VaspErrorHandler(),
    NonConvergingErrorHandler(),
    FrozenJobErrorHandler()
]

# Create job
job = VaspJob(['mpirun', '-np', '4', 'vasp_std'])

# Run with custodian
custodian = Custodian(handlers, [job], max_errors=10)
custodian.run()
```

## Analysis Tools

### Extract Formation Energy

```python
def get_formation_energy(structure, total_energy, reference_energies):
    """
    Calculate formation energy per atom.
    
    Args:
        structure: pymatgen Structure
        total_energy: DFT total energy in eV
        reference_encies: dict of {element: energy_per_atom}
    """
    composition = structure.composition
    ref_energy = sum(
        composition[el] * reference_energies[str(el)] 
        for el in composition.elements
    )
    
    formation_energy = total_energy - ref_energy
    formation_energy_per_atom = formation_energy / len(structure)
    
    return formation_energy_per_atom
```

### Convergence Testing

```python
import numpy as np

# ENCUT convergence
cutoff_energies = [300, 400, 500, 600, 700, 800]
energies = []

for encut in cutoff_energies:
    # Run calculation with given ENCUT
    # ... (setup and run)
    vasprun = Vasprun(f'encut_{encut}/vasprun.xml')
    energies.append(vasprun.final_energy)

# Plot convergence
import matplotlib.pyplot as plt
plt.plot(cutoff_energies, energies, 'o-')
plt.xlabel('ENCUT (eV)')
plt.ylabel('Total Energy (eV)')
plt.savefig('encut_convergence.png')
```

## Best Practices

1. **ENCUT**: Set to 1.3 × max(ENMAX) of POTCARs
2. **KPOINTS**: Use automatic density for consistent accuracy
3. **Convergence**: Always check ionic and electronic convergence
4. **Pseudopotentials**: Use consistent PAW potential set
5. **Validation**: Compare with known benchmarks
6. **Backup**: Save WAVECAR for restart if needed

## Common Issues

- **IBRION=2 but not relaxing**: Check EDIFFG value
- **Memory errors**: Reduce NCORE or KPAR
- **Non-convergence**: Increase NELM or adjust ALGO
- **Missing POTCAR**: Check VASP_PP_PATH environment variable

## References

- [VASP Manual](https://www.vasp.at/wiki/index.php/The_VASP_Manual)
- [pymatgen VASP docs](https://pymatgen.org/pymatgen.io.vasp.html)
- [Custodian](https://materialsproject.github.io/custodian/)
