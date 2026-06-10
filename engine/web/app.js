// The viewer is a derived view of the graph and the statement store. It reads
// /api/graph per load and polls /api/version to stay live; its one write is
// /api/endorse, which is the operator acting (endorsement.md): the click
// takes a machine-owned statement on.

const state = {
  graph: null,
  cy: null,
  selected: null, // {type: "node"|"statement", id}
  version: null, // /api/version fingerprint the poll compares against
};

const THEME_KEY = "hypercore-theme";
const POLL_MS = 3000;

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
    derive: "#5d7480",
    generate: "#9aa0a6",
    test: "#7a4f9f",
    commit: "#2f7d6d",
    // pre-alphabet kinds, kept so folded history reads as the graph it was
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
    derive: "#8aa0ad",
    generate: "#aab0b6",
    test: "#a47fd0",
    commit: "#3fa08c",
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

// The segments in their canonical order (cli.py SEGMENTS); the payload sorts
// them alphabetically, which is not how the intent reads.
const SEGMENTS = ["foundations", "structure", "statements", "endorsement", "work"];

function segmentRank(segment) {
  const index = SEGMENTS.indexOf(segment);
  return index === -1 ? SEGMENTS.length : index;
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
  renderSummary();
  renderIntent();
  buildGraph();
  wireToolbar();
  restoreSelection();
  startPolling();
}

async function reload() {
  // The store changed (an endorsement here, or a verb elsewhere noticed by
  // the poll); re-derive the whole view but keep the operator's place:
  // selection and viewport survive the rebuild.
  const response = await fetch("/api/graph");
  const graph = await response.json();
  if (graph.error) {
    renderError(graph.error);
    return;
  }
  state.graph = graph;
  renderSummary();
  renderIntent();
  rebuildGraph({ keepViewport: true });
  restoreSelection();
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
}

/* ---------- left: intent panel ---------- */

function renderIntent() {
  const panel = document.getElementById("intent");
  panel.innerHTML = "";

  const pending = statements().filter((s) => s.owner === "machine");
  panel.appendChild(heading(`pending endorsement (${pending.length})`));
  if (pending.length === 0) {
    panel.appendChild(mutedLine("nothing awaits the operator"));
  }
  for (const s of pending) {
    panel.appendChild(statementRow(s, { endorsable: true }));
  }

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

/* ---------- endorsement: the operator's click ---------- */

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
    const response = await fetch("/api/endorse", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ids: [sid] }),
    });
    const result = await response.json();
    if (result.error) {
      renderError(result.error);
      return;
    }
    await reload();
  });
  return button;
}

/* ---------- center: the graph ---------- */

