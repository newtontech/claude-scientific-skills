---
name: materials-molecular-dynamics
description: Molecular dynamics simulation setup and analysis. LAMMPS integration, trajectory file processing, and MD workflow automation for materials simulations.
homepage: https://www.lammps.org
metadata: {"clawdbot":{"emoji":"🔄","requires":{"bins":["python3"],"env":["LAMMPS_COMMAND"]},"primaryEnv":"LAMMPS_COMMAND"}}
---

# Materials Molecular Dynamics

Molecular dynamics (MD) simulation setup and analysis. LAMMPS integration, trajectory processing, and MD workflow automation.

## Prerequisites

```bash
# Install MDAnalysis for trajectory processing
pip install MDAnalysis MDAnalysisTests

# Install OVITO for visualization (optional)
pip install ovito

# Install LAMMPS Python interface
pip install lammps

# Or build LAMMPS from source with Python interface
```

## LAMMPS Input File Generation

### Basic MD Input

```python
from pymatgen.io.lammps.data import LammpsData
from pymatgen.io.lammps.inputs import LammpsInputFile
from pymatgen.core import Structure
import numpy as np

# Load structure
structure = Structure.from_file("structure.cif")

# Create LAMMPS data file
lammps_data = LammpsData.from_structure(structure, atom_style='atomic')
lammps_data.write_file('data.structure')

# Create input script
input_script = """
# LAMMPS input for MD simulation
units           metal
atom_style      atomic
boundary        p p p

# Read structure
read_data       data.structure

# Potential
pair_style      lj/cut 10.0
pair_coeff      * * 1.0 1.0

# Neighbor list
neighbor        0.3 bin
neigh_modify    every 1 delay 0 check yes

# Temperature
velocity        all create 300.0 12345 mom yes rot yes dist gaussian

# Thermodynamic output
thermo          100
thermo_style    custom step temp pe ke etotal press vol

# Fix
fix             1 all nvt temp 300.0 300.0 0.1

# Run
timestep        0.001
run             10000

# Output
dump            1 all atom 100 dump.atom
dump_modify     1 element Si O
write_data      final.data
"""

with open('in.md', 'w') as f:
    f.write(input_script)
```

### ReaxFF Input

```python
# Reactive MD with ReaxFF
reaxff_input = """
# ReaxFF simulation
units           real
atom_style      charge
boundary        p p p

read_data       data.structure

pair_style      reax/c lmp_control
pair_coeff      * * ffield.reax.Fe_O_C_H H O C Fe

compute         reax all pair reax/c

neighbor        2.5 bin
neigh_modify    every 10 delay 0 check no

fix             1 all nve
fix             2 all qeq/reax 1 0.0 10.0 1e-6 param.qeq
fix             3 all temp/berendsen 300.0 300.0 100.0

timestep        0.25
dump            1 all atom 100 dump.reaxff
run             100000
"""
```

### Structure to LAMMPS Data

```python
from pymatgen.io.lammps.data import LammpsData

# Convert structure with box
structure = Structure.from_file("POSCAR")

# Add box if needed (already in periodic structure)
lammps_data = LammpsData.from_structure(
    structure,
    atom_style='charge',  # or 'atomic', 'full', etc.
)

# Customize atom types
unique_elements = sorted(set([str(s.specie) for s in structure]))
element_map = {el: i+1 for i, el in enumerate(unique_elements)}

# Write with comments
lammps_data.write_file('data.lmp')
```

## Trajectory Analysis with MDAnalysis

### Load and Process Trajectory

```python
import MDAnalysis as mda
from MDAnalysis.analysis import rms, align

# Load trajectory
u = mda.Universe('data.structure', 'dump.atom', format='LAMMPSDUMP')

# Basic trajectory info
print(f"Number of atoms: {len(u.atoms)}")
print(f"Number of frames: {len(u.trajectory)}")
print(f"Time step: {u.trajectory.dt}")

# Iterate through frames
for ts in u.trajectory:
    print(f"Frame {ts.frame}, Time {ts.time:.2f} ps")
    # Access coordinates: ts.positions
```

### Calculate RMSD

