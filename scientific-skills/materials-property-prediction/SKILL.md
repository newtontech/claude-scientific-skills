---
name: materials-property-prediction
description: Machine learning for materials science - predict properties, train models on Materials Project data, use graph neural networks, featurize crystal structures, and build high-throughput screening pipelines.
license: MIT license
metadata:
    skill-author: K-Dense Inc.
---

# Materials Property Prediction

## Overview

A comprehensive skill for applying machine learning to materials science. Train models to predict material properties from crystal structures and composition, use pre-trained graph neural networks, featurize materials descriptors, build high-throughput screening pipelines, and accelerate materials discovery with AI-powered property prediction.

## When to Use This Skill

This skill should be used when:
- Predicting material properties (band gap, formation energy, bulk modulus) from structure
- Training ML models on materials databases (Materials Project, OQMD)
- Using graph neural networks (CGCNN, MEGNet, ALIGNN) for materials
- Featurizing crystal structures and compositions
- Building high-throughput screening workflows for materials discovery
- Accelerating DFT calculations with surrogate ML models
- Predicting stability of new compounds
- Performing inverse design of materials with target properties
- Using pre-trained foundation models for materials (MatterSim, SevenNet)
- Creating composition-based feature vectors (Magpie, Matminer)

## Quick Start Guide

### Installation

```bash
# Core ML packages
uv pip install torch torch-geometric scikit-learn pandas numpy matplotlib

# Materials ML libraries
uv pip install dgl deepchem matminer megnet cgcnn

# For graph neural networks
uv pip install pymatgen torch_scatter torch_sparse

# Additional utilities
uv pip install tqdm wandb optuna  # For hyperparameter tuning
```

### Basic Property Prediction

```python
from pymatgen.core import Structure
from megnet.models import MEGNetModel
import numpy as np

# Load pre-trained MEGNet model
model = MEGNetModel.from_file("pretrained_models/formation_energy.hdf5")

# Predict formation energy for a structure
struct = Structure.from_file("POSCAR")
predicted_energy = model.predict_structure(struct)

print(f"Predicted formation energy: {predicted_energy:.3f} eV/atom")
```

### Featurizing Structures

```python
from matminer.featurizers.structure import DensityFeatures, StructuralComplexity
from matminer.featurizers.composition import ElementProperty
from pymatgen.core import Structure

# Structure-based features
struct = Structure.from_file("POSCAR")

density_feat = DensityFeatures()
complexity_feat = StructuralComplexity()

density_features = density_feat.featurize(struct)
complexity_features = complexity_feat.featurize(struct)

print(f"Density features: {density_features}")
print(f"Complexity features: {complexity_features}")

# Composition-based features
from matminer.featurizers.conversions import StrToComposition

comp = StrToComposition()
composition = comp.featurize(struct.composition.formula.replace(" ", ""))

# Element property features
elem_prop = ElementProperty.from_preset("magpie")
comp_features = elem_prop.featurize(composition[0])

print(f"Number of composition features: {len(comp_features)}")
```

## Core Capabilities

### 1. Structure Featurization

Convert crystal structures into machine-learnable feature vectors.

