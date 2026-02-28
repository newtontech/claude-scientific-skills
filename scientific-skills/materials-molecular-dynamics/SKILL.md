---
name: materials-molecular-dynamics
description: Molecular dynamics simulations using LAMMPS. Set up input files, run simulations, analyze trajectories, compute thermodynamic properties, and study dynamic behavior of materials at the atomic scale.
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# Materials Molecular Dynamics

## Overview

A comprehensive skill for performing and analyzing molecular dynamics (MD) simulations using LAMMPS (Large-scale Atomic/Molecular Massively Parallel Simulator). Set up simulation inputs, run MD calculations, analyze trajectories, compute thermodynamic properties, radial distribution functions, mean square displacements, and study dynamic behavior of materials at the atomic scale.

## When to Use This Skill

This skill should be used when:
- Running molecular dynamics simulations of materials
- Setting up LAMMPS input files and force fields
- Analyzing MD trajectories and extracting thermodynamic properties
- Computing radial distribution functions (RDF)
- Calculating mean square displacement (MSD) and diffusion coefficients
- Studying phase transitions and melting behavior
- Simulating mechanical deformation (tension, compression, shear)
- Computing thermal conductivity and transport properties
- Analyzing vibrational spectra from MD simulations
- Setting up reactive force field (ReaxFF) simulations
- Running hybrid quantum/classical (QM/MM) simulations

## Quick Start Guide

### Installation

```bash
# Install LAMMPS
# macOS/Linux (via conda)
conda install -c conda-forge lammps

# Or download from https://www.lammps.org/

# Python packages for analysis
uv pip install lammps-logfile mdanalysis ase ovito matplotlib numpy scipy

# For trajectory analysis
uv pip install freud-analysis dask[array]
```

### Basic LAMMPS Input

```python
# Generate LAMMPS input file
lammps_input = """
# SiO2 MD simulation
units           metal
atom_style      atomic
boundary        p p p

# Read structure
read_data       structure.data

# Potential
pair_style      reax/c NULL
pair_coeff      * * ffield.reax.cho Si O

# Settings
neighbor        2.0 bin
neigh_modify    every 10 delay 0 check yes

# Thermodynamics
timestep        0.001  # 1 fs in metal units
thermo          100
thermo_style    custom step temp pe ke etotal press vol

# Ensemble
fix             1 all nvt temp 300.0 300.0 0.1

# Output
dump            1 all custom 100 trajectory.lammpstrj id type x y z vx vy vz
restart         10000 restart.*.data

# Run
run             10000
"""

with open("in.md", "w") as f:
    f.write(lammps_input)

print("✓ Generated LAMMPS input file: in.md")
```

### Running Simulations

```python
import lammps
import os

# Initialize LAMMPS
lmp = lammps.lammps()

# Run input file
lmp.file("in.md")

# Extract thermodynamic data
thermo_data = lmp.extract_compute("thermo_pe", lmp.TYPE_GLOBAL, lmp.SCALAR)
print(f"Potential energy: {thermo_data}")

# Close LAMMPS
lmp.close()
```

## Core Capabilities

### 1. Input File Generation

Generate LAMMPS input files for different simulation types.

**NVT Ensemble (Canonical):**
```python
def generate_nvt_input(structure_file, temperature=300, 
                       n_steps=10000, timestep=1.0,
                       potential="reax/c"):
    """
    Generate LAMMPS input for NVT simulation
    """
    input_script = f"""
# NVT Molecular Dynamics Simulation
units           metal
atom_style      atomic
boundary        p p p

# Read structure
read_data       {structure_file}

# Potential settings
pair_style      {potential} NULL
pair_coeff      * * ffield.reax.cho Si O

# Neighbor lists
neighbor        2.0 bin
neigh_modify    every 10 delay 0 check yes

# Timestep (1 fs = 0.001 ps in metal units)
timestep        {timestep/1000:.6f}

# Thermodynamics output
thermo          100
thermo_style    custom step temp pe ke etotal press vol density

# NVT ensemble
fix             nvt all nvt temp {temperature} {temperature} $(100.0*dt)

# Trajectory output
dump            traj all custom 100 trajectory.lammpstrj \\
                id type x y z vx vy vz fx fy fz
dump_modify     traj sort id

# Restart files
restart         10000 restart.*.data

# Run simulation
run             {n_steps}

# Final output
write_data      final.data
"""
    return input_script

# Generate input
input_script = generate_nvt_input(
    structure_file="sio2.data",
    temperature=300,
    n_steps=50000,
    timestep=1.0
)

with open("in.nvt", "w") as f:
    f.write(input_script)

print("✓ Generated NVT input: in.nvt")
```