```python
from MDAnalysis.analysis import rms

# Reference structure
ref = mda.Universe('data.structure', 'dump.atom', format='LAMMPSDUMP')

# Calculate RMSD
R = rms.RMSD(u, ref, select='all', groupselections=['name Si', 'name O'])
R.run()

# Get results
rmsd = R.rmsd.T  # transpose
import matplotlib.pyplot as plt
plt.plot(rmsd[1], rmsd[2], label='All')
plt.plot(rmsd[1], rmsd[3], label='Si')
plt.xlabel('Time (ps)')
plt.ylabel('RMSD (Å)')
plt.legend()
plt.savefig('rmsd.png')
```

### Radial Distribution Function (RDF)

```python
from MDAnalysis.analysis.rdf import InterRDF

# Calculate Si-O RDF
si = u.select_atoms('name Si')
o = u.select_atoms('name O')

rdf = InterRDF(si, o, nbins=100, range=(0.0, 10.0))
rdf.run()

# Plot
plt.plot(rdf.results.bins, rdf.results.rdf)
plt.xlabel('r (Å)')
plt.ylabel('g(r)')
plt.title('Si-O RDF')
plt.savefig('rdf.png')
```

### Mean Square Displacement (MSD)

```python
from MDAnalysis.analysis.msd import EinsteinMSD

# Calculate MSD
msd_analysis = EinsteinMSD(u, select='all', msd_type='xyz', fft=True)
msd_analysis.run()

# Extract data
msd = msd_analysis.results.timeseries
time = msd_analysis.time

# Calculate diffusion coefficient from slope
from scipy.stats import linregress
slope, intercept, r_value, p_value, std_err = linregress(time, msd)
diffusion_coeff = slope / 6  # 3D: factor of 6

print(f"Diffusion coefficient: {diffusion_coeff:.2e} cm²/s")

# Plot
plt.loglog(time, msd)
plt.xlabel('Time (ps)')
plt.ylabel('MSD (Å²)')
plt.savefig('msd.png')
```

### Coordination Number Analysis

```python
from MDAnalysis.analysis.rdf import InterRDF

# Define coordination shell cutoff
cutoff = 3.0  # Å

# Count neighbors for each Si
si_atoms = u.select_atoms('name Si')
coord_numbers = []

for ts in u.trajectory[::10]:  # Sample every 10 frames
    for si in si_atoms:
        # Find O atoms within cutoff
        distances = np.linalg.norm(
            u.select_atoms('name O').positions - si.position, 
            axis=1
        )
        coord_numbers.append(np.sum(distances < cutoff))

avg_coord = np.mean(coord_numbers)
print(f"Average coordination number: {avg_coord:.2f}")
```

## Temperature and Energy Analysis

```python
# Parse LAMMPS log file
def parse_lammps_log(log_file):
    """Parse thermodynamic output from LAMMPS log file."""
    data = []
    with open(log_file, 'r') as f:
        lines = f.readlines()
    
    # Find data sections
    in_data = False
    headers = []
    
    for line in lines:
        if 'Step' in line and 'Temp' in line:
            headers = line.split()
            in_data = True
            continue
        if in_data:
            if line.strip() == '' or 'Loop' in line:
                in_data = False
                continue
            try:
                values = [float(x) for x in line.split()]
                if len(values) == len(headers):
                    data.append(dict(zip(headers, values)))
            except:
                pass
    
    return data

# Load and plot
log_data = parse_lammps_log('log.lammps')
steps = [d['Step'] for d in log_data]
temps = [d['Temp'] for d in log_data]
energies = [d['TotEng'] for d in log_data]

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
ax1.plot(steps, temps)
ax1.set_ylabel('Temperature (K)')
ax2.plot(steps, energies)
ax2.set_ylabel('Total Energy (eV)')
ax2.set_xlabel('Step')
plt.tight_layout()
plt.savefig('thermo.png')
```

## Structure Analysis

### Density Profile

