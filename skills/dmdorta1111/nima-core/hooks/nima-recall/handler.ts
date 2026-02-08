import { execSync } from 'child_process';
import { readFileSync } from 'fs';
import { join } from 'path';

interface HookEvent {
  type: string;
  action: string;
  sessionKey: string;
  timestamp: Date;
  messages: string[];
  context: {
    workspaceDir?: string;
    sessionFile?: string;
    bootstrapFiles?: Array<{ path: string; content: string; source: string; }>;
    cfg?: Record<string, unknown>;
  };
}

interface NimaRecallConfig {
  enabled?: boolean;
  limit?: number;
  minScore?: number;
  timeout?: number;
}

/**
 * Extract recent conversation context from session file
 */
function extractRecentContext(sessionFile: string, maxMessages: number = 10): string {
  try {
    const content = readFileSync(sessionFile, 'utf-8');
    const lines = content.split('\n').filter(line => line.trim());
    
    // Extract user/assistant messages from session file
    const messages: string[] = [];
    let currentRole = '';
    let currentContent = '';
    
    for (const line of lines) {
      // Look for role indicators (adjust based on actual session file format)
      if (line.startsWith('user:') || line.startsWith('User:')) {
        if (currentContent) messages.push(`${currentRole}: ${currentContent}`);
        currentRole = 'user';
        currentContent = line.substring(line.indexOf(':') + 1).trim();
      } else if (line.startsWith('assistant:') || line.startsWith('Assistant:')) {
        if (currentContent) messages.push(`${currentRole}: ${currentContent}`);
        currentRole = 'assistant';
        currentContent = line.substring(line.indexOf(':') + 1).trim();
      } else if (currentRole) {
        currentContent += ' ' + line.trim();
      }
    }
    
    // Add last message
    if (currentContent) messages.push(`${currentRole}: ${currentContent}`);
    
    // Take last N messages
    const recentMessages = messages.slice(-maxMessages);
    return recentMessages.join('\n');
  } catch (error) {
    console.error('[nima-recall] Error reading session file:', error);
    return '';
  }
}

/**
 * Query NIMA memory system
 */
function queryNima(workspaceDir: string, query: string, limit: number, timeout: number): string[] {
  const nimaCorePath = join(workspaceDir, 'nima-core');
  
  // Escape query for shell
  const escapedQuery = query.replace(/"/g, '\\"');
  
  // Build Python command
  const pythonCmd = `python3 -c "import sys; sys.path.insert(0, '${nimaCorePath}'); from nima_core import NimaCore; n = NimaCore(); results = n.recall(sys.argv[1], top_k=${limit}); [print(f'[{i+1}] {r.get(\\"who\\",\\"?\\")}|{r.get(\\"what\\",\\"?\\")}') for i, r in enumerate(results)]" "${escapedQuery}"`;
  
  try {
    const output = execSync(pythonCmd, {
      encoding: 'utf-8',
      timeout: timeout,
      stdio: ['pipe', 'pipe', 'pipe']
    });
    
    // Parse output lines
    const lines = output.trim().split('\n').filter(line => line.trim());
    return lines;
  } catch (error) {
    console.error('[nima-recall] NIMA query failed:', error);
    return [];
  }
}

/**
 * Format NIMA results as markdown
 */
function formatResults(results: string[]): string {
  if (results.length === 0) {
    return '# 🧠 NIMA Recall\n\nNo relevant memories found.\n';
  }
  
  let markdown = '# 🧠 NIMA Recall\n\nRelevant memories from NIMA:\n\n';
  
  for (const result of results) {
    // Parse format: [1] who|what
    const match = result.match(/\[(\d+)\]\s+([^|]+)\|(.+)/);
    if (match) {
      const [, num, who, what] = match;
      const truncated = what.length > 100 ? what.substring(0, 100) + '...' : what;
      markdown += `**[${num}]** ${who.trim()}: ${truncated.trim()}\n\n`;
    }
  }
  
  markdown += `---\n*Retrieved ${results.length} ${results.length === 1 ? 'memory' : 'memories'}*\n`;
  
  return markdown;
}

/**
 * Main hook handler
 */
const handler = async (event: HookEvent): Promise<void> => {
  // Only process agent:bootstrap events
  if (event.action !== 'bootstrap') {
    return;
  }
  
  // Skip subagent sessions
  if (event.sessionKey.includes(':subagent:')) {
    console.log('[nima-recall] Skipping subagent session');
    return;
  }
  
  // Skip heartbeat sessions
  if (event.sessionKey.includes('heartbeat')) {
    console.log('[nima-recall] Skipping heartbeat session');
    return;
  }
  
  // Get configuration
  const config = (event.context.cfg as any)?.hooks?.internal?.entries?.['nima-recall'] || {} as NimaRecallConfig;
  const limit = config.limit ?? 3;
  const minScore = config.minScore ?? 0.0;
  const timeout = config.timeout ?? 15000;
  
  // Check if enabled
  if (config.enabled === false) {
    console.log('[nima-recall] Hook disabled in config');
    return;
  }
  
  // Validate workspace directory
  const workspaceDir = event.context.workspaceDir;
  if (!workspaceDir) {
    console.error('[nima-recall] No workspace directory in context');
    return;
  }
  
  // Validate session file
  const sessionFile = event.context.sessionFile;
  if (!sessionFile) {
    console.log('[nima-recall] No session file available, skipping');
    return;
  }
  
  try {
    // Extract recent context from session
    console.log('[nima-recall] Extracting recent conversation context...');
    const context = extractRecentContext(sessionFile, 10);
    
    // Validate context
    if (!context || context.trim().length < 20) {
      console.log('[nima-recall] Insufficient context, skipping');
      return;
    }
    
    if (context.toLowerCase().includes('new session')) {
      console.log('[nima-recall] New session detected, skipping');
      return;
    }
    
    // Query NIMA
    console.log('[nima-recall] Querying NIMA memory system...');
    const results = queryNima(workspaceDir, context, limit, timeout);
    
    // Format results
    const markdown = formatResults(results);
    
    // Inject into bootstrap context
    if (!event.context.bootstrapFiles) {
      event.context.bootstrapFiles = [];
    }
    
    event.context.bootstrapFiles.push({
      path: 'NIMA_RECALL.md',
      content: markdown,
      source: 'nima-recall-hook'
    });
    
    console.log(`[nima-recall] Injected ${results.length} memories into context`);
    
  } catch (error) {
    // Fail gracefully - log but don't throw
    console.error('[nima-recall] Error during recall:', error);
  }
};

export default handler;