**NPT Ensemble (Isothermal-Isobaric):**
```python
def generate_npt_input(structure_file, temperature=300, pressure=1.0,
                       n_steps=10000, timestep=1.0):
    """
    Generate LAMMPS input for NPT simulation
    """
    input_script = f"""
# NPT Molecular Dynamics Simulation
units           metal
atom_style      atomic
boundary        p p p

read_data       {structure_file}

pair_style      reax/c NULL
pair_coeff      * * ffield.reax.cho Si O

neighbor        2.0 bin
neigh_modify    every 10 delay 0 check yes

timestep        {timestep/1000:.6f}

thermo          100
thermo_style    custom step temp pe press vol density lx ly lz

# NPT ensemble
fix             npt all npt temp {temperature} {temperature} $(100.0*dt) \\
                iso {pressure} {pressure} $(1000.0*dt)

# Output
dump            traj all custom 100 trajectory.lammpstrj id type x y z
dump_modify     traj sort id

restart         10000 restart.*.data
run             {n_steps}
write_data      final.data
"""
    return input_script
```

**NVE Ensemble (Microcanonical):**
```python
def generate_nve_input(structure_file, n_steps=10000, timestep=1.0):
    """
    Generate LAMMPS input for NVE simulation
    """
    input_script = f"""
# NVE Molecular Dynamics Simulation
units           metal
atom_style      atomic
boundary        p p p

read_data       {structure_file}

pair_style      reax/c NULL
pair_coeff      * * ffield.reax.cho Si O

neighbor        2.0 bin
neigh_modify    every 10 delay 0 check yes

timestep        {timestep/1000:.6f}

thermo          100
thermo_style    custom step temp pe ke etotal press

# NVE ensemble (constant energy)
fix             nve all nve

# Optional: velocity rescaling for initial equilibration
# velocity      all create 300.0 12345

dump            traj all custom 100 trajectory.lammpstrj id type x y z vx vy vz
dump_modify     traj sort id

run             {n_steps}
write_data      final.data
"""
    return input_script
```

### 2. Structure File Generation

Create LAMMPS data files from structures.

```python
from pymatgen.core import Structure
from pymatgen.io.lammps.data import LammpsData

def structure_to_lammps(structure, output_file="structure.data"):
    """
    Convert pymatgen Structure to LAMMPS data file
    """
    # Create LAMMPS data
    lammps_data = LammpsData.from_structure(
        structure,
        atom_style="atomic"
    )
    
    # Write to file
    lammps_data.write_file(output_file)
    
    print(f"✓ Wrote LAMMPS data file: {output_file}")
    print(f"  Atoms: {len(structure)}")
    print(f"  Elements: {list(structure.composition.as_dict().keys())}")
    
    return lammps_data

# Usage
struct = Structure.from_file("POSCAR")
lammps_data = structure_to_lammps(struct, "sio2.data")

# For more complex systems with bonds
def molecule_to_lammps(molecule, force_field="UFF", output_file="molecule.data"):
    """
    Convert molecule to LAMMPS data with bonds/angles
    """
    from pymatgen.io.lammps.data import LammpsData
    
    # Create topology
    lammps_data = LammpsData.from_structure(
        molecule,
        atom_style="full"
    )
    
    lammps_data.write_file(output_file)
    return lammps_data
```

### 3. Trajectory Analysis

Analyze MD trajectories using MDAnalysis or custom tools.

