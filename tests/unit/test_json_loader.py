import pytest
import json
from pathlib import Path
import wotr_planner.models.json_loader as jl

def loader_params():
    """
    Returns a list of tuples containing loader functions and their corresponding JSON filenames.
    Each tuple is in the form (loader_function, "filename.json").
    """
    return [
        (jl.load_classes, "classes.json"),
        (jl.load_races, "races.json"),
        (jl.load_feats, "feats.json"),
        (jl.load_skills, "skills.json"),
        (jl.load_heritages, "heritages.json"),
        (jl.load_backgrounds, "backgrounds.json")
    ]

def make_loader_dirs(tmp_path):
    """
    Create the directory structure for the loaders.
    Args:
        tmp_path: pytest fixture to create a temporary directory.
    Returns:
        Tuple of (module_dir, data_dir) Paths.
    """
    module_dir = tmp_path / "src" / "wotr_planner" / "models"
    data_dir = tmp_path / "src" / "wotr_planner" / "data"
    module_dir.mkdir(parents=True)
    data_dir.mkdir(parents=True)
    return module_dir, data_dir

def patch_loader_file(monkeypatch, module_dir):
    """
    Patch the __file__ attribute of the json_loader module to point to the temporary module directory.
    Args:
        monkeypatch: pytest fixture to modify behavior for testing.
        module_dir: Path to the temporary module directory.
    """
    monkeypatch.setattr(jl, "__file__", str(module_dir / "json_loader.py"))

# Parametrized tests for multiple loaders
@pytest.mark.parametrize("loader, filename", loader_params())
def test_loaders_valid_json(monkeypatch, tmp_path, loader, filename):
    """
    Test that various loaders can successfully load valid JSON data.
    Args:
        monkeypatch: pytest fixture to modify behavior for testing.
        tmp_path: pytest fixture to create a temporary directory.
        loader: The loader function to test.
        filename: The name of the JSON file to create with valid content.
    """
    module_dir, data_dir = make_loader_dirs(tmp_path)
    (data_dir / filename).write_text('["ok"]', encoding="utf-8")
    patch_loader_file(monkeypatch, module_dir)

    result = loader()
    assert result == ["ok"]

# Parametrized tests for multiple loaders
@pytest.mark.parametrize("loader, filename", loader_params())
def test_loaders_invalid_json(monkeypatch, tmp_path, loader, filename):
    """
    Test that various loaders raise JSONDecodeError when the file contains invalid JSON.
    Args:
        monkeypatch: pytest fixture to modify behavior for testing.
        tmp_path: pytest fixture to create a temporary directory.
        loader: The loader function to test.
        filename: The name of the JSON file to create with invalid content.
    """
    # Create a temporary invalid JSON file
    module_dir, data_dir = make_loader_dirs(tmp_path)

    # Write invalid JSON content to the specified file
    (data_dir / filename).write_text("{ invalid json }", encoding="utf-8")

    # Patch the data directory path in the json_loader module
    patch_loader_file(monkeypatch, module_dir)

    with pytest.raises(json.JSONDecodeError):
        loader()

# Parametrized tests for multiple loaders
@pytest.mark.parametrize("loader, filename", loader_params())
def test_loaders_file_not_found(monkeypatch, tmp_path, loader, filename):
    """
    Test that various loaders raise FileNotFoundError when the file does not exist.
    Args:
        monkeypatch: pytest fixture to modify behavior for testing.
        tmp_path: pytest fixture to create a temporary directory.
        loader: The loader function to test.
        filename: The name of the JSON file to create with invalid content.
    """
    # Create a temporary directory structure without the JSON file
    module_dir, data_dir = make_loader_dirs(tmp_path)

    # Patch the data directory path in the json_loader module
    patch_loader_file(monkeypatch, module_dir)

    with pytest.raises(FileNotFoundError):
        loader()