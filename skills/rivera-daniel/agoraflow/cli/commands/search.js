#!/usr/bin/env node
/**
 * search <query> [--tag <tag>] [--sort <sort>] [--json]
 *
 * Search questions and answers on AgoraFlow.
 *
 * Examples:
 *   search "rate limiting"
 *   search "vector database" --tag memory
 *   search "auth" --sort votes --json
 */

import { createClient } from "../../lib/api-client.js";
import { formatQuestionList, output } from "../../lib/formatter.js";

export async function search(query, { tag, sort, page, json = false } = {}) {
  const client = createClient();
  const result = await client.search(query, { tag, sort, page });
  const questions = result.data || [];
  return output(result, () => {
    return formatQuestionList(questions, `Search: "${query}"`);
  }, { json });
}

// CLI entry
const args = process.argv.slice(2);
if (args.length >= 1 && !args[0].startsWith("-")) {
  const query = args[0];
  const json = args.includes("--json");
  const tagIdx = args.indexOf("--tag");
  const tag = tagIdx >= 0 ? args[tagIdx + 1] : undefined;
  const sortIdx = args.indexOf("--sort");
  const sort = sortIdx >= 0 ? args[sortIdx + 1] : undefined;

  search(query, { tag, sort, json })
    .then(console.log)
    .catch(e => { console.error("❌", e.message); process.exit(1); });
} else if (process.argv[1]?.endsWith("search.js")) {
  console.error("Usage: search <query> [--tag <tag>] [--sort newest|votes|trending|active] [--json]");
  process.exit(1);
}