**Matminer Featurizers:**
```python
from matminer.featurizers.structure import (
    DensityFeatures,
    StructuralComplexity,
    GlobalSymmetryFeatures,
    RadialDistributionFunction,
    CoulombMatrix,
    SineCoulombMatrix,
    OrbitalFieldMatrix
)
from matminer.featurizers.site import (
    LocalStructOrderParams,
    CrystalNNFingerprint,
    OPSiteFingerprint
)
from pymatgen.core import Structure
import pandas as pd

def featurize_structure(structure):
    """
    Extract comprehensive features from structure
    """
    features = {}
    
    # Global structure features
    density_feat = DensityFeatures()
    features['density'] = density_feat.featurize(structure)
    
    complexity_feat = StructuralComplexity()
    features['complexity'] = complexity_feat.featurize(structure)
    
    symmetry_feat = GlobalSymmetryFeatures()
    features['symmetry'] = symmetry_feat.featurize(structure)
    
    # RDF features
    rdf_feat = RadialDistributionFunction()
    rdf = rdf_feat.featurize(structure)
    features['rdf'] = rdf
    
    return features

# Site-based features
def featurize_sites(structure):
    """
    Extract local environment features for each site
    """
    ops_feat = OPSiteFingerprint()
    
    site_features = []
    for i in range(len(structure)):
        feat = ops_feat.featurize(structure, i)
        site_features.append(feat)
    
    # Aggregate site features
    site_features = np.array(site_features)
    mean_features = np.mean(site_features, axis=0)
    std_features = np.std(site_features, axis=0)
    
    return {
        'site_mean': mean_features,
        'site_std': std_features
    }

# Coulomb matrix representation
def get_coulomb_matrix(structure, max_atoms=50):
    """
    Get Coulomb matrix representation for structure
    """
    cm_feat = SineCoulombMatrix(flatten=True)
    cm = cm_feat.featurize(structure)
    return cm

# Batch featurization
def featurize_dataset(structures, n_jobs=4):
    """
    Featurize multiple structures in parallel
    """
    from joblib import Parallel, delayed
    
    results = Parallel(n_jobs=n_jobs)(
        delayed(featurize_structure)(s) for s in structures
    )
    
    return results
```

**Composition Featurization:**
```python
from matminer.featurizers.composition import (
    ElementProperty,
    OxidationStates,
    ElectronAffinity,
    ElectronegativityDiff,
    AtomicPackingEfficiency,
    CohesiveEnergy,
    BandCenter
)
from pymatgen.core import Composition

def featurize_composition(composition):
    """
    Extract features from chemical composition
    """
    # Convert to Composition object if string
    if isinstance(composition, str):
        composition = Composition(composition)
    
    features = {}
    
    # Element property statistics (Magpie preset)
    elem_prop = ElementProperty.from_preset("magpie")
    features['element'] = elem_prop.featurize(composition)
    
    # Electronegativity features
    en_diff = ElectronegativityDiff()
    features['en_diff'] = en_diff.featurize(composition)
    
    # Atomic packing efficiency
    ape = AtomicPackingEfficiency()
    features['packing'] = ape.featurize(composition)
    
    return features

# Generate composition-based dataframe
def create_features_df(structures, properties=None):
    """
    Create feature dataframe from structures
    """
    data = []
    
    for i, struct in enumerate(structures):
        row = {}
        
        # Composition features
        comp_feat = featurize_composition(struct.composition)
        for key, val in comp_feat.items():
            if isinstance(val, (list, np.ndarray)):
                for j, v in enumerate(val):
                    row[f"{key}_{j}"] = v
            else:
                row[key] = val
        
        # Structure features
        struct_feat = featurize_structure(struct)
        row['density'] = struct_feat['density'][0]
        row['vpa'] = struct_feat['density'][1]  # volume per atom
        
        # Add property if provided
        if properties is not None:
            row['target'] = properties[i]
        
        data.append(row)
    
    return pd.DataFrame(data)
```

### 2. Graph Neural Networks

Use graph neural networks for property prediction.

