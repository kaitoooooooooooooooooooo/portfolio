Captures de Recto pour l'aperçu du portfolio (serveur local lancé sur le port 5190 ; site/recto est
une jonction vers E:\Dev\Recto\site, le dépôt de l'application) :

  node tools/capture-steps.mjs http://localhost:5190/recto/ recto "wait:1500;js:recto-capture/demo.js;reload;wait:1800;shot;goto:http://localhost:5190/recto/#/l/demoeng/cartes;wait:1200;js:recto-capture/flip.js;wait:1000;shot;goto:http://localhost:5190/recto/#/l/demoeng/apprendre;wait:1200;js:recto-capture/answer.js;wait:700;shot"
  python tools/make-previews.py

demo.js remplit le navigateur de capture (profil à part) avec trois listes ; rien n'est envoyé au serveur.
