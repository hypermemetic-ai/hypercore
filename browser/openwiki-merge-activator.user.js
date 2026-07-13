// ==UserScript==
// @name         qq OpenWiki merge activator
// @namespace    https://github.com/hypermemetic-ai/qq
// @version      1.0.0
// @description  Activates the local OpenWiki maintainer after the operator confirms a GitHub merge.
// @match        https://github.com/*/*/pull/*
// @downloadURL  https://raw.githubusercontent.com/hypermemetic-ai/qq/main/browser/openwiki-merge-activator.user.js
// @updateURL    https://raw.githubusercontent.com/hypermemetic-ai/qq/main/browser/openwiki-merge-activator.user.js
// @grant        none
// @run-at       document-start
// ==/UserScript==

(function () {
  "use strict";

  const PULL_REQUEST = /^https:\/\/github\.com\/[^/]+\/[^/]+\/pull\/[1-9][0-9]*$/;
  const CONFIRM_MERGE = /^confirm (?:merge|squash and merge|rebase and merge)$/;

  function canonicalPullRequestUrl(href) {
    const url = new URL(href);
    const match = url.pathname.match(/^\/([^/]+)\/([^/]+)\/pull\/([1-9][0-9]*)/);
    if (!match) {
      return null;
    }
    const candidate = `${url.origin}/${match[1]}/${match[2]}/pull/${match[3]}`;
    return PULL_REQUEST.test(candidate) ? candidate : null;
  }

  document.addEventListener(
    "click",
    (event) => {
      const button = event.target && event.target.closest
        ? event.target.closest("button")
        : null;
      if (!button) {
        return;
      }
      const label = button.textContent.replace(/\s+/g, " ").trim().toLowerCase();
      if (!CONFIRM_MERGE.test(label)) {
        return;
      }
      const pullRequest = canonicalPullRequestUrl(location.href);
      if (!pullRequest) {
        return;
      }
      const activation = `qq-openwiki://activate?pr=${encodeURIComponent(pullRequest)}`;
      // Let GitHub receive the confirmation click before opening the local
      // protocol. The handler independently waits for and verifies the merge.
      setTimeout(() => location.assign(activation), 750);
    },
    true,
  );
})();
