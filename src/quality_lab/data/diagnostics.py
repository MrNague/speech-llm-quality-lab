import json
import shutil
import time
from pathlib import Path
from quality_lab.storage.paths import get_runs_dir, get_diagnostics_dir


def export_diagnostic(run_id: str, fields: list, include_audio: bool = False) -> Path:
    """Crée un package de diagnostic localement."""
    run_path = get_runs_dir() / run_id
    if not run_path.exists():
        raise ValueError(f"Run {run_id} introuvable.")

    diag_dir = get_diagnostics_dir()
    export_path = diag_dir / f"diag_{run_id}_{int(time.time())}"
    export_path.mkdir(parents=True, exist_ok=True)

    # Création du manifeste
    manifest = {"run_id": run_id, "fields": fields, "has_audio": include_audio}
    (export_path / "manifest.json").write_text(json.dumps(manifest))

    # Inclusion conditionnelle de l'audio
    if include_audio:
        (export_path / "audio_samples.zip").touch()

    return export_path


def import_diagnostic(package_path: Path) -> dict:
    """Importe un package et rejette les doublons."""
    package_path = Path(package_path)
    if not package_path.exists() or not (package_path / "manifest.json").exists():
        raise ValueError("Schéma du package invalide.")

    manifest = json.loads((package_path / "manifest.json").read_text())
    run_id = manifest.get("run_id")

    imported_dir = get_diagnostics_dir() / f"imported_{run_id}"

    # Détection des doublons
    if imported_dir.exists():
        raise FileExistsError(f"Le diagnostic pour le run {run_id} a déjà été importé.")

    # Simuler l'import et l'enregistrement de l'expiration (ex: 7 jours)
    shutil.copytree(package_path, imported_dir)
    (imported_dir / ".expiry").write_text(str(int(time.time()) + 7 * 86400))

    return {"success": True, "path": str(imported_dir)}