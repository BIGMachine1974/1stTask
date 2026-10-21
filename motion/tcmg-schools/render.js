// usage: node render.js stills t1,t2,... [dir]  |  node render.js video
let pw; try { pw = require('playwright'); } catch { pw = require('/opt/node22/lib/node_modules/playwright'); }
const { chromium } = pw;
const { spawn } = require('child_process');
const path = require('path');
const mode = process.argv[2], dir = __dirname, FPS = 30;
(async () => {
  const b = await chromium.launch({ args: ['--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  p.on('pageerror', e => console.error('PAGE ERROR', e.message));
  await p.goto('file://' + path.join(dir, 'index.html'));
  await p.evaluate(() => window.ready);
  const DUR = await p.evaluate(() => window.DUR);
  const shot = async t => { await p.evaluate(t => window.seek(t), t); return p.screenshot({ type: 'png', clip: { x: 0, y: 0, width: 1080, height: 1920 } }); };
  if (mode === 'stills') {
    for (const t of process.argv[3].split(',').map(Number)) require('fs').writeFileSync(path.join(dir, process.argv[4] || 'stills', `t${t.toFixed(2)}.png`), await shot(t));
  } else {
    const ff = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-i', '-',
      '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18', '-preset', 'medium', path.join(dir, 'video_only.mp4')], { stdio: ['pipe', 'inherit', 'inherit'] });
    const N = Math.round(DUR * FPS);
    for (let i = 0; i < N; i++) { const buf = await shot(i / FPS); if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r)); if (i % 100 === 0) console.log('frame', i, '/', N); }
    ff.stdin.end(); await new Promise(r => ff.on('close', r));
  }
  await b.close();
})();