**CGCNN (Crystal Graph Convolutional Neural Network):**
```python
import torch
from cgcnn.data import CIFData, collate_pool
from cgcnn.model import CrystalGraphConvNet
from torch.utils.data import DataLoader

def prepare_cgcnn_data(cif_dir, batch_size=32):
    """
    Prepare data for CGCNN training
    """
    dataset = CIFData(cif_dir)
    
    # Split dataset
    train_size = int(0.8 * len(dataset))
    val_size = int(0.1 * len(dataset))
    test_size = len(dataset) - train_size - val_size
    
    train_dataset, val_dataset, test_dataset = torch.utils.data.random_split(
        dataset, [train_size, val_size, test_size]
    )
    
    # Create data loaders
    train_loader = DataLoader(
        train_dataset, batch_size=batch_size,
        shuffle=True, collate_fn=collate_pool
    )
    val_loader = DataLoader(
        val_dataset, batch_size=batch_size,
        collate_fn=collate_pool
    )
    
    return train_loader, val_loader, dataset

def create_cgcnn_model(orig_atom_fea_len, nbr_fea_len):
    """
    Create CGCNN model
    """
    model = CrystalGraphConvNet(
        orig_atom_fea_len=orig_atom_fea_len,
        nbr_fea_len=nbr_fea_len,
        atom_fea_len=64,
        n_conv=3,
        h_fea_len=128,
        n_h=1,
        classification=False
    )
    return model

# Training loop
def train_cgcnn(model, train_loader, val_loader, epochs=100, lr=0.001):
    """
    Train CGCNN model
    """
    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=50, gamma=0.5)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    best_val_loss = float('inf')
    
    for epoch in range(epochs):
        # Training
        model.train()
        train_loss = 0
        for batch in train_loader:
            atom_fea, nbr_fea, nbr_fea_idx, target, _ = batch
            
            atom_fea = atom_fea.to(device)
            nbr_fea = nbr_fea.to(device)
            nbr_fea_idx = nbr_fea_idx.to(device)
            target = target.to(device)
            
            optimizer.zero_grad()
            output = model(atom_fea, nbr_fea, nbr_fea_idx, None)
            loss = criterion(output, target)
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item()
        
        # Validation
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for batch in val_loader:
                atom_fea, nbr_fea, nbr_fea_idx, target, _ = batch
                
                atom_fea = atom_fea.to(device)
                nbr_fea = nbr_fea.to(device)
                nbr_fea_idx = nbr_fea_idx.to(device)
                target = target.to(device)
                
                output = model(atom_fea, nbr_fea, nbr_fea_idx, None)
                loss = criterion(output, target)
                val_loss += loss.item()
        
        scheduler.step()
        
        if (epoch + 1) % 10 == 0:
            print(f"Epoch {epoch+1}: Train Loss = {train_loss/len(train_loader):.4f}, "
                  f"Val Loss = {val_loss/len(val_loader):.4f}")
        
        # Save best model
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            torch.save(model.state_dict(), "best_cgcnn_model.pth")
    
    return model
```

**PyTorch Geometric for Materials:**
```python
import torch
import torch.nn as nn
from torch_geometric.nn import GCNConv, global_mean_pool, MessagePassing
from torch_geometric.data import Data, DataLoader

def structure_to_graph(structure, y=None, cutoff=8.0):
    """
    Convert pymatgen Structure to PyTorch Geometric Data
    """
    # Node features: atomic numbers
    atomic_nums = torch.tensor([site.specie.Z for site in structure], 
                               dtype=torch.long)
    
    # One-hot encoding for atomic numbers (up to 100)
    x = torch.zeros(len(structure), 100)
    x[torch.arange(len(structure)), atomic_nums - 1] = 1
    
    # Edge features: neighbor list within cutoff
    edges = []
    edge_feats = []
    
    for i, site in enumerate(structure):
        neighbors = structure.get_neighbors(site, cutoff)
        for neighbor in neighbors:
            j = neighbor[2]  # site index
            distance = neighbor[1]  # distance
            edges.append([i, j])
            edge_feats.append([distance])
    
    edge_index = torch.tensor(edges, dtype=torch.long).t().contiguous()
    edge_attr = torch.tensor(edge_feats, dtype=torch.float)
    
    # Create data object
    data = Data(x=x, edge_index=edge_index, edge_attr=edge_attr)
    
    if y is not None:
        data.y = torch.tensor([y], dtype=torch.float)
    
    return data

class MaterialsGNN(nn.Module):
    """
    Graph Neural Network for materials property prediction
    """
    def __init__(self, hidden_dim=64, num_layers=3):
        super().__init__()
        
        self.convs = nn.ModuleList()
        self.batch_norms = nn.ModuleList()
        
        # Input layer
        self.convs.append(GCNConv(100, hidden_dim))
        self.batch_norms.append(nn.BatchNorm1d(hidden_dim))
        
        # Hidden layers
        for _ in range(num_layers - 1):
            self.convs.append(GCNConv(hidden_dim, hidden_dim))
            self.batch_norms.append(nn.BatchNorm1d(hidden_dim))
        
        # Output layer
        self.fc = nn.Linear(hidden_dim, 1)
    
    def forward(self, data):
        x, edge_index, batch = data.x, data.edge_index, data.batch
        
        # Graph convolutions
        for conv, bn in zip(self.convs, self.batch_norms):
            x = conv(x, edge_index)
            x = bn(x)
            x = torch.relu(x)
        
        # Global pooling
        x = global_mean_pool(x, batch)
        
        # Output
        x = self.fc(x)
        
        return x.squeeze(-1)

# Training function
def train_gnn(model, train_loader, val_loader, epochs=100):
    """
    Train GNN model
    """
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    criterion = nn.MSELoss()
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        
        for batch in train_loader:
            batch = batch.to(device)
            optimizer.zero_grad()
            
            pred = model(batch)
            loss = criterion(pred, batch.y)
            
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
        
        # Validation
        if (epoch + 1) % 10 == 0:
            model.eval()
            val_loss = 0
            with torch.no_grad():
                for batch in val_loader:
                    batch = batch.to(device)
                    pred = model(batch)
                    val_loss += criterion(pred, batch.y).item()
            
            print(f"Epoch {epoch+1}: Train Loss = {total_loss/len(train_loader):.4f}, "
                  f"Val Loss = {val_loss/len(val_loader):.4f}")
```

