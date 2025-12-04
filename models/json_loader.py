from pathlib import Path
import json

def load_classes():
    base_dir = Path(__file__).resolve().parent.parent
    classes_path = base_dir / "data" / "classes.json"
    with classes_path.open(encoding="utf-8") as classes_file:
        return json.load(classes_file)

def load_races():
    base_dir = Path(__file__).resolve().parent.parent
    races_path = base_dir / "data" / "races.json"
    with races_path.open(encoding="utf-8") as races_file:
        return json.load(races_file)
    
def load_skills():
    base_dir = Path(__file__).resolve().parent.parent
    skills_path = base_dir / "data" / "skills.json"
    with skills_path.open(encoding="utf-8") as skills_file:
        return json.load(skills_file)
    
def load_heritages():
    base_dir = Path(__file__).resolve().parent.parent
    heritages_path = base_dir / "data" / "heritages.json"
    with heritages_path.open(encoding="utf-8") as heritages_file:
        return json.load(heritages_file)
    
def load_backgrounds():
    base_dir = Path(__file__).resolve().parent.parent
    backgrounds_path = base_dir / "data" / "backgrounds.json"
    with backgrounds_path.open(encoding="utf-8") as backgrounds_file:
        return json.load(backgrounds_file)