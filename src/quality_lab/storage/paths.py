import platform
from pathlib import Path


def get_runtime_root() -> Path:
    """Retourne le dossier racine spécifique au système pour les données utilisateur."""
    if platform.system() == "Darwin":  # macOS
        base_dir = Path.home() / "Library" / "Application Support" / "QualityLab"
    elif platform.system() == "Windows":
        base_dir = Path.home() / "AppData" / "Local" / "QualityLab"
    else:  # Linux
        base_dir = Path.home() / ".local" / "share" / "QualityLab"

    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir


def get_runs_dir() -> Path:
    runs_dir = get_runtime_root() / "runs"
    runs_dir.mkdir(exist_ok=True)
    return runs_dir


def get_diagnostics_dir() -> Path:
    diag_dir = get_runtime_root() / "diagnostics"
    diag_dir.mkdir(exist_ok=True)
    return diag_dir