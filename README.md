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
```bash
  J ai choisis la piramide de test avec les tests unitaire en grande majorité (70-80%), 
  ensuite les tests d intégration avec environ (10-15%),
  et pour finir les tests End to End avec envrion (5%)
  J ai choisis cela car nous sommes plutot sur une api donc cette piramide favorise les tests sur la logique métier 

```


### Pipeline CI vs local

<!-- Qu'est-ce qui tourne en CI, qu'est-ce qui reste en local, et pourquoi ? -->
#### Ce qui tourne en CI :
- Les tests unitaires, afin de voir si les différentes fonctionnalités fonctionne unitairement
- Les tests d'intégrations , pour vérifier que les différents enchainement d'action focntionne avec l'api
- Les tests Newman pour tester les tests postman automatiquement
- Les test Playwright pour vérifier que les intéractions sur le front marche correctement

#### Ce qui tourne en local :

- les test Locust , car ce sont des tests de charge, plus longs a exécuter 
- Les tests OWASP

### Mes choix libres

<!-- Pour chaque test libre : ce qu'il teste et pourquoi vous l'avez choisi. -->

- Pour le test unitaire "test_creation_valide_retourne_201" j'ai choisis de crée une fixture pour avoir un jeu fictif réutilisable dans les autres test pour évité la duplication de code .
- Pour le test unitaire "sans titre", "prix négatif", je me suis permis de les effacés afin de crée une suite de test a l'aide de "@pytest.mark.parametrize" qui va répondre au test "sans titre", "prix négatif", ainsi que 4 tests en +. J'ai vu ensuite quil y avait le "@pytest.mark.parametrize", donc jai effacé celuis-ci vu que mes tests ont déjà été faits auparavant
- J'ai rajouté le test get_stats pour vérifier que la route répond correctement , l'enpoint n'a pas été testé auparavant
- J'ai rajouté le test get_genre afin de vérifier que la route repond bien
- J'ai rajouté le test search_par_titre afin de testé si l'enpoint renvoie bien une liste qui contient le titre de notre recherche,une fonctionnalité qui est quand meme principal pour un stutio qui distribue des jeux
- J'ai rajouté le test create_game_sans_body_retourne_400 afin de vérifier si on peut crée un jeu sans body et retourne bien erreur 400

- Pour le test test_featured_tries_par_rating_decroissant, la route api été paramétré en croissant , alors que le test est fait pour du décroissant , donc jai remplacer "ASC" par "DESC" pour convenir au test 

- Pour le test libre avec postamn jai fais un test qui vérifie que le temps de réponse ne dépasse pas 200ms pour vérifier que la requete ne prenent pas trop de temps pour arrivé jusqua l utilisateur qui pourrait perdre de l interet si la requete est trop longue

- Pour le test libre avec Playwright jai fait un test qui permet de vérifier que la modal de formulaire puisse bien ce fermer , afin d évité de resté bloqué dans la modal sans pourvoir rien faire 

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
- Avec les tests Postman jai découvert que la route delete renvoyé un code 200 dans le code alors que normalement ça doit etre un code 204
```bash
Avec Locust avec 1000 utilisateurs dont 50 par seconde 
on peut remarqué que la route "DELETE" luis arrive de fail 3 , aucune autre route na fail . Le p95ms des routes est entre (700 et 1400ms en moyenne) avec un pick max de 4000ms envrion
A partir de 1000 utilisateurs on peut voir dans "charts" un spike testing , cet a dire quon voit un pick d un seul coup sur le graphique.

Apres plusieurs essai plus tard pour le meme nombre d utilisateurs , je genere des fails sur un peut toute les routes , ce qui montre que le seveur peut saturer tres fort avec 5000ms en moyenne par requete.

```

```bash
    Avec OWASP ZAP :
    - Il y a au total 10 alertes trouvé 
      - 2 medium
      - 6 low
      - 2 Informational
      
    L alerte quon retrouve le plus est "Cross-Origin-Embedder-Policy"
    J ai rajouté les headers de sécurité dans le fichier app_gamestores.py
    
    - Après modification :
      - 1 medium
      - 5 low
      - 2 Informational
    
```


## Pipeline CI/CD

<!-- État de votre pipeline sur GitHub Actions. -->
```bash
  A ce moment la , j ai crée la pipeline les tests unitaires passe ,
   je n est pas encore fais pour les tests d intégration car pour l instant je préfére faire le reste pour y revenir si jai le temps , pour les jobs Newman et Playwright la pipeline passe.

```

---

## Ce que j'ai appris

<!-- Optionnel. -->
```bash
 - Jai appris a écrire une serie de test unitaire fonctionnel avec un coverage de ~80%
 - J ai appris a crée une pipeline sur github alors que je n en avais jamais fais (a par le tp d hier)
 - J ai appris a écrire des tests dans postman et récupéré la collection .json
 - Générer des tests de performance sur des routes api, et ainsi voir les posibles limite.
 - J ai découvert comment scan les sécurités des mon api avec OWASP ZAP
```
