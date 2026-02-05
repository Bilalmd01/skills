#!/usr/bin/env node
/**
 * trending [limit] [--json]
 *
 * Fetch the hottest / trending questions on AgoraFlow.
 *
 * Examples:
 *   trending
 *   trending 5
 *   trending 20 --json
 */

import { createClient } from "../../lib/api-client.js";
import { formatQuestionList, output } from "../../lib/formatter.js";

export async function trending(limit = 10, { json = false } = {}) {
  const client = createClient();
  const result = await client.getTrending(limit);
  const questions = result.data || [];
  return output(result, () => {
    return formatQuestionList(questions, "🔥 Trending");
  }, { json });
}

// CLI entry
const args = process.argv.slice(2);
if (process.argv[1]?.endsWith("trending.js") || args.length >= 0) {
  const limit = parseInt(args.find(a => /^\d+$/.test(a)) || "10", 10);
  const json = args.includes("--json");

  trending(limit, { json })
    .then(console.log)
    .catch(e => { console.error("❌", e.message); process.exit(1); });
}
