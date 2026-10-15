from quality_lab.storage.lifecycle import list_runs, delete_run, prune
from quality_lab.storage.paths import get_runs_dir


def test_delete_run_not_found():
    # Tester qu'une suppression d'un faux run renvoie une erreur propre, pas un crash
    result = delete_run("run_fantome_inexistant")
    assert result["success"] is False
    assert "n'existe pas" in result["error"]


def test_lifecycle_success():
    # Créer un faux run pour le test
    runs_dir = get_runs_dir()
    test_run = runs_dir / "run_test_api_123"
    test_run.mkdir(exist_ok=True)

    # 1. Vérifier qu'il est bien listé
    liste = list_runs()
    assert liste["success"] is True
    assert "run_test_api_123" in liste["data"]

    # 2. Le supprimer
    delete_res = delete_run("run_test_api_123")
    assert delete_res["success"] is True
    assert not test_run.exists()


def test_prune_executes_without_error():
    # S'assurer que la fonction prune ne plante pas, même sans vieux dossiers
    result = prune(days_old=30)
    assert result["success"] is True
    assert isinstance(result["data"], list)