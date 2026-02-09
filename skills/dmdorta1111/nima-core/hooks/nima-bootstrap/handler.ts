import { execSync } from 'child_process';
import { existsSync, readFileSync } from 'fs';
import { join } from 'path';

interface HookEvent {
  type: string;
  action: string;
  sessionKey: string;
  timestamp: Date;
  messages: string[];
  context: {
    workspaceDir?: string;
    bootstrapFiles?: Array<{ path: string; content: string; source: string; }>;
    cfg?: Record<string, unknown>;
  };
}

type HookHandler = (event: HookEvent) => Promise<void> | void;

const handler: HookHandler = (event: HookEvent) => {
  const { sessionKey, context } = event;
  const workspaceDir = context.workspaceDir;

  // Skip subagent sessions
  if (sessionKey.includes(':subagent:')) {
    console.log('[nima-bootstrap] Skipping subagent session');
    return;
  }

  // Skip heartbeat sessions
  if (sessionKey.includes('heartbeat')) {
    console.log('[nima-bootstrap] Skipping heartbeat session');
    return;
  }

  // Require workspace directory
  if (!workspaceDir) {
    console.log('[nima-bootstrap] No workspace directory configured, skipping');
    return;
  }

  console.log('[nima-bootstrap] Initializing NIMA cognitive memory system...');

  try {
    // Check for local nima_core installation
    const localNimaPath = join(workspaceDir, 'nima-core', 'nima_core');
    const nimaExists = existsSync(localNimaPath);

    // Build Python command
    const pythonCmd = `python3 -c "from nima_core import NimaCore; n = NimaCore(); s = n.status(); print(f'NIMA: {s[\\"memory_count\\"]} memories, v2={s[\\"config\\"][\\"any_enabled\\"]}')"`;

    // Execute with timeout
    const result = execSync(pythonCmd, {
      cwd: workspaceDir,
      timeout: 15000,
      encoding: 'utf-8',
      stdio: ['pipe', 'pipe', 'pipe']
    }).trim();

    console.log(`[nima-bootstrap] ${result}`);

    // Parse status (attempt to extract structured data)
    let statusContent = '# NIMA Status\n\n';
    statusContent += `**Generated:** ${new Date().toISOString()}\n\n`;
    statusContent += `## System Output\n\n\`\`\`\n${result}\n\`\`\`\n\n`;

    // Try to extract memory count and version info
    const memoryMatch = result.match(/(\d+)\s+memories/);
    const v2Match = result.match(/v2=(\w+)/);

    if (memoryMatch) {
      statusContent += `## Statistics\n\n`;
      statusContent += `- **Memory Count:** ${memoryMatch[1]}\n`;
    }

    if (v2Match) {
      statusContent += `- **V2 Enabled:** ${v2Match[1]}\n`;
    }

    statusContent += `\n## Installation\n\n`;
    statusContent += nimaExists 
      ? `- Local installation detected at \`nima-core/nima_core/\`\n`
      : `- Using pip-installed module\n`;

    statusContent += `\n---\n\n`;
    statusContent += `*NIMA (Neural Integration Memory Architecture) provides persistent cognitive memory and insight extraction.*\n`;

    // Inject into bootstrap files
    if (!context.bootstrapFiles) {
      context.bootstrapFiles = [];
    }

    context.bootstrapFiles.push({
      path: 'NIMA_STATUS.md',
      content: statusContent,
      source: 'nima-bootstrap'
    });

    console.log('[nima-bootstrap] ✓ NIMA_STATUS.md injected into bootstrap context');

  } catch (error) {
    // Log error but don't throw - allow session to continue
    const errorMsg = error instanceof Error ? error.message : String(error);
    console.error(`[nima-bootstrap] Failed to initialize NIMA: ${errorMsg}`);
    console.log('[nima-bootstrap] Session will continue without NIMA status');

    // Optionally inject error status
    if (context.bootstrapFiles) {
      context.bootstrapFiles.push({
        path: 'NIMA_STATUS.md',
        content: `# NIMA Status\n\n⚠️ **NIMA not available**\n\nError: ${errorMsg}\n\nThe session will continue without cognitive memory integration.\n`,
        source: 'nima-bootstrap'
      });
    }
  }
};

export default handler;
