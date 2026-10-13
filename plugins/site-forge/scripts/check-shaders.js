/* Guards the bug that cost the most time on this project: a shader declaring a
   uniform the JS uniforms object does not define. Writing to the missing entry
   throws inside requestAnimationFrame, which the browser swallows, so the
   canvas renders nothing while every inspectable value looks healthy.

   Run: node check-shaders.js <file.js> [more.js ...]   (non-zero exit = broken)
   Defaults to ./gl.js when given no argument. */
const fs = require('fs');
const files = process.argv.slice(2).length ? process.argv.slice(2) : ['gl.js'];
const src = files.map((f) => {
  try { return fs.readFileSync(f, 'utf8'); }
  catch (e) { console.error('cannot read', f); process.exit(2); }
}).join('\n');
let bad = 0;

/* Each `const uniforms = { ... };` block, brace-matched rather than regexed,
   because the values contain braces themselves. */
function blocks(marker) {
  const out = [];
  let i = -1;
  while ((i = src.indexOf(marker, i + 1)) !== -1) {
    let d = 0, j = src.indexOf('{', i);
    const start = j;
    for (; j < src.length; j++) {
      if (src[j] === '{') d++;
      else if (src[j] === '}' && --d === 0) break;
    }
    out.push({ at: i, body: src.slice(start, j + 1) });
  }
  return out;
}

const declared = new Set();
for (const b of blocks('const uniforms = ')) {
  for (const m of b.body.matchAll(/(\bu[A-Z]\w*)\s*:\s*\{/g)) declared.add(m[1]);
}
/* Blob-style scenes merge their uniforms in via onBeforeCompile. */
for (const m of src.matchAll(/(\bu[A-Z]\w*)\s*:\s*\{\s*value:/g)) declared.add(m[1]);

const used = new Set();
for (const m of src.matchAll(/uniform\s+\w+\s+(u\w+)\s*;/g)) used.add(m[1]);
/* Three injects these itself. */
const BUILTIN = new Set(['uTime2']);

const missing = [...used].filter((u) => !declared.has(u) && !BUILTIN.has(u));
if (missing.length) { console.error('MISSING uniforms (shader declares, JS does not):', missing); bad = 1; }
else console.log('uniforms: all', used.size, 'shader uniforms are defined in JS  [' + files.join(', ') + ']');

const attrsUsed = new Set([...src.matchAll(/attribute\s+\w+\s+(a\w+)\s*;/g)].map((m) => m[1]));
const attrsSet = new Set([...src.matchAll(/setAttribute\('(a\w+)'/g)].map((m) => m[1]));
const attrMissing = [...attrsUsed].filter((a) => !attrsSet.has(a));
if (attrMissing.length) { console.error('MISSING attributes:', attrMissing); bad = 1; }
else console.log('attributes: all', attrsUsed.size, 'shader attributes are set on the geometry');

/* Every uniform written by the render loop must also exist. */
const written = new Set([...src.matchAll(/uniforms\.(u\w+)\.value/g)].map((m) => m[1]));
const writeMissing = [...written].filter((u) => !declared.has(u));
if (writeMissing.length) { console.error('WRITTEN but never declared:', writeMissing); bad = 1; }
else console.log('writes:', written.size, 'uniform writes all resolve');

process.exit(bad);
