from pathlib import Path
import json
# Loaders for various JSON data files

# Load classes from JSON file
def load_classes():
    base_dir = Path(__file__).resolve().parent.parent
    classes_path = base_dir / "data" / "classes.json"
    with classes_path.open(encoding="utf-8") as classes_file:
        return json.load(classes_file)

# Load races from JSON file
def load_races():
    base_dir = Path(__file__).resolve().parent.parent
    races_path = base_dir / "data" / "races.json"
    with races_path.open(encoding="utf-8") as races_file:
        return json.load(races_file)
    
# Load skills from JSON file
def load_skills():
    base_dir = Path(__file__).resolve().parent.parent
    skills_path = base_dir / "data" / "skills.json"
    with skills_path.open(encoding="utf-8") as skills_file:
        return json.load(skills_file)
    
# Load heritages from JSON file
def load_heritages():
    base_dir = Path(__file__).resolve().parent.parent
    heritages_path = base_dir / "data" / "heritages.json"
    with heritages_path.open(encoding="utf-8") as heritages_file:
        return json.load(heritages_file)
    
# Load backgrounds from JSON file
def load_backgrounds():
    base_dir = Path(__file__).resolve().parent.parent
    backgrounds_path = base_dir / "data" / "backgrounds.json"
    with backgrounds_path.open(encoding="utf-8") as backgrounds_file:
        return json.load(backgrounds_file)
    
# Load feats from JSON file
def load_feats():
    base_dir = Path(__file__).resolve().parent.parent
    feats_path = base_dir / "data" / "feats.json"
    with feats_path.open(encoding="utf-8") as feats_file:
        return json.load(feats_file)
    
def load_traits():
    base_dir = Path(__file__).resolve().parent.parent
    feats_path = base_dir / "data" / "traits.json"
    with feats_path.open(encoding="utf-8") as traits_file:
        return json.load(traits_file)