```python
import MDAnalysis as mda
import numpy as np
import matplotlib.pyplot as plt

def analyze_trajectory(trajectory_file, topology_file=None):
    """
    Comprehensive trajectory analysis
    """
    # Load trajectory
    if topology_file:
        u = mda.Universe(topology_file, trajectory_file)
    else:
        # LAMMPS dump file can be read directly
        u = mda.Universe(trajectory_file, format="LAMMPSDUMP")
    
    print(f"Loaded trajectory:")
    print(f"  Frames: {len(u.trajectory)}")
    print(f"  Atoms: {len(u.atoms)}")
    print(f"  Time: {u.trajectory.totaltime} ps")
    
    return u

# Extract thermodynamic properties
def extract_thermo(log_file):
    """
    Extract thermodynamic data from LAMMPS log
    """
    import lammps_logfile
    
    log = lammps_logfile.File(log_file)
    
    # Get available properties
    print(f"Available properties: {log.get_keywords()}")
    
    # Extract data
    steps = log.get("Step")
    temp = log.get("Temp")
    pe = log.get("TotEng")  # or PotEng
    pressure = log.get("Press")
    
    return {
        "steps": steps,
        "temperature": temp,
        "energy": pe,
        "pressure": pressure
    }

# Usage
thermo = extract_thermo("log.lammps")

# Plot thermodynamic properties
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

axes[0, 0].plot(thermo["steps"], thermo["temperature"])
axes[0, 0].set_ylabel("Temperature (K)")
axes[0, 0].set_title("Temperature")

axes[0, 1].plot(thermo["steps"], thermmo["energy"])
axes[0, 1].set_ylabel("Energy (eV)")
axes[0, 1].set_title("Total Energy")

axes[1, 0].plot(thermo["steps"], thermo["pressure"])
axes[1, 0].set_ylabel("Pressure (bar)")
axes[1, 0].set_xlabel("Step")
axes[1, 0].set_title("Pressure")

plt.tight_layout()
plt.savefig("thermodynamics.png", dpi=150)
```

### 4. Radial Distribution Function (RDF)

Compute RDF from trajectory.

```python
import freud
import numpy as np
import matplotlib.pyplot as plt

def compute_rdf(trajectory_file, topology_file=None, 
                r_max=10.0, bins=100, pairs=None):
    """
    Compute radial distribution function
    
    Args:
        trajectory_file: Path to trajectory
        r_max: Maximum radius for RDF (Angstroms)
        bins: Number of bins
        pairs: List of (type_i, type_j) tuples, or None for all pairs
    """
    import MDAnalysis as mda
    
    # Load trajectory
    u = mda.Universe(trajectory_file, format="LAMMPSDUMP")
    
    # Get box dimensions
    box = u.dimensions[:3]  # Lx, Ly, Lz
    
    # Initialize RDF calculator
    rdf = freud.density.RDF(bins=bins, r_max=r_max)
    
    # Accumulate RDF over frames
    for ts in u.trajectory:
        positions = u.atoms.positions
        box_obj = freud.box.Box.from_box(box)
        rdf.compute(system=(box_obj, positions), reset=False)
    
    # Plot results
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(rdf.bin_centers, rdf.rdf)
    ax.set_xlabel("r (Å)")
    ax.set_ylabel("g(r)")
    ax.set_title("Radial Distribution Function")
    ax.axhline(1.0, color='k', linestyle='--', alpha=0.5)
    
    plt.savefig("rdf.png", dpi=150)
    
    return rdf

# Partial RDF for specific element pairs
def compute_partial_rdf(trajectory_file, r_max=10.0, bins=100):
    """
    Compute partial RDFs for all element pairs
    """
    import MDAnalysis as mda
    
    u = mda.Universe(trajectory_file, format="LAMMPSDUMP")
    box = u.dimensions[:3]
    
    # Get unique elements
    elements = set(u.atoms.names)
    
    fig, axes = plt.subplots(len(elements), len(elements), 
                            figsize=(12, 12))
    
    for i, elem_i in enumerate(sorted(elements)):
        for j, elem_j in enumerate(sorted(elements)):
            ax = axes[i, j]
            
            # Select atoms
            group_i = u.select_atoms(f"name {elem_i}")
            group_j = u.select_atoms(f"name {elem_j}")
            
            # Compute RDF
            rdf = freud.density.RDF(bins=bins, r_max=r_max)
            
            for ts in u.trajectory:
                box_obj = freud.box.Box.from_box(box)
                rdf.compute(system=(box_obj, group_i.positions),
                           query_points=group_j.positions, reset=False)
            
            ax.plot(rdf.bin_centers, rdf.rdf)
            ax.set_title(f"{elem_i}-{elem_j}")
            if i == len(elements) - 1:
                ax.set_xlabel("r (Å)")
            if j == 0:
                ax.set_ylabel("g(r)")
    
    plt.tight_layout()
    plt.savefig("partial_rdf.png", dpi=150)
```

