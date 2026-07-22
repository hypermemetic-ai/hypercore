// qq-trace-context — one root trace context per accountable Pi session (T-141).
//
// pi-subagents passes process.env through bin/qq-dispatch at dispatch time. A
// project-local extension can therefore establish the accountable session's
// trace and root span before its first dispatch. With no pre-set span context,
// every top-level dispatch becomes a direct child of that session root.
//
// Explicitly-set values always win. A foreign pre-set parent without a trace ID
// becomes a cross-trace reference when the trace ID is minted, matching
// qq-dispatch's fallback for that explicit input. Nested delegate sessions
// inherit all three variables, so the extension is a no-op there and does not
// emit a duplicate session-root marker.
import { spawnSync } from "node:child_process";
import { randomBytes } from "node:crypto";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

// This file lives at <repo>/.pi/extensions/qq-trace-context.ts; the repo root
// is two levels up. In a worktree, observation therefore uses that checkout's
// bin/qq-observe while the span store remains outside every Git worktree.
const REPO_ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..", "..");
let initialized = false;

function initializeTraceContext(): void {
	if (initialized) return;
	initialized = true;

	const needsTraceId = process.env.QQ_TRACE_ID === undefined;
	const needsRootSpanId = process.env.PI_ROOT_SPAN_ID === undefined;
	const needsParentSpanId = process.env.PI_PARENT_SPAN_ID === undefined;
	if (!needsTraceId && !needsRootSpanId && !needsParentSpanId) return;

	const anchor =
		process.env.PI_PARENT_SPAN_ID ?? process.env.PI_ROOT_SPAN_ID ?? null;
	const markerSpanId = randomBytes(8).toString("hex");
	if (needsTraceId) {
		process.env.QQ_TRACE_ID = randomBytes(16).toString("hex");
	}
	if (needsRootSpanId) {
		process.env.PI_ROOT_SPAN_ID = anchor ?? markerSpanId;
	}
	if (needsParentSpanId) {
		process.env.PI_PARENT_SPAN_ID = markerSpanId;
	}

	const traceId = process.env.QQ_TRACE_ID!;
	const rootSpanId = process.env.PI_ROOT_SPAN_ID!;
	console.error(
		`[qq-trace-context] trace_id=${traceId} root_span_id=${rootSpanId}`,
	);

	// Supply marker context only through arguments, never qq-observe's inherited
	// fallbacks. The fresh marker ID cannot collide with inherited span context.
	const observationEnv = { ...process.env };
	delete observationEnv.QQ_TRACE_ID;
	delete observationEnv.PI_ROOT_SPAN_ID;
	delete observationEnv.PI_PARENT_SPAN_ID;
	const now = new Date().toISOString();
	const result = spawnSync(
		join(REPO_ROOT, "bin/qq-observe"),
		[
			"record",
			"--name",
			"invoke_workflow",
			"--actor",
			"accountable-session",
			"--trace-id",
			traceId,
			"--span-id",
			markerSpanId,
			"--root-span-id",
			rootSpanId,
			...(anchor === null ? [] : ["--parent-span-id", anchor]),
			"--start",
			now,
			"--end",
			now,
			"--source",
			"qq-trace-context",
		],
		{ cwd: REPO_ROOT, env: observationEnv, stdio: "ignore" },
	);
	if (result.error || result.status !== 0) {
		console.error("[qq-trace-context] unable to record session-root span");
	}
}

export default function (_pi: ExtensionAPI) {
	initializeTraceContext();
}