### 3. Using Pre-trained Models

Leverage pre-trained foundation models for materials.

**MEGNet:**
```python
from megnet.models import MEGNetModel
from megnet.data.crystal import CrystalGraph
from pymatgen.core import Structure
import numpy as np

def load_pretrained_megnet(property_name="formation_energy"):
    """
    Load pre-trained MEGNet model
    
    Available models: formation_energy, band_gap, bulk_modulus, 
                      shear_modulus, thermal_conductivity
    """
    # Download or load from local path
    model_path = f"pretrained_models/megnet_{property_name}.hdf5"
    
    try:
        model = MEGNetModel.from_file(model_path)
        print(f"Loaded pre-trained MEGNet model for {property_name}")
        return model
    except:
        print(f"Model not found. Using base MEGNet architecture.")
        from megnet.models import MEGNetModel
        model = MEGNetModel(nblocks=3, lr=1e-3,
                           n1=64, n2=32, n3=16,
                           npass=3, ntarget=1)
        return model

def predict_properties(structures, model=None):
    """
    Predict properties for multiple structures
    """
    if model is None:
        model = load_pretrained_megnet("formation_energy")
    
    predictions = []
    for struct in structures:
        pred = model.predict_structure(struct)
        predictions.append(pred)
    
    return np.array(predictions)

# Multi-property prediction
def predict_all_properties(structure):
    """
    Predict multiple properties for a structure
    """
    properties = {}
    
    property_names = [
        "formation_energy",
        "band_gap", 
        "bulk_modulus",
        "shear_modulus"
    ]
    
    for prop_name in property_names:
        try:
            model = load_pretrained_megnet(prop_name)
            pred = model.predict_structure(structure)
            properties[prop_name] = float(pred)
        except Exception as e:
            print(f"Could not predict {prop_name}: {e}")
            properties[prop_name] = None
    
    return properties

# Usage
struct = Structure.from_file("POSCAR")
props = predict_all_properties(struct)
print(f"Predicted properties: {props}")
```

### 4. Training Custom Models

Train models on your own dataset.