### 5. Mean Square Displacement and Diffusion

Calculate MSD and diffusion coefficients.

```python
import freud
import numpy as np
import matplotlib.pyplot as plt

def compute_msd(trajectory_file, output_file="msd.png"):
    """
    Compute mean square displacement and diffusion coefficient
    """
    import MDAnalysis as mda
    
    u = mda.Universe(trajectory_file, format="LAMMPSDUMP")
    box = u.dimensions[:3]
    
    # Get timestep (in ps, assuming metal units)
    timestep = 0.001  # 1 fs = 0.001 ps
    
    # Initialize MSD calculator
    msd_calc = freud.msd.MSD(box=box, mode="direct")
    
    # Collect positions over time
    positions = []
    times = []
    
    for ts in u.trajectory:
        positions.append(u.atoms.positions.copy())
        times.append(ts.frame * timestep)
    
    positions = np.array(positions)
    
    # Compute MSD
    msd_calc.compute(positions)
    
    # Get MSD values
    msd = msd_calc.msd
    
    # Fit to get diffusion coefficient
    # MSD = 6*D*t for 3D
    times_array = np.array(times[:len(msd)])
    
    # Linear fit (skip first few points)
    fit_start = len(msd) // 4
    slope, intercept = np.polyfit(times_array[fit_start:], msd[fit_start:], 1)
    
    D = slope / 6  # Diffusion coefficient in Å²/ps
    D_cm2s = D * 1e-4  # Convert to cm²/s
    
    # Plot
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(times_array, msd, 'b-', label='MSD')
    ax.plot(times_array[fit_start:], 
            slope * times_array[fit_start:] + intercept,
            'r--', label=f'Fit: D = {D_cm2s:.2e} cm²/s')
    
    ax.set_xlabel("Time (ps)")
    ax.set_ylabel("MSD (Å²)")
    ax.set_title("Mean Square Displacement")
    ax.legend()
    
    plt.savefig(output_file, dpi=150)
    
    print(f"Diffusion coefficient: {D_cm2s:.2e} cm²/s")
    
    return {
        "msd": msd,
        "times": times_array,
        "diffusion_coefficient": D_cm2s
    }

# Element-specific MSD
def compute_element_msd(trajectory_file):
    """
    Compute MSD for each element type separately
    """
    import MDAnalysis as mda
    
    u = mda.Universe(trajectory_file, format="LAMMPSDUMP")
    box = u.dimensions[:3]
    timestep = 0.001
    
    elements = set(u.atoms.names)
    results = {}
    
    fig, ax = plt.subplots(figsize=(8, 6))
    
    for elem in sorted(elements):
        group = u.select_atoms(f"name {elem}")
        
        positions = []
        for ts in u.trajectory:
            positions.append(group.positions.copy())
        
        positions = np.array(positions)
        
        msd_calc = freud.msd.MSD(box=box, mode="direct")
        msd_calc.compute(positions)
        
        times = np.arange(len(msd_calc.msd)) * timestep
        ax.plot(times, msd_calc.msd, label=elem)
        
        # Fit diffusion coefficient
        fit_start = len(msd_calc.msd) // 4
        slope, _ = np.polyfit(times[fit_start:], msd_calc.msd[fit_start:], 1)
        D = slope / 6 * 1e-4  # cm²/s
        
        results[elem] = {
            "msd": msd_calc.msd,
            "diffusion_coefficient": D
        }
        
        print(f"{elem}: D = {D:.2e} cm²/s")
    
    ax.set_xlabel("Time (ps)")
    ax.set_ylabel("MSD (Å²)")
    ax.set_title("Mean Square Displacement by Element")
    ax.legend()
    plt.savefig("msd_elements.png", dpi=150)
    
    return results
```

### 6. Mechanical Deformation Simulations

Set up and analyze deformation simulations.

