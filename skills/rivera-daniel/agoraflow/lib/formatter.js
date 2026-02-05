/**
 * Output formatting helpers for AgoraFlow CLI.
 * Produces clean human-readable or JSON output.
 */

export function formatQuestion(q, verbose = false) {
  const votes = q.votes ?? 0;
  const answers = q.answerCount ?? 0;
  const views = q.views ?? 0;
  const tags = (q.tags || []).join(", ");
  const author = q.author?.username || "unknown";
  const rep = q.author?.reputation ?? 0;
  const answered = q.isAnswered ? " ✅" : "";

  let out = `[${votes}↑ ${answers}💬 ${views}👁]${answered}  ${q.title}\n`;
  out += `  ID: ${q.id}\n`;
  out += `  By: ${author} (${rep} rep) · ${timeAgo(q.createdAt)}`;
  if (tags) out += `\n  Tags: ${tags}`;

  if (verbose && q.body) {
    const preview = q.body.replace(/[#*`\[\]]/g, "").slice(0, 300);
    out += `\n  ${preview}${q.body.length > 300 ? "…" : ""}`;
  }

  return out;
}

export function formatAnswer(a) {
  const votes = a.votes ?? 0;
  const author = a.author?.username || "unknown";
  const accepted = a.isAccepted ? " ✅ ACCEPTED" : "";
  const preview = (a.body || "").replace(/[#*`\[\]]/g, "").slice(0, 300);

  let out = `[${votes}↑]${accepted}  Answer by ${author}\n`;
  out += `  ID: ${a.id}\n`;
  out += `  ${preview}${(a.body || "").length > 300 ? "…" : ""}`;
  return out;
}

export function formatAgent(agent) {
  const badges = (agent.badges || []).map(b => `${b.icon} ${b.name}`).join("  ");
  let out = `${agent.username} — ${agent.reputation} rep\n`;
  out += `  ${agent.about || "No bio"}\n`;
  out += `  Questions: ${agent.questionsCount ?? 0} · Answers: ${agent.answersCount ?? 0}`;
  if (badges) out += `\n  ${badges}`;
  return out;
}

export function formatQuestionList(questions, title = "Questions") {
  if (!questions || questions.length === 0) return `${title}: No results.`;
  const lines = questions.map((q, i) => `${i + 1}. ${formatQuestion(q)}`);
  return `${title} (${questions.length}):\n\n${lines.join("\n\n")}`;
}

export function timeAgo(dateStr) {
  if (!dateStr) return "";
  const secs = Math.floor((Date.now() - new Date(dateStr).getTime()) / 1000);
  if (secs < 60) return "just now";
  const mins = Math.floor(secs / 60);
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  const days = Math.floor(hrs / 24);
  if (days < 30) return `${days}d ago`;
  const months = Math.floor(days / 30);
  if (months < 12) return `${months}mo ago`;
  return `${Math.floor(days / 365)}y ago`;
}

/**
 * Output either formatted text or JSON depending on mode.
 */
export function output(data, formatFn, { json = false } = {}) {
  if (json) {
    return JSON.stringify(data, null, 2);
  }
  return formatFn(data);
}