```python
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

def train_property_predictor(structures, properties, model_type="gbr"):
    """
    Train a property prediction model
    
    Args:
        structures: List of pymatgen Structures
        properties: Array of target properties
        model_type: "gbr" (GradientBoosting), "rf" (RandomForest), "nn" (NeuralNet)
    """
    # Create features
    print("Featurizing structures...")
    df = create_features_df(structures, properties)
    
    X = df.drop('target', axis=1).values
    y = df['target'].values
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Select model
    if model_type == "gbr":
        model = GradientBoostingRegressor(
            n_estimators=200,
            max_depth=5,
            learning_rate=0.1,
            random_state=42
        )
    elif model_type == "rf":
        model = RandomForestRegressor(
            n_estimators=200,
            max_depth=10,
            random_state=42
        )
    elif model_type == "nn":
        from sklearn.neural_network import MLPRegressor
        model = MLPRegressor(
            hidden_layer_sizes=(128, 64, 32),
            max_iter=500,
            early_stopping=True,
            random_state=42
        )
    
    # Train
    print(f"Training {model_type} model...")
    model.fit(X_train_scaled, y_train)
    
    # Evaluate
    y_pred_train = model.predict(X_train_scaled)
    y_pred_test = model.predict(X_test_scaled)
    
    train_mae = mean_absolute_error(y_train, y_pred_train)
    test_mae = mean_absolute_error(y_test, y_pred_test)
    test_r2 = r2_score(y_test, y_pred_test)
    
    print(f"\nTraining MAE: {train_mae:.4f}")
    print(f"Test MAE: {test_mae:.4f}")
    print(f"Test R²: {test_r2:.4f}")
    
    # Cross-validation
    cv_scores = cross_val_score(model, X_train_scaled, y_train, 
                                 cv=5, scoring='neg_mean_absolute_error')
    print(f"CV MAE: {-cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
    
    # Save model and scaler
    joblib.dump({
        'model': model,
        'scaler': scaler,
        'feature_names': df.drop('target', axis=1).columns.tolist()
    }, 'property_predictor.pkl')
    
    return model, scaler

# Prediction function
def predict_with_model(structures, model_path='property_predictor.pkl'):
    """
    Predict properties using trained model
    """
    # Load model
    saved = joblib.load(model_path)
    model = saved['model']
    scaler = saved['scaler']
    
    # Featurize
    df = create_features_df(structures)
    X = df.values
    X_scaled = scaler.transform(X)
    
    # Predict
    predictions = model.predict(X_scaled)
    
    return predictions
```

### 5. High-Throughput Screening

Screen large databases for materials with target properties.

```python
from mp_api.client import MPRester
from tqdm import tqdm
import pandas as pd

def screen_materials_project(criteria, property_predictor=None, 
                              max_results=1000):
    """
    Screen Materials Project for materials meeting criteria
    
    Args:
        criteria: Dict with property filters (e.g., {'band_gap': (1, 3)})
        property_predictor: Optional trained model for additional properties
        max_results: Maximum number of results
    """
    with MPRester() as mpr:
        # Search for materials
        docs = mpr.materials.summary.search(
            **criteria,
            fields=["material_id", "formula_pretty", "structure",
                   "band_gap", "formation_energy_per_atom"],
            num_sites=(1, 50),  # Reasonable size
            total_docs=max_results
        )
        
        results = []
        
        for doc in tqdm(docs, desc="Processing materials"):
            result = {
                'material_id': doc.material_id,
                'formula': doc.formula_pretty,
                'band_gap': doc.band_gap,
                'formation_energy': doc.formation_energy_per_atom,
            }
            
            # Predict additional properties if model provided
            if property_predictor is not None:
                struct = doc.structure
                pred = property_predictor.predict_structure(struct)
                result['predicted_property'] = float(pred)
            
            results.append(result)
        
        return pd.DataFrame(results)

# Stability screening
def find_stable_materials(chemsys, energy_above_hull=0.05):
    """
    Find stable materials in a chemical system
    """
    with MPRester() as mpr:
        docs = mpr.materials.summary.search(
            chemsys=chemsys,
            energy_above_hull=(0, energy_above_hull),
            fields=["material_id", "formula_pretty", "structure",
                   "energy_above_hull", "formation_energy_per_atom"]
        )
        
        results = []
        for doc in docs:
            results.append({
                'material_id': doc.material_id,
                'formula': doc.formula_pretty,
                'energy_above_hull': doc.energy_above_hull,
                'formation_energy': doc.formation_energy_per_atom
            })
        
        return pd.DataFrame(results)

# Inverse design: find materials with target properties
def inverse_design(target_properties, search_space, tolerance=0.2):
    """
    Find materials matching target properties
    
    Args:
        target_properties: Dict like {'band_gap': 2.0, 'formation_energy': -2.0}
        search_space: List of candidate structures
        tolerance: Acceptable fractional deviation
    """
    matches = []
    
    for struct in search_space:
        score = 0
        match = True
        
        for prop, target in target_properties.items():
            # Predict property
            predicted = predict_property(struct, prop)
            
            # Check if within tolerance
            if abs(predicted - target) / abs(target) > tolerance:
                match = False
                break
            
            score += abs(predicted - target) / abs(target)
        
        if match:
            matches.append({
                'structure': struct,
                'formula': struct.composition.reduced_formula,
                'score': score
            })
    
    # Sort by score (lower is better)
    matches.sort(key=lambda x: x['score'])
    
    return matches
```

