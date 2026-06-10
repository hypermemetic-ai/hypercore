// The viewer is a derived view of the graph and the statement store — and the
// operator's workbench (s_a6ea7c7a). It reads /api/graph per load and polls
// /api/version to stay live. Its writes are the operator acting, never the
// machine: /api/endorse takes a statement on, /api/verdict spends judgment on
// a test, /api/amend and /api/strike answer a statement, /api/fold confirms a
// settlement. Every write maps one-to-one onto a verb.

const state = {
  graph: null,
  cy: null,
  selected: null, // {type: "node"|"statement", id}
  version: null, // /api/version fingerprint the poll compares against
  expanded: loadExpanded(), // work ids whose operations are shown (less, not more)
  snapshot: null, // previous view of the store, diffed into the feed
  feed: [], // recent moves, newest first: {time, text, target}
};

const THEME_KEY = "hypercore-theme";
const EXPANDED_KEY = "hypercore-expanded";
const POLL_MS = 3000;
const FEED_LIMIT = 30;
const FEED_SHOWN = 12;

// One palette per theme: the dark canvas needs lighter inks for the same
// kinds, or the frame's navy vanishes into the background.
const KIND_COLORS = {
  light: {
    dataset: "#2f7d6d",
    process: "#7a4f9f",
    spec: "#c05a36",
    document: "#496cba",
    code: "#5d7480",
    node: "#1f2a44",
    segment: "#496cba",
    statement: "#6f767d",
    work: "#c05a36",
    // the operation alphabet (work: s_3729cb59)
    frame: "#1f2a44",
    gather: "#496cba",
    generate: "#9aa0a6",
    test: "#7a4f9f",
    commit: "#2f7d6d",
    // retired kinds, kept so folded history reads as the graph it was
    // (derive cut 2026-06-10, s_88dc042e; never used in any graph)
    derive: "#5d7480",
    step: "#9aa0a6",
    candidate: "#9aa0a6",
    check: "#7a4f9f",
    result: "#2f7d6d",
  },
  dark: {
    dataset: "#3fa08c",
    process: "#a47fd0",
    spec: "#d97a55",
    document: "#7d9be0",
    code: "#8aa0ad",
    node: "#8fa7d9",
    segment: "#7d9be0",
    statement: "#8d949b",
    work: "#d97a55",
    frame: "#8fa7d9",
    gather: "#7d9be0",
    generate: "#aab0b6",
    test: "#a47fd0",
    commit: "#3fa08c",
    derive: "#8aa0ad",
    step: "#aab0b6",
    candidate: "#aab0b6",
    check: "#a47fd0",
    result: "#3fa08c",
  },
};

function currentTheme() {
  return document.documentElement.dataset.theme === "light" ? "light" : "dark";
}

function kindColor(kind) {
  const palette = KIND_COLORS[currentTheme()];
  return palette[kind] || (currentTheme() === "dark" ? "#8d949b" : "#6f767d");
}

// The canvas follows the stylesheet: cytoscape colors come from the same
// CSS variables the panels use, read at build time.
function cssVar(name) {
  return getComputedStyle(document.documentElement)
    .getPropertyValue(name)
    .trim();
}

// Work membership; every other relation type is a combinator and keeps its
// label on the edge.
const MEMBERSHIP = "contains";

// The alphabet in its causal order: a work's operations lay out as rows in
// this order, so the story reads top-down — what was gathered, what was
// generated from it, what tested it, what settled it.
const ALPHABET_ORDER = [
  "frame",
  "gather",
  "generate",
  "test",
  "commit",
  // retired kinds (derive, cut 2026-06-10) and pre-alphabet kinds keep
  // their own rows below, so folded history reads
  "derive",
  "step",
  "candidate",
  "check",
  "result",
];

// The segments in their canonical order (cli.py SEGMENTS); the payload sorts
// them alphabetically, which is not how the intent reads.
const SEGMENTS = ["foundations", "structure", "statements", "endorsement", "work"];

function segmentRank(segment) {
  const index = SEGMENTS.indexOf(segment);
  return index === -1 ? SEGMENTS.length : index;
}

function loadExpanded() {
  try {
    return new Set(JSON.parse(localStorage.getItem(EXPANDED_KEY)) || []);
  } catch {
    return new Set();
  }
}

function persistExpanded() {
  localStorage.setItem(EXPANDED_KEY, JSON.stringify([...state.expanded]));
}

main();

async function main() {
  const [response, version] = await Promise.all([
    fetch("/api/graph"),
    fetchVersion(),
  ]);
  const graph = await response.json();
  if (graph.error) {
    renderError(graph.error);
    return;
  }
  state.graph = graph;
  state.version = version;
  state.snapshot = snapshotOf(graph);
  renderSummary();
  renderIntent();
  buildGraph();
  wireToolbar();
  restoreSelection();
  startPolling();
}

async function reload() {
  // The store changed (an action here, or a verb elsewhere noticed by the
  // poll); re-derive the whole view but keep the operator's place: selection
  // and viewport survive the rebuild. The diff against the previous view
  // becomes the feed — the loop is watched, not refreshed.
  const response = await fetch("/api/graph");
  const graph = await response.json();
  if (graph.error) {
    renderError(graph.error);
    return;
  }
  state.graph = graph;
  const next = snapshotOf(graph);
  const moves = diffMoves(state.snapshot, next);
  state.snapshot = next;
  state.feed = [...moves.entries, ...state.feed].slice(0, FEED_LIMIT);
  renderSummary();
  renderIntent();
  rebuildGraph({ keepViewport: true });
  restoreSelection();
  flash(moves.touched);
}

function rebuildGraph({ keepViewport } = {}) {
  const viewport =
    keepViewport && state.cy
      ? { zoom: state.cy.zoom(), pan: state.cy.pan() }
      : null;
  if (state.cy) state.cy.destroy();
  buildGraph();
  if (viewport) state.cy.viewport(viewport);
}

/* ---------- staying live: the version poll ---------- */

async function fetchVersion() {
  try {
    const response = await fetch("/api/version");
    const payload = await response.json();
    return payload.version || null;
  } catch {
    return null;
  }
}

function setLive(mode) {
  const live = document.getElementById("live");
  live.className = "live" + (mode === "live" ? "" : ` ${mode}`);
  live.textContent = { live: "live", syncing: "syncing", stale: "offline" }[
    mode
  ];
}

