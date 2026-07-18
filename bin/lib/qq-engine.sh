#!/usr/bin/env bash
# Shared JSON result vocabulary for qq's stateless workflow engines.
# shellcheck disable=SC2016

qq_engine_init() {
  if [ "$#" -ne 2 ]; then
    printf '%s\n' '{"engine":"qq-engine","action":"init","status":"error","message":"internal engine initialization error","state":{}}'
    exit 1
  fi

  QQ_ENGINE_NAME="$1"
  QQ_ENGINE_ACTION="$2"
  if ! qq_resolve_bin jq; then
    printf '%s\n' '{"engine":"qq-engine","action":"init","status":"error","message":"jq is required to emit engine JSON","state":{}}'
    exit 1
  fi
  QQ_ENGINE_JQ="$QQ_BIN_RESULT"
}

qq_engine_set_action() {
  QQ_ENGINE_ACTION="$1"
}

qq_engine_finish() {
  local exit_code="$1"
  local status="$2"
  local message="$3"
  local state="${4-}"

  if [ -z "$state" ]; then
    state='{}'
  fi

  "$QQ_ENGINE_JQ" -cn \
    --arg engine "$QQ_ENGINE_NAME" \
    --arg action "$QQ_ENGINE_ACTION" \
    --arg status "$status" \
    --arg message "$message" \
    --argjson state "$state" \
    '{
      engine: $engine,
      action: $action,
      status: $status,
      message: $message,
      state: $state
    }'
  exit "$exit_code"
}

qq_engine_done() {
  local state="${2-}"
  qq_engine_finish 0 "done" "$1" "$state"
}

qq_engine_refuse() {
  local state="${2-}"
  qq_engine_finish 2 refused "$1" "$state"
}

qq_engine_error() {
  local state="${2-}"
  qq_engine_finish 1 error "$1" "$state"
}
