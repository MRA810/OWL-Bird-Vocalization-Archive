// OWL — Bird Vocalization Archive — Frontend JS

// File upload preview (images)
document.querySelectorAll('.upload-area').forEach(area => {
  const input = area.querySelector('input[type="file"]');
  const preview = area.querySelector('.upload-preview');
  const text = area.querySelector('.upload-text');

  area.addEventListener('click', () => input && input.click());
  area.addEventListener('dragover', e => { e.preventDefault(); area.style.borderColor = 'var(--accent)'; });
  area.addEventListener('dragleave', () => area.style.borderColor = '');
  area.addEventListener('drop', e => {
    e.preventDefault();
    area.style.borderColor = '';
    if (input && e.dataTransfer.files[0]) {
      input.files = e.dataTransfer.files;
      handleFilePreview(e.dataTransfer.files[0], preview, text);
    }
  });

  if (input) {
    input.addEventListener('change', () => {
      if (input.files[0]) handleFilePreview(input.files[0], preview, text);
    });
  }
});

function handleFilePreview(file, preview, text) {
  if (!preview) return;
  if (file.type.startsWith('image/')) {
    const reader = new FileReader();
    reader.onload = e => {
      preview.style.display = 'block';
      const img = preview.querySelector('img') || document.createElement('img');
      img.src = e.target.result;
      if (!preview.querySelector('img')) preview.appendChild(img);
      if (text) text.textContent = file.name;
    };
    reader.readAsDataURL(file);
  } else {
    if (text) text.textContent = '🎵 ' + file.name;
    if (preview) preview.style.display = 'none';
  }
}

// Confirm delete dialogs
document.querySelectorAll('[data-confirm]').forEach(btn => {
  btn.addEventListener('click', e => {
    const msg = btn.dataset.confirm || 'Are you sure? This action cannot be undone.';
    if (!confirm(msg)) e.preventDefault();
  });
});

// Auto-dismiss flash messages after 4s
document.querySelectorAll('.flash').forEach(flash => {
  setTimeout(() => {
    flash.style.transition = 'opacity 0.4s';
    flash.style.opacity = '0';
    setTimeout(() => flash.remove(), 400);
  }, 4000);
});

// Animate bird cards on load
document.querySelectorAll('.bird-card').forEach((card, i) => {
  card.style.opacity = '0';
  card.style.transform = 'translateY(12px)';
  card.style.transition = `opacity 0.3s ease ${i * 0.04}s, transform 0.3s ease ${i * 0.04}s, box-shadow 0.15s, border-color 0.15s`;
  requestAnimationFrame(() => {
    card.style.opacity = '1';
    card.style.transform = 'translateY(0)';
  });
});