function startPolling() {
  const tick = async () => {
    if (document.hidden) return;
    const version = await fetchVersion();
    if (!version) {
      setLive("stale");
      return;
    }
    if (state.version !== null && version !== state.version) {
      state.version = version;
      setLive("syncing");
      await reload();
    } else {
      state.version = version;
    }
    setLive("live");
  };
  setInterval(tick, POLL_MS);
  // Coming back to the tab checks immediately instead of waiting a tick.
  document.addEventListener("visibilitychange", () => {
    if (!document.hidden) tick();
  });
}

/* ---------- the feed: the loop, watched ---------- */

// A flat, diffable picture of the store: enough to name what moved.
function snapshotOf(graph) {
  const stmts = new Map(
    (graph.statements || []).map((s) => [s.id, { owner: s.owner, text: s.text }]),
  );
  const nodes = new Map(
    graph.nodes.map((n) => {
      const props = n.props || {};
      return [
        n.id,
        {
          kind: n.kind,
          label: n.label,
          verdict: props.verdict || "",
          status: props.status || "",
          work: props.work || "",
        },
      ];
    }),
  );
  return { stmts, nodes };
}

function diffMoves(prev, next) {
  const entries = [];
  const touched = [];
  if (!prev) return { entries, touched };
  const time = new Date().toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });
  const move = (text, target) => entries.push({ time, text, target });

  for (const [id, node] of next.nodes) {
    const before = prev.nodes.get(id);
    const home = node.work && next.nodes.get(node.work);
    if (!before) {
      move(
        `${node.kind} arrived${home ? ` in “${clip(home.label, 34)}”` : ""}: ${clip(node.label, 60)}`,
        { type: "node", id },
      );
      touched.push(id);
      continue;
    }
    if (node.verdict !== before.verdict && node.verdict) {
      move(`test ${node.verdict}: ${clip(node.label, 60)}`, { type: "node", id });
      touched.push(id);
    }
    if (node.status !== before.status && node.kind === "work") {
      move(`work ${node.status}: ${clip(node.label, 60)}`, { type: "node", id });
      touched.push(id);
    }
  }
  for (const [id, node] of prev.nodes) {
    if (!next.nodes.has(id)) move(`${node.kind} left the graph: ${clip(node.label, 60)}`);
  }
  for (const [id, s] of next.stmts) {
    const before = prev.stmts.get(id);
    if (!before) {
      move(`new statement ${id} awaits endorsement: ${clip(s.text, 60)}`, {
        type: "statement",
        id,
      });
      continue;
    }
    if (before.owner === "machine" && s.owner === "operator") {
      move(`operator endorsed ${id}: ${clip(s.text, 60)}`, { type: "statement", id });
    }
    if (before.text !== s.text) {
      move(`statement amended ${id}: ${clip(s.text, 60)}`, { type: "statement", id });
    }
  }
  for (const [id, s] of prev.stmts) {
    if (!next.stmts.has(id)) move(`statement struck ${id}: ${clip(s.text, 60)}`);
  }
  return { entries, touched };
}

// A change that just landed glows for a few seconds, where it lives — or on
// the closed work box that holds it.
function flash(ids) {
  if (!state.cy) return;
  for (const id of ids) {
    const visible = visibleStandIn(id);
    if (!visible) continue;
    const el = state.cy.getElementById(visible);
    if (el.empty()) continue;
    el.addClass("arrived");
    setTimeout(() => {
      if (!state.cy) return;
      const later = state.cy.getElementById(visible);
      if (!later.empty()) later.removeClass("arrived");
    }, 6000);
  }
}

/* ---------- helpers over the payload ---------- */

function clip(text, width) {
  return text.length <= width ? text : text.slice(0, width - 1) + "…";
}

function statements() {
  return (state.graph.statements || [])
    .slice()
    .sort(
      (a, b) => segmentRank(a.segment) - segmentRank(b.segment) || a.ord - b.ord,
    );
}

function statementById(id) {
  return statements().find((s) => s.id === id) || null;
}

function nodeById(id) {
  return state.graph.nodes.find((n) => n.id === id) || null;
}

function works() {
  return state.graph.nodes.filter((n) => n.kind === "work");
}

function membersOf(workId) {
  return state.graph.nodes.filter((n) => (n.props || {}).work === workId);
}

// The reverse index a statement carries implicitly: the nodes bound by it
// (props.on) and the nodes that produced it (props.produces).
function statementReferences(sid) {
  const bound = [];
  const produced = [];
  for (const node of state.graph.nodes) {
    const props = node.props || {};
    if (props.on === sid) bound.push(node);
    if ((props.produces || []).includes(sid)) produced.push(node);
  }
  return { bound, produced };
}

// The blast radius of answering a statement, computed before the click —
// the consequence engine's client half (s_7c4763c0, s_070617cf). Mirrors
// Store.statement_consequences so card and verb tell the same story.
function statementConsequences(sid) {
  const { bound, produced } = statementReferences(sid);
  const anchorsOpen = bound.filter((n) => (n.props || {}).status !== "folded");
  const anchorsFolded = bound.filter(
    (n) => (n.props || {}).status === "folded",
  );
  const linkedBy = statements().filter((s) =>
    (s.links || []).some((link) => link.to === sid),
  );
  return { anchorsOpen, anchorsFolded, produced, linkedBy };
}

// Open tests whose judge is the operator: their verdicts are judgment the
// machine cannot spend (s_81c38173).
function operatorTestsOpen() {
  const openWorks = new Set(
    works()
      .filter((w) => (w.props || {}).status === "open")
      .map((w) => w.id),
  );
  return state.graph.nodes.filter((n) => {
    const props = n.props || {};
    return (
      n.kind === "test" &&
      (props.roles || {}).judge === "operator" &&
      !props.verdict &&
      openWorks.has(props.work)
    );
  });
}