```python
def generate_deformation_input(structure_file, direction="x", 
                               strain_rate=1e9,  # 1e9 s^-1
                               temperature=300,
                               n_steps=100000):
    """
    Generate LAMMPS input for uniaxial deformation
    """
    # Convert strain rate to LAMMPS units (1/time)
    # strain_rate is in s^-1, need to convert
    
    input_script = f"""
# Uniaxial Deformation Simulation
units           metal
atom_style      atomic
boundary        p p p

read_data       {structure_file}

pair_style      reax/c NULL
pair_coeff      * * ffield.reax.cho Si O

neighbor        2.0 bin
neigh_modify    every 10 delay 0 check yes

timestep        0.001  # 1 fs

thermo          100
thermo_style    custom step temp pe press pxx pyy pzz lx ly lz vol

# Initial equilibration (NPT)
fix             npt all npt temp {temperature} {temperature} 0.1 iso 0 0 1.0
dump            equil all custom 100 equil.lammpstrj id type x y z
run             10000
unfix           npt
undump          equil

write_data      equilibrated.data

# Deformation
reset_timestep  0

variable        srate equal 1.0e9  # strain rate in s^-1
variable        srate1 equal "v_srate / 1.0e15"  # convert to fs^-1
variable        strain equal "step*dt*v_srate1"

# Apply deformation in {direction} direction
fix             nph all nph {direction} 0 0 1.0
fix             deform all deform 1 {direction} erate ${{srate1}} units box

# Output stress and strain
variable        p{direction} equal "press"
fix             print_stress all print 100 "${{strain}} ${{p{direction}}}" \\
                file stress_strain.txt title "# Strain Stress"

dump            deform all custom 100 deform.lammpstrj id type x y z
run             {n_steps}

write_data      deformed.data
"""
    return input_script

def analyze_stress_strain(stress_strain_file):
    """
    Analyze stress-strain curve and compute elastic properties
    """
    import numpy as np
    import matplotlib.pyplot as plt
    
    # Load data
    data = np.loadtxt(stress_strain_file, skiprows=1)
    strain = data[:, 0]
    stress = data[:, 1]  # in bars (LAMMPS metal units)
    
    # Convert stress to GPa (1 bar = 1e-4 GPa)
    stress_gpa = stress * 1e-4
    
    # Plot
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(strain, stress_gpa)
    ax.set_xlabel("Strain")
    ax.set_ylabel("Stress (GPa)")
    ax.set_title("Stress-Strain Curve")
    
    # Fit Young's modulus in elastic region
    elastic_limit = len(strain) // 10  # First 10% of curve
    slope, intercept = np.polyfit(strain[:elastic_limit], 
                                  stress_gpa[:elastic_limit], 1)
    
    youngs_modulus = slope  # in GPa
    
    ax.plot(strain[:elastic_limit], 
            slope * strain[:elastic_limit] + intercept,
            'r--', label=f"E = {youngs_modulus:.1f} GPa")
    ax.legend()
    
    plt.savefig("stress_strain.png", dpi=150)
    
    print(f"Young's modulus: {youngs_modulus:.1f} GPa")
    
    return {
        "strain": strain,
        "stress": stress_gpa,
        "youngs_modulus": youngs_modulus
    }
```

### 7. Temperature-Dependent Properties

Simulate and analyze heating/cooling.

