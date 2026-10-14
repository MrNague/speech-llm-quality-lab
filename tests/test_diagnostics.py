import pytest
import shutil
from quality_lab.data.diagnostics import export_diagnostic, import_diagnostic
from quality_lab.storage.paths import get_runs_dir, get_diagnostics_dir


@pytest.fixture
def setup_fake_run():
    run_id = "test_diag_run_1"
    run_path = get_runs_dir() / run_id
    run_path.mkdir(exist_ok=True)
    yield run_id
    # Nettoyage après le test
    if run_path.exists():
        shutil.rmtree(run_path)


def test_audio_off_by_default(setup_fake_run):
    run_id = setup_fake_run
    export_path = export_diagnostic(run_id, ["metrics"])

    # L'audio ne doit pas être présent
    assert not (export_path / "audio_samples.zip").exists()


def test_rejects_duplicate_import(setup_fake_run):
    run_id = setup_fake_run
    export_path = export_diagnostic(run_id, ["metrics"])

    # Premier import (doit réussir)
    import_diagnostic(export_path)

    # Deuxième import (doit échouer avec une erreur précise)
    with pytest.raises(FileExistsError, match="déjà été importé"):
        import_diagnostic(export_path)

    # Nettoyage
    imported_dir = get_diagnostics_dir() / f"imported_{run_id}"
    if imported_dir.exists():
        shutil.rmtree(imported_dir)