"""Mise à jour ponctuelle de site/index.html : retrait de WikiCartes, renumérotation,
aperçu dans chaque projet, schéma de Multi Web Manager (SVG en ligne, aux couleurs du thème)."""
import re
from pathlib import Path

P = Path(r"E:\Dev\Portfolio\site\index.html")
s = P.read_text(encoding="utf-8")

# 1. WikiCartes Lab retiré.
s, n = re.subn(r'\s*<li data-cat="web" id="wikicartes-lab">.*?</li>\n', "\n", s, flags=re.S)
assert n == 1, "WikiCartes introuvable"

# 2. Renumérotation 01…09 et compteurs.
items = re.findall(r'<span class="n">\d+</span>', s)
for i, old in enumerate(items, 1):
    s = s.replace(old, f'<span class="n">@{i:02d}</span>', 1)
s = s.replace('<span class="n">@', '<span class="n">')
s = s.replace('<span id="count-hero">10</span>', f'<span id="count-hero">{len(items)}</span>')
s = s.replace('<span class="count" id="count">(10)</span>', f'<span class="count" id="count">({len(items)})</span>')

# 3. Nova Strike : description fidèle à l'écran du jeu.
s = s.replace("<li>Météores, aliens, bouclier et armes à ramasser.</li>",
              "<li>Météores et aliens à abattre, bonus à ramasser.</li>\n              <li>Améliorations&nbsp;: vitesse, dégâts, vie supplémentaire.</li>")

# 4. Schéma de Multi Web Manager : le mur de 20 cellules (le même curseur dans chacune) et la console.
cells = []
x0, y0, cw, ch, gap = 90, 210, 166, 128, 10
for r in range(4):
    for c in range(5):
        x, y = x0 + c * (cw + gap), y0 + r * (ch + gap)
        k = r * 5 + c + 1
        cells.append(
            f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" class="ln"/>'
            f'<text x="{x + 10}" y="{y + 22}" class="mono sm">{k:02d}</text>'
            f'<path d="M{x + 14} {y + 42}h{cw - 28}M{x + 14} {y + 58}h{cw - 60}M{x + 14} {y + 74}h{cw - 44}" class="ln faint"/>'
            f'<path d="M{x + 104} {y + 84}l0 26 7 -7 5 11 5 -2 -5 -11 10 0z" class="{"cur" if k == 7 else "cur ghost"}"/>'
        )
side = "".join(
    f'<circle cx="1102" cy="{318 + i * 38}" r="5" class="dot"/><text x="1118" y="{324 + i * 38}" class="mono sm">WEB {i + 1:02d}</text>'
    for i in range(8)
)
svg = f'''<svg class="schema" viewBox="0 0 1600 1000" role="img" aria-labelledby="mwm-schema">
              <title id="mwm-schema">Schéma : à gauche le mur de 20 pages web en grille, le même curseur reproduit dans chaque cellule ; à droite la console d’administration.</title>
              <text x="90" y="180" class="mono">ÉCRAN 1 — LE MUR</text>
              <rect x="80" y="200" width="896" height="568" class="ln thick"/>
              {"".join(cells)}
              <text x="1040" y="180" class="mono">ÉCRAN 2 — LA CONSOLE</text>
              <rect x="1040" y="200" width="480" height="568" class="ln thick"/>
              <text x="1064" y="250" class="mono">MULTI WEB MANAGER</text><text x="1496" y="250" class="mono sm" text-anchor="end">20 INSTANCES</text>
              <path d="M1040 276h480M1210 276v492" class="ln"/>
              {side}<text x="1118" y="636" class="mono sm">…</text>
              <text x="1232" y="318" class="sans">Toutes les instances</text>
              <text x="1232" y="352" class="mono sm">même site · même zoom</text>
              <rect x="1232" y="378" width="18" height="18" class="ln"/><path d="M1236 387l4 4 7-8" class="ln"/>
              <text x="1262" y="393" class="mono sm">répliquer la souris</text>
              <path d="M1232 430h264" class="ln faint"/>
              <text x="1232" y="470" class="sans">Instance choisie</text>
              <text x="1232" y="504" class="mono sm">adresse · recharger · zoom</text>
              <path d="M1232 540h264" class="ln faint"/>
              <text x="1232" y="580" class="sans">Grille · écrans</text>
              <text x="1232" y="614" class="mono sm">5 × 4 · automatique</text>
              <text x="90" y="830" class="mono sm">Un clic dans la cellule 07 est reproduit au même endroit dans toutes les autres.</text>
            </svg>'''

previews = {
    "multi-web-manager": svg,
    "rivano": '<img src="img/rivano.webp" width="1600" height="1000" loading="lazy" decoding="async" alt="Rivano : liste des voitures, fiche d’un véhicule et panneau de filtres.">',
    "pdf-to-markdown": '<img src="img/pdf-to-markdown.webp" width="1600" height="1000" loading="lazy" decoding="async" alt="La fenêtre de PDF to Markdown après la conversion de trois fichiers.">',
    "nova-strike": '<img src="img/nova-strike.webp" width="1600" height="1000" loading="lazy" decoding="async" alt="L’écran d’accueil de Nova Strike, avec le score, les bonus et les améliorations.">',
    "bookedo": '<img src="img/bookedo.webp" width="1600" height="1000" loading="lazy" decoding="async" alt="Bookedo : accueil, bibliothèque et fiche d’un livre.">',
    "crypto-widget": '<img src="img/crypto-widget.webp" width="1600" height="1000" loading="lazy" decoding="async" alt="Le widget Crypto : cours du bitcoin et graphique sur sept jours.">',
    "neodex": '<img src="img/neodex.webp" width="1600" height="1000" loading="lazy" decoding="async" alt="NeoDex : liste des Pokémon, fiche de Bulbizarre et tirage au hasard.">',
    "3d-viewer": '<img src="img/3d-viewer.webp" width="1600" height="1000" loading="lazy" decoding="async" alt="3D Viewer : un modèle de voiture chargé, avec le panneau des réglages.">',
    "countdown-widget": '<img src="img/countdown-widget.webp" width="1600" height="1000" loading="lazy" decoding="async" alt="Le widget Countdown, prêt à compter les jours jusqu’à un événement.">',
}
for pid, media in previews.items():
    pat = re.compile(rf'(<li data-cat="\w+" id="{re.escape(pid)}">.*?<div class="body">\n)', re.S)
    s, n = pat.subn(lambda m: m.group(1) + f'            <figure class="preview">{media}</figure>\n', s, count=1)
    assert n == 1, pid

P.write_text(s, encoding="utf-8")
print("projets :", len(items), "| aperçus :", s.count('<figure class="preview">'))