```python
# Calculate density along z-axis
z_bins = np.linspace(0, u.dimensions[2], 50)
density_profile = np.zeros(len(z_bins) - 1)

for ts in u.trajectory[::10]:
    z_positions = u.atoms.positions[:, 2]
    hist, _ = np.histogram(z_positions, bins=z_bins)
    density_profile += hist

density_profile /= len(u.trajectory[::10])  # Average
z_centers = (z_bins[:-1] + z_bins[1:]) / 2

plt.plot(z_centers, density_profile)
plt.xlabel('z (Å)')
plt.ylabel('Density')
plt.savefig('density_profile.png')
```

### Bond Length Distribution

```python
# Calculate bond length distribution for specific pairs
from MDAnalysis.lib.distances import distance_array

si_atoms = u.select_atoms('name Si')
o_atoms = u.select_atoms('name O')

bond_lengths = []

for ts in u.trajectory[::5]:
    dist_matrix = distance_array(si_atoms.positions, o_atoms.positions)
    # Find bonds (distances within cutoff)
    bonds = dist_matrix[dist_matrix < 2.5]  # Si-O bond cutoff
    bond_lengths.extend(bonds)

plt.hist(bond_lengths, bins=50, density=True)
plt.xlabel('Si-O Bond Length (Å)')
plt.ylabel('Probability Density')
plt.savefig('bond_distribution.png')
```

## Advanced Workflows

### Melting Point Estimation

```python
# NPT simulation with temperature ramp
temp_ramp_input = """
# Temperature ramp simulation
units           metal
atom_style      atomic
boundary        p p p

read_data       data.structure

pair_style      lj/cut 10.0
pair_coeff      1 1 1.0 1.0

variable        t equal temp

fix             1 all npt temp 300 2000 0.1 iso 1.0 1.0 1.0

# Variable temperature
variable        T ramp 300 2000
fix             2 all temp/berendsen ${T} ${T} 0.1

thermo          100
timestep        0.001
run             100000
"""
```

### Batch Simulation Script

```python
import os
import subprocess

def run_md_simulation(structure_file, temperature, pressure, output_dir):
    """Run a single MD simulation."""
    
    os.makedirs(output_dir, exist_ok=True)
    
    # Load structure
    structure = Structure.from_file(structure_file)
    lammps_data = LammpsData.from_structure(structure)
    lammps_data.write_file(f'{output_dir}/data.structure')
    
    # Generate input
    input_script = f"""
units           metal
atom_style      atomic
boundary        p p p
read_data       data.structure
pair_style      lj/cut 10.0
pair_coeff      * * 1.0 1.0
velocity        all create {temperature} 12345
timestep        0.001
fix             1 all npt temp {temperature} {temperature} 0.1 \\
                iso {pressure} {pressure} 1.0
thermo          100
dump            1 all atom 100 dump.atom
run             50000
write_data      final.data
"""
    
    with open(f'{output_dir}/in.md', 'w') as f:
        f.write(input_script)
    
    # Run LAMMPS
    subprocess.run(['lmp', '-in', 'in.md'], cwd=output_dir)

# Run batch
conditions = [
    ('structure1.cif', 300, 1.0, 'run_300K'),
    ('structure1.cif', 500, 1.0, 'run_500K'),
    ('structure1.cif', 700, 1.0, 'run_700K'),
]

for struct, temp, press, out_dir in conditions:
    run_md_simulation(struct, temp, press, out_dir)
```

## Best Practices

1. **Equilibration**: Run NVT/NPT equilibration before production
2. **Timestep**: 1 fs for atomic systems, 0.25 fs for ReaxFF
3. **Thermostat**: Nose-Hoover for NVT, Berendsen for equilibration only
4. **Barostat**: Use NPT for constant pressure simulations
5. **Neighbor list**: Update frequency affects performance
6. **Trajectory storage**: Balance frequency vs disk space

## Common Issues

- **Atom lost**: Check periodic boundary conditions
- **Bad dynamics**: Verify force field parameters
- **Energy drift**: Reduce timestep, check integrator
- **Memory**: Use dump frequency appropriate for trajectory size

## References

- [LAMMPS Documentation](https://docs.lammps.org/)
- [MDAnalysis Documentation](https://userguide.mdanalysis.org/)
- [LAMMPS Tutorials](https://www.lammps.org/tutorials.html)
