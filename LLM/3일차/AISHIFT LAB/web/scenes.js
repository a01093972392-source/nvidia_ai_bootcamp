/* 장면 그림 (SVG). 구성 영역은 800x350 이고, 배경은 좌우로 훨씬 넓게 그려
   화면이 아무리 넓어도 잘리지 않고 빈 곳 없이 이어진다 (preserveAspectRatio="meet").

   text.lbl  : 읽어야 하는 이름표. 화면 배율과 무관하게 같은 크기로 보이도록 index.html이 --lbl 을 보정한다.
   text.deco : 장식용 글자(모니터 화면, 간판 등). 읽지 않아도 되는 것. */

const VIEW_W = 800, VIEW_H = 350;
const X0 = -1400, XW = 3600; // 배경이 깔리는 가로 범위

const rnd = (n) => { const x = Math.sin(n * 12.9898 + 78.233) * 43758.5453; return x - Math.floor(x); };

const DEFS = `<defs>
  <linearGradient id="gSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d0022"/><stop offset=".55" stop-color="#2b0a52"/><stop offset="1" stop-color="#6a1670"/></linearGradient>
  <linearGradient id="gDawn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#050d1c"/><stop offset=".55" stop-color="#14405a"/><stop offset="1" stop-color="#e9a766"/></linearGradient>
  <linearGradient id="gWallLab" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#07101c"/><stop offset="1" stop-color="#0f2234"/></linearGradient>
  <linearGradient id="gWallSrv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a0516"/><stop offset="1" stop-color="#1a0b30"/></linearGradient>
  <linearGradient id="gWallCtl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0c0509"/><stop offset="1" stop-color="#1c0b12"/></linearGradient>
  <linearGradient id="gWallRoom" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#070b18"/><stop offset="1" stop-color="#101c3a"/></linearGradient>
  <linearGradient id="gFloor" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#101a2c"/><stop offset="1" stop-color="#04060c"/></linearGradient>
  <linearGradient id="gMetal" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1b2640"/><stop offset=".45" stop-color="#46547a"/><stop offset="1" stop-color="#1b2640"/></linearGradient>
  <linearGradient id="gSteel" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#2a3350"/><stop offset=".5" stop-color="#5a6890"/><stop offset="1" stop-color="#2a3350"/></linearGradient>
  <linearGradient id="gWood" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a4a6c"/><stop offset="1" stop-color="#1b2540"/></linearGradient>
  <linearGradient id="gCone" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cfe9ff" stop-opacity=".26"/><stop offset="1" stop-color="#cfe9ff" stop-opacity="0"/></linearGradient>
  <linearGradient id="gLamp" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffe27a" stop-opacity=".5"/><stop offset="1" stop-color="#ffe27a" stop-opacity="0"/></linearGradient>
  <linearGradient id="gDoorLight" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f4fff0"/><stop offset="1" stop-color="#9cff8a"/></linearGradient>
  <linearGradient id="gRed" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff2a4a" stop-opacity=".4"/><stop offset="1" stop-color="#ff2a4a" stop-opacity="0"/></linearGradient>
  <pattern id="pHazard" width="16" height="16" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="16" fill="#ffd400"/><rect x="8" width="8" height="16" fill="#111522"/></pattern>
  <pattern id="pScan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".4"/></pattern>
  <clipPath id="cScreen"><rect x="302" y="78" width="196" height="110" rx="3"/></clipPath>
  <filter id="glow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <filter id="blur8" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="9"/></filter>
</defs>`;

/* 모니터 화면 글자. 글자 수에 맞춘 폭을 계산하되 maxW를 넘으면 textLength로 눌러 화면 밖으로 나가지 않게 한다 */
const screenLines = (lines, x, y0, step, maxW) =>
  lines.map((s, i) => {
    const w = Math.min(maxW, Math.round(s.length * 7.4));
    const blink = i === lines.length - 1 ? " neon-flicker" : "";
    return `<text class="deco${blink}" x="${x}" y="${y0 + i * step}" textLength="${w}" lengthAdjust="spacingAndGlyphs">${s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")}</text>`;
  }).join("");

/* 바닥: 소실점으로 모이는 세로선 + 간격이 넓어지는 가로선 */
const floorGrid = (y0, color, op = 0.35) => {
  let s = "";
  for (let i = -44; i <= 44; i++) s += `<line x1="${400 + i * 16}" y1="${y0}" x2="${400 + i * 78}" y2="${VIEW_H + 20}" stroke="${color}" stroke-opacity="${op}"/>`;
  for (let j = 0; j < 9; j++) { const y = y0 + j * j * 1.5 + j * 3; s += `<line x1="${X0}" y1="${y}" x2="${X0 + XW}" y2="${y}" stroke="${color}" stroke-opacity="${op}"/>`; }
  return s;
};

/* ───────── 항목 아이콘: 서버가 알려주는 오브젝트/출구를 이름에 맞는 그림으로 ─────────
   각 아이콘은 (0,0)을 중심으로 가로 ±40, 세로 ±36 안에 그린다. */
