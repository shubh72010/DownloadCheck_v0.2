const themeToggle = document.getElementById('theme-toggle');
const html = document.documentElement;
const downloadBtn = document.getElementById('download-btn');
const spinner = document.querySelector('.spinner');
const btnText = document.querySelector('.btn-text');

themeToggle.addEventListener('click', () => {
  const isDark = html.getAttribute('data-theme') === 'dark';
  html.setAttribute('data-theme', isDark ? 'light' : 'dark');
  themeToggle.textContent = isDark ? '☀️' : '🌙';
});

downloadBtn.addEventListener('click', () => {
  const url = document.getElementById('url').value;
  if (!url) return alert('Paste a URL first.');

  spinner.classList.remove('hidden');
  btnText.textContent = 'Loading...';

  fetch('/download', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ url })
  })
  .then(res => {
    if (res.ok) return res.blob();
    throw new Error('Download failed');
  })
  .then(blob => {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'video.mp4';
    a.click();
  })
  .catch(err => alert(err.message))
  .finally(() => {
    spinner.classList.add('hidden');
    btnText.textContent = 'Download';
  });
});