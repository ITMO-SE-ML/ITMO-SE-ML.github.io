(() => {
  const options = [...document.querySelectorAll('.recording-option')];
  const player = document.getElementById('recording-player');
  const cover = document.getElementById('play-recording');
  if (!options.length || !player || !cover) return;
  let selected = options[0];
  function select(option) {
    selected = option;
    player.removeAttribute('src');
    player.hidden = true;
    cover.hidden = false;
    options.forEach(item => item.removeAttribute('aria-current'));
    option.setAttribute('aria-current', 'true');
    const {number, title} = option.dataset;
    document.getElementById('cover-number').textContent = number;
    document.getElementById('watch-number').textContent = `Лекция ${number}`;
    document.getElementById('watch-title').textContent = title;
    document.getElementById('watch-youtube').href = option.href;
    cover.setAttribute('aria-label', `Смотреть лекцию ${number}: ${title}`);
    player.title = `Запись лекции ${number}: ${title}`;
  }
  function selectHash() {
    const option = options.find(item => '#' + item.id === location.hash);
    if (option && option !== selected) select(option);
  }
  options.forEach(option => option.addEventListener('click', event => {
    event.preventDefault();
    if (option !== selected) select(option);
    history.replaceState(null, '', '#' + option.id);
  }));
  cover.addEventListener('click', () => {
    player.src = `https://www.youtube-nocookie.com/embed/${selected.dataset.video}?autoplay=1`;
    cover.hidden = true;
    player.hidden = false;
    player.focus();
  });
  addEventListener('hashchange', selectHash);
  select(selected);
  selectHash();
})();
