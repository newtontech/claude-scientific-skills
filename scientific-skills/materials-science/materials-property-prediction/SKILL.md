---
name: materials-property-prediction
description: Materials property prediction workflows. Integrate with Materials Project API, apply machine learning models for property prediction, and automate high-throughput screening.
homepage: https://materialsproject.org
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":["python3"],"env":["MP_API_KEY"]},"primaryEnv":"MP_API_KEY"}}
---

# Materials Property Prediction

Materials property prediction workflows. Integrate with Materials Project API, apply machine learning models, and automate high-throughput screening.

## Prerequisites

```bash
# Install required packages
pip install mp-api pymatgen scikit-learn xgboost

# Optional for deep learning
pip install torch torch-geometric

# Set API key
export MP_API_KEY="your_api_key_here"
# Get API key from: https://materialsproject.org/api
```

## Materials Project API Integration

### Search Materials

```python
from mp_api.client import MPRester

# Initialize API client
with MPRester() as mpr:
    # Search by formula
    docs = mpr.materials.summary.search(
        formula="LiFePO4",
        fields=["material_id", "formula_pretty", "energy_per_atom", "band_gap"]
    )
    
    for doc in docs:
        print(f"{doc.material_id}: {doc.formula_pretty}")
        print(f"  Energy/atom: {doc.energy_per_atom:.4f} eV")
        print(f"  Band gap: {doc.band_gap:.3f} eV")
```

### Get Material Properties

```python
with MPRester() as mpr:
    # Get detailed properties by material ID
    doc = mpr.materials.summary.get_data_by_id("mp-19017")
    
    print(f"Formula: {doc.formula_pretty}")
    print(f"Structure: {doc.structure}")
    print(f"Density: {doc.density:.3f} g/cm³")
    print(f"Bulk modulus: {doc.k_voigt:.2f} GPa")
    print(f"Shear modulus: {doc.g_voigt:.2f} GPa")
    
    # Get electronic structure
    bandstructure = mpr.get_bandstructure_by_material_id("mp-19017")
    dos = mpr.get_dos_by_material_id("mp-19017")
```

### Batch Query

```python
# Query multiple materials at once
with MPRester() as mpr:
    # Search by elements
    docs = mpr.materials.summary.search(
        elements=["Li", "Fe", "P", "O"],
        num_elements=(4, 4),
        band_gap=(0.5, 3.0),
        fields=["material_id", "formula_pretty", "band_gap", "energy_above_hull"]
    )
    
    print(f"Found {len(docs)} materials")
    
    for doc in docs:
        if doc.energy_above_hull < 0.05:  # Stable materials only
            print(f"{doc.material_id}: {doc.formula_pretty}, "
                  f"Eg={doc.band_gap:.2f} eV")
```

### Download Structure Data

```python
import json

with MPRester() as mpr:
    # Get structures for a set of materials
    mp_ids = ["mp-19017", "mp-135", "mp-149"]
    
    structures_data = []
    for mp_id in mp_ids:
        doc = mpr.materials.summary.get_data_by_id(mp_id)
        structures_data.append({
            'material_id': mp_id,
            'formula': doc.formula_pretty,
            'structure': doc.structure.as_dict(),
            'band_gap': doc.band_gap,
            'energy_per_atom': doc.energy_per_atom
        })
    
    # Save to JSON
    with open('mp_structures.json', 'w') as f:
        json.dump(structures_data, f)
```

## Feature Engineering

### Structure Featurization

