// Run the generated viewer's JavaScript against a minimal DOM stub.
//
// WHY THIS EXISTS
// `node --check` proves the script PARSES. It does not run it, so a
// ReferenceError inside a draw function is invisible -- and one shipped: `pk`
// was read in gfilter() and referenced in drawG(), which threw on every call
// and silently killed the ring numbering and every click handler on that tab.
// The page still loaded, the tabs still switched, and nothing in the build
// output said otherwise.
//
// So this calls each entry point and reports the first error. It is a smoke
// test, not a rendering test: it cannot see that a chord is the wrong colour,
// only that the code which draws it runs.
//
// Usage (needs node):
//   node scripts/forkscope_check.js figures/forkscope.html
const fs = require('fs');
const path = process.argv[2] ||
  require('path').join(__dirname, '..', 'figures', 'forkscope.html');
const html = fs.readFileSync(path, 'utf8');
const js = html.split('<script>')[1].split('</script>')[0];

const vals = {q: '', arm: '', gsort: 'runs', topn: '10', hw: false, shf: false,
              pay: 'ci_width', ef: '15', met: 'effr', parm: '', rq: '',
              rarm: '', rc: ''};
const cache = {};
function node(id) {
  return cache[id] || (cache[id] = {
    id,
    get value() { return vals[id] !== undefined ? String(vals[id]) : ''; },
    get checked() { return !!vals[id]; },
    set innerHTML(v) { this._h = v; }, get innerHTML() { return this._h || ''; },
    set textContent(v) { this._t = v; }, get textContent() { return this._t || ''; },
    hidden: false,
    tBodies: [{set innerHTML(v) { this._h = v; },
               get innerHTML() { return this._h || ''; }}],
    setAttribute() {}, scrollIntoView() {}, querySelector() { return node('_'); },
    showModal() {}, close() {},
    // Geometry and events. A real element has all of these, so leaving them out
    // does not make the test stricter -- it makes it unable to run on any
    // viewer that fits, zooms or pans, which is a gap that hides real errors
    // rather than catching them. Added when the ring gained scroll-to-zoom and
    // drag-to-pan and the check died on `addEventListener` before reaching a
    // single draw call.
    addEventListener() {}, removeEventListener() {},
    getBoundingClientRect() {
      return {left: 0, top: 0, right: 900, bottom: 900,
              width: 900, height: 900, x: 0, y: 0};
    },
    getClientRects() {
      return [{left: 0, top: 0, right: 900, bottom: 900,
               width: 900, height: 900}];
    },
    style: {setProperty() {}, removeProperty() {},
            getPropertyValue() { return ''; }},
    dataset: {},
    classList: {add() {}, remove() {}, toggle() {},
                contains() { return false; }},
    appendChild() {}, removeChild() {}, focus() {}, blur() {},
    getAttribute() { return null; }, querySelectorAll() { return []; },
    children: [], childNodes: [],
  });
}
global.document = {
  getElementById: node,
  querySelectorAll: () => [],
  querySelector: () => node('_'),
  createElement: () => node('_'),
  addEventListener() {},
  body: node('_'),
  documentElement: node('_'),
};
global.window = global;
// A browser resolves a bare `addEventListener(...)` through the global scope
// chain to window's. Without these the viewer's own resize hook throws before
// anything is drawn.
global.addEventListener = () => {};
global.removeEventListener = () => {};
global.requestAnimationFrame = () => {};
global.cancelAnimationFrame = () => {};
global.innerWidth = 1400;
global.innerHeight = 900;
global.getComputedStyle = () => ({getPropertyValue: () => ''});
global.ResizeObserver = class {
  observe() {} unobserve() {} disconnect() {}
};

// Exercise every entry point INSIDE the eval, so const-scoped data is visible.
const probe = `
  drawG(); drawP(); drawL(); drawR(); drawA();
  showFork(FORKS[0]);
  if (HWY.length) showHwy(0);
  showRun(RUNS.find(r => r.spans.length).id);
  ({forks: FORKS.length, runs: RUNS.length, hwy: HWY.length,
    circle: document.getElementById("circle").innerHTML.length,
    list: document.getElementById("gt").tBodies[0].innerHTML.length,
    panB: document.getElementById("panB").innerHTML.length,
    life: document.getElementById("lstage").innerHTML.length,
    iter: document.getElementById("literm").innerHTML.length,
    nov: document.getElementById("lnov").innerHTML.length,
    about: document.getElementById("agates").innerHTML.length,
    panC: document.getElementById("panC").innerHTML.length,
    rows: document.getElementById("rt").tBodies[0].innerHTML.length});
`;
try {
  const r = eval(js + probe);
  for (const [k, v] of Object.entries(r)) {
    if (!v) { console.log(`  FAIL: ${k} is empty`); process.exit(1); }
  }
  console.log(`  ok  ${r.forks} forks, ${r.runs} analyses, ${r.hwy} highways`);
  console.log(`  ok  circle ${r.circle}b · list ${r.list}b · B ${r.panB}b · ` +
              `C ${r.panC}b · corpus ${r.rows}b`);
  console.log(`  ok  lifecycle: stages ${r.life}b · iteration ${r.iter}b · ` +
              `novelty ${r.nov}b`);
  console.log('  ok  showFork, showHwy, showRun all ran');
} catch (e) {
  console.log('  FAIL:', e.message);
  console.log((e.stack || '').split('\n').slice(0, 3).join('\n'));
  process.exit(1);
}
