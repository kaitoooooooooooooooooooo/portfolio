// Listes de démonstration pour les captures du portfolio (navigateur de capture uniquement).
// Les clés « fiches:… » sont celles de l'application (son ancien nom), à ne pas renommer.
(() => {
  const now = Date.now();
  const make = (id, title, rows, levels, ago) => {
    const cards = rows.map(([t, d], i) => ({ id: `${id}${i}`, t, d }));
    const prog = {};
    cards.forEach((c, i) => { if (levels[i]) prog[c.id] = { lv: levels[i], ok: levels[i], ko: 0, at: now - ago }; });
    return { id, title, cards, prog, created: now - ago - 86400000, updated: now - ago };
  };
  const english = [
    ['to look forward to', 'attendre avec impatience'], ['to give up', 'abandonner'], ['throughout', 'tout au long de'],
    ['lonely', 'seul, solitaire'], ['weather', 'le temps (météo)'], ['to run out of', 'être à court de'],
    ['reliable', 'fiable'], ['to get rid of', 'se débarrasser de'], ['although', 'bien que'], ['to carry on', 'continuer'],
    ['skill', 'compétence'], ['to deal with', 's’occuper de'], ['furthermore', 'de plus'], ['to come up with', 'trouver (une idée)'],
    ['meanwhile', 'pendant ce temps'], ['to take part in', 'participer à'], ['behaviour', 'comportement'], ['to point out', 'faire remarquer'],
  ];
  const bio = [
    ['mitochondrie', 'produit l’énergie de la cellule'], ['ribosome', 'fabrique les protéines'], ['noyau', 'contient l’ADN'],
    ['membrane', 'délimite la cellule'], ['cytoplasme', 'liquide où baignent les organites'], ['chloroplaste', 'photosynthèse'],
    ['vacuole', 'réserve d’eau et de déchets'], ['appareil de Golgi', 'trie et expédie les protéines'],
    ['lysosome', 'digère les déchets'], ['réticulum endoplasmique', 'transporte les protéines'],
  ];
  const capitals = [
    ['Suisse', 'Berne'], ['Italie', 'Rome'], ['Espagne', 'Madrid'], ['Portugal', 'Lisbonne'], ['Autriche', 'Vienne'],
    ['Belgique', 'Bruxelles'], ['Pays-Bas', 'Amsterdam'], ['Suède', 'Stockholm'], ['Norvège', 'Oslo'], ['Hongrie', 'Budapest'],
  ];
  const sets = [
    make('demoeng', 'Anglais — vocabulaire B2', english, [2, 2, 2, 2, 2, 2, 2, 1, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0], 3600e3),
    make('demobio', 'Biologie — la cellule', bio, [2, 2, 2, 2, 2, 1, 2, 2, 1, 2], 2 * 86400e3),
    make('democap', 'Capitales d’Europe', capitals, [2, 2, 2, 2, 2, 2, 2, 2, 2, 2], 6 * 86400e3),
  ];
  localStorage.setItem('fiches:sets', JSON.stringify(sets));
  localStorage.setItem('fiches:cards', JSON.stringify({ sort: true, shuffle: false, defFirst: false, v: 2 })); // capture : ordre fixe
  localStorage.setItem('fiches:learn', JSON.stringify({ dir: 'term', types: 'choice' })); // question à choix à l'écran
})();