## Common Workflows

### Workflow 1: Complete ML Pipeline

```python
"""
Complete ML pipeline: data → features → model → predictions
"""
from mp_api.client import MPRester
from pymatgen.core import Structure
import pandas as pd
import numpy as np

def complete_ml_pipeline(chemsys="Si-O", target_property="band_gap",
                         output_dir="./ml_model"):
    """
    End-to-end ML pipeline for materials property prediction
    """
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # Step 1: Download data from Materials Project
    print("[1/5] Downloading data from Materials Project...")
    with MPRester() as mpr:
        docs = mpr.materials.summary.search(
            chemsys=chemsys,
            fields=["material_id", "structure", target_property],
            total_docs=1000
        )
    
    structures = [doc.structure for doc in docs]
    properties = [getattr(doc, target_property) for doc in docs]
    
    # Remove None values
    valid_data = [(s, p) for s, p in zip(structures, properties) if p is not None]
    structures = [d[0] for d in valid_data]
    properties = [d[1] for d in valid_data]
    
    print(f"  Downloaded {len(structures)} structures")
    
    # Step 2: Featurize
    print("[2/5] Featurizing structures...")
    df = create_features_df(structures, properties)
    df.to_csv(os.path.join(output_dir, "features.csv"), index=False)
    print(f"  Created {len(df.columns)-1} features")
    
    # Step 3: Train model
    print("[3/5] Training model...")
    model, scaler = train_property_predictor(
        structures, properties, model_type="gbr"
    )
    print("  Model trained and saved")
    
    # Step 4: Evaluate
    print("[4/5] Evaluating model...")
    predictions = predict_with_model(structures[:100], 
                                     os.path.join(output_dir, 'property_predictor.pkl'))
    mae = np.mean(np.abs(np.array(properties[:100]) - predictions))
    print(f"  MAE on sample: {mae:.4f}")
    
    # Step 5: Screen new materials
    print("[5/5] Screening new candidates...")
    # Generate candidate structures (e.g., from prototype library)
    # or use hypothetical structures
    print("  Pipeline complete!")
    
    print(f"\n{'='*50}")
    print("ML PIPELINE SUMMARY")
    print(f"{'='*50}")
    print(f"Target property: {target_property}")
    print(f"Training samples: {len(structures)}")
    print(f"Number of features: {len(df.columns)-1}")
    print(f"Model type: Gradient Boosting Regressor")
    print(f"Model saved to: {output_dir}/property_predictor.pkl")

# Usage
complete_ml_pipeline(chemsys="Si-O", target_property="band_gap")
```

### Workflow 2: Active Learning for Materials Discovery