// A work is ready for the operator's fold once a commit operation records the
// settlement; for machine-checked works every test must also pass.
function foldReadiness(work) {
  const props = work.props || {};
  if (props.status !== "open") return { ready: false, why: "not open" };
  const members = membersOf(work.id);
  const commits = members.filter((m) => m.kind === "commit");
  if (commits.length === 0) {
    return {
      ready: false,
      why: "no settlement yet: a commit operation must record the decision",
    };
  }
  const tests = members.filter((m) => m.kind === "test");
  const unpassed = tests.filter((t) => (t.props || {}).verdict !== "pass");
  if (props.check === "machine" && unpassed.length > 0) {
    return { ready: false, why: `${unpassed.length} test(s) without a pass verdict` };
  }
  return { ready: true, why: "" };
}

/* ---------- acting: every write is the operator ---------- */

async function act(path, payload) {
  const response = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  let result;
  try {
    result = await response.json();
  } catch {
    result = { error: `the server answered ${response.status}` };
  }
  if (result.error) {
    renderError(result.error);
    return null;
  }
  await reload();
  return result;
}

/* ---------- toolbar ---------- */

function renderSummary() {
  const pending = statements().filter((s) => s.owner === "machine").length;
  const open = works().filter((w) => (w.props || {}).status === "open").length;
  document.getElementById("summary").textContent =
    `${pending} pending endorsement · ${open} open work`;
}

function wireToolbar() {
  const toggle = document.getElementById("themeToggle");
  const face = () => {
    toggle.textContent = currentTheme() === "dark" ? "☀" : "☾";
    toggle.title = `Switch to ${currentTheme() === "dark" ? "light" : "dark"}`;
  };
  face();
  toggle.addEventListener("click", () => {
    const next = currentTheme() === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    localStorage.setItem(THEME_KEY, next);
    face();
    // The canvas colors were read at build time; rebuild it in place.
    rebuildGraph({ keepViewport: true });
    restoreSelection();
  });
  document.getElementById("zoomIn").addEventListener("click", () => {
    state.cy.zoom({
      level: state.cy.zoom() * 1.3,
      renderedPosition: { x: state.cy.width() / 2, y: state.cy.height() / 2 },
    });
  });
  document.getElementById("zoomOut").addEventListener("click", () => {
    state.cy.zoom({
      level: state.cy.zoom() / 1.3,
      renderedPosition: { x: state.cy.width() / 2, y: state.cy.height() / 2 },
    });
  });
  document.getElementById("zoomFit").addEventListener("click", () => {
    state.cy.fit(undefined, 40);
  });
  // Less, not more: one motion back to the overview of closed boxes.
  document.getElementById("collapseAll").addEventListener("click", () => {
    state.expanded.clear();
    persistExpanded();
    rebuildGraph();
    restoreSelection();
  });
}

/* ---------- left: the judgment queue, the feed, the intent ---------- */

function renderIntent() {
  const panel = document.getElementById("intent");
  panel.innerHTML = "";

  renderQueue(panel);
  renderFeed(panel);

  const open = works().filter((w) => (w.props || {}).status === "open");
  panel.appendChild(heading(`open work (${open.length})`));
  if (open.length === 0) {
    panel.appendChild(mutedLine("no open work"));
  }
  for (const w of open) {
    panel.appendChild(workRow(w));
  }

  panel.appendChild(heading("statements"));
  const segments = [...new Set(statements().map((s) => s.segment))];
  for (const segment of segments) {
    const group = statements().filter((s) => s.segment === segment);
    const machine = group.filter((s) => s.owner === "machine").length;
    const box = document.createElement("details");
    box.className = "segment";
    const summary = document.createElement("summary");
    summary.innerHTML =
      `${segment} <span class="muted">· ${group.length}` +
      (machine ? ` · ${machine} machine-owned` : "") +
      `</span>`;
    box.appendChild(summary);
    for (const s of group) {
      box.appendChild(statementRow(s, { endorsable: s.owner === "machine" }));
    }
    panel.appendChild(box);
  }

  const folded = works()
    .filter((w) => ["folded", "abandoned"].includes((w.props || {}).status))
    .sort((a, b) =>
      ((b.props || {}).folded_at || "").localeCompare(
        (a.props || {}).folded_at || "",
      ),
    );
  panel.appendChild(heading("recent folds"));
  if (folded.length === 0) {
    panel.appendChild(mutedLine("nothing folded yet"));
  }
  for (const w of folded.slice(0, 5)) {
    panel.appendChild(workRow(w));
  }
}

// Everything that awaits the operator, in one place: verdicts only they may
// give, folds only they may confirm, statements to endorse. The machine
// fills this queue; only the operator drains it.
function renderQueue(panel) {
  const pending = statements().filter((s) => s.owner === "machine");
  const tests = operatorTestsOpen();
  const foldable = works().filter((w) => foldReadiness(w).ready);
  const count = pending.length + tests.length + foldable.length;

  const box = document.createElement("div");
  box.className = "queue";
  box.appendChild(heading(`awaiting your judgment (${count})`));
  if (count === 0) {
    box.appendChild(mutedLine("nothing awaits the operator"));
    panel.appendChild(box);
    return;
  }

  for (const test of tests) {
    const home = nodeById((test.props || {}).work);
    const row = document.createElement("div");
    row.className = "row task";
    row.dataset.node = test.id;
    const meta = document.createElement("span");
    meta.className = "meta";
    meta.appendChild(badge("verdict", "open"));
    const where = document.createElement("span");
    where.className = "id";
    where.textContent = home ? clip(home.label, 38) : test.id;
    meta.appendChild(where);
    row.appendChild(meta);
    const text = document.createElement("div");
    text.className = "task-text link";
    text.textContent = clip(test.label, 110);
    text.addEventListener("click", () => selectNode(test.id));
    row.appendChild(text);
    row.appendChild(verdictControls(test));
    box.appendChild(row);
  }

  for (const work of foldable) {
    const row = document.createElement("div");
    row.className = "row task";
    row.dataset.node = work.id;
    const meta = document.createElement("span");
    meta.className = "meta";
    meta.appendChild(badge("fold", "folded"));
    const id = document.createElement("span");
    id.className = "id";
    id.textContent = work.id;
    meta.appendChild(id);
    row.appendChild(meta);
    const text = document.createElement("div");
    text.className = "task-text link";
    text.textContent = clip(work.label, 110);
    text.addEventListener("click", () => selectNode(work.id));
    row.appendChild(text);
    const actions = document.createElement("div");
    actions.className = "actions";
    actions.appendChild(foldButton(work));
    row.appendChild(actions);
    box.appendChild(row);
  }

  for (const s of pending) {
    box.appendChild(decisionCard(s));
  }
  panel.appendChild(box);
}

