"""
test_unit.py — Tests unitaires NexusGame
==========================================
Contexte : Suite de tests unitaires sur l'API GameStore.
Chaque test est isolé — BDD fraîche à chaque appel (fixture function scope).

Lancement :
    pytest tests/test_unit.py -v
    pytest tests/test_unit.py -v --cov=app_gamestore --cov-report=html
"""
import pytest

@pytest.fixture
def sample_game():
    return {
        'title': 'The Legend of Zelda: BOTW 2',
        'genre': 'RPG',
        'price': 50,
        'rating': 5,
        'stock': 100,
    }
@pytest.fixture
def sample_game_2():
    return {
        'title': 'The Legend of Zelda: BOTW ',
        'genre': 'RPG',
        'price': 40,
        'rating': 4,
        'stock': 100,
    }
@pytest.fixture
def sample_game_3():
    return {
        'title': 'The Legend of Zelda: BOTW 3',
        'genre': 'RPG',
        'price': 0,
        'rating': 3,
        'stock': 100,
    }

# ════════════════════════════════════════════════════════════════════════════════
# SECTION 1 — Health & endpoints de base
# ════════════════════════════════════════════════════════════════════════════════

class TestHealth:
    def test_health_retourne_200(self, client):
        """
        TODO — Vérifier que GET /health retourne 200 et {"status": "ok"}.
        """
        r = client.get('/health')
        assert r.status_code == 200
        data = r.get_json()
        assert data["status"] == "ok"


    def test_health_contient_service(self, client):
        """
        TODO — Vérifier que la réponse contient la clé "service".
        """
        r = client.get('/health')
        data = r.get_json()
        assert data["service"]


# ════════════════════════════════════════════════════════════════════════════════
# SECTION 2 — Liste des jeux
# ════════════════════════════════════════════════════════════════════════════════

class TestListGames:
    def test_liste_retourne_200(self, client):
        """
        TODO — GET /games retourne 200 et une liste non vide.
        """
        r = client.get('/games')
        assert r.status_code == 200

        data = r.get_json()
        assert isinstance(data, list)
        assert len(data) > 0


    def test_liste_contient_les_champs_attendus(self, client):
        """
        TODO — Chaque jeu retourné contient au moins : id, title, genre, price, rating.
        """
        r = client.get('/games')
        data = r.get_json()

        liste = {"id", "title", "genre", "price", "rating"}
        for game in data:
            assert liste.issubset(game.keys())

    def test_filtre_par_genre(self, client):
        """
        TODO — GET /games?genre=RPG retourne uniquement des jeux RPG.
        """
        r = client.get('/games?genre=RPG')
        data = r.get_json()

        for game in data:
            assert game["genre"] == "RPG"



    def test_tri_par_prix_croissant(self, client):
        """
        TODO — GET /games?sort=price&order=asc retourne les jeux triés par prix croissant.
        """
        r = client.get('/games?sort=price&order=asc')
        data = r.get_json()

        for game in range(len(data) - 1):
            assert data[game]["price"] <= data[game + 1]["price"]



# ════════════════════════════════════════════════════════════════════════════════
# SECTION 3 — Création de jeux
# ════════════════════════════════════════════════════════════════════════════════

class TestCreateGame:
    def test_creation_valide_retourne_201(self, client, sample_game):
        """
        TODO — POST /games avec titre, genre, prix valides → 201 + id dans la réponse.
        """
        r = client.post('/games',json=sample_game)
        assert r.status_code == 201

        data = r.get_json()
        assert "id" in data
        assert data["title"] == sample_game["title"]

    @pytest.mark.parametrize("title,genre,price,expected_status", [
        ("Zelda", "RPG", 59.99, 201), # cas valide
        ("", "RPG", 29.99, 400),  # titre vide → erreur
        ("Mario", "RPG", -5.0, 400), # prix négatif → erreur
        (None, "RPG", 9.99, 400),  # titre absent → erreur
        ("Zelda", "", 9.99, 400),  # Genre obligatoire
        ("Zelda", "RPG", 'a', 400),  # prix doit etre un nombre
        (None, None, None, 400),  # aucune data
    ])
    def test_create_game_validation(self, client, title, genre, price, expected_status):
        r = client.post("/games", json={"title": title, "genre": genre, "price": price})
        assert r.status_code == expected_status

    def test_creation_titre_duplique_retourne_409(self, client, sample_game):
        """
        TODO — Créer le même jeu deux fois → second appel retourne 409.
        """
        r1 = client.post('/games', json=sample_game)
        assert r1.status_code == 201

        r2 = client.post('/games', json=sample_game)
        assert r2.status_code == 409

# ════════════════════════════════════════════════════════════════════════════════
# SECTION 4 — Récupération, mise à jour, suppression
# ════════════════════════════════════════════════════════════════════════════════

