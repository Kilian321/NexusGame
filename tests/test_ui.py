"""
test_ui.py — Tests UI Playwright NexusGame
===========================================
Contexte : Tests de l'interface utilisateur GameStore avec Playwright.
Pattern Page Object Model (POM) obligatoire — les sélecteurs ne doivent
pas être écrits directement dans les tests.

Lancement :
    pytest tests/test_ui.py -v --headed          # avec navigateur visible
    pytest tests/test_ui.py -v                   # headless (CI)
    pytest tests/test_ui.py -v --html=reports/ui.html

Prérequis :
    playwright install chromium
    # L'API GameStore doit tourner sur http://localhost:5000
"""
import pytest
import time
from playwright.sync_api import Page, expect

from tests.pages.home_page import HomePage
from tests.pages.add_game_modal import AddGameModal

BASE_URL = "http://localhost:5000"


# ════════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Tests basiques (sans POM)
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.ui
class TestPageBasique:
    """
    Tests directs avec l'objet Page de Playwright.
    Pas de POM ici — comparer avec la section 2 pour voir la différence.
    """

    def test_page_se_charge(self, page: Page):
        page.goto(BASE_URL)
        assert page.title() == "GameStore"
        expect(page.locator("[data-testid=game-list]")).to_be_visible()

    def test_compteur_jeux_positif(self, page: Page):
        """
        TODO — Vérifier que le compteur de jeux affiche un nombre > 0.
        [data-testid=game-count] doit contenir un nombre extrait du texte.
        """
        page.goto(BASE_URL)

        compteur = page.locator('[data-testid="game-count"]').inner_text()
        nombre = int(compteur.split(" ")[0])
        assert nombre > 0

    def test_annuler_ferme_le_modal(self, page: Page):
        """
        TODO — Ouvrir le formulaire d'ajout, cliquer Annuler,
        vérifier que [data-testid=add-game-modal] n'est plus visible.
        """
        page.goto(BASE_URL)

        page.locator('[data-testid="add-game-btn"]').click()
        page.locator('[data-testid="cancel-btn"]').click()

        assert not page.locator('[data-testid="add-game-modal"]').is_visible()


# ════════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Tests avec Page Object Model
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.ui
class TestAvecPOM:
    """
    Mêmes scénarios qu'en section 1, mais via les classes POM.
    Comparer la lisibilité et la maintenabilité.
    """

    def test_page_charge_via_pom(self, page: Page):
        """
        TODO — Instancier HomePage, naviguer, vérifier game_list visible.
        """
        home = HomePage(page)
        home.navigate()

        assert page.title() == "GameStore"

        expect(home.game_list).to_be_visible()

    def test_ajouter_jeu_via_pom(self, page: Page):
        home = HomePage(page)
        modal = AddGameModal(page)

        home.navigate()
        home.open_add_form()

        expect(modal.modal).to_be_visible()

        modal.fill_and_submit("Jeu POM Test", "Action", 20)

        expect(home.game_list).to_contain_text("Jeu POM Test")

    def test_recherche_filtre_resultats(self, page: Page):
        home = HomePage(page)

        home.navigate()
        home.search("Zelda")

        first_card = home.get_game_cards().first

        expect(first_card).to_contain_text("Zelda")

    def test_filtre_genre_rpg(self, page: Page):
        """
        TODO — Filtrer par "RPG", vérifier que toutes les cartes visibles
        """
        page.goto(BASE_URL)

        page.locator('[data-testid="genre-filter"]').select_option("RPG")

        genres = page.locator('[data-testid="game-genre"]').all_text_contents()

        for genre in genres:
            assert "RPG" in genre




# ════════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Choix libres (à justifier dans le README)
# ════════════════════════════════════════════════════════════════════════════════

@pytest.mark.ui
class TestChoixLibresUI:
    """
    Ajoutez ici les parcours utilisateur que vous jugez critiques.
    Documentez vos choix dans le README.
    """

    def test_pom_annuler_formulaire(self,page: Page):
        home = HomePage(page)
        modal = AddGameModal(page)

        home.navigate()
        home.open_add_form()

        expect(modal.modal).to_be_visible()

        modal.cancel()

        expect(modal.modal).not_to_be_visible()