/* ---------- decision cards: context and consequences before the click ---------- */

// A pending statement as a decision card (s_7c4763c0): the question, why
// it is in front of the operator, what each answer entails — with the
// breakage computed and in view at the moment of deciding, not after it.
function decisionCard(statement) {
  const card = document.createElement("div");
  card.className = "row task card machine";
  card.dataset.statement = statement.id;

  const meta = document.createElement("span");
  meta.className = "meta";
  meta.appendChild(badge("ratify", "machine"));
  const id = document.createElement("span");
  id.className = "id";
  id.textContent = `${statement.id} · ${statement.segment}`;
  meta.appendChild(id);
  card.appendChild(meta);

  const text = document.createElement("div");
  text.className = "task-text link";
  text.textContent = clip(statement.text, 240);
  text.addEventListener("click", () => selectStatement(statement.id));
  card.appendChild(text);

  card.appendChild(whyLine(statement));
  card.appendChild(consequencesBlock(statement));

  const actions = document.createElement("div");
  actions.className = "actions";
  actions.appendChild(endorseButton(statement.id));
  card.appendChild(actions);
  actions.appendChild(statementActions(statement));
  return card;
}

// Why this decision is in front of the operator: its provenance.
function whyLine(statement) {
  const why = document.createElement("div");
  why.className = "why";
  const { produced } = statementReferences(statement.id);
  if (produced.length) {
    const work = produced[0];
    why.textContent = "drafted by the machine, produced by ";
    const link = document.createElement("span");
    link.className = "link";
    link.textContent = `${work.id} — ${clip(work.label, 60)}`;
    link.addEventListener("click", () => selectNode(work.id));
    why.appendChild(link);
  } else {
    why.textContent =
      "drafted by the machine, awaiting your answer: endorse, amend, or strike";
  }
  return why;
}

// What each answer entails — the card's consequence readout. Endorse and
// amend never break anything; strike's line is computed, never assumed.
function consequencesBlock(statement) {
  const list = document.createElement("ul");
  list.className = "consequences";

  const line = (verb, parts, warn) => {
    const li = document.createElement("li");
    if (warn) li.className = "warn";
    const v = document.createElement("span");
    v.className = "verb";
    v.textContent = verb;
    li.appendChild(v);
    for (const part of parts) {
      li.appendChild(
        typeof part === "string" ? document.createTextNode(part) : part,
      );
    }
    list.appendChild(li);
  };

  const idLink = (node) => {
    const span = document.createElement("span");
    span.className = "link";
    span.textContent = node.id;
    span.title = node.label || node.text || "";
    span.addEventListener("click", () =>
      node.kind ? selectNode(node.id) : selectStatement(node.id),
    );
    return span;
  };

  if (statement.owner === "machine") {
    line("endorse", ["the words become yours; nothing else moves"]);
    line("amend", ["your words replace the machine's; ownership follows"]);
  } else {
    line("amend", ["your words replace these"]);
  }

  const c = statementConsequences(statement.id);
  const broken = [];
  for (const n of c.anchorsOpen) {
    broken.push("open work loses its anchor: ", idLink(n), "  ");
  }
  for (const n of c.anchorsFolded.concat(c.produced)) {
    broken.push("a folded record points at nothing: ", idLink(n), "  ");
  }
  for (const s of c.linkedBy) {
    broken.push("loses its link target: ", idLink(s), "  ");
  }
  if (broken.length) {
    line("strike", ["⚠ ", ...broken], true);
  } else {
    line("strike", ["removes the words; nothing references them"]);
  }
  return list;
}

function renderFeed(panel) {
  panel.appendChild(heading("recent moves"));
  if (state.feed.length === 0) {
    panel.appendChild(mutedLine("the loop is quiet — moves land here live"));
    return;
  }
  const list = document.createElement("ul");
  list.className = "feed";
  for (const entry of state.feed.slice(0, FEED_SHOWN)) {
    const li = document.createElement("li");
    const time = document.createElement("span");
    time.className = "id";
    time.textContent = entry.time;
    li.appendChild(time);
    li.appendChild(document.createTextNode(" " + entry.text));
    if (entry.target) {
      li.className = "link";
      li.addEventListener("click", () =>
        entry.target.type === "statement"
          ? selectStatement(entry.target.id)
          : selectNode(entry.target.id),
      );
    }
    list.appendChild(li);
  }
  panel.appendChild(list);
}

function heading(text) {
  const h = document.createElement("h3");
  h.textContent = text;
  return h;
}

function mutedLine(text) {
  const p = document.createElement("p");
  p.className = "muted";
  p.textContent = text;
  return p;
}

function statementRow(statement, { endorsable } = {}) {
  const row = document.createElement("button");
  row.type = "button";
  row.className = "row" + (statement.owner === "machine" ? " machine" : "");
  row.dataset.statement = statement.id;

  const meta = document.createElement("span");
  meta.className = "meta";
  meta.appendChild(badge(statement.segment, "kind"));
  const id = document.createElement("span");
  id.className = "id";
  id.textContent = statement.id;
  meta.appendChild(id);
  if (statement.owner === "machine") {
    meta.appendChild(badge("machine", "machine"));
  }
  row.appendChild(meta);

  if (endorsable) {
    row.appendChild(endorseButton(statement.id));
  }
  row.appendChild(document.createTextNode(clip(statement.text, 110)));
  row.addEventListener("click", () => selectStatement(statement.id));
  return row;
}

function workRow(work) {
  const props = work.props || {};
  const row = document.createElement("button");
  row.type = "button";
  row.className = "row";
  row.dataset.node = work.id;

  const meta = document.createElement("span");
  meta.className = "meta";
  meta.appendChild(badge(props.status || "work", props.status || "kind"));
  const id = document.createElement("span");
  id.className = "id";
  id.textContent = work.id;
  meta.appendChild(id);
  row.appendChild(meta);

  row.appendChild(document.createTextNode(work.label));
  row.addEventListener("click", () => selectNode(work.id));
  return row;
}

function badge(text, flavor) {
  const span = document.createElement("span");
  span.className = `badge ${flavor}`;
  span.textContent = text;
  return span;
}