class TestGameCRUD:
    def test_get_jeu_existant(self, client,sample_game):
        """
        TODO — Créer un jeu, récupérer son id, GET /games/{id} → 200.
        """
        r_create = client.post('/games', json=sample_game)

        game_id = r_create.get_json()["id"]
        r = client.get(f'/games/{game_id}')
        assert r.status_code == 200

        data = r.get_json()
        assert data["id"] == game_id
        assert data["title"] == sample_game["title"]

    def test_get_jeu_inexistant_retourne_404(self, client):
        r = client.get('/games/9999')
        assert r.status_code == 404

    def test_update_prix(self, client,sample_game):
        """
        TODO — Créer un jeu, PUT /games/{id} avec nouveau prix, vérifier la mise à jour.
        """
        r_create = client.post('/games', json=sample_game)

        game_id = r_create.get_json()["id"]

        update_sample_game = {
            "price": 30.99
        }
        r_update = client.put(f'/games/{game_id}', json=update_sample_game)
        assert r_update.status_code == 200

        data = r_update.get_json()
        assert data["id"] == game_id
        assert data["price"] == 30.99

    def test_delete_jeu(self, client,sample_game):
        """
        TODO — Créer un jeu, DELETE /games/{id} → 204, puis GET → 404.
        """
        r_create = client.post('/games', json=sample_game)
        assert r_create.status_code == 201

        game_id = r_create.get_json()["id"]

        r_delete = client.delete(f'/games/{game_id}')
        assert r_delete.status_code == 204

        r_get = client.get(f'/games/{game_id}')
        assert r_get.status_code == 404


# ════════════════════════════════════════════════════════════════════════════════
# SECTION 5 — Choix libres (à justifier dans le README)
# ════════════════════════════════════════════════════════════════════════════════

class TestChoixLibres:
    def test_get_stats(self, client, sample_game):
        client.post('/games', json=sample_game)

        r = client.get('/games/stats')
        assert r.status_code == 200

    def test_get_genre_returns_200(self, client):
        r = client.get('/genres')
        assert r.status_code == 200

    def test_search_par_titre(self, client, sample_game):
        client.post('/games', json=sample_game)

        r = client.get(f"/games/search?q={sample_game['title']}")
        assert r.status_code == 200

        data = r.get_json()
        assert data["count"] >= 1
        assert data["results"][0]["title"] == sample_game["title"]

    def test_create_game_sans_body_retourne_400(self, client):
        r = client.post('/games')
        assert r.status_code == 400

        data = r.get_json()
        assert data["error"] == "Body JSON requis"


# ════════════════════════════════════════════════════════════════════════════════
# SECTION 6 — Endpoint /games/featured (NGS-108)
# ════════════════════════════════════════════════════════════════════════════════

class TestFeatured:
    """
    Tests sur l'endpoint GET /games/featured.
    Consultez la documentation de l'endpoint dans app_gamestore.py.
    Si un test échoue alors que votre assertion est correcte,
    documentez ce que vous observez dans le README.
    """

    def test_featured_retourne_200(self, client):
        """TODO — GET /games/featured retourne 200."""
        r = client.get('/games/featured')
        assert r.status_code == 200


    def test_featured_retourne_liste(self, client):
        """TODO — La réponse contient une clé 'featured' qui est une liste."""
        r = client.get('/games/featured')
        data = r.get_json()
        assert isinstance(data["featured"], list)

    def test_featured_max_5_par_defaut(self, client):
        """TODO — Sans paramètre, au maximum 5 jeux sont retournés."""
        r = client.get('/games/featured')
        assert r.status_code == 200

        data = r.get_json()
        assert len(data["featured"]) <= 5

    def test_featured_limit_param(self, client):
        """TODO — ?limit=3 retourne au maximum 3 jeux."""
        r = client.get('/games/featured?limit=3')
        assert r.status_code == 200

        data = r.get_json()
        assert len(data["featured"]) <= 3


    def test_featured_tries_par_rating_decroissant(self, client,sample_game, sample_game_2, sample_game_3):
            """TODO — Les jeux sont triés par rating décroissant."""
            client.post('/games', json=sample_game)
            client.post('/games', json=sample_game_2)
            client.post('/games', json=sample_game_3)

            r = client.get('/games/featured')
            assert r.status_code == 200

            data = r.get_json()["featured"]
            ratings = [game["rating"] for game in data]

            assert ratings == sorted(ratings, reverse=True)

    def test_featured_sans_jeux_gratuits(self, client,sample_game,sample_game_3):
        """TODO — Les jeux gratuits ne doivent pas apparaître dans featured."""
        r = client.get('/games/featured')
        assert r.status_code == 200

        data = r.get_json()["featured"]

        for game in data:
            assert game["price"] > 0


    def test_featured_sans_jeux_hors_stock(self, client):
        """TODO — Les jeux hors stock ne doivent pas apparaître dans featured."""
        r = client.get('/games/featured')
        assert r.status_code == 200

        data = r.get_json()["featured"]

        for game in data:
            assert game["stock"] > 0