```python
def generate_heating_input(structure_file, 
                           t_start=300, t_end=2000, 
                           ramp_rate=10.0,  # K/ps
                           n_steps=100000):
    """
    Generate LAMMPS input for heating simulation
    """
    input_script = f"""
# Heating Simulation
units           metal
atom_style      atomic
boundary        p p p

read_data       {structure_file}

pair_style      reax/c NULL
pair_coeff      * * ffield.reax.cho Si O

neighbor        2.0 bin
neigh_modify    every 10 delay 0 check yes

timestep        0.001  # 1 fs

thermo          100
thermo_style    custom step temp pe press vol density

# Linear temperature ramp
variable        t equal "{t_start} + (step * dt * {ramp_rate * 1000})"
fix             nvt all nvt temp $t $t 0.1

# Output
dump            traj all custom 100 heating.lammpstrj id type x y z
dump_modify     traj sort id

fix             temp_out all print 100 "$(step) $(temp) $(pe) $(press) $(vol)" \\
                file temp_profile.txt title "# Step Temp Energy Press Vol"

run             {n_steps}
write_data      heated.data
"""
    return input_script

def analyze_melting(log_file, temp_profile_file):
    """
    Detect melting point from heating simulation
    """
    import numpy as np
    import matplotlib.pyplot as plt
    
    # Load temperature profile
    data = np.loadtxt(temp_profile_file, skiprows=1)
    step = data[:, 0]
    temp = data[:, 1]
    energy = data[:, 2]
    volume = data[:, 5]
    
    # Compute heat capacity (dE/dT)
    dE = np.gradient(energy)
    dT = np.gradient(temp)
    Cp = dE / dT
    
    # Melting detected by sharp increase in volume or energy
    # Find where dV/dT is maximum
    dV = np.gradient(volume)
    melting_idx = np.argmax(dV)
    melting_temp = temp[melting_idx]
    
    # Plot
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    axes[0, 0].plot(temp, energy)
    axes[0, 0].axvline(melting_temp, color='r', linestyle='--')
    axes[0, 0].set_xlabel("Temperature (K)")
    axes[0, 0].set_ylabel("Energy (eV)")
    
    axes[0, 1].plot(temp, volume)
    axes[0, 1].axvline(melting_temp, color='r', linestyle='--')
    axes[0, 1].set_xlabel("Temperature (K)")
    axes[0, 1].set_ylabel("Volume (Å³)")
    
    axes[1, 0].plot(temp[1:], Cp[1:])
    axes[1, 0].axvline(melting_temp, color='r', linestyle='--')
    axes[1, 0].set_xlabel("Temperature (K)")
    axes[1, 0].set_ylabel("Heat Capacity")
    
    axes[1, 1].plot(temp, dV)
    axes[1, 1].axvline(melting_temp, color='r', linestyle='--')
    axes[1, 1].set_xlabel("Temperature (K)")
    axes[1, 1].set_ylabel("dV/dT")
    
    plt.tight_layout()
    plt.savefig("melting_analysis.png", dpi=150)
    
    print(f"Estimated melting temperature: {melting_temp:.0f} K")
    
    return {
        "melting_temperature": melting_temp,
        "temperature": temp,
        "energy": energy,
        "volume": volume
    }
```

## Common Workflows

### Workflow 1: Complete MD Simulation Pipeline

```python
"""
Complete MD simulation workflow: setup → run → analyze
"""
from pymatgen.core import Structure
import os

def md_workflow(structure_file, temperature=300, pressure=1.0,
                n_steps=100000, output_dir="./md_simulation"):
    """
    Complete MD workflow from structure to analysis
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Step 1: Convert structure to LAMMPS format
    print("[1/5] Converting structure...")
    struct = Structure.from_file(structure_file)
    data_file = os.path.join(output_dir, "structure.data")
    structure_to_lammps(struct, data_file)
    
    # Step 2: Generate input files
    print("[2/5] Generating input files...")
    
    # 2a: Minimization
    min_input = """
# Energy minimization
units           metal
atom_style      atomic
boundary        p p p
read_data       structure.data
pair_style      reax/c NULL
pair_coeff      * * ffield.reax.cho Si O
neighbor        2.0 bin
neigh_modify    every 10 delay 0 check yes
thermo          10
thermo_style    custom step pe press
min_style       cg
minimize        1e-25 1e-25 5000 10000
write_data      minimized.data
"""
    with open(os.path.join(output_dir, "in.minimize"), "w") as f:
        f.write(min_input)
    
    # 2b: Equilibration (NPT)
    equil_input = generate_npt_input(
        "minimized.data", 
        temperature=temperature,
        pressure=pressure,
        n_steps=50000
    )
    with open(os.path.join(output_dir, "in.equilibrate"), "w") as f:
        f.write(equil_input)
    
    # 2c: Production (NVT)
    prod_input = generate_nvt_input(
        "equilibrated.data",
        temperature=temperature,
        n_steps=n_steps
    )
    with open(os.path.join(output_dir, "in.production"), "w") as f:
        f.write(prod_input)
    
    # Step 3: Create run script
    print("[3/5] Creating run script...")
    run_script = """#!/bin/bash
# MD simulation pipeline

# Step 1: Minimization
echo "Running energy minimization..."
lmp -in in.minimize -log log.minimize

# Step 2: Equilibration
echo "Running NPT equilibration..."
lmp -in in.equilibrate -log log.equilibrate

# Step 3: Production
echo "Running NVT production..."
lmp -in in.production -log log.production

echo "Simulation complete!"
"""
    with open(os.path.join(output_dir, "run.sh"), "w") as f:
        f.write(run_script)
    os.chmod(os.path.join(output_dir, "run.sh"), 0o755)
    
    print("[4/5] Creating analysis script...")
    analysis_script = """
import os
import sys
sys.path.insert(0, '.')

# Analyze trajectory
from md_analysis import analyze_trajectory, compute_rdf, compute_msd

trajectory = "trajectory.lammpstrj"

print("Analyzing trajectory...")
u = analyze_trajectory(trajectory)

print("Computing RDF...")
rdf = compute_rdf(trajectory)

print("Computing MSD...")
msd = compute_msd(trajectory)

print("Analysis complete!")
"""
    with open(os.path.join(output_dir, "analyze.py"), "w") as f:
        f.write(analysis_script)
    
    print("[5/5] Workflow setup complete!")
    print(f"\nTo run:")
    print(f"  cd {output_dir}")
    print(f"  ./run.sh")
    print(f"\nTo analyze:")
    print(f"  python analyze.py")

# Usage
md_workflow("POSCAR", temperature=300, n_steps=100000)
```