/* ---------- the operator's controls ---------- */

function endorseButton(sid) {
  const button = document.createElement("span");
  button.className = "endorse";
  button.textContent = "endorse";
  button.title = "Take this statement on as the operator";
  button.addEventListener("click", async (event) => {
    event.stopPropagation();
    // Judgment should not be spent by a stray click: ask once to confirm.
    if (!button.classList.contains("confirm")) {
      button.classList.add("confirm");
      button.textContent = "sure?";
      setTimeout(() => {
        button.classList.remove("confirm");
        button.textContent = "endorse";
      }, 2500);
      return;
    }
    button.textContent = "…";
    await act("/api/endorse", { ids: [sid] });
  });
  return button;
}

// Pass or fail, with grounds: the operator's verdict on a test. The buttons
// open a small inline form so the grounds travel with the judgment.
function verdictControls(test) {
  const wrap = document.createElement("div");
  wrap.className = "actions";
  const form = document.createElement("div");
  form.className = "inline-form";
  form.hidden = true;

  const open = (verdict) => {
    form.hidden = false;
    form.innerHTML = "";
    const input = document.createElement("input");
    input.className = "grounds";
    input.placeholder = "grounds — what this verdict rests on";
    const record = document.createElement("button");
    record.type = "button";
    record.className = `verdict ${verdict}`;
    record.textContent = `record ${verdict}`;
    record.addEventListener("click", async () => {
      record.textContent = "…";
      await act("/api/verdict", {
        id: test.id,
        verdict,
        grounds: input.value.trim(),
      });
    });
    const cancel = document.createElement("button");
    cancel.type = "button";
    cancel.className = "quiet";
    cancel.textContent = "cancel";
    cancel.addEventListener("click", () => {
      form.hidden = true;
    });
    form.append(input, record, cancel);
    input.focus();
  };

  const pass = document.createElement("button");
  pass.type = "button";
  pass.className = "verdict pass";
  pass.textContent = "✓ pass";
  pass.addEventListener("click", (event) => {
    event.stopPropagation();
    open("pass");
  });
  const fail = document.createElement("button");
  fail.type = "button";
  fail.className = "verdict fail";
  fail.textContent = "✕ fail";
  fail.addEventListener("click", (event) => {
    event.stopPropagation();
    open("fail");
  });
  wrap.append(pass, fail, form);
  return wrap;
}

function foldButton(work) {
  const button = document.createElement("button");
  button.type = "button";
  button.className = "verdict pass";
  button.textContent = "fold";
  button.title = "Confirm the fold: the settlement stands";
  button.addEventListener("click", async (event) => {
    event.stopPropagation();
    if (!button.classList.contains("confirm")) {
      button.classList.add("confirm");
      button.textContent = "sure?";
      setTimeout(() => {
        button.classList.remove("confirm");
        button.textContent = "fold";
      }, 2500);
      return;
    }
    button.textContent = "…";
    await act("/api/fold", { id: work.id });
  });
  return button;
}

/* ---------- center: the graph ---------- */

// A node draws as a card that carries its words: a head line naming the kind
// and its state, then the label itself. The border carries the kind's color;
// state overrides it where state matters more (verdicts, ownership, folds).
const CARD_W = 210;
const CARD_CHARS = 30; // ~chars per wrapped line at font 11 inside the card

function verdictGlyph(verdict) {
  return verdict === "pass" ? "✓" : verdict === "fail" ? "✕" : "○";
}

function nodeDisplay(node, { collapsed } = {}) {
  const props = node.props || {};
  if (node.kind === "work") {
    const status = props.status || "open";
    if (!collapsed) return `${node.label} — ${status}`;
    const members = membersOf(node.id);
    const tests = members.filter((m) => m.kind === "test");
    const tally = { pass: 0, fail: 0, open: 0 };
    for (const t of tests) {
      tally[(t.props || {}).verdict || "open"] += 1;
    }
    const counts =
      `${members.length} operation${members.length === 1 ? "" : "s"}` +
      (tests.length ? ` · ${tally.pass}✓ ${tally.fail}✕ ${tally.open}○` : "") +
      " · tap to open";
    return `work · ${status}\n${clip(node.label, 90)}\n${counts}`;
  }
  if (props.role === "root") {
    return `frame · root\n${clip(node.label, 90)}`;
  }
  let head = node.kind;
  if (node.kind === "test") {
    const verdict = props.verdict || "open";
    head += ` · ${verdictGlyph(props.verdict)} ${verdict}`;
    if (!props.verdict && (props.roles || {}).judge === "operator") {
      head += " · yours to judge";
    }
  }
  return `${head}\n${clip(node.label, 130)}`;
}

function cardHeight(display) {
  const lines = display
    .split("\n")
    .reduce((n, seg) => n + Math.max(1, Math.ceil(seg.length / CARD_CHARS)), 0);
  return lines * 15 + 22;
}

// Less, not more: a work's operations render only while the work is
// expanded. Everything inside a closed work stands in as the closed box.
function visibleStandIn(id) {
  const node = nodeById(id);
  if (!node) return null;
  const wid = (node.props || {}).work;
  if (!wid) return id;
  return state.expanded.has(wid) ? id : wid;
}