const ICONS = {
  rack: (c) => `<rect x="-24" y="-36" width="48" height="72" rx="3" fill="#0a0714" stroke="${c}" stroke-width="2"/>
    ${[0, 1, 2, 3, 4].map((i) => `<rect x="-19" y="${-31 + i * 13}" width="38" height="10" rx="1" fill="#140d26" stroke="#3b2a66"/><rect x="-15" y="${-28 + i * 13}" width="14" height="2" fill="#07040f"/><circle cx="13" cy="${-26 + i * 13}" r="2" fill="${i % 2 ? "#00e5ff" : "#ff2bd6"}" filter="url(#glow)"/>`).join("")}`,
  terminal: (c) => `<rect x="-30" y="-32" width="60" height="42" rx="4" fill="#0a111c" stroke="${c}" stroke-width="2"/><rect x="-25" y="-27" width="50" height="32" fill="#02120a"/>
    <rect x="-21" y="-22" width="26" height="2.5" fill="#39ff88"/><rect x="-21" y="-16" width="38" height="2.5" fill="#39ff88" opacity=".7"/><rect x="-21" y="-10" width="20" height="2.5" fill="#39ff88" opacity=".5"/><rect x="-21" y="-4" width="6" height="3" fill="#39ff88" class="neon-flicker"/>
    <rect x="-6" y="10" width="12" height="7" fill="#182440"/><rect x="-34" y="18" width="68" height="12" rx="2" fill="#111a2e" stroke="${c}" stroke-opacity=".6"/>
    ${Array.from({ length: 8 }, (_, i) => `<rect x="${-30 + i * 8}" y="21" width="6" height="3" fill="#2a3a5c"/>`).join("")}`,
  panel: (c) => `<rect x="-32" y="-34" width="64" height="68" rx="3" fill="#101a2e" stroke="${c}" stroke-width="2"/><rect x="-32" y="-34" width="64" height="9" fill="url(#pHazard)"/>
    <circle cx="-14" cy="-6" r="11" fill="#04101c" stroke="#8fe9ff"/><line x1="-14" y1="-6" x2="-8" y2="-13" stroke="#ff2a4a" stroke-width="2"/><circle cx="-14" cy="-6" r="2" fill="#8fe9ff"/>
    ${[0, 1, 2].map((i) => `<rect x="${6 + i * 9}" y="-14" width="5" height="18" rx="1" fill="#0a1020" stroke="#4a5a80"/><rect x="${6 + i * 9}" y="${i % 2 ? -6 : -14}" width="5" height="8" fill="${i % 2 ? "#39ff88" : "#ffd400"}"/>`).join("")}
    ${[0, 1, 2, 3].map((i) => `<circle cx="${-22 + i * 14}" cy="18" r="3" fill="${i % 3 ? "#39ff88" : "#ff2a4a"}" filter="url(#glow)"/>`).join("")}`,
  cable: (c) => `<ellipse cx="0" cy="22" rx="30" ry="9" fill="#0a1020" stroke="#3a4a70"/>
    <path d="M-28 20 C -28 -10, 0 -22, 0 6 C 0 -22, 28 -10, 28 20" fill="none" stroke="${c}" stroke-width="5" stroke-linecap="round"/>
    <path d="M-20 20 C -20 0, 0 -8, 0 12 C 0 -8, 20 0, 20 20" fill="none" stroke="#00e5ff" stroke-width="4" stroke-linecap="round" opacity=".8"/>
    <rect x="-34" y="14" width="12" height="9" rx="2" fill="#c0cbe6"/><rect x="22" y="14" width="12" height="9" rx="2" fill="#c0cbe6"/>`,
  safe: (c) => `<rect x="-30" y="-34" width="60" height="68" rx="4" fill="url(#gMetal)" stroke="${c}" stroke-width="2"/><rect x="-23" y="-27" width="46" height="54" rx="2" fill="#0a1220" stroke="#2c3a58"/>
    <circle cx="0" cy="-2" r="14" fill="#101a2e" stroke="#c0cbe6" stroke-width="2"/><line x1="0" y1="-2" x2="7" y2="-9" stroke="#ffd400" stroke-width="3"/>${[0, 1, 2, 3, 4, 5].map((i) => `<line x1="${Math.cos(i * 1.05) * 11}" y1="${-2 + Math.sin(i * 1.05) * 11}" x2="${Math.cos(i * 1.05) * 14}" y2="${-2 + Math.sin(i * 1.05) * 14}" stroke="#8fa3c8"/>`).join("")}
    <rect x="-8" y="16" width="16" height="7" rx="1" fill="#ffd400" filter="url(#glow)"/>`,
  note: (c) => `<g transform="rotate(-5)"><rect x="-24" y="-34" width="48" height="66" fill="#d9e8ff" opacity=".95"/><rect x="-24" y="-34" width="48" height="8" fill="${c}" opacity=".8"/>
    ${[0, 1, 2, 3, 4, 5].map((i) => `<line x1="-17" y1="${-16 + i * 9}" x2="${i % 3 === 2 ? 4 : 17}" y2="${-16 + i * 9}" stroke="#6a7fa8" stroke-width="2"/>`).join("")}
    <circle cx="0" cy="-34" r="4" fill="#ff2a4a"/></g>`,
  key: (c) => `<circle cx="-16" cy="0" r="15" fill="none" stroke="${c}" stroke-width="6"/><circle cx="-16" cy="0" r="5" fill="#04101c"/>
    <rect x="-3" y="-4" width="40" height="8" rx="2" fill="${c}"/><rect x="20" y="4" width="6" height="12" fill="${c}"/><rect x="30" y="4" width="6" height="9" fill="${c}"/>`,
  disk: (c) => `<rect x="-30" y="-28" width="60" height="56" rx="4" fill="#0e1628" stroke="${c}" stroke-width="2"/><circle cx="0" cy="-2" r="20" fill="#05080f" stroke="#4a5a80"/>
    <circle cx="0" cy="-2" r="8" fill="#1c2748" stroke="#8fa3c8"/><circle cx="0" cy="-2" r="2" fill="#c0cbe6"/><line x1="12" y1="-18" x2="4" y2="-4" stroke="#c0cbe6" stroke-width="3"/>
    <rect x="-22" y="20" width="22" height="4" fill="#4a5a80"/><circle cx="22" cy="22" r="2.5" fill="#39ff88" filter="url(#glow)"/>`,
  camera: (c) => `<rect x="-30" y="-20" width="46" height="28" rx="4" fill="#161f36" stroke="${c}" stroke-width="2" transform="rotate(-8)"/>
    <circle cx="-22" cy="-2" r="9" fill="#05080f" stroke="#8fa3c8" stroke-width="2" transform="rotate(-8)"/><circle cx="-22" cy="-2" r="4" fill="#2a4a8a" transform="rotate(-8)"/>
    <circle cx="6" cy="-14" r="2.5" fill="#ff2a4a" filter="url(#glow)" class="neon-flicker"/><path d="M14 4 L24 14 H32 M24 14 V32" fill="none" stroke="#8fa3c8" stroke-width="5"/><rect x="14" y="30" width="22" height="5" fill="#4a5a80"/>`,
  display: (c) => `<rect x="-36" y="-30" width="72" height="50" rx="3" fill="#0a111c" stroke="${c}" stroke-width="2"/><rect x="-31" y="-25" width="62" height="40" fill="#04101c"/>
    <polyline points="-27,8 -16,-4 -6,2 6,-14 18,-6 27,-18" fill="none" stroke="#39ff88" stroke-width="2.5"/>${[0, 1, 2, 3].map((i) => `<rect x="${-27 + i * 15}" y="10" width="9" height="3" fill="#00e5ff" opacity=".7"/>`).join("")}
    <rect x="-4" y="20" width="8" height="8" fill="#182440"/><rect x="-18" y="28" width="36" height="5" rx="2" fill="#182440"/>`,
  desk: (c) => `<rect x="-36" y="-4" width="72" height="9" rx="2" fill="url(#gWood)" stroke="${c}"/><rect x="-32" y="5" width="6" height="28" fill="#0d1526" stroke="#26324e"/><rect x="26" y="5" width="6" height="28" fill="#0d1526" stroke="#26324e"/>
    <rect x="-24" y="5" width="22" height="20" fill="#121c33" stroke="#34466e"/><rect x="-18" y="13" width="10" height="3" fill="#8fa3c8"/><rect x="-12" y="-20" width="20" height="16" rx="2" fill="#0a111c" stroke="${c}"/><rect x="14" y="-12" width="14" height="8" fill="#d9e8ff" opacity=".9"/>`,
  door: (c) => `<rect x="-26" y="-36" width="52" height="72" rx="2" fill="#0e1830" stroke="${c}" stroke-width="2.5"/><rect x="-26" y="-36" width="52" height="8" fill="url(#pHazard)"/>
    <rect class="door-light" x="-20" y="-26" width="40" height="58" fill="url(#gDoorLight)"/>
    <g class="door-leaf"><rect x="-20" y="-26" width="40" height="58" fill="url(#gSteel)"/><line x1="0" y1="-26" x2="0" y2="32" stroke="#0a1020" stroke-width="3"/>
    <rect x="-12" y="-14" width="24" height="7" rx="1" fill="#16081f" stroke="${c}"/><rect x="-8" y="6" width="4" height="16" rx="1" fill="#c0cbe6"/><rect x="4" y="6" width="4" height="16" rx="1" fill="#c0cbe6"/></g>`,
  generic: (c) => `<rect x="-28" y="-26" width="56" height="52" rx="4" fill="#101a2e" stroke="${c}" stroke-width="2"/><line x1="-28" y1="-10" x2="28" y2="-10" stroke="${c}" stroke-opacity=".5"/>
    <text class="deco" x="0" y="18" text-anchor="middle" font-size="30" font-weight="700" fill="${c}" filter="url(#glow)">?</text>`,
};
/* 이름(id + label)에서 아이콘을 고른다. 위에서부터 먼저 맞는 것. 문서/출입문처럼 '문'이 겹치는 말에 주의 */
const ICON_RULES = [
  ["safe", /금고|보관함|캐비닛|사물함|safe|locker|cabinet|vault/i],
  ["note", /메모|문서|노트|일지|쪽지|기록|종이|서류|note|memo|paper|document|log|file/i],
  ["key", /열쇠|키카드|카드|배지|key|card|badge/i],
  ["camera", /카메라|cctv|camera/i],
  ["disk", /디스크|드라이브|저장|테이프|usb|disk|drive|tape/i],
  ["cable", /케이블|배선|전선|선로|cable|wire/i],
  ["panel", /패널|전원|제어|배전|차단기|스위치|분전|panel|power|breaker|switch|control/i],
  ["door", /출입문|출입구|출구|해치|door|hatch|gate|exit|(^|\s)문$/i],
  ["terminal", /단말|콘솔|컴퓨터|모니터|pc|터미널|console|terminal|computer|monitor|workstation/i],
  ["rack", /랙|서버|rack|server/i],
  ["display", /화면|보드|디스플레이|스크린|screen|display|board/i],
  ["desk", /책상|테이블|desk|table/i],
];
const iconFor = (id, label, isExit) => {
  if (isExit) return "door";
  // 사람이 읽는 이름(label)을 먼저, 못 찾으면 id(research_pc 같은 값)로 고른다
  for (const text of [label, String(id).replace(/_/g, " ")])
    for (const [name, re] of ICON_RULES) if (re.test(text)) return name;
  return "generic";
};
/* 라벨을 두 줄로 나눈다 (공백 기준, 없으면 가운데). 줄당 5글자 안팎 */
const wrapLabel = (s) => {
  if (s.length <= 5) return [s];
  const sp = s.indexOf(" ", 2);
  if (sp > 0 && sp < s.length - 1) return [s.slice(0, sp), s.slice(sp + 1)];
  const h = Math.ceil(s.length / 2);
  return [s.slice(0, h), s.slice(h)];
};
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

/* ───────── 출구(문) 배치: 방 크기에 비례하는 큰 문 ─────────
   문 높이는 장면 높이(350)의 약 63% 로, 연구실의 문과 같은 비율이다. 물체(아이콘)보다 훨씬 크게 그린다.
   앞으로 가는 문은 오른쪽, 이미 가 본 방으로 돌아가는 문은 왼쪽 벽에 세운다. 3개째부터는 아이콘으로 둔다. */
const DOOR_W = 135, DOOR_H = 220, DOOR_LEFT_X = 100, DOOR_RIGHT_X = 700;

/* '연구실 출입문' → '연구실' : 이름에서 문 이름을 떼어 어느 방으로 가는 문인지 본다 */
const doorTarget = (label) => String(label).replace(/\s*(출입문|출입구|입구|출구|문)\s*$/, "").trim();
const leadsBack = (exit, visited) => {
  const t = doorTarget(exit.label);
  return t.length >= 2 && (visited || []).some((v) => v && (v.includes(t) || t.includes(v)));
};
/* 큰 문 두 개(오른쪽=앞, 왼쪽=뒤)와 나머지를 나눈다 */
const layoutExits = (ctx) => {
  const exits = (ctx && ctx.exits) || [], visited = (ctx && ctx.visited) || [];
  const forward = exits.filter((e) => !leadsBack(e, visited)), back = exits.filter((e) => leadsBack(e, visited));
  const ordered = [...forward, ...back];
  return { right: ordered[0] || null, left: ordered[1] || null, rest: ordered.slice(2) };
};
/* 물체 아이콘이 놓일 가로 범위: 문이 서 있는 쪽은 비운다 */
const objectArea = (lay) => (lay.left && lay.right ? [190, 610] : lay.right ? [30, 620] : lay.left ? [180, 770] : [20, 780]);

/* 이름표 줄바꿈: 공백 기준(없으면 가운데)으로 두 줄, 줄당 max글자 안팎 */
const wrapLabelMax = (s, max) => {
  if (s.length <= max) return [s];
  const sp = s.indexOf(" ", 2);
  const parts = sp > 0 && sp < s.length - 1 ? [s.slice(0, sp), s.slice(sp + 1)] : [s.slice(0, Math.ceil(s.length / 2)), s.slice(Math.ceil(s.length / 2))];
  return parts.map((p) => (p.length > max + 3 ? p.slice(0, max + 2) + "…" : p));
};

const bigDoor = (e, cx, base) => {
  const sx = DOOR_W / 52, sy = DOOR_H / 72, top = base - DOOR_H;
  const lines = wrapLabelMax("→ " + e.label, 6);
  const label = lines.length === 1
    ? `<tspan x="${cx}" dy="0">${esc(lines[0])}</tspan>`
    : `<tspan x="${cx}" dy="-1.08em">${esc(lines[0])}</tspan><tspan x="${cx}" dy="1.08em">${esc(lines[1])}</tspan>`;
  return `<g data-item="${esc(e.id)}" data-icon="door" data-exit="true" data-big="true">
    <ellipse cx="${cx}" cy="${base + 2}" rx="${DOOR_W * 0.62}" ry="9" fill="#00e5ff" opacity=".2" filter="url(#blur8)"/>
    <g transform="translate(${cx} ${base - 36 * sy}) scale(${sx} ${sy})">${ICONS.door("#00e5ff")}</g>
    <text class="lbl" x="${cx}" y="${top - 8}" text-anchor="middle" fill="#8fe9ff">${label}</text></g>`;
};

/* 항목 층: 큰 문은 벽 좌우에, 물체와 남는 출구는 가운데 아이콘 + 이름표로 늘어놓는다.
   top: 물체 영역의 위쪽 y, base: 문이 서는 바닥 y */
const itemsLayer = (ctx, top, opts = {}) => {
  const base = opts.base || 300;
  const objs = (ctx && ctx.objects) || [];
  const lay = layoutExits(ctx);
  const things = [...objs.map((o) => ({ ...o, exit: false })), ...lay.rest.map((o) => ({ ...o, exit: true }))];
  const n = things.length;
  const [a0, a1] = objectArea(lay), width = a1 - a0, mid = (a0 + a1) / 2;
  let out = "";
  if (n) {
    const cap = Math.max(3, Math.floor(width / 100));
    const rows = n > cap ? 2 : 1, per = Math.ceil(n / rows), sc = rows === 1 ? 1 : 0.62;
    const areaTop = rows === 2 ? Math.min(top, 110) : top;
    const rowCy = rows === 1 ? [areaTop + 32] : [areaTop + 28, areaTop + 134];
    const gap = Math.min(170, width / per), maxChars = gap < 125 ? 4 : 5;
    out += `<rect x="${a0 - 12}" y="${areaTop}" width="${width + 24}" height="${VIEW_H - areaTop + 20}" fill="#03050c" opacity=".62"/><line x1="${a0 - 12}" y1="${areaTop}" x2="${a1 + 12}" y2="${areaTop}" stroke="#ff2bd6" stroke-opacity=".55"/>`;
    things.forEach((it, i) => {
      const r = Math.floor(i / per), k = i % per, inRow = Math.min(per, n - r * per);
      const cx = mid + (k - (inRow - 1) / 2) * gap, cy = rowCy[r];
      const icon = iconFor(it.id, it.label, it.exit), color = it.exit ? "#00e5ff" : "#ff8aeb";
      const lines = wrapLabelMax((it.exit ? "→ " : "") + it.label, maxChars);
      const ly = cy + 47 * sc;  // 글자 윗선 기준: 아이콘 바로 아래에서 시작한다
      out += `<g data-item="${esc(it.id)}" data-icon="${icon}" data-exit="${it.exit}">
        <ellipse cx="${cx}" cy="${cy + 38 * sc}" rx="${34 * sc}" ry="${6 * sc}" fill="${color}" opacity=".18" filter="url(#blur8)"/>
        <g transform="translate(${cx} ${cy}) scale(${sc})">${ICONS[icon](color)}</g>
        <text class="lbl" x="${cx}" y="${ly}" text-anchor="middle" dominant-baseline="hanging" fill="${it.exit ? "#8fe9ff" : "#ffd6f6"}">${lines.map((l, j) => `<tspan x="${cx}" dy="${j ? "1.08em" : "0"}">${esc(l)}</tspan>`).join("")}</text></g>`;
    });
  }
  if (lay.right) out += bigDoor(lay.right, DOOR_RIGHT_X, base);
  if (lay.left) out += bigDoor(lay.left, DOOR_LEFT_X, base);
  return out;
};

