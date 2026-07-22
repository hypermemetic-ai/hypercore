#!/usr/bin/env bash
set -euo pipefail

TESTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
# shellcheck disable=SC2034
TEST_NAME="test-qq-trace-context-extension"
# shellcheck source=tests/helpers.sh
# shellcheck disable=SC1091
source "$TESTS_DIR/helpers.sh"
ROOT="$(cd "$TESTS_DIR/.." && pwd -P)"
EXT="$ROOT/.pi/extensions/qq-trace-context.ts"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

[ -f "$EXT" ] || fail "missing extension: $EXT"

# Structural guards: root resolution, absent-only context, required ID shapes,
# explicit marker context, scrubbed observation env, and non-fatal observation.
assert_file_contains "$EXT" 'fileURLToPath(import.meta.url)'
assert_file_contains "$EXT" 'process.env.QQ_TRACE_ID === undefined'
assert_file_contains "$EXT" 'process.env.PI_ROOT_SPAN_ID === undefined'
assert_file_contains "$EXT" 'process.env.PI_PARENT_SPAN_ID === undefined'
assert_file_contains "$EXT" 'randomBytes(16).toString("hex")'
assert_file_contains "$EXT" 'randomBytes(8).toString("hex")'
assert_file_contains "$EXT" 'delete observationEnv.QQ_TRACE_ID'
assert_file_contains "$EXT" 'delete observationEnv.PI_ROOT_SPAN_ID'
assert_file_contains "$EXT" 'delete observationEnv.PI_PARENT_SPAN_ID'
assert_file_contains "$EXT" '"--trace-id"'
assert_file_contains "$EXT" '"--span-id"'
assert_file_contains "$EXT" '"--root-span-id"'
assert_file_contains "$EXT" '"--parent-span-id"'
assert_file_contains "$EXT" '"bin/qq-observe"'
assert_file_contains "$EXT" '"invoke_workflow"'
assert_file_contains "$EXT" '"accountable-session"'
assert_file_contains "$EXT" '"qq-trace-context"'
assert_file_contains "$EXT" '[qq-trace-context] trace_id='
assert_file_contains "$EXT" 'unable to record session-root span'

# Functional: exercise absent, partial, and complete pre-set context under
# isolated state. Every initializing import gets one marker even when called
# twice; complete inherited context gets none.
export HOME="$tmp/home"
export XDG_STATE_HOME="$tmp/state"
mkdir -p "$HOME"
git_common_dir="$(git -C "$ROOT" rev-parse --path-format=absolute --git-common-dir)"
repository_name="$(basename "$(dirname "$(realpath -e "$git_common_dir")")")"
store="$XDG_STATE_HOME/qq/spans/$repository_name/spans.jsonl"

EXT="$EXT" STORE="$store" LAYOUT="$tmp/missing-observer" \
  node --experimental-strip-types --input-type=module - <<'JS'
import { pathToFileURL } from "node:url";
import fs from "node:fs";
import path from "node:path";

const ext = process.env.EXT;
const store = process.env.STORE;
const layout = process.env.LAYOUT;
const pi = { on() {} };
const contextKeys = ["QQ_TRACE_ID", "PI_ROOT_SPAN_ID", "PI_PARENT_SPAN_ID"];
const markerValue = Symbol("marker span ID");
const die = (message) => { console.error(message); process.exit(1); };
const assertEq = (actual, expected, label) => {
  if (actual !== expected) die(`${label}: expected ${expected}, got ${actual}`);
};
const captureNotes = async (load) => {
  const notes = [];
  const original = console.error;
  console.error = (...args) => notes.push(args.join(" "));
  try {
    await load();
  } finally {
    console.error = original;
  }
  return notes;
};
const readRecords = () => {
  if (!fs.existsSync(store)) return [];
  const contents = fs.readFileSync(store, "utf8").trim();
  return contents ? contents.split("\n").map(JSON.parse) : [];
};
const expectedValue = (value, marker) => value === markerValue ? marker.span_id : value;