function buildGraph() {
  const graph = state.graph;
  const visible = graph.nodes.filter((n) => {
    const wid = (n.props || {}).work;
    return !wid || state.expanded.has(wid);
  });
  const visibleIds = new Set(visible.map((n) => n.id));

  const nodeElements = visible.map((node) => {
    const props = node.props || {};
    const collapsed = node.kind === "work" && !state.expanded.has(node.id);
    const display = nodeDisplay(node, { collapsed });
    return {
      data: {
        id: node.id,
        display,
        cardH: cardHeight(display),
        kind: node.kind,
        // Membership becomes nesting: an operation sits inside the work
        // that contains it, so the execution graph reads as a folder and
        // only the combinators are drawn as edges.
        parent:
          props.work && visibleIds.has(props.work) ? props.work : undefined,
        // Lifted out of props so style selectors can reach them: ownership,
        // verdicts, and the state of work are what the operator reads at a
        // glance.
        owner: props.owner || "",
        status: props.status || "",
        verdict: node.kind === "test" ? props.verdict || "open" : "",
        judge: (props.roles || {}).judge || "",
        props: node.props,
      },
    };
  });

  // An edge into a closed work lands on the closed box, so causality
  // between works stays visible while the detail stays put away.
  const seen = new Set();
  const edgeElements = [];
  for (const relation of graph.relations) {
    if (relation.type === MEMBERSHIP) continue;
    const src = visibleStandIn(relation.src);
    const dst = visibleStandIn(relation.dst);
    if (!src || !dst || src === dst) continue;
    if (!visibleIds.has(src) || !visibleIds.has(dst)) continue;
    const key = `${src}->${dst}:${relation.type}`;
    if (seen.has(key)) continue;
    seen.add(key);
    edgeElements.push({
      data: {
        id: relation.id,
        source: src,
        target: dst,
        label: relation.type,
        type: relation.type,
        props: relation.props,
      },
    });
  }

  state.cy = cytoscape({
    container: document.getElementById("cy"),
    wheelSensitivity: 0.2,
    elements: [...nodeElements, ...edgeElements],
    style: [
      {
        selector: "node",
        style: {
          shape: "round-rectangle",
          width: CARD_W,
          height: (el) => el.data("cardH"),
          "background-color": cssVar("--card-bg"),
          "border-width": 2,
          "border-color": (el) => kindColor(el.data("kind")),
          label: "data(display)",
          color: cssVar("--text"),
          "font-size": 11,
          "line-height": 1.35,
          "text-wrap": "wrap",
          "text-max-width": CARD_W - 18,
          "text-valign": "center",
          "text-halign": "center",
        },
      },
      {
        selector: "edge",
        style: {
          width: 2,
          "line-color": cssVar("--graph-edge"),
          "target-arrow-color": cssVar("--graph-edge"),
          "target-arrow-shape": "triangle",
          "arrow-scale": 0.9,
          "curve-style": "bezier",
          label: "data(label)",
          color: cssVar("--graph-edge-label"),
          "font-size": 10,
          "text-background-color": cssVar("--bg"),
          "text-background-opacity": 0.9,
          "text-background-padding": 2,
        },
      },
      {
        selector: 'node[owner = "machine"]',
        style: {
          "border-color": cssVar("--machine-accent"),
          "border-style": "dashed",
        },
      },
      {
        // the expanded work is the box around its operations
        selector: ":parent",
        style: {
          "background-color": cssVar("--graph-parent-bg"),
          "background-opacity": 0.6,
          "border-width": 2,
          "border-color": cssVar("--graph-parent-border"),
          "text-valign": "top",
          "text-halign": "center",
          "text-margin-y": -8,
          "font-size": 13,
          "font-weight": 700,
          padding: 20,
        },
      },
      // Verdicts are loud: green settles, red demands attention, amber waits.
      {
        selector: 'node[verdict = "pass"]',
        style: { "border-color": cssVar("--folded-border"), "border-width": 3 },
      },
      {
        selector: 'node[verdict = "fail"]',
        style: { "border-color": cssVar("--fail"), "border-width": 4 },
      },
      {
        selector: 'node[verdict = "open"]',
        style: {
          "border-color": cssVar("--machine-accent"),
          "border-style": "dashed",
        },
      },
      {
        selector: 'node[verdict = "open"][judge = "operator"]',
        style: { "border-width": 4, "border-style": "double" },
      },
      {
        selector: 'node[kind = "work"][status = "open"]',
        style: { "border-width": 3, "border-color": cssVar("--open-strong") },
      },
      {
        selector: 'node[kind = "work"][status = "folded"]',
        style: { "border-color": cssVar("--folded-border"), opacity: 0.7 },
      },
      {
        selector: 'node[kind = "work"][status = "abandoned"]',
        style: { opacity: 0.4 },
      },
      {
        selector: "node.arrived",
        style: {
          "overlay-color": cssVar("--accent"),
          "overlay-opacity": 0.18,
          "overlay-padding": 8,
        },
      },
      {
        selector: "node:selected",
        style: { "border-width": 4, "border-color": cssVar("--accent") },
      },
    ],
    layout: {
      // Deterministic: the same graph always lands in the same place, so
      // the operator keeps a stable mental map between visits.
      name: "preset",
      positions: presetPositions(graph, visibleIds),
      fit: true,
      padding: 30,
      animate: false,
    },
  });

  state.cy.on("tap", "node", (event) => {
    const id = event.target.id();
    const node = nodeById(id);
    if (node && node.kind === "work") {
      // The first tap opens (and selects) the box; a tap on the already-
      // selected work closes it again. Detail on demand, in both directions.
      if (!state.expanded.has(id)) {
        state.expanded.add(id);
        persistExpanded();
        rebuildGraph({ keepViewport: true });
      } else if (state.selected && state.selected.id === id) {
        state.expanded.delete(id);
        persistExpanded();
        rebuildGraph({ keepViewport: true });
      }
    }
    selectNode(id, { fromGraph: true });
  });
}

// Lay the graph out by hand: the founding frame on top, each work below —
// a closed card while collapsed, a box of rows while expanded. Rows follow
// the alphabet's causal order, so the story reads top-down: what was
// gathered, what was generated, what tested it, what settled it.
function presetPositions(graph, visibleIds) {
  const CELL_W = CARD_W + 40;
  const ROW_H = 150;
  const GAP = 130;
  const TOP = 200;

  const positions = {};
  const workNodes = graph.nodes
    .filter((n) => n.kind === "work")
    .sort((a, b) => {
      const open = (w) => ((w.props || {}).status === "open" ? 0 : 1);
      return open(a) - open(b) || a.id.localeCompare(b.id);
    });

  let x = 0;
  for (const work of workNodes) {
    if (!state.expanded.has(work.id)) {
      positions[work.id] = { x, y: TOP };
      x += CELL_W + GAP;
      continue;
    }
    const members = membersOf(work.id).sort(
      (a, b) =>
        ALPHABET_ORDER.indexOf(a.kind) - ALPHABET_ORDER.indexOf(b.kind) ||
        a.id.localeCompare(b.id),
    );
    if (members.length === 0) {
      positions[work.id] = { x, y: TOP };
      x += CELL_W + GAP;
      continue;
    }
    const kindsPresent = [...new Set(members.map((m) => m.kind))].sort(
      (a, b) => ALPHABET_ORDER.indexOf(a) - ALPHABET_ORDER.indexOf(b),
    );
    let widest = 1;
    kindsPresent.forEach((kind, rowIndex) => {
      const row = members.filter((m) => m.kind === kind);
      widest = Math.max(widest, row.length);
      row.forEach((member, col) => {
        positions[member.id] = {
          x: x + col * CELL_W,
          y: TOP + rowIndex * ROW_H,
        };
      });
    });
    x += widest * CELL_W + GAP;
  }

  const width = Math.max(x - GAP, CELL_W);
  const root = graph.nodes.find((n) => (n.props || {}).role === "root");
  if (root) {
    positions[root.id] = { x: width / 2 - CELL_W / 2, y: -80 };
  }
  let spare = 0;
  for (const node of graph.nodes) {
    if (!visibleIds.has(node.id)) continue;
    if (!positions[node.id] && node.kind !== "work") {
      positions[node.id] = { x: spare++ * CELL_W, y: -260 };
    }
  }
  return positions;
}

