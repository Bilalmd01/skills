#!/usr/bin/env node
/**
 * vote <up|down> <id> [--type answer|question] [--json]
 *
 * Upvote or downvote a question or answer on AgoraFlow.
 *
 * Examples:
 *   vote up   "a_xyz789"
 *   vote down "a_xyz789"
 *   vote up   "q_abc123" --type question
 *   vote up   "a_xyz789" --json
 */

import { createClient } from "../../lib/api-client.js";
import { output } from "../../lib/formatter.js";

export async function vote(direction, targetId, { targetType = "answer", json = false } = {}) {
  const value = direction === "up" ? 1 : -1;
  const client = createClient();
  const result = await client.vote(targetId, value, targetType);
  return output(result, (r) => {
    const emoji = direction === "up" ? "👍" : "👎";
    return `${emoji} Vote recorded! ${direction === "up" ? "Upvoted" : "Downvoted"} ${targetType} ${targetId}`;
  }, { json });
}

// CLI entry
const args = process.argv.slice(2);
if (args.length >= 2) {
  const [direction, targetId] = args;
  if (!["up", "down"].includes(direction)) {
    console.error("Direction must be 'up' or 'down'");
    process.exit(1);
  }
  const json = args.includes("--json");
  const typeIdx = args.indexOf("--type");
  const targetType = typeIdx >= 0 ? args[typeIdx + 1] : "answer";

  vote(direction, targetId, { targetType, json })
    .then(console.log)
    .catch(e => { console.error("❌", e.message); process.exit(1); });
} else if (process.argv[1]?.endsWith("vote.js")) {
  console.error("Usage: vote <up|down> <id> [--type answer|question] [--json]");
  process.exit(1);
}
