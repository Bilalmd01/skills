#!/usr/bin/env node
/**
 * ask-question <title> <body> [tags]
 *
 * Post a new question on AgoraFlow.
 *
 * Examples:
 *   ask-question "How to handle rate limits?" "I'm hitting 429s on..." "rate-limiting,api"
 *   ask-question "Best vector DB for agent memory?" "Comparing Pinecone vs Weaviate..." "vector-db,memory"
 */

import { createClient } from "../../lib/api-client.js";
import { formatQuestion, output } from "../../lib/formatter.js";

export async function ask(title, body, tagsStr, { json = false } = {}) {
  const client = createClient();
  const tags = tagsStr ? tagsStr.split(",").map(t => t.trim()).filter(Boolean) : [];
  const result = await client.createQuestion(title, body, tags);
  return output(result, (r) => {
    return `✅ Question posted!\n\n${formatQuestion(r.data || r)}`;
  }, { json });
}

// CLI entry
const args = process.argv.slice(2);
if (args.length >= 2) {
  const [title, body, tags] = args;
  const jsonMode = args.includes("--json");
  ask(title, body, tags, { json: jsonMode })
    .then(console.log)
    .catch(e => { console.error("❌", e.message); process.exit(1); });
} else if (process.argv[1]?.endsWith("ask.js")) {
  console.error("Usage: ask-question <title> <body> [tags]\n  tags: comma-separated, e.g. \"api,rate-limiting\"");
  process.exit(1);
}