const runCase = async ({ name, preset, envRoot, envParent, markerRoot, markerParent, emits = true }) => {
  for (const key of contextKeys) delete process.env[key];
  Object.assign(process.env, preset);
  const beforeCount = readRecords().length;
  const notes = await captureNotes(async () => {
    const mod = await import(`${pathToFileURL(ext).href}?${name}`);
    mod.default(pi);
    mod.default(pi);
  });

  for (const [key, value] of Object.entries(preset)) {
    assertEq(process.env[key], value, `${name} preserves ${key}`);
  }
  if (!emits) {
    assertEq(notes.length, 0, `${name} note count`);
    assertEq(readRecords().length, beforeCount, `${name} marker count`);
    return;
  }

  if (!/^[0-9a-f]{32}$/.test(process.env.QQ_TRACE_ID ?? "")) die(`${name} trace ID has the wrong shape`);
  const records = readRecords();
  assertEq(records.length, beforeCount + 1, `${name} marker count`);
  const marker = records.at(-1);
  if (!/^[0-9a-f]{16}$/.test(marker.span_id)) die(`${name} marker span ID has the wrong shape`);
  if (Object.values(preset).includes(marker.span_id)) die(`${name} reused a pre-set ID for its marker`);
  assertEq(process.env.PI_ROOT_SPAN_ID, expectedValue(envRoot, marker), `${name} env root`);
  assertEq(process.env.PI_PARENT_SPAN_ID, expectedValue(envParent, marker), `${name} env parent`);
  assertEq(notes.length, 1, `${name} note count`);
  assertEq(
    notes[0],
    `[qq-trace-context] trace_id=${process.env.QQ_TRACE_ID} root_span_id=${expectedValue(markerRoot, marker)}`,
    `${name} note`,
  );
  assertEq(marker.trace_id, process.env.QQ_TRACE_ID, `${name} marker trace ID`);
  assertEq(marker.root_span_id, expectedValue(markerRoot, marker), `${name} marker root span ID`);
  assertEq(marker.parent_span_id, expectedValue(markerParent, marker), `${name} marker parent span ID`);
  assertEq(marker.name, "invoke_workflow", `${name} marker name`);
  assertEq(marker.actor, "accountable-session", `${name} marker actor`);
  assertEq(marker.source, "qq-trace-context", `${name} marker source`);
  assertEq(marker.phase, null, `${name} marker phase`);
  assertEq(marker.duration_ms, 0, `${name} marker duration`);
  assertEq(marker.start_time, marker.end_time, `${name} marker timestamps`);
};

await runCase({
  name: "none-set",
  preset: {},
  envRoot: markerValue,
  envParent: markerValue,
  markerRoot: markerValue,
  markerParent: null,
});
await runCase({
  name: "parent-only",
  preset: { PI_PARENT_SPAN_ID: "aaaaaaaaaaaaaaaa" },
  envRoot: "aaaaaaaaaaaaaaaa",
  envParent: "aaaaaaaaaaaaaaaa",
  markerRoot: "aaaaaaaaaaaaaaaa",
  markerParent: "aaaaaaaaaaaaaaaa",
});
await runCase({
  name: "root-only",
  preset: { PI_ROOT_SPAN_ID: "bbbbbbbbbbbbbbbb" },
  envRoot: "bbbbbbbbbbbbbbbb",
  envParent: markerValue,
  markerRoot: "bbbbbbbbbbbbbbbb",
  markerParent: "bbbbbbbbbbbbbbbb",
});
await runCase({
  name: "parent-and-root",
  preset: {
    PI_PARENT_SPAN_ID: "cccccccccccccccc",
    PI_ROOT_SPAN_ID: "dddddddddddddddd",
  },
  envRoot: "dddddddddddddddd",
  envParent: "cccccccccccccccc",
  markerRoot: "dddddddddddddddd",
  markerParent: "cccccccccccccccc",
});
await runCase({
  name: "all-set",
  preset: {
    QQ_TRACE_ID: "11111111111111111111111111111111",
    PI_ROOT_SPAN_ID: "2222222222222222",
    PI_PARENT_SPAN_ID: "3333333333333333",
  },
  emits: false,
});
assertEq(readRecords().length, 4, "context matrix marker count");

const copiedExtension = path.join(layout, ".pi/extensions/qq-trace-context.ts");
fs.mkdirSync(path.dirname(copiedExtension), { recursive: true });
fs.copyFileSync(ext, copiedExtension);
for (const key of contextKeys) delete process.env[key];
const missingNotes = await captureNotes(async () => {
  const mod = await import(pathToFileURL(copiedExtension).href);
  mod.default(pi);
});
if (!/^[0-9a-f]{32}$/.test(process.env.QQ_TRACE_ID ?? "")) die("missing-observer trace ID has the wrong shape");
if (!/^[0-9a-f]{16}$/.test(process.env.PI_ROOT_SPAN_ID ?? "")) die("missing-observer root ID has the wrong shape");
assertEq(process.env.PI_PARENT_SPAN_ID, process.env.PI_ROOT_SPAN_ID, "missing-observer dispatch parent");
if (!missingNotes.some((note) => note.includes("unable to record session-root span"))) {
  die("missing observer did not produce a stderr note");
}
JS

assert_file_contains "$ROOT/README.md" '.pi/extensions/qq-trace-context.ts'
assert_file_contains "$ROOT/README.md" 'qq-observe read-session <session.jsonl> --trace-id <trace> --parent-span-id <root>'

printf 'test-qq-trace-context-extension: pass\n'