```python
from pymatgen.core import Structure, Composition
from pymatgen.core.periodic_table import Element
import numpy as np

def featurize_structure(structure):
    """Extract features from crystal structure."""
    
    features = {}
    comp = structure.composition
    
    # Composition features
    features['num_elements'] = len(comp.elements)
    features['num_sites'] = len(structure)
    
    # Average atomic properties
    avg_properties = {
        'atomic_radius': [],
        'electronegativity': [],
        'row': [],
        'group': [],
        'atomic_mass': []
    }
    
    for element in comp.elements:
        el = Element(str(element))
        frac = comp.get_atomic_fraction(element)
        
        avg_properties['atomic_radius'].append(el.atomic_radius * frac)
        avg_properties['electronegativity'].append(el.X * frac)
        avg_properties['row'].append(el.row * frac)
        avg_properties['group'].append(el.group * frac)
        avg_properties['atomic_mass'].append(el.atomic_mass * frac)
    
    for prop, values in avg_properties.items():
        features[f'avg_{prop}'] = sum(values)
        features[f'std_{prop}'] = np.std(values) if len(values) > 1 else 0
    
    # Structural features
    features['density'] = structure.density
    features['volume_per_atom'] = structure.volume / len(structure)
    
    # Lattice features
    lattice = structure.lattice
    features['a'] = lattice.a
    features['b'] = lattice.b
    features['c'] = lattice.c
    features['alpha'] = lattice.alpha
    features['beta'] = lattice.beta
    features['gamma'] = lattice.gamma
    features['volume'] = lattice.volume
    
    # Space group
    from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
    sga = SpacegroupAnalyzer(structure)
    features['space_group_number'] = sga.get_space_group_number()
    features['crystal_system'] = sga.get_crystal_system()
    
    return features

# Example usage
structure = Structure.from_file("POSCAR")
features = featurize_structure(structure)
print(features)
```

### Matminer Featurizers

```bash
pip install matminer
```

```python
from matminer.featurizers.composition import ElementProperty
from matminer.featurizers.structure import SiteStatsFingerprint

# Element property featurizer
ep_featurizer = ElementProperty.from_preset("magpie")
comp_features = ep_featurizer.featurize(composition)

# Structural fingerprint
ssf = SiteStatsFingerprint.from_preset("CrystalNNFingerprint_ops")
struct_features = ssf.featurize(structure)
```

## Machine Learning Models

### Train Band Gap Predictor

```python
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import pandas as pd

# Load data
df = pd.read_csv('materials_data.csv')

# Features and target
feature_cols = ['num_elements', 'num_sites', 'avg_atomic_radius',
                'avg_electronegativity', 'density', 'volume_per_atom']
X = df[feature_cols]
y = df['band_gap']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MAE: {mae:.3f} eV")
print(f"R²: {r2:.3f}")

# Feature importance
importances = pd.Series(model.feature_importances_, index=feature_cols)
print("\nFeature Importances:")
print(importances.sort_values(ascending=False))
```

### Classification Model (Metal vs. Insulator)

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Binary classification: metal (0) vs insulator (1)
df['is_insulator'] = (df['band_gap'] > 0.1).astype(int)

X = df[feature_cols]
y = df['is_insulator']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Evaluate
y_pred = clf.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
print(classification_report(y_test, y_pred, target_names=['Metal', 'Insulator']))
```

### XGBoost Model

```python
import xgboost as xgb

# XGBoost regressor
xgb_model = xgb.XGBRegressor(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    random_state=42
)

xgb_model.fit(X_train, y_train)
y_pred = xgb_model.predict(X_test)

print(f"MAE: {mean_absolute_error(y_test, y_pred):.3f} eV")

# Save model
xgb_model.save_model('band_gap_model.json')
```

## High-Throughput Screening

### Screen Candidate Materials

```python
def screen_materials(candidate_structures, model, threshold):
    """
    Screen materials for desired property.
    
    Args:
        candidate_structures: List of pymatgen Structures
        model: Trained ML model
        threshold: Property threshold
    
    Returns:
        List of promising candidates
    """
    candidates = []
    
    for i, structure in enumerate(candidate_structures):
        # Featurize
        features = featurize_structure(structure)
        X = np.array([[features[col] for col in feature_cols]])
        
        # Predict
        prediction = model.predict(X)[0]
        
        if prediction > threshold:
            candidates.append({
                'index': i,
                'formula': structure.formula,
                'predicted_band_gap': prediction,
                'features': features
            })
    
    return candidates

