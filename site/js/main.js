// Filtres de la liste des projets, ouverture par l'adresse (#rivano), curseur personnalisé.
document.addEventListener('DOMContentLoaded', () => {
  const items = [...document.querySelectorAll('.index > li')];
  const buttons = [...document.querySelectorAll('.filters button')];
  const count = document.getElementById('count');
  items.forEach((li, i) => li.style.setProperty('--i', i));

  buttons.forEach((btn) => btn.addEventListener('click', () => {
    const f = btn.dataset.filter;
    buttons.forEach((b) => b.setAttribute('aria-pressed', String(b === btn)));
    let shown = 0;
    items.forEach((li) => {
      li.hidden = f !== 'tous' && li.dataset.cat !== f;
      if (!li.hidden) shown++;
    });
    count.textContent = `(${shown})`;
  }));

  // Lien direct vers un projet : il s'ouvre.
  const openFromHash = () => {
    const id = decodeURIComponent(location.hash.slice(1));
    const d = id ? document.getElementById(id)?.querySelector('details') : null;
    if (d) d.open = true;
  };
  openFromHash();
  window.addEventListener('hashchange', openFromHash);

  // Curseur : un disque qui inverse ce qu'il survole (noir sur blanc, blanc sur noir) et
  // grossit sur ce qui se clique. Souris uniquement : rien ne change sur un écran tactile.
  if (matchMedia('(hover: hover) and (pointer: fine)').matches) {
    const cursor = document.createElement('div');
    cursor.className = 'cursor';
    cursor.setAttribute('aria-hidden', 'true');
    document.body.append(cursor);
    document.documentElement.classList.add('custom-cursor');
    let x = 0, y = 0, frame = 0;
    addEventListener('mousemove', (e) => {
      x = e.clientX; y = e.clientY;
      if (!frame) frame = requestAnimationFrame(() => { cursor.style.transform = `translate(${x}px, ${y}px)`; frame = 0; });
      cursor.classList.add('on');
      cursor.classList.toggle('big', !!e.target.closest('a, button, summary'));
    }, { passive: true });
    document.addEventListener('mouseout', (e) => { if (!e.relatedTarget) cursor.classList.remove('on'); });
    addEventListener('mousedown', () => cursor.classList.add('down'));
    addEventListener('mouseup', () => cursor.classList.remove('down'));
  }
});