const ART = {
  /* ───────── 오프닝: 비 내리는 사이버펑크 도시 ───────── */
  intro: () => {
    let far = "", near = "", antenna = "";
    for (let i = -18; i < 50; i++) { // 뒤쪽 건물 (흐릿)
      const h = 70 + rnd(i) * 90, x = i * 40, w = 30 + rnd(i + 9) * 16;
      far += `<rect x="${x}" y="${252 - h}" width="${w}" height="${h + 40}" fill="#150a33" opacity=".9"/>`;
    }
    for (let i = -14; i < 38; i++) { // 앞쪽 건물 (창문 불빛)
      const h = 80 + rnd(i * 3) * 130, x = i * 56, w = 40 + rnd(i + 4) * 20;
      near += `<rect x="${x}" y="${290 - h}" width="${w}" height="${h + 20}" fill="#0a1030" stroke="#00e5ff" stroke-opacity=".35"/>`;
      for (let r = 0; r < Math.floor(h / 22); r++) for (let c = 0; c < 3; c++) {
        if (rnd(i * 31 + r * 7 + c) > 0.45) near += `<rect x="${x + 6 + c * 12}" y="${290 - h + 8 + r * 20}" width="7" height="10" fill="${rnd(i + r + c) > 0.5 ? "#00e5ff" : "#ff2bd6"}" opacity=".85"/>`;
      }
      if (rnd(i) > 0.7) antenna += `<line x1="${x + w / 2}" y1="${290 - h}" x2="${x + w / 2}" y2="${290 - h - 26}" stroke="#4a5a80"/><circle cx="${x + w / 2}" cy="${290 - h - 28}" r="2.5" fill="#ff2a4a" class="neon-flicker"/>`;
    }
    let stars = "";
    for (let i = 0; i < 60; i++) stars += `<circle cx="${rnd(i) * 1600 - 400}" cy="${rnd(i + 50) * 150}" r="${0.6 + rnd(i + 3)}" fill="#fff" opacity="${0.3 + rnd(i + 8) * 0.6}"/>`;
    return `${DEFS}<rect x="${X0}" y="0" width="${XW}" height="${VIEW_H}" fill="url(#gSky)"/>${stars}
      <circle cx="650" cy="86" r="46" fill="#ff2bd6" opacity=".9" filter="url(#glow)"/>
      <circle cx="636" cy="76" r="9" fill="#c01e9e" opacity=".6"/><circle cx="668" cy="98" r="6" fill="#c01e9e" opacity=".6"/><circle cx="650" cy="62" r="4" fill="#c01e9e" opacity=".5"/>
      ${far}${near}${antenna}
      <rect x="${X0}" y="288" width="${XW}" height="70" fill="url(#gFloor)"/>${floorGrid(290, "#ff2bd6", 0.45)}
      <rect x="${X0}" y="96" width="${XW}" height="92" fill="#05060d" opacity=".78"/>
      <line x1="${X0}" y1="96" x2="${X0 + XW}" y2="96" stroke="#00e5ff" opacity=".7"/><line x1="${X0}" y1="188" x2="${X0 + XW}" y2="188" stroke="#ff2bd6" opacity=".7"/>
      <text class="deco neon-flicker" x="400" y="156" text-anchor="middle" font-size="50" font-weight="700" fill="#00e5ff" filter="url(#glow)" letter-spacing="10">AI SHIFT LAB</text>
      <text class="deco" x="400" y="180" text-anchor="middle" font-size="15" fill="#ff8aeb" letter-spacing="7">EMERGENCY POWER RESTORED</text>`;
  },

  /* ───────── AI 연구실 ───────── */
  lab: () => {
    const FL = 262; // 바닥 시작
    let panels = "", pipes = "", tiles = "";
    for (let x = -1400; x < 2200; x += 100) panels += `<line x1="${x}" y1="34" x2="${x}" y2="${FL}" stroke="#16324c" stroke-opacity=".7"/><circle cx="${x + 6}" cy="46" r="1.6" fill="#1f4466"/><circle cx="${x + 6}" cy="${FL - 12}" r="1.6" fill="#1f4466"/>`;
    for (let x = -1400; x < 2200; x += 180) pipes += `<rect x="${x}" y="8" width="12" height="18" rx="2" fill="#1f4466"/>`;
    for (let i = 0; i < 7; i++) tiles += `<rect x="${566 + (i % 2) * 14}" y="${112 + Math.floor(i / 2) * 11}" width="54" height="3" fill="#050b14"/>`;
    return `${DEFS}
      <rect x="${X0}" y="0" width="${XW}" height="${FL}" fill="url(#gWallLab)"/>${panels}
      <rect x="${X0}" y="8" width="${XW}" height="18" fill="#0e2034" stroke="#1f4466"/>${pipes}
      <rect x="${X0}" y="72" width="${XW}" height="5" fill="#123049"/><rect x="${X0}" y="206" width="${XW}" height="5" fill="#123049"/>
      <!-- 천장 형광등 + 빛 -->
      <polygon points="140,34 300,34 380,${FL} 40,${FL}" fill="url(#gCone)" opacity=".6"/>
      <polygon points="500,34 660,34 760,${FL} 420,${FL}" fill="url(#gCone)" opacity=".45"/>
      <rect x="140" y="28" width="160" height="7" rx="2" fill="#dff1ff" filter="url(#glow)" class="neon-flicker"/>
      <rect x="500" y="28" width="160" height="7" rx="2" fill="#dff1ff" filter="url(#glow)"/>
      <!-- 벽 시계 (멈춤) -->
      <circle cx="252" cy="122" r="22" fill="#0a1626" stroke="#4a7aa0" stroke-width="3"/><circle cx="252" cy="122" r="18" fill="none" stroke="#1f4466"/>
      <line x1="252" y1="122" x2="252" y2="108" stroke="#8fe9ff" stroke-width="2.5"/><line x1="252" y1="122" x2="262" y2="127" stroke="#8fe9ff" stroke-width="2"/><circle cx="252" cy="122" r="2.5" fill="#ff2a4a"/>
      <!-- 환기구 -->
      <rect x="560" y="100" width="66" height="48" rx="3" fill="#0a1626" stroke="#2c4a66"/>${tiles}
      <!-- 바닥 -->
      <rect x="${X0}" y="${FL}" width="${XW}" height="100" fill="url(#gFloor)"/>${floorGrid(FL, "#2f8a6a", 0.28)}
      <ellipse cx="400" cy="312" rx="200" ry="20" fill="#39ff88" opacity=".12" filter="url(#blur8)"/>
      <ellipse cx="700" cy="318" rx="110" ry="14" fill="#ff2bd6" opacity=".14" filter="url(#blur8)"/>
      <path d="M432 238 C 470 292, 520 300, 590 322" fill="none" stroke="#141f38" stroke-width="4"/><path d="M432 238 C 462 296, 500 306, 552 330" fill="none" stroke="#1b2a4a" stroke-width="2"/>

      <!-- 잠긴 보관함 -->
      <g data-item="storage_locker" data-icon="safe">
        <rect x="52" y="96" width="120" height="222" rx="3" fill="url(#gMetal)" stroke="#3b7da0" stroke-width="2"/>
        ${[0, 1, 2, 3, 4, 5].map((i) => `<rect x="66" y="${110 + i * 8}" width="92" height="3" rx="1" fill="#04101c"/>`).join("")}
        <line x1="112" y1="162" x2="112" y2="318" stroke="#0a1220" stroke-width="3"/>
        <rect x="98" y="214" width="6" height="26" rx="2" fill="#8fa3c8"/><rect x="120" y="214" width="6" height="26" rx="2" fill="#8fa3c8"/>
        <rect x="68" y="168" width="40" height="22" fill="#0b1a2a" stroke="#8fe9ff" stroke-opacity=".6"/><rect x="74" y="175" width="28" height="3" fill="#8fe9ff" opacity=".7"/><rect x="74" y="181" width="18" height="3" fill="#8fe9ff" opacity=".5"/>
        <path d="M105 214 v-10 a7 7 0 0 1 14 0 v10" fill="none" stroke="#e6e6e6" stroke-width="3"/>
        <rect x="100" y="214" width="20" height="16" rx="2" fill="#ffd400" filter="url(#glow)"/><circle cx="110" cy="221" r="2" fill="#7a5c00"/>
        <rect x="52" y="298" width="120" height="14" fill="url(#pHazard)"/>
      </g>

      <!-- 연구원 책상 + 연구용 PC -->
      <g data-item="research_desk" data-icon="desk">
        <rect x="225" y="248" width="104" height="70" fill="#0d1526" stroke="#26324e"/>
        <rect x="233" y="256" width="88" height="25" fill="#121c33" stroke="#34466e"/><rect x="233" y="286" width="88" height="25" fill="#121c33" stroke="#34466e"/>
        <rect x="269" y="266" width="16" height="4" rx="2" fill="#8fa3c8"/><rect x="269" y="296" width="16" height="4" rx="2" fill="#8fa3c8"/>
        <rect x="566" y="248" width="16" height="70" fill="#0d1526" stroke="#26324e"/>
        <rect x="335" y="248" width="224" height="46" fill="#091020" opacity=".9"/>
        <rect x="212" y="236" width="376" height="13" rx="2" fill="url(#gWood)" stroke="#00e5ff" stroke-opacity=".7"/>
        <line x1="212" y1="249" x2="588" y2="249" stroke="#00e5ff" stroke-width="2" filter="url(#glow)"/>
        <!-- 모니터 -->
        <g data-item="research_pc" data-icon="terminal">
        <rect x="286" y="62" width="228" height="146" rx="10" fill="#0a111c" stroke="#33466a" stroke-width="3"/>
        <rect id="pc-screen" x="298" y="74" width="204" height="118" rx="4" fill="#02120a" stroke="#39ff88" stroke-opacity=".9" filter="url(#glow)"/>
        <rect x="298" y="74" width="204" height="118" rx="4" fill="url(#pScan)" opacity=".8"/>
        <!-- 화면 글자: 글자 폭을 화면(여백 12) 안에 맞추고, 넘치는 부분은 화면 밖으로 그려지지 않게 자른다 -->
        <g clip-path="url(#cScreen)" font-size="12" fill="#7dffae" style="font-weight:700">
          ${screenLines(["> POWER: EMERGENCY OK", "> SECURITY LV.1 : LOCKED", "> USER: ??????", "> _"], 310, 98, 22, 180)}</g>
        <circle cx="496" cy="200" r="2.5" fill="#39ff88" filter="url(#glow)"/>
        <path d="M388 208 h24 l6 22 h-36 z" fill="#101a2c" stroke="#33466a"/><rect x="352" y="229" width="96" height="8" rx="3" fill="#182440" stroke="#33466a"/></g>
        <!-- 키보드, 마우스, 머그, 서류, 스탠드 -->
        <rect x="330" y="224" width="140" height="12" rx="2" fill="#111a2e" stroke="#33466a"/>
        ${Array.from({ length: 14 }, (_, i) => `<rect x="${334 + i * 9.8}" y="227" width="7" height="3" fill="#2a3a5c"/><rect x="${334 + i * 9.8}" y="231" width="7" height="3" fill="#2a3a5c"/>`).join("")}
        <ellipse cx="496" cy="231" rx="9" ry="5" fill="#111a2e" stroke="#33466a"/>
        <g><rect x="233" y="214" width="19" height="22" rx="3" fill="#1d2a48" stroke="#8fe9ff"/><path d="M252 219 q8 2 0 12" fill="none" stroke="#8fe9ff" stroke-width="2"/>
           <path d="M238 210 q-3 -6 0 -10 M246 210 q-3 -6 0 -10" fill="none" stroke="#cfe9ff" stroke-opacity=".5" stroke-width="2" class="neon-flicker"/></g>
        <g transform="rotate(-4 540 232)"><rect x="522" y="224" width="46" height="12" fill="#d9e8ff" opacity=".9"/><rect x="526" y="219" width="46" height="6" fill="#bcd0ee" opacity=".9"/><line x1="530" y1="229" x2="560" y2="229" stroke="#7a8fb5"/></g>
        <polygon points="548,172 536,176 524,236 566,236" fill="url(#gLamp)"/>
        <polyline points="552,236 560,206 546,176" fill="none" stroke="#7a8fb5" stroke-width="3"/><polygon points="534,170 556,166 560,178 530,182" fill="#243558" stroke="#ffe27a"/>
        <ellipse cx="552" cy="236" rx="10" ry="3" fill="#243558"/>
      </g>

      <!-- 서버실 출입문 -->
      <g data-item="server_room_door" data-icon="door">
        <rect x="632" y="74" width="138" height="244" rx="2" fill="#0e1830" stroke="#ff2bd6" stroke-width="3" filter="url(#glow)"/>
        <rect x="632" y="74" width="138" height="12" fill="url(#pHazard)"/>
        <rect class="door-light" x="644" y="90" width="114" height="228" fill="url(#gDoorLight)"/>
        <g class="door-leaf"><rect x="644" y="90" width="114" height="228" fill="url(#gSteel)"/><line x1="701" y1="90" x2="701" y2="318" stroke="#0a1020" stroke-width="4"/>
        <rect x="668" y="118" width="64" height="14" rx="2" fill="#16081f" stroke="#ff2bd6" filter="url(#glow)"/><rect x="672" y="122" width="56" height="6" fill="#ff2bd6" opacity=".35"/>
        <rect x="662" y="150" width="78" height="18" fill="#0b1020" stroke="#3a4a70"/><text class="deco" x="701" y="163" text-anchor="middle" font-size="11" fill="#ff8aeb" letter-spacing="2">SERVER ROOM</text>
        <rect x="688" y="220" width="6" height="30" rx="2" fill="#c0cbe6"/><rect x="708" y="220" width="6" height="30" rx="2" fill="#c0cbe6"/></g>
        <rect x="596" y="166" width="26" height="46" rx="3" fill="#0b1020" stroke="#4a5a80"/>
        ${[0, 1, 2, 3, 4, 5].map((i) => `<rect x="${601 + (i % 3) * 7}" y="${182 + Math.floor(i / 3) * 9}" width="5" height="6" fill="#4a5a80"/>`).join("")}
        <circle cx="609" cy="174" r="3.5" fill="#ff2a4a" filter="url(#glow)" class="neon-flicker"/>
      </g>

      <text class="lbl" x="112" y="84" text-anchor="middle" fill="#8fe9ff">잠긴 보관함</text>
      <text class="lbl" x="400" y="50" text-anchor="middle" fill="#8dffb4">연구용 PC</text>
      <text class="lbl" x="701" y="60" text-anchor="middle" fill="#ff8aeb">서버실 출입문</text>
      <text class="lbl" x="400" y="334" text-anchor="middle" fill="#8fe9ff">연구원 책상</text>`;
  },

  /* ───────── 서버실: 뒤쪽엔 랙, 앞쪽엔 서버가 알려준 항목들을 그림으로 ───────── */
  server: (ctx) => {
    const FL = 196;
    const has = ((ctx && ctx.objects && ctx.objects.length) || 0) + ((ctx && ctx.exits && ctx.exits.length) || 0) > 0;
    let racks = "", trays = "", fog = "";
    const [ra, rb] = objectArea(layoutExits(ctx)), rackN = Math.max(2, Math.floor((rb - ra) / 112));
    for (let i = 0; i < rackN; i++) {
      const x = ra + 9 + i * 112;
      let units = "";
      for (let k = 0; k < 7; k++) {
        const y = 52 + k * 19, led = (i + k) % 3 ? "#ff2bd6" : "#00e5ff", on = (i * 3 + k) % 4 ? "neon-flicker" : "";
        units += `<rect x="${x + 6}" y="${y}" width="82" height="16" rx="1" fill="#140d26" stroke="#3b2a66"/>
          ${[0, 1, 2, 3, 4].map((v) => `<rect x="${x + 10 + v * 4}" y="${y + 3}" width="2" height="10" fill="#07040f"/>`).join("")}
          <rect x="${x + 34}" y="${y + 5}" width="28" height="6" fill="${k % 4 === 0 ? "#06231a" : "#0c0818"}" stroke="#2a1f4a"/>
          <circle cx="${x + 74}" cy="${y + 5}" r="2" fill="${led}" class="${on}" filter="url(#glow)"/><circle cx="${x + 81}" cy="${y + 5}" r="2" fill="${(i + k) % 5 ? "#39ff88" : "#ff2a4a"}" class="${on}"/>`;
      }
      racks += `<g opacity=".9"><rect x="${x}" y="44" width="94" height="${FL - 44}" rx="3" fill="#0a0714" stroke="#ff2bd6" stroke-opacity=".6" stroke-width="2"/>${units}</g>`;
    }
    for (let x = -1400; x < 2200; x += 40) trays += `<line x1="${x}" y1="12" x2="${x}" y2="26" stroke="#3b2a66"/>`;
    for (let i = 0; i < 10; i++) fog += `<ellipse cx="${i * 90 - 40}" cy="${FL + 16}" rx="120" ry="12" fill="#c8a8ff" opacity=".06" filter="url(#blur8)"/>`;
    return `${DEFS}
      <rect x="${X0}" y="0" width="${XW}" height="${FL + 20}" fill="url(#gWallSrv)"/>
      <rect x="${X0}" y="8" width="${XW}" height="20" fill="#120a24" stroke="#3b2a66"/>${trays}
      <path d="M-200 32 C 100 44, 300 20, 600 36 S 1000 28, 1200 38" fill="none" stroke="#ff2bd6" stroke-opacity=".5" stroke-width="3"/>
      <path d="M-200 38 C 150 26, 350 48, 650 32 S 1000 44, 1200 34" fill="none" stroke="#00e5ff" stroke-opacity=".5" stroke-width="3"/>
      <rect x="${X0}" y="${FL}" width="${XW}" height="170" fill="url(#gFloor)"/>${floorGrid(FL, "#a02ad0", 0.4)}
      <polygon points="724,40 640,${FL} 808,${FL}" fill="url(#gRed)" class="rays"/>
      ${racks}${fog}
      <rect x="712" y="14" width="24" height="10" rx="3" fill="#3a0a14" stroke="#ff2a4a"/><circle cx="724" cy="32" r="8" fill="#ff2a4a" filter="url(#glow)" class="neon-flicker"/>
      ${has ? "" : `<text class="lbl" x="400" y="290" text-anchor="middle" fill="#ffd6f6">둘러보면 이곳의 항목이 나타납니다</text>`}
      ${itemsLayer(ctx, FL + 10, { base: 300 })}`;
  },

  /* ───────── 보안 통제실: 벽 가득한 CCTV 모니터, 콘솔, 붉은 경보등 ───────── */
  control: (ctx) => {
    const FL = 214;
    let screens = "", ceiling = "";
    for (let r = 0; r < 2; r++) for (let c = 0; c < 4; c++) {
      const x = 196 + c * 104, y = 30 + r * 74, id = r * 4 + c, feed = id % 4;
      let pic = "";
      if (feed === 0) pic = `<polygon points="${x + 8},${y + 52} ${x + 40},${y + 20} ${x + 56},${y + 20} ${x + 88},${y + 52}" fill="#0a2a38"/><rect x="${x + 40}" y="${y + 20}" width="16" height="12" fill="#02080c"/>`;
      else if (feed === 1) pic = `<rect x="${x + 10}" y="${y + 38}" width="76" height="14" fill="#0a2a38"/><circle cx="${x + 46}" cy="${y + 26}" r="5" fill="#39ff88"/><rect x="${x + 42}" y="${y + 31}" width="8" height="14" fill="#39ff88"/>`;
      else if (feed === 2) pic = [0, 1, 2, 3].map((k) => `<rect x="${x + 10 + k * 20}" y="${y + 14}" width="14" height="36" fill="#0a2a38" stroke="#1d5a78"/><circle cx="${x + 17 + k * 20}" cy="${y + 20}" r="1.8" fill="${k % 2 ? "#00e5ff" : "#ff2bd6"}"/>`).join("");
      else pic = Array.from({ length: 9 }, (_, k) => `<rect x="${x + 4}" y="${y + 6 + k * 5.4}" width="${30 + rnd(id * 9 + k) * 58}" height="1.6" fill="#8fa3c8" opacity=".5"/>`).join("") + `<text class="deco" x="${x + 48}" y="${y + 34}" text-anchor="middle" font-size="9" fill="#ff8aeb">NO SIGNAL</text>`;
      screens += `<g><rect x="${x}" y="${y}" width="96" height="66" rx="3" fill="#06090f" stroke="#4a5a82" stroke-width="2"/>
        <rect x="${x + 4}" y="${y + 4}" width="88" height="52" fill="#031018"/>${pic}<rect x="${x + 4}" y="${y + 4}" width="88" height="52" fill="url(#pScan)" opacity=".75"/>
        <circle cx="${x + 11}" cy="${y + 12}" r="2.4" fill="#ff2a4a" class="neon-flicker"/><text class="deco" x="${x + 88}" y="${y + 14}" text-anchor="end" font-size="7" fill="#8fe9ff">CAM ${String(id + 1).padStart(2, "0")}</text>
        <rect x="${x + 36}" y="${y + 58}" width="24" height="3" fill="#2a3552"/></g>`;
    }
    for (let x = -1400; x < 2200; x += 90) ceiling += `<rect x="${x}" y="6" width="50" height="5" rx="2" fill="#ff4a5e" opacity=".55"/>`;
    return `${DEFS}
      <rect x="${X0}" y="0" width="${XW}" height="${FL + 20}" fill="url(#gWallCtl)"/>${ceiling}
      <rect x="${X0}" y="${FL - 6}" width="${XW}" height="6" fill="#2a0e16"/>
      ${[0, 1, 2, 3, 4, 5].map((i) => `<line x1="${X0}" y1="${44 + i * 28}" x2="${X0 + XW}" y2="${44 + i * 28}" stroke="#3a1420" stroke-opacity=".55"/>`).join("")}
      <rect x="180" y="22" width="440" height="156" rx="4" fill="#0a0d16" stroke="#ff4a5e" stroke-opacity=".7" stroke-width="2" filter="url(#glow)"/>${screens}
      <rect x="${X0}" y="${FL}" width="${XW}" height="170" fill="url(#gFloor)"/>${floorGrid(FL, "#ff4a5e", 0.35)}
      <ellipse cx="400" cy="${FL + 24}" rx="230" ry="16" fill="#ff4a5e" opacity=".14" filter="url(#blur8)"/>
      <rect x="170" y="174" width="460" height="20" rx="3" fill="url(#gWood)" stroke="#ff4a5e"/><line x1="170" y1="194" x2="630" y2="194" stroke="#ff4a5e" stroke-width="2" filter="url(#glow)"/>
      ${Array.from({ length: 14 }, (_, i) => `<rect x="${190 + i * 14}" y="179" width="9" height="6" rx="1" fill="${i % 5 === 0 ? "#ff2a4a" : "#2a3a5c"}"/>`).join("")}
      ${[0, 1, 2].map((i) => `<circle cx="${420 + i * 26}" cy="185" r="5" fill="${["#39ff88", "#ffd400", "#ff2a4a"][i]}" filter="url(#glow)" class="${i === 2 ? "neon-flicker" : ""}"/>`).join("")}
      <rect x="392" y="6" width="16" height="9" rx="3" fill="#3a0a14" stroke="#ff2a4a"/><circle cx="400" cy="22" r="6" fill="#ff2a4a" filter="url(#glow)" class="neon-flicker"/>
      ${itemsLayer(ctx, FL - 16, { base: 300 })}`;
  },

  /* ───────── 그 밖의 장소 (복도) ───────── */
  room: (ctx) => {
    let lights = "", doors = "";
    for (let i = 0; i < 4; i++) {
      const t = (i + 1) / 5, y = 150 - t * 0, w = 150 * (1 - t * 0.78);
      lights += `<rect x="${400 - w / 2}" y="${24 + t * 70}" width="${w}" height="${6 - t * 3}" fill="#dff1ff" filter="url(#glow)" class="${i % 2 ? "neon-flicker" : ""}" opacity="${0.9 - t * 0.4}"/>`;
    }
    const hasExits = !!(ctx && ctx.exits && ctx.exits.length);
    doors = hasExits ? "" : `<polygon points="60,70 150,102 150,246 60,300" fill="#0d1830" stroke="#3d7bff" stroke-width="2"/><polygon points="740,70 650,102 650,246 740,300" fill="#0d1830" stroke="#00e5ff" stroke-width="2"/>
      <polygon points="190,114 250,128 250,226 190,246" fill="#0a1226" stroke="#3d7bff" stroke-opacity=".7"/><polygon points="610,114 550,128 550,226 610,246" fill="#0a1226" stroke="#00e5ff" stroke-opacity=".7"/>`;
    return `${DEFS}<rect x="${X0}" y="0" width="${XW}" height="${VIEW_H}" fill="url(#gWallRoom)"/>
      <polygon points="0,0 800,0 560,128 240,128" fill="#0a1028"/><polygon points="0,350 800,350 560,262 240,262" fill="url(#gFloor)"/>
      <polygon points="0,0 240,128 240,262 0,350" fill="#0b1838"/><polygon points="800,0 560,128 560,262 800,350" fill="#0b1838"/>
      <rect x="240" y="128" width="320" height="134" fill="#02040a" stroke="#3d7bff"/>${doors}${lights}
      ${floorGrid(262, "#3d7bff", 0.3)}<ellipse cx="400" cy="300" rx="170" ry="16" fill="#3d7bff" opacity=".15" filter="url(#blur8)"/>
      <text class="lbl" x="400" y="108" text-anchor="middle" fill="#9cb8ff">복도</text>${itemsLayer(ctx, 214, { base: 300 })}`;
  },

  /* ───────── 탈출 성공: 열리는 출입문, 새벽 ───────── */
  escape: () => {
    let stars = "", city = "";
    for (let i = 0; i < 50; i++) stars += `<circle cx="${300 + rnd(i) * 200}" cy="${rnd(i + 70) * 120 + 60}" r="${0.7 + rnd(i + 2)}" fill="#fff" opacity="${0.4 + rnd(i + 5) * 0.5}" class="${i % 3 ? "" : "neon-flicker"}"/>`;
    for (let i = 0; i < 14; i++) { const h = 20 + rnd(i * 5) * 60, x = 308 + i * 14; city += `<rect x="${x}" y="${296 - h}" width="12" height="${h}" fill="#0a1a26"/>`; }
    return `${DEFS}<rect x="${X0}" y="0" width="${XW}" height="${VIEW_H}" fill="#02060a"/>
      <polygon points="400,190 -300,0 200,0" fill="#7dff6a" opacity=".16" class="rays"/><polygon points="400,190 1100,0 600,0" fill="#7dff6a" opacity=".16" class="rays"/>
      <polygon points="400,300 120,350 680,350" fill="#e8ffe0" opacity=".32" class="rays"/>
      <rect x="${X0}" y="300" width="${XW}" height="60" fill="url(#gFloor)"/>${floorGrid(302, "#7dff6a", 0.28)}
      <rect x="292" y="62" width="216" height="244" fill="#0a1218" stroke="#7dff6a" stroke-width="3" filter="url(#glow)"/>
      <rect x="302" y="72" width="196" height="228" fill="url(#gDawn)"/>${stars}
      <circle cx="400" cy="262" r="26" fill="#ffd38a" opacity=".85" filter="url(#glow)"/>${city}
      <rect x="302" y="72" width="196" height="228" fill="url(#gDoorLight)" opacity=".28"/>
      <rect class="door-open" x="302" y="72" width="196" height="228" fill="url(#gSteel)" stroke="#7dff6a" stroke-width="2"/>
      <rect x="352" y="22" width="96" height="30" rx="4" fill="#06260f" stroke="#7dff6a" stroke-width="2" filter="url(#glow)"/>
      <text class="lbl" x="400" y="46" text-anchor="middle" fill="#b8ffae">EXIT</text>`;
  },
};

window.SCENE_ART = ART;
window.SCENE_ICON_FOR = iconFor;
window.SCENE_VIEW = { w: VIEW_W, h: VIEW_H };