# Example usage
with MPRester() as mpr:
    # Query candidate materials
    docs = mpr.materials.summary.search(
        chemsys="Li-Fe-O",
        energy_above_hull=(0, 0.1),
        fields=["structure", "formula_pretty"]
    )
    
    structures = [doc.structure for doc in docs]
    
    # Screen for wide band gap materials
    promising = screen_materials(structures, model, threshold=2.0)
    
    print(f"Found {len(promising)} candidates with Eg > 2.0 eV")
    for cand in promising:
        print(f"  {cand['formula']}: {cand['predicted_band_gap']:.2f} eV")
```

### Generate Candidate Structures

```python
from pymatgen.core import Structure, Lattice, Specie
from itertools import product

def generate_substitutions(base_structure, substitutions, num_subs=1):
    """
    Generate structures with elemental substitutions.
    
    Args:
        base_structure: Base pymatgen Structure
        substitutions: Dict {original_element: [substitute_elements]}
        num_subs: Number of sites to substitute
    """
    from pymatgen.transformations.standard_transformations import \
        SubstitutionTransformation
    
    new_structures = []
    
    for element, substitutes in substitutions.items():
        for sub in substitutes:
            trans = SubstitutionTransformation({element: sub})
            new_struct = trans.apply_transformation(base_structure)
            new_structures.append(new_struct)
    
    return new_structures

# Example: Generate Li-Mn-O variants
base = Structure.from_file("LiFePO4.cif")
substitutions = {
    "Fe": ["Mn", "Co", "Ni"]
}

variants = generate_substitutions(base, substitutions)
print(f"Generated {len(variants)} variants")
```

## Workflow Automation

### Complete ML Pipeline

```python
class PropertyPredictor:
    """Complete ML pipeline for materials property prediction."""
    
    def __init__(self, property_name='band_gap'):
        self.property_name = property_name
        self.model = RandomForestRegressor(n_estimators=100)
        self.feature_cols = None
        self.scaler = StandardScaler()
        
    def fetch_training_data(self, elements, max_entries=1000):
        """Fetch training data from Materials Project."""
        
        with MPRester() as mpr:
            docs = mpr.materials.summary.search(
                elements=elements,
                fields=["material_id", "structure", self.property_name]
            )
        
        data = []
        for doc in docs[:max_entries]:
            if getattr(doc, self.property_name) is not None:
                features = featurize_structure(doc.structure)
                features['material_id'] = doc.material_id
                features[self.property_name] = getattr(doc, self.property_name)
                data.append(features)
        
        return pd.DataFrame(data)
    
    def train(self, df):
        """Train the model."""
        
        # Select feature columns (exclude non-numeric)
        exclude = ['material_id', self.property_name, 'crystal_system']
        self.feature_cols = [c for c in df.columns if c not in exclude]
        
        X = df[self.feature_cols].fillna(0)
        y = df[self.property_name]
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        mae = mean_absolute_error(y_test, y_pred)
        
        print(f"Training complete. MAE: {mae:.3f}")
        return mae
    
    def predict(self, structure):
        """Predict property for a new structure."""
        
        features = featurize_structure(structure)
        X = np.array([[features.get(col, 0) for col in self.feature_cols]])
        X_scaled = self.scaler.transform(X)
        
        return self.model.predict(X_scaled)[0]

# Usage
predictor = PropertyPredictor(property_name='band_gap')
df = predictor.fetch_training_data(elements=['Li', 'Fe', 'O', 'P'])
predictor.train(df)

# Predict for new structure
new_struct = Structure.from_file("new_material.cif")
predicted_gap = predictor.predict(new_struct)
print(f"Predicted band gap: {predicted_gap:.2f} eV")
```

## Best Practices

1. **Data Quality**: Filter unstable materials (energy_above_hull < 0.05)
2. **Feature Selection**: Remove correlated features
3. **Cross-Validation**: Use k-fold CV for robust evaluation
4. **Domain Knowledge**: Include physics-based features
5. **Validation**: Compare with DFT calculations for key predictions
6. **Uncertainty**: Estimate prediction confidence

## References

- [Materials Project API](https://api.materialsproject.org/)
- [Matminer Documentation](https://hackingmaterials.lbl.gov/matminer/)
- [pymatgen Machine Learning](https://pymatgen.org/pymatgen.analysis.html)
- [CGCNN Paper](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.120.145301)