/* ---------- selection and the right panel ---------- */

function markSelectedRow() {
  for (const row of document.querySelectorAll(".row.selected")) {
    row.classList.remove("selected");
  }
  if (!state.selected) return;
  const key = state.selected.type === "statement" ? "statement" : "node";
  for (const row of document.querySelectorAll(
    `.row[data-${key}="${state.selected.id}"]`,
  )) {
    row.classList.add("selected");
  }
}

function restoreSelection() {
  if (!state.selected) return;
  if (state.selected.type === "statement") {
    const statement = statementById(state.selected.id);
    if (statement) selectStatement(statement.id);
    else {
      state.selected = null;
      markSelectedRow();
    }
    return;
  }
  // quiet: re-select without re-centering, so a live reload does not yank
  // the viewport back to the selection.
  if (nodeById(state.selected.id)) selectNode(state.selected.id, { quiet: true });
}

function selectStatement(sid) {
  const statement = statementById(sid);
  if (!statement) return;
  state.selected = { type: "statement", id: sid };
  markSelectedRow();
  state.cy.$(":selected").unselect();
  renderStatementDetails(statement);
}

function selectNode(id, { fromGraph, quiet } = {}) {
  const node = nodeById(id);
  if (!node) return;
  // Focus opens the box: selecting an operation expands the work around it —
  // but a quiet restore after a rebuild must not reopen what was just closed.
  const wid = (node.props || {}).work;
  if (wid && !state.expanded.has(wid) && !quiet) {
    state.expanded.add(wid);
    persistExpanded();
    rebuildGraph({ keepViewport: true });
  }
  state.selected = { type: "node", id };
  markSelectedRow();
  if (!fromGraph) {
    state.cy.$(":selected").unselect();
    const target = state.cy.getElementById(id);
    if (!target.empty()) {
      target.select();
      if (!quiet) {
        state.cy.animate({ center: { eles: target } }, { duration: 250 });
      }
    }
  }
  renderNodeDetails(node);
}

function renderStatementDetails(statement) {
  const details = document.getElementById("details");
  details.innerHTML = "";

  details.appendChild(titleEl(statement.text));
  const meta = document.createElement("p");
  meta.className = "muted";
  meta.textContent = `${statement.id} · ${statement.segment} · ord ${statement.ord}`;
  details.appendChild(meta);

  const owner = document.createElement("p");
  owner.className = "muted";
  if (statement.owner === "machine") {
    owner.append(badge("machine", "machine"), " pending endorsement ");
    owner.appendChild(endorseButton(statement.id));
  } else {
    owner.textContent = "operator-owned";
  }
  details.appendChild(owner);

  // What each answer entails, computed — the same readout the card shows.
  details.appendChild(consequencesBlock(statement));

  // The operator's other two answers (endorsement.md): amend and strike.
  details.appendChild(statementActions(statement));

  const links = statement.links || [];
  if (links.length) {
    const linkSection = section("Links");
    const list = document.createElement("ul");
    for (const link of links) {
      const other = statementById(link.to);
      const li = document.createElement("li");
      li.className = "link";
      li.textContent = `${link.type} → ${link.to}` +
        (other ? ` · ${clip(other.text, 70)}` : "");
      if (other) li.addEventListener("click", () => selectStatement(other.id));
      list.appendChild(li);
    }
    linkSection.appendChild(list);
    details.appendChild(linkSection);
  }

  const { bound, produced } = statementReferences(statement.id);
  appendNodeList(details, "Bound by it", bound);
  appendNodeList(details, "Produced by", produced);
}

function statementActions(statement) {
  const wrap = document.createElement("div");
  wrap.className = "actions";

  const amend = document.createElement("button");
  amend.type = "button";
  amend.className = "quiet";
  amend.textContent = "amend";
  amend.title = "Rewrite this statement in your words";
  const strike = document.createElement("button");
  strike.type = "button";
  strike.className = "quiet danger";
  strike.textContent = "strike";
  strike.title = "Remove this statement";

  const form = document.createElement("div");
  form.className = "inline-form column";
  form.hidden = true;

  // Grounds ride with every answer (s_565ca729): a strike that means
  // "I disagree" and one that means "I don't understand" should be
  // tellable apart in the record.
  const groundsInput = (placeholder) => {
    const input = document.createElement("input");
    input.type = "text";
    input.className = "grounds";
    input.placeholder = placeholder;
    return input;
  };

  amend.addEventListener("click", (event) => {
    event.stopPropagation();
    form.hidden = false;
    form.innerHTML = "";
    const input = document.createElement("textarea");
    input.className = "grounds";
    input.value = statement.text;
    const because = groundsInput("because — recorded with the decision");
    const save = document.createElement("button");
    save.type = "button";
    save.className = "verdict pass";
    save.textContent = "save amendment";
    save.addEventListener("click", async () => {
      const text = input.value.trim();
      if (!text) return;
      save.textContent = "…";
      const result = await act("/api/amend", {
        id: statement.id,
        text,
        grounds: because.value.trim(),
      });
      if (result) selectStatement(statement.id);
    });
    const cancel = document.createElement("button");
    cancel.type = "button";
    cancel.className = "quiet";
    cancel.textContent = "cancel";
    cancel.addEventListener("click", () => {
      form.hidden = true;
    });
    const buttons = document.createElement("div");
    buttons.className = "inline-form";
    buttons.append(save, cancel);
    form.append(input, because, buttons);
    input.focus();
  });

  strike.addEventListener("click", (event) => {
    // Striking opens the decision, never lands it: the breakage and a
    // grounds field come first (s_070617cf), the red button second.
    event.stopPropagation();
    form.hidden = false;
    form.innerHTML = "";
    form.appendChild(consequencesBlock(statement));
    const because = groundsInput(
      "because — disagreement and confusion read differently later",
    );
    const confirm = document.createElement("button");
    confirm.type = "button";
    confirm.className = "quiet danger confirm";
    confirm.textContent = "strike it";
    confirm.addEventListener("click", async () => {
      confirm.textContent = "…";
      const result = await act("/api/strike", {
        id: statement.id,
        grounds: because.value.trim(),
      });
      if (result) {
        state.selected = null;
        markSelectedRow();
        const details = document.getElementById("details");
        details.innerHTML = "";
        details.appendChild(titleEl("Statement struck"));
        details.appendChild(
          mutedLine(`${statement.id} removed: ${clip(statement.text, 90)}`),
        );
      }
    });
    const cancel = document.createElement("button");
    cancel.type = "button";
    cancel.className = "quiet";
    cancel.textContent = "keep it";
    cancel.addEventListener("click", () => {
      form.hidden = true;
    });
    const buttons = document.createElement("div");
    buttons.className = "inline-form";
    buttons.append(because, confirm, cancel);
    form.appendChild(buttons);
    because.focus();
  });

  wrap.append(amend, strike, form);
  return wrap;
}

