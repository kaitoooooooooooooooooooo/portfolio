# Portfolio — kaito-lab.ch

Site statique d'une seule page, noir et blanc : `site/index.html`, `site/css/style.css`, `site/js/main.js`.
Aucune dépendance, aucun traqueur, polices hébergées sur le site.

L'application de révision **Recto** (kaito-lab.ch/recto/) a son propre dépôt :
[kaitoooooooooooooooooooo/recto](https://github.com/kaitoooooooooooooooooooo/recto). Elle est ajoutée
au site au moment de la mise en ligne (voir plus bas).

## Modifier un projet

Tout est dans `site/index.html`, un `<li>` par projet dans la liste `<ol class="index">` :

- `data-cat` : `web`, `mobile` ou `bureau` (sert aux filtres) ;
- la ligne (`summary`) : numéro, nom, catégorie, technologies, date ;
- le détail : une phrase (`.desc`), deux ou trois points (`.points`), les liens (`.links`).

Pour ajouter un projet, copier un `<li>` existant, changer son `id` (sert de lien direct : `kaito-lab.ch/#rivano`)
et renuméroter. Le compteur « 10 projets » est en haut de la page (`count-hero` et `count`).

## Voir en local

```bash
php -S localhost:5190 -t site
```

Pour voir aussi Recto à <http://localhost:5190/recto/>, `site/recto` doit être une jonction vers le
dépôt de l'application, cloné à côté de celui-ci (`..\Recto`). Elle est ignorée par git :

```powershell
New-Item -ItemType Junction -Path site\recto -Target ..\Recto\site
```

## Mettre en ligne

1. `powershell -ExecutionPolicy Bypass -File tools\package.ps1` → `dist\portfolio.zip` (le portfolio,
   plus Recto pris dans `..\Recto\site` et placé sous `recto/`).
2. Manager Infomaniak → Hébergement → FTP / SSH → **Web FTP**, dossier racine du site kaito-lab.ch.
3. Déposer le zip, clic droit → Extraire (remplace la page « en construction »), puis supprimer le zip.
4. Une fois HTTPS actif, décommenter la redirection à la fin de `site/.htaccess`.

Le zip ne contient jamais la base de Recto ni sa clé (`recto/api/data/` part vide, avec son `.htaccess`).
Sur le serveur, `recto/api/data/` se remplit tout seul au premier compte créé : ne pas l'écraser
lors d'une mise à jour (l'extraction du zip ne touche pas aux fichiers absents du zip).
Les comptes de Recto demandent PHP 8.1+ actif sur le site (réglage « version PHP » du Manager).
L'ancienne adresse `/fiches/` (premier nom de l'application) redirige vers `/recto/` (`site/.htaccess`).


## Aperçus des projets

Chaque projet ouvert montre un aperçu en niveaux de gris (`site/img/<projet>.webp`, 1600 × 1000).
Multi Web Manager a un schéma SVG dans la page.

Les captures brutes sont dans `previews-src/raw` (jamais mises en ligne) :

- démos web : `powershell -ExecutionPolicy Bypass -File tools\capture-web.ps1` (Chrome sans fenêtre) ;
- applis Flutter : compiler une copie avec `flutter build web`, puis `tools\capture-flutter.ps1`
  (écrans par adresse) et `node tools\capture-steps.mjs` (écrans qui demandent un clic) ;
  Rivano demande son API (`node app.js`, MongoDB local) ;
- PDF to Markdown : `python tools\capture-pdf-to-markdown.py` (vraie conversion de 3 PDF de démonstration) ;
- NeoDex et 3D Viewer : captures déjà présentes dans leurs dépôts GitHub.

Puis `python tools\make-previews.py` : niveaux de gris, recadrage, écrans de téléphone par trois.

## Recto dans le portfolio

Aperçu : `node tools/capture-steps.mjs` avec les listes de démonstration de `tools/recto-capture/`
(commande dans `tools/recto-capture/README.txt`), puis `python tools/make-previews.py`.

## Polices

Archivo (Omnibus-Type) et IBM Plex Mono (IBM), licence SIL Open Font License 1.1 : `site/fonts/OFL-*.txt`.
