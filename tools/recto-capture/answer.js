// Mode Apprendre : affiche une question à choix et y répond juste.
(() => {
  const sets = JSON.parse(localStorage.getItem('fiches:sets'));
  const prompt = document.querySelector('.q-prompt')?.textContent;
  const card = sets.flatMap((s) => s.cards).find((c) => c.t === prompt);
  const btn = [...document.querySelectorAll('.choice')].find((b) => b.querySelector('.choice-text').textContent === card?.d);
  btn?.click();
  document.activeElement?.blur();
})();