### Workflow 2: High-Throughput MD Screening

```python
"""
High-throughput MD screening of multiple structures
"""
import os
from pathlib import Path

def screen_structures(structure_dir, output_base="./md_screening"):
    """
    Set up MD simulations for multiple structures
    """
    structure_files = list(Path(structure_dir).glob("*.vasp")) + \
                     list(Path(structure_dir).glob("*.cif"))
    
    results = []
    
    for struct_file in structure_files:
        formula = struct_file.stem
        calc_dir = os.path.join(output_base, formula)
        
        try:
            print(f"Setting up {formula}...")
            md_workflow(
                str(struct_file),
                temperature=300,
                n_steps=50000,
                output_dir=calc_dir
            )
            results.append({
                "formula": formula,
                "status": "setup_complete",
                "path": calc_dir
            })
        except Exception as e:
            results.append({
                "formula": formula,
                "status": "error",
                "error": str(e)
            })
    
    # Save summary
    import json
    with open(os.path.join(output_base, "screening_summary.json"), "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*50}")
    print("SCREENING SETUP SUMMARY")
    print(f"{'='*50}")
    print(f"Total structures: {len(structure_files)}")
    print(f"Successful: {sum(1 for r in results if r['status'] == 'setup_complete')}")
    print(f"Failed: {sum(1 for r in results if r['status'] == 'error')}")
    
    return results

# Usage
# screen_structures("./structures")
```

## Best Practices

### Force Field Selection
1. **ReaxFF**: For reactive chemistry, bond breaking/forming
2. **EAM**: For metals and alloys
3. **Tersoff/Brenner**: For covalent materials (Si, C)
4. **Lennard-Jones**: For noble gases, simple fluids
5. **Validate**: Compare known properties before production runs

### Simulation Setup
1. **Minimize first**: Always energy minimize before dynamics
2. **Equilibrate**: Run NPT before NVT for correct density
3. **Timestep**: 1 fs for most systems, 0.5 fs for reactive systems
4. **Neighbor lists**: Update every 10 steps for efficiency

### Analysis
1. **Convergence**: Check thermodynamic properties are stable
2. **Sampling**: Save trajectories every 10-100 fs
3. **Statistics**: Run multiple independent simulations
4. **Validation**: Compare with experimental values when available

### Performance
1. **Parallelization**: Use MPI for large systems
2. **GPU acceleration**: LAMMPS supports GPU for some potentials
3. **Output frequency**: Don't dump too frequently (I/O bottleneck)

## Troubleshooting

**"Lost atoms" error:**
- Check potential parameters
- Reduce timestep
- Check initial structure for overlaps

**Energy drift:**
- Reduce timestep
- Check neighbor list settings
- Verify potential is appropriate

**Pressure oscillations:**
- Increase damping parameter
- Longer equilibration
- Check barostat settings

## Additional Resources

- **LAMMPS manual**: https://docs.lammps.org/
- **LAMMPS tutorials**: https://www.lammps.org/tutorials.html
- **MDAnalysis docs**: https://www.mdanalysis.org/
- **Freud docs**: https://freud.readthedocs.io/

## Version Notes

- Requires LAMMPS stable version (2020 or later)
- Python 3.10 or higher recommended
- Compatible with MPI for parallel simulations