function buildGraph() {
  const graph = state.graph;
  const root = graph.nodes.find((n) => (n.props || {}).role === "root");
  const ids = new Set(graph.nodes.map((n) => n.id));
  state.cy = cytoscape({
    container: document.getElementById("cy"),
    wheelSensitivity: 0.2,
    elements: [
      ...graph.nodes.map((node) => ({
        data: {
          id: node.id,
          label: clip(node.label, 42),
          kind: node.kind,
          // Membership becomes nesting: an operation sits inside the work
          // that contains it, so the execution graph reads as a folder and
          // only the combinators are drawn as edges.
          parent:
            (node.props || {}).work && ids.has(node.props.work)
              ? node.props.work
              : undefined,
          // Lifted out of props so style selectors can reach them: ownership
          // and the state of work are what the operator reads at a glance.
          owner: (node.props || {}).owner || "",
          status: (node.props || {}).status || "",
          props: node.props,
        },
      })),
      ...graph.relations
        .filter((relation) => relation.type !== MEMBERSHIP)
        .map((relation) => ({
          data: {
            id: relation.id,
            source: relation.src,
            target: relation.dst,
            label: relation.type,
            type: relation.type,
            props: relation.props,
          },
        })),
    ],
    style: [
      {
        selector: "node",
        style: {
          "background-color": (el) => kindColor(el.data("kind")),
          label: "data(label)",
          color: cssVar("--graph-label"),
          "font-size": 11.5,
          "text-wrap": "wrap",
          "text-max-width": 150,
          "text-valign": "bottom",
          "text-halign": "center",
          "text-margin-y": 7,
          // A halo of the background keeps labels readable where they
          // cross edges or each other.
          "text-outline-color": cssVar("--bg"),
          "text-outline-width": 2,
          "text-outline-opacity": 0.85,
          "border-width": 2,
          "border-color": cssVar("--graph-node-border"),
          width: 28,
          height: 28,
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
          "background-color": cssVar("--machine-accent"),
          "border-color": cssVar("--machine-border"),
          "border-style": "dashed",
        },
      },
      {
        // a work with members renders as the box around them; the diamond
        // only shows while it has none
        selector: 'node[kind = "work"]',
        style: { shape: "diamond", width: 40, height: 40 },
      },
      {
        selector: ":parent",
        style: {
          shape: "round-rectangle",
          "background-color": cssVar("--graph-parent-bg"),
          "background-opacity": 0.6,
          "border-width": 2,
          "border-color": cssVar("--graph-parent-border"),
          label: "data(label)",
          "text-valign": "top",
          "text-halign": "center",
          "text-margin-y": -6,
          "font-size": 13,
          "font-weight": 700,
          padding: 18,
        },
      },
      {
        selector: 'node[kind = "frame"]',
        style: { shape: "round-rectangle", width: 40, height: 40 },
      },
      {
        selector: 'node[kind = "work"][status = "open"]',
        style: { "border-width": 4, "border-color": cssVar("--open-strong") },
      },
      {
        selector: 'node[kind = "work"][status = "folded"]',
        style: { opacity: 0.55 },
      },
      {
        selector: 'node[kind = "work"][status = "abandoned"]',
        style: { opacity: 0.35 },
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
      positions: presetPositions(graph),
      fit: true,
      padding: 30,
      animate: false,
    },
  });

  state.cy.on("tap", "node", (event) => {
    selectNode(event.target.id(), { fromGraph: true });
  });
}

// Lay the graph out by hand: the founding frame on top, each work a box of
// its operations below, members in alphabet-then-id order inside a grid.
function presetPositions(graph) {
  const ALPHABET_ORDER = [
    "frame",
    "gather",
    "derive",
    "generate",
    "test",
    "commit",
  ];
  const CELL_W = 200;
  const CELL_H = 110;
  const GAP = 110;
  const TOP = 140;

  const positions = {};
  const works = graph.nodes
    .filter((n) => n.kind === "work")
    .sort((a, b) => {
      const open = (w) => ((w.props || {}).status === "open" ? 0 : 1);
      return open(a) - open(b) || a.id.localeCompare(b.id);
    });
  const byWork = new Map(works.map((w) => [w.id, []]));
  for (const node of graph.nodes) {
    const wid = (node.props || {}).work;
    if (wid && byWork.has(wid)) byWork.get(wid).push(node);
  }

  let x = 0;
  for (const work of works) {
    const members = byWork
      .get(work.id)
      .sort(
        (a, b) =>
          ALPHABET_ORDER.indexOf(a.kind) - ALPHABET_ORDER.indexOf(b.kind) ||
          a.id.localeCompare(b.id),
      );
    if (members.length === 0) {
      positions[work.id] = { x, y: TOP };
      x += CELL_W + GAP;
      continue;
    }
    const cols = Math.max(1, Math.round(Math.sqrt(members.length)));
    members.forEach((member, index) => {
      positions[member.id] = {
        x: x + (index % cols) * CELL_W,
        y: TOP + Math.floor(index / cols) * CELL_H,
      };
    });
    x += cols * CELL_W + GAP;
  }

  const width = Math.max(x - GAP, CELL_W);
  const root = graph.nodes.find((n) => (n.props || {}).role === "root");
  if (root) {
    positions[root.id] = { x: width / 2 - CELL_W / 2, y: -60 };
  }
  let spare = 0;
  for (const node of graph.nodes) {
    if (!positions[node.id] && node.kind !== "work") {
      positions[node.id] = { x: spare++ * CELL_W, y: -220 };
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
  title.textContent = "Something went wrong";
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
