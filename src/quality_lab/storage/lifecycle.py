import shutil
import time
from pathlib import Path
from quality_lab.storage.paths import get_runs_dir


def list_runs() -> dict:
    """Liste tous les runs existants."""
    try:
        runs_dir = get_runs_dir()
        runs = [d.name for d in runs_dir.iterdir() if d.is_dir()]
        return {"success": True, "data": runs, "error": None}
    except Exception as e:
        return {"success": False, "data": [], "error": f"Impossible de lister les runs : {e}"}


def delete_run(run_id: str) -> dict:
    """Supprime un run spécifique de manière sécurisée."""
    try:
        target = get_runs_dir() / run_id
        if not target.exists():
            return {"success": False, "error": f"Le run '{run_id}' n'existe pas."}

        shutil.rmtree(target)
        return {"success": True, "error": None}
    except Exception as e:
        return {"success": False, "error": f"Échec de la suppression de '{run_id}' : {e}"}


def prune(days_old: int = 30) -> dict:
    """Supprime les runs plus vieux que le nombre de jours spécifié."""
    try:
        runs_dir = get_runs_dir()
        now = time.time()
        deleted = []

        for run_path in runs_dir.iterdir():
            if run_path.is_dir():
                # Vérifier l'âge du dossier
                if (now - run_path.stat().st_mtime) > (days_old * 86400):
                    shutil.rmtree(run_path)
                    deleted.append(run_path.name)

        return {"success": True, "data": deleted, "error": None}
    except Exception as e:
        return {"success": False, "data": [], "error": f"Erreur lors du nettoyage : {e}"}