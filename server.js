const PORT = process.env.PORT || 8080;
const SITE = 'Namit Filipino Barbecue';
const ORIGIN = 'https://namit-filipino-barbecue-demo.up.railway.app';

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.xml': 'application/xml; charset=utf-8',
  '.txt': 'text/plain; charset=utf-8',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.gif': 'image/gif',
};

function esc(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function send(res, code, body, type) {
  res.writeHead(code, { 'Content-Type': type || 'text/html; charset=utf-8', 'X-Robots-Tag': 'noindex, nofollow' });
  res.end(body);
}

async function readBody(req, limit) {
  return new Promise((resolve, reject) => {
    let size = 0; const chunks = [];
    req.on('data', (c) => {
      size += c.length;
      if (size > limit) { reject(new Error('body too large')); req.destroy(); return; }
      chunks.push(c);
    });
    req.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    req.on('error', reject);
  });
}

async function relay(form) {
  const key = process.env.BREVO_API_KEY;
  if (!key) throw new Error('BREVO_API_KEY not set');
  const text = [
    `New message from the ${SITE} site (${ORIGIN})`, '',
    `Name: ${form.name || '(not given)'}`,
    `Email: ${form.email || '(not given)'}`, '', '',
    form.message || '(empty message)', '',
    `IP: ${req_ip}`,
  ].join('\n');
  const html = `<p><b>New message from the ${esc(SITE)} site</b> (${esc(ORIGIN)})</p>` +
    `<ul><li>Name: ${esc(form.name || '(not given)')}</li>` +
    `<li>Email: ${esc(form.email || '(not given)')}</li></ul>` +
    `<p>${esc((form.message || '(empty message)').replace(/\r?\n/g, '<br>'))}</p>`;
  const r = await fetch('https://api.brevo.com/v3/smtp/email', {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'api-key': key },
    body: JSON.stringify({
      sender: { name: `${SITE} site`, email: 'jarvis@onsmalltalk.com' },
      to: [{ email: 'jarvis@onsmalltalk.com', name: 'Jarvis (Websites desk)' }],
      replyTo: { email: form.email || 'jarvis@onsmalltalk.com', name: form.name || 'Visitor' },
      subject: `${SITE} site message${form.name ? ' — ' + form.name : ''}`,
      htmlContent: html,
      textContent: text,
    }),
  });
  if (!r.ok) { const body = await r.text(); throw new Error(`Brevo ${r.status}: ${body.slice(0, 300)}`); }
  return r;
}

let req_ip = '';

const server = require('http').createServer(async (req, res) => {
  const u = new URL(req.url, ORIGIN);
  req_ip = (req.headers['x-forwarded-for'] || '').split(',')[0].trim();
  let path = u.pathname;
  if (path === '/open') {
    res.writeHead(200, { 'Content-Type': 'image/gif', 'Cache-Control': 'no-store, no-cache, must-revalidate', 'X-Robots-Tag': 'noindex, nofollow' });
    res.end(require('fs').readFileSync(require('path').join(__dirname, 'public', 'pixel.gif')));
    return;
  }
  if (path.endsWith('/') && path !== '/') path = path.slice(0, -1);
  if (path === '') path = '/';
  if (path === '/healthz') { send(res, 200, 'ok', 'text/plain; charset=utf-8'); return; }

  if (path === '/contact' && req.method === 'POST') {
    let form;
    try {
      const raw = await readBody(req, 64 * 1024);
      form = Object.fromEntries(new URLSearchParams(raw));
    } catch (e) { send(res, 400, '<p>Could not read the form.</p>'); return; }
    if (!form.message || !String(form.message).trim()) { send(res, 400, '<p>Please add a message.</p>'); return; }
    if (form.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) { send(res, 400, '<p>That email address looks off — please check it.</p>'); return; }
    try { await relay(form); } catch (e) { console.error('MAILERR', e.message); send(res, 502, '<p>The message could not be sent right now. Please try again, or email us directly.</p>'); return; }
    res.writeHead(303, { Location: '/thanks' }); res.end(); return;
  }

  if (req.method !== 'GET' && req.method !== 'HEAD') { send(res, 405, 'Method not allowed', 'text/plain; charset=utf-8'); return; }

  const pub = require('path').join(__dirname, 'public');
  let file = path === '/' ? 'index.html' : path.replace(/^\/+/, '');
  if (!file.includes('.') && require('fs').existsSync(require('path').join(pub, file + '.html'))) file += '.html';
  if (file.includes('.')) {
    try {
      const data = require('fs').readFileSync(require('path').join(pub, file));
      send(res, 200, data, MIME[require('path').extname(file)] || 'application/octet-stream');
      return;
    } catch (e) { /* fall to 404 */ }
  }
  try {
    const data = require('fs').readFileSync(require('path').join(pub, '404.html'));
    send(res, 404, data);
  } catch (e) { send(res, 404, 'Not found', 'text/plain; charset=utf-8'); }
});

server.listen(PORT, () => console.log(`${SITE} site listening on ${PORT}`));
