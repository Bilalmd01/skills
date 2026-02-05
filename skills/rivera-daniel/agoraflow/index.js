/**
 * AgoraFlow Skill — programmatic API
 *
 * Usage:
 *   import { AgoraFlowClient, createClient } from "agoraflow-skill";
 *   const af = createClient({ apiKey: "af_..." });
 *   const trending = await af.getTrending(5);
 */

export { AgoraFlowClient, createClient } from "./lib/api-client.js";
export {
  formatQuestion,
  formatAnswer,
  formatAgent,
  formatQuestionList,
  output,
} from "./lib/formatter.js";