```python
"""
Active learning loop for efficient materials discovery
"""
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF, ConstantKernel as C

def active_learning_loop(candidates, n_iterations=5, n_initial=10, 
                         n_query=5):
    """
    Active learning for materials discovery
    
    Iteratively selects most informative candidates for DFT calculation
    """
    # Initialize with random samples
    labeled_idx = np.random.choice(len(candidates), n_initial, replace=False)
    unlabeled_idx = np.setdiff1d(np.arange(len(candidates)), labeled_idx)
    
    # Featurize all candidates
    print("Featurizing candidates...")
    X_all = np.array([featurize_structure(s) for s in candidates])
    
    # Active learning loop
    for iteration in range(n_iterations):
        print(f"\n{'='*50}")
        print(f"Active Learning Iteration {iteration + 1}/{n_iterations}")
        print(f"{'='*50}")
        
        # Get labeled data
        X_labeled = X_all[labeled_idx]
        y_labeled = np.array([get_property(candidates[i]) for i in labeled_idx])
        
        # Train GP model
        kernel = C(1.0, (1e-3, 1e3)) * RBF(1.0, (1e-2, 1e2))
        gp = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10)
        gp.fit(X_labeled, y_labeled)
        
        # Predict on unlabeled data
        X_unlabeled = X_all[unlabeled_idx]
        y_pred, sigma = gp.predict(X_unlabeled, return_std=True)
        
        # Acquisition: select points with highest uncertainty
        # (uncertainty sampling)
        query_idx_in_unlabeled = np.argsort(sigma)[-n_query:]
        query_idx = unlabeled_idx[query_idx_in_unlabeled]
        
        print(f"Query {n_query} new samples for DFT calculation:")
        for idx in query_idx:
            print(f"  - {candidates[idx].composition.reduced_formula}")
        
        # Simulate DFT calculation (in practice, run VASP)
        # Here we just update indices
        labeled_idx = np.concatenate([labeled_idx, query_idx])
        unlabeled_idx = np.setdiff1d(unlabeled_idx, query_idx)
        
        print(f"Labeled samples: {len(labeled_idx)}")
        print(f"Unlabeled samples: {len(unlabeled_idx)}")
    
    return labeled_idx
```

## Best Practices

### Data Preparation
1. **Filter data**: Remove outliers and erroneous entries
2. **Stratified splitting**: Ensure compositional diversity in train/test
3. **Feature scaling**: Always scale features before training
4. **Validation**: Use nested cross-validation for hyperparameter tuning

### Model Selection
1. **Start simple**: Try Random Forest or Gradient Boosting first
2. **Graph models**: Use GNNs when structure matters most
3. **Ensemble**: Combine multiple models for robust predictions
4. **Uncertainty**: Use GP or ensemble disagreement for uncertainty estimates

### Evaluation
1. **Domain validation**: Test on materials outside training distribution
2. **Physics constraints**: Ensure predictions satisfy physical bounds
3. **Error analysis**: Understand where model fails
4. **Calibration**: Check if uncertainty estimates are well-calibrated

### Deployment
1. **Version control**: Track model versions and training data
2. **Monitoring**: Track prediction quality on new data
3. **Update strategy**: Plan for periodic retraining
4. **Documentation**: Document model limitations and valid ranges

## Troubleshooting

**"Poor prediction accuracy":**
- Check if features are informative for target property
- Try different model architectures
- Increase training data size
- Check for data leakage

**"Model overfitting":**
- Reduce model complexity
- Add regularization
- Use dropout for neural networks
- Collect more training data

**"Slow training":**
- Use GPU acceleration for deep learning
- Reduce feature dimensionality
- Sample training data
- Use distributed training

## Additional Resources

- **Matminer docs**: https://hackingmaterials.lbl.gov/matminer/
- **MEGNet paper**: https://doi.org/10.1021/acs.chemmater.9b01294
- **CGCNN paper**: https://doi.org/10.1103/PhysRevLett.120.145301
- **Materials Project ML**: https://materialsproject.org/ml

## Version Notes

- Requires pymatgen >= 2023.x
- PyTorch 2.0+ recommended for GNNs
- Python 3.10 or higher recommended
- Some features require CUDA for GPU acceleration
