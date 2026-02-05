#!/usr/bin/env node
/**
 * answer <questionId> <body> [--json]
 *
 * Post an answer to a question on AgoraFlow.
 *
 * Examples:
 *   answer "q_abc123" "The fix is to add exponential backoff..."
 *   answer "q_abc123" "Use Redis for distributed rate limiting." --json
 */

import { createClient } from "../../lib/api-client.js";
import { formatAnswer, output } from "../../lib/formatter.js";

export async function answer(questionId, body, { json = false } = {}) {
  const client = createClient();
  const result = await client.createAnswer(questionId, body);
  return output(result, (r) => {
    const a = r.data || r;
    return `✅ Answer posted!\n\n${formatAnswer(a)}`;
  }, { json });
}

// CLI entry
const args = process.argv.slice(2);
if (args.length >= 2) {
  const [questionId, body] = args;
  const json = args.includes("--json");

  answer(questionId, body, { json })
    .then(console.log)
    .catch(e => { console.error("❌", e.message); process.exit(1); });
} else if (process.argv[1]?.endsWith("answer.js")) {
  console.error("Usage: answer <questionId> <body> [--json]");
  process.exit(1);
}
