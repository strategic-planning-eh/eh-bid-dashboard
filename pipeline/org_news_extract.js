#!/usr/bin/env node
/* org_news_extract.js — reads the data blocks of the Vision 2030 dashboard and the PIF Strategy page and prints them as JSON,
   so build_org_news.py can link them to organisation profiles. Nothing is fetched; the two pages are the only source.
   usage: node org_news_extract.js <vision2030_dashboard.html> <pif_strategy_2026_2030.html> */
const fs = require('fs');
function scripts(f) {
  const s = fs.readFileSync(f, 'utf8'), out = [], re = /<script(?![^>]*src=)[^>]*>([\s\S]*?)<\/script>/g; let m;
  while ((m = re.exec(s))) out.push(m[1]); return out;
}
function constBlock(src, name) {           // text of `const NAME = …` up to the next top-level declaration
  const a = src.indexOf('const ' + name); if (a < 0) return null;
  const ends = ['\nconst ', '\nlet ', '\nvar ', '\nfunction '].map(k => src.indexOf(k, a + 8)).filter(x => x > 0);
  return src.slice(a, Math.min.apply(null, ends.concat([src.length])));
}
function evalConst(src, name) { const b = constBlock(src, name); if (!b) return null; try { return new Function(b + ';return ' + name)(); } catch (e) { return null; } }

const out = { v2030: null, pif: null, errors: [] };
try {
  const v = scripts(process.argv[2]).find(x => x.includes('const PROJECTS'));
  out.v2030 = { projects: evalConst(v, 'PROJECTS'), reviewed: evalConst(v, 'LAST_REVIEWED'), ar_names: evalConst(v, 'AR_NAMES') || {},
    ar_txt: evalConst(v, 'AR_TXT') || {}, ar_status: evalConst(v, 'AR_STATUS') || {} };
  if (!out.v2030.projects) throw new Error('PROJECTS not readable');
} catch (e) { out.errors.push('v2030: ' + e.message); out.v2030 = null; }
try {
  const p = scripts(process.argv[3]).find(x => x.includes('const S') && x.includes('ecosystems'));
  const a = p.indexOf('const S'), b = p.indexOf('const I18N');
  const S = new Function(p.slice(a, b) + ';return S')();
  const B = evalConst(p, 'BUILD') || {};
  out.pif = { build: B, ecosystems: S.ecosystems, relevance: S.relevance, giga: S.giga, regional: (S.regional || {}).assets || [] };
} catch (e) { out.errors.push('pif: ' + e.message); out.pif = null; }
process.stdout.write(JSON.stringify(out));
