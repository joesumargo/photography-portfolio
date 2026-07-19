function closeLightbox() {
  const lb = document.getElementById('lightbox');
  const inner = lb.firstElementChild;
  if (inner) {
    inner.style.transition = 'opacity 150ms ease-out';
    inner.style.opacity = '0';
    setTimeout(() => {
      lb.classList.add('hidden');
      lb.innerHTML = '';
    }, 150);
  } else {
    lb.classList.add('hidden');
    lb.innerHTML = '';
  }
}

// ── Click-and-hold zoom with pan ─────────────────────────────

let zoomState = null;

function originFromCursor(img, e) {
  const rect = img.getBoundingClientRect();
  const x = ((e.clientX - rect.left) / rect.width) * 100;
  const y = ((e.clientY - rect.top) / rect.height) * 100;
  return { x, y };
}

document.addEventListener('mousedown', function(e) {
  const img = e.target.closest('#lightbox img');
  if (!img) return;
  e.preventDefault();

  const origin = originFromCursor(img, e);
  img.style.transition = 'transform 200ms ease-out';
  img.style.transformOrigin = `${origin.x}% ${origin.y}%`;
  img.style.transform = 'scale(2.5)';
  img.style.cursor = 'zoom-out';

  zoomState = {
    img,
    originX: origin.x,
    originY: origin.y,
    startX: e.clientX,
    startY: e.clientY,
  };
});

document.addEventListener('mousemove', function(e) {
  if (!zoomState) return;
  const dx = e.clientX - zoomState.startX;
  const dy = e.clientY - zoomState.startY;

  zoomState.img.style.transition = 'none';
  zoomState.img.style.transform = `scale(2.5) translate(${-dx / 2.5}px, ${-dy / 2.5}px)`;
});

document.addEventListener('mouseup', function(e) {
  if (!zoomState) return;
  const img = zoomState.img;
  zoomState = null;

  img.style.transition = 'transform 200ms ease-out';
  img.style.transform = 'scale(1)';
  img.style.cursor = 'zoom-in';
});

document.addEventListener('mouseleave', function(e) {
  if (!zoomState) return;
  const img = zoomState.img;
  zoomState = null;

  img.style.transition = 'transform 200ms ease-out';
  img.style.transform = 'scale(1)';
  img.style.cursor = 'zoom-in';
});

// Touch support
document.addEventListener('touchstart', function(e) {
  const img = e.target.closest('#lightbox img');
  if (!img) return;
  if (e.touches.length !== 1) return;

  const touch = e.touches[0];
  const origin = originFromCursor(img, touch);
  img.style.transition = 'transform 200ms ease-out';
  img.style.transformOrigin = `${origin.x}% ${origin.y}%`;
  img.style.transform = 'scale(2.5)';
  img.style.cursor = 'zoom-out';

  zoomState = {
    img,
    originX: origin.x,
    originY: origin.y,
    startX: touch.clientX,
    startY: touch.clientY,
  };
});

document.addEventListener('touchmove', function(e) {
  if (!zoomState) return;
  const touch = e.touches[0];
  const dx = touch.clientX - zoomState.startX;
  const dy = touch.clientY - zoomState.startY;

  zoomState.img.style.transition = 'none';
  zoomState.img.style.transform = `scale(2.5) translate(${-dx / 2.5}px, ${-dy / 2.5}px)`;
});

document.addEventListener('touchend', function(e) {
  if (!zoomState) return;
  const img = zoomState.img;
  zoomState = null;

  img.style.transition = 'transform 200ms ease-out';
  img.style.transform = 'scale(1)';
  img.style.cursor = 'zoom-in';
});

// ─────────────────────────────────────────────────────────────

document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') {
    closeLightbox();
  }
});