function appendNodeList(details, title, nodes) {
  const wrap = section(title);
  if (nodes.length === 0) {
    wrap.appendChild(mutedLine("(none)"));
  } else {
    const list = document.createElement("ul");
    for (const node of nodes) {
      const li = document.createElement("li");
      li.className = "link";
      const status = (node.props || {}).status;
      li.textContent =
        `${node.kind}${status ? ` (${status})` : ""} · ${clip(node.label, 70)}`;
      li.addEventListener("click", () => selectNode(node.id));
      list.appendChild(li);
    }
    wrap.appendChild(list);
  }
  details.appendChild(wrap);
}

function renderNodeDetails(node) {
  const details = document.getElementById("details");
  details.innerHTML = "";

  details.appendChild(titleEl(node.label));
  const meta = document.createElement("p");
  meta.className = "muted";
  meta.textContent = `${node.kind} · ${node.id}`;
  details.appendChild(meta);

  const props = node.props || {};

  if (node.kind === "work") {
    const state_ = document.createElement("p");
    state_.className = "muted";
    state_.textContent =
      `${props.status} · check: ${props.check} · fold when: ${props.fold_when}`;
    details.appendChild(state_);
    const on = statementById(props.on);
    if (on) {
      const wrap = section("On (the statement that spawned it)");
      const row = statementRow(on, { endorsable: on.owner === "machine" });
      wrap.appendChild(row);
      details.appendChild(wrap);
    }
    if (props.status === "open") {
      const readiness = foldReadiness(node);
      const wrap = section("Folding");
      if (readiness.ready) {
        const line = document.createElement("p");
        line.className = "muted";
        line.append("the settlement is recorded — the fold is yours ");
        line.appendChild(foldButton(node));
        wrap.appendChild(line);
      } else {
        wrap.appendChild(mutedLine(readiness.why));
      }
      details.appendChild(wrap);
    }
  }

  // Who proposes / executes / judges / decides (s_81c38173).
  if (props.roles) {
    const roles = document.createElement("div");
    roles.className = "roles";
    for (const [role, who] of Object.entries(props.roles)) {
      roles.appendChild(
        badge(`${role}: ${who}`, who === "operator" ? "open" : "kind"),
      );
    }
    details.appendChild(roles);
  }

  if (node.kind === "test") {
    const verdict = document.createElement("p");
    verdict.className = "muted";
    verdict.textContent = props.verdict
      ? `verdict: ${props.verdict}` +
        (props.grounds ? ` — ${props.grounds}` : "")
      : "verdict: open";
    details.appendChild(verdict);
    // An open verdict that is the operator's to give is actionable here.
    if (!props.verdict && (props.roles || {}).judge === "operator") {
      details.appendChild(verdictControls(node));
    }
  }

  const extras = Object.fromEntries(
    Object.entries(props).filter(
      ([k]) => !["roles", "owner"].includes(k),
    ),
  );
  if (Object.keys(extras).length) {
    const propsSection = section("Props");
    const pre = document.createElement("pre");
    pre.textContent = JSON.stringify(extras, null, 2);
    propsSection.appendChild(pre);
    details.appendChild(propsSection);
  }

  const materialSection = section("Material");
  const material = state.graph.material[node.id] || [];
  if (material.length === 0) {
    materialSection.appendChild(mutedLine("No material attached."));
  } else {
    const list = document.createElement("ul");
    for (const item of material) {
      const row = document.createElement("li");
      const label = item.label || item.id;
      const path = item.path ? ` · ${item.path}` : "";
      row.textContent = `${label} · ${item.kind}${path}`;
      if (item.has_body) {
        row.className = "link";
        row.title = "Show the body";
        row.addEventListener("click", async () => {
          const response = await fetch(`/api/material/${item.id}`);
          const payload = await response.json();
          const pre = document.createElement("pre");
          pre.textContent = payload.error || payload.body;
          row.replaceWith(pre);
        });
      }
      list.appendChild(row);
    }
    materialSection.appendChild(list);
  }
  details.appendChild(materialSection);
}

function titleEl(text) {
  const title = document.createElement("h2");
  title.textContent = text;
  return title;
}

function renderError(message) {
  const details = document.getElementById("details");
  details.innerHTML = "";
  const title = document.createElement("h2");
  title.textContent = "The verb refused";
  const body = document.createElement("pre");
  body.textContent = message;
  details.appendChild(title);
  details.appendChild(body);
}

function section(titleText) {
  const wrapper = document.createElement("div");
  wrapper.className = "section";
  const title = document.createElement("h3");
  title.textContent = titleText;
  wrapper.appendChild(title);
  return wrapper;
}
