# NexusGame — Suite de Tests

> Projet final 2TES3 — Tests Avancés & Automatisation

## Présentation du projet

<!-- Décrivez le contexte du projet et l'API GameStore. -->

```Nous sommes recrutez chez NexusGame Studio. Leurs mise en production a échoué silencieusement, ce qui a crée certains problèmes avec l'api , notre mission est de sécurisé l'api avec une suite de test performante```

---

## Structure du repo

```
NexusGame/
├── app_gamestore.py
├── requirements.txt
├── tests/
│   ├── conftest.py
│   ├── test_unit.py
│   ├── test_integration.py
│   ├── test_ui.py
│   ├── gamestore_collection.json
│   ├── locust_gamestore.py
│   └── pages/
│       ├── home_page.py
│       └── add_game_modal.py
└── .github/
    └── workflows/
        └── tests.yml
```

---

## Lancer les tests

```bash
# Installation
pip install -r requirements.txt
playwright install chromium
npm install -g newman newman-reporter-htmlextra
pip install locust

# Démarrer l'API
python app_gamestore.py

# Tests unitaires
pytest tests/test_unit.py -v --cov=app_gamestore --cov-report=html

# Tests d'intégration
pytest tests/test_integration.py -v -m integration

# Tests UI
pytest tests/test_ui.py -v --headed

# Collection Newman
newman run tests/gamestore_collection.json --env-var "base_url=http://localhost:5000" --reporters cli,htmlextra

# Tests de charge
locust -f tests/locust_gamestore.py --host=http://localhost:5000 --headless -u 20 -r 2 --run-time 30s
```

---

## Mes choix techniques

### Pyramide de tests adoptée

<!-- Quelle pyramide avez-vous choisie et pourquoi ? -->

### Pipeline CI vs local

<!-- Qu'est-ce qui tourne en CI, qu'est-ce qui reste en local, et pourquoi ? -->

### Mes choix libres

<!-- Pour chaque test libre : ce qu'il teste et pourquoi vous l'avez choisi. -->

- Pour le test unitaire "test_creation_valide_retourne_201" j'ai choisis de crée une fixture pour avoir un jeu fictif réutilisable dans les autres test pour évité la duplication de code .
- Pour le test unitaire "sans titre", "prix négatif", je me suis permis de les effacés afin de crée une suite de test a l'aide de "@pytest.mark.parametrize" qui va répondre au test "sans titre", "prix négatif", ainsi que 4 tests en +. J'ai vu ensuite quil y avait le "@pytest.mark.parametrize", donc jai effacé celuis-ci vu que mes tests ont déjà été faits auparavant
- J'ai rajouté le test get_stats pour vérifier que la route répond correctement , l'enpoint n'a pas été testé auparavant
- J'ai rajouté le test get_genre afin de vérifier que la route repond bien
- J'ai rajouté le test search_par_titre afin de testé si l'enpoint renvoie bien une liste qui contient le titre de notre recherche,une fonctionnalité qui est quand meme principal pour un stutio qui distribue des jeux
- J'ai rajouté le test create_game_sans_body_retourne_400 afin de vérifier si on peut crée un jeu sans body et retourne bien erreur 400

- Pour le test test_featured_tries_par_rating_decroissant, la route api été paramétré en croissant , alors que le test est fait pour du décroissant , donc jai remplacer "ASC" par "DESC" pour convenir au test 


---

## Investigation de l'API

<!-- Ce que vous avez observé en testant l'API.
     Comportements inattendus, hypothèses, ce que vos tests révèlent. -->

- Dans le fichier requirements.txt il y a une ligne pour "newman" alors que ce n'est pas un packet python ce qui a crée une erreur.
- Dans app_gamestore il y a un problème de chargement des jeux sur le front 
```bash
 Initial : "showToast(data.error || 'Erreur lors de l\'ajout', true);"
 Corection :  "showToast(data.error || 'Erreur lors de l ajout', true);"
```
---

## Pipeline CI/CD

<!-- État de votre pipeline sur GitHub Actions. -->

---

## Ce que j'ai appris

<!-- Optionnel. -->
