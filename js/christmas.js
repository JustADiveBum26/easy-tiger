// HOLIDAY POPUP (Christmas edition): gentle falling snow, ornaments, logo swap. Loaded only inside the Christmas window (see index.html).
// Visual only. Does nothing if the visitor prefers reduced motion.
(function () {
  // ----- logos: swap in the Christmas (wreath) versions; the normal files are untouched, so the regular look returns by itself -----
  var LOGO = { 'easy-tiger-logo-small.png': 'logo-small.png', 'easy-tiger-logo-medium.png': 'logo-medium.png', 'easy-tiger-logo.png': 'logo.png' };
  var imgs = document.querySelectorAll('img[src*="assets/logo/easy-tiger-logo"]');
  for (var k = 0; k < imgs.length; k++) {
    var f = imgs[k].getAttribute('src').split('?')[0].split('/').pop();
    if (LOGO[f]) imgs[k].src = 'assets/xmas/' + LOGO[f];
  }
  var emb = document.querySelector('.gate-emblem img');        // the end of the door opening: the wreath cut out of its black square
  if (emb) { emb.src = 'assets/xmas/logo-cutout.png'; emb.width = 760; emb.height = 760; }

  // ----- decorations: bows, twinkles and soft lights (the still ones also show for reduced motion) -----
  function el(tag, cls, host, style) {
    var e = document.createElement(tag); e.className = cls; if (style) e.setAttribute('style', style); host.appendChild(e); return e;
  }
  function bow(host) { if (!host) return; var b = el('img', 'xmas-bow', host); b.src = 'assets/xmas/bow.png'; b.alt = ''; b.width = 270; b.height = 200; }
  function sparks(host, n, area) {
    if (!host) return;
    for (var i = 0; i < n; i++) {
      var x = area[0] + Math.random() * (area[2] - area[0]), y = area[1] + Math.random() * (area[3] - area[1]);
      el('i', 'xmas-spark', host, 'left:' + x.toFixed(1) + '%;top:' + y.toFixed(1) + '%;--s:' + (9 + Math.random() * 15).toFixed(0) + 'px;--d:' + (2.6 + Math.random() * 3).toFixed(1) + 's;--delay:' + (Math.random() * 5).toFixed(1) + 's');
    }
  }
  function bokeh(host, n, area) {
    if (!host) return;
    var box = el('div', 'xmas-bokeh', host); host.insertBefore(box, host.firstChild);
    var cols = ['rgba(255,190,90,.34)', 'rgba(255,214,130,.30)', 'rgba(214,52,58,.30)', 'rgba(255,170,70,.28)', 'rgba(60,170,100,.22)'];
    for (var i = 0; i < n; i++) {
      el('i', '', box, 'left:' + (area[0] + Math.random() * (area[2] - area[0])).toFixed(1) + '%;top:' + (area[1] + Math.random() * (area[3] - area[1])).toFixed(1) + '%;--s:' + (26 + Math.random() * 70).toFixed(0) + 'px;--c:' + cols[i % cols.length] + ';--d:' + (5 + Math.random() * 6).toFixed(1) + 's;--delay:-' + (Math.random() * 6).toFixed(1) + 's');
    }
  }
  bow(document.querySelector('.hero'));
  bow(document.querySelector('.poster'));
  bow(document.querySelector('.gate-door'));
  bow(document.querySelector('.footer'));
  bokeh(document.querySelector('.hero'), 16, [10, 10, 90, 92]);
  bokeh(document.querySelector('.gate-light'), 18, [0, 0, 100, 100]);
  sparks(document.querySelector('.hero'), 16, [8, 4, 92, 70]);
  sparks(document.querySelector('.gate-light'), 22, [6, 8, 94, 90]);
  sparks(document.querySelector('.poster'), 8, [2, -6, 98, 8]);

  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  var canvas = document.createElement('canvas');
  canvas.id = 'xmas-snow';
  canvas.setAttribute('aria-hidden', 'true');
  document.body.appendChild(canvas);
  var ctx = canvas.getContext('2d');
  var w = 0, h = 0, dpr = Math.min(window.devicePixelRatio || 1, 2), flakes = [];

  function resize() {
    w = window.innerWidth; h = window.innerHeight;
    canvas.width = w * dpr; canvas.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var count = Math.round(Math.min(90, Math.max(36, w * h / 17000)));   // fewer on small screens
    while (flakes.length < count) flakes.push(make(true));
    flakes.length = count;
  }

  function make(anywhere) {
    var r = Math.random();
    return {
      x: Math.random() * w,
      y: anywhere ? Math.random() * h : -8,
      size: 0.8 + r * r * 2.6,               // mostly tiny, a few larger and softer
      speed: 14 + r * 36,                    // pixels per second
      drift: 6 + Math.random() * 14,         // sideways sway
      phase: Math.random() * Math.PI * 2,
      alpha: 0.30 + r * 0.50,
      gold: Math.random() < 0.10
    };
  }

  var last = performance.now();
  function frame(now) {
    var dt = Math.min(0.05, (now - last) / 1000); last = now;
    ctx.clearRect(0, 0, w, h);
    for (var i = 0; i < flakes.length; i++) {
      var f = flakes[i];
      f.y += f.speed * dt;
      f.phase += dt * 0.8;
      var x = f.x + Math.sin(f.phase) * f.drift;
      if (f.y > h + 8) { flakes[i] = make(false); continue; }
      var g = ctx.createRadialGradient(x, f.y, 0, x, f.y, f.size * 1.9);
      var rgb = f.gold ? '255,214,120' : '255,250,240';
      g.addColorStop(0, 'rgba(' + rgb + ',' + f.alpha + ')');
      g.addColorStop(1, 'rgba(' + rgb + ',0)');
      ctx.fillStyle = g;
      ctx.beginPath(); ctx.arc(x, f.y, f.size * 1.9, 0, 6.2832); ctx.fill();
    }
    requestAnimationFrame(frame);
  }

  window.addEventListener('resize', resize);
  resize();
  requestAnimationFrame(frame);
})();
