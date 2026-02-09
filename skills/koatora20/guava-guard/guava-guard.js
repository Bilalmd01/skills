#!/usr/bin/env node
/**
 * GuavaGuard v2.0 — Agent Skill Security Scanner 🍈🛡️
 * 
 * Based on Snyk ToxicSkills taxonomy (8 threat categories)
 * + ClawHavoc campaign IoCs + Koi Security intel
 * 
 * Key improvements over v1:
 * - Context-aware: docs vs code differentiated (reduces false positives ~80%)
 * - Self-exclusion: scanner doesn't flag its own IoC definitions
 * - Whitelist: .guava-guard-ignore support
 * - Flow analysis: credential-read → network-send data flow detection
 * - Entropy analysis: detects hardcoded secrets/tokens
 * - ToxicSkills taxonomy: 8 categories aligned with Snyk research
 * - Extended IoCs: zaycv, Ddoy233, glot.io snippets, setup-service.com
 * 
 * Zero dependencies. Single file. Node.js 18+.
 * 
 * Usage:
 *   node guava-guard.js [scan-dir] [options]
 * 
 * Options:
 *   --verbose, -v       Show detailed findings
 *   --json              Output JSON report
 *   --self-exclude      Exclude the guava-guard skill directory itself
 *   --strict            Lower thresholds (suspicious=20, malicious=60)
 *   --summary-only      Only print summary, no per-skill output
 */

const fs = require('fs');
const path = require('path');

// ===== CONFIGURATION =====
const VERSION = '2.0.0';

const THRESHOLDS = {
  normal:  { suspicious: 30, malicious: 80 },
  strict:  { suspicious: 20, malicious: 60 },
};

// File classification
const CODE_EXTENSIONS = new Set(['.js', '.ts', '.mjs', '.cjs', '.py', '.sh', '.bash', '.ps1', '.rb', '.go', '.rs', '.php', '.pl']);
const DOC_EXTENSIONS = new Set(['.md', '.txt', '.rst', '.adoc']);
const DATA_EXTENSIONS = new Set(['.json', '.yaml', '.yml', '.toml', '.xml', '.csv']);
const BINARY_EXTENSIONS = new Set(['.png', '.jpg', '.jpeg', '.gif', '.ico', '.woff', '.woff2', '.ttf', '.eot', '.wasm', '.wav', '.mp3', '.mp4', '.webm', '.ogg', '.pdf', '.zip', '.tar', '.gz', '.bz2', '.7z', '.exe', '.dll', '.so', '.dylib']);

// Severity weights for risk scoring
const SEVERITY_WEIGHTS = { CRITICAL: 40, HIGH: 15, MEDIUM: 5, LOW: 2 };

// ===== IoCs (Indicators of Compromise) =====
const KNOWN_MALICIOUS = {
  ips: [
    '91.92.242.30',           // ClawHavoc C2
  ],
  domains: [
    'webhook.site',            // Common exfil endpoint
    'requestbin.com',          // Common exfil endpoint
    'hookbin.com',             // Common exfil endpoint
    'pipedream.net',           // Common exfil endpoint
    'ngrok.io',                // Tunnel (context-dependent)
    'download.setup-service.com', // ClawHavoc decoy domain
  ],
  urls: [
    'glot.io/snippets/hfd3x9ueu5',  // ClawHavoc macOS payload
    'github.com/Ddoy233',            // ClawHavoc payload host
  ],
  usernames: ['zaycv', 'Ddoy233'],   // Known malicious actors
  filenames: ['openclaw-agent.zip', 'openclawcli.zip'],
  typosquats: [
    // ClawHavoc campaign
    'clawhub', 'clawhub1', 'clawhubb', 'clawhubcli', 'clawwhub', 'cllawhub', 'clawdhub1',
    // Polymarket scams
    'polymarket-trader', 'polymarket-pro', 'polytrading',
    'better-polymarket', 'polymarket-all-in-one',
    // YouTube scams
    'youtube-summarize', 'youtube-thumbnail-grabber', 'youtube-video-downloader',
    // Misc
    'auto-updater-agent', 'yahoo-finance-pro', 'x-trends-tracker',
    'lost-bitcoin-finder', 'solana-wallet-tracker', 'rankaj',
    // Snyk ToxicSkills confirmed malicious
    'moltyverse-email', 'buy-anything', 'youtube-data', 'prediction-markets-roarin',
  ],
};

// ===== THREAT TAXONOMY (Snyk ToxicSkills aligned) =====
// Each pattern has: id, category, regex, severity, desc, codeOnly (skip in docs)
const PATTERNS = [
  // ── Category 1: Prompt Injection (CRITICAL) ──
  { id: 'PI_IGNORE', cat: 'prompt-injection', regex: /ignore\s+(all\s+)?previous\s+instructions|disregard\s+(all\s+)?prior/gi, severity: 'CRITICAL', desc: 'Prompt injection: ignore instructions', docOnly: true },
  { id: 'PI_ROLE', cat: 'prompt-injection', regex: /you\s+are\s+(now|actually)|your\s+new\s+role|forget\s+your\s+(rules|instructions)/gi, severity: 'CRITICAL', desc: 'Prompt injection: role override', docOnly: true },
  { id: 'PI_SYSTEM', cat: 'prompt-injection', regex: /\[SYSTEM\]|\<system\>|<<SYS>>|system:\s*you\s+are/gi, severity: 'CRITICAL', desc: 'Prompt injection: system message impersonation', docOnly: true },
  { id: 'PI_ZWSP', cat: 'prompt-injection', regex: /[\u200b\u200c\u200d\u2060\ufeff]/g, severity: 'CRITICAL', desc: 'Zero-width Unicode (hidden text)', all: true },
  { id: 'PI_HOMOGLYPH', cat: 'prompt-injection', regex: /[а-яА-Я].*[a-zA-Z]|[a-zA-Z].*[а-яА-Я]/g, severity: 'HIGH', desc: 'Cyrillic/Latin homoglyph mixing', all: true },
  { id: 'PI_BASE64_MD', cat: 'prompt-injection', regex: /(?:run|execute|eval|decode)\s+(?:this\s+)?base64/gi, severity: 'CRITICAL', desc: 'Base64 execution instruction in docs', docOnly: true },

  // ── Category 2: Malicious Code (CRITICAL) ──
  { id: 'MAL_EVAL', cat: 'malicious-code', regex: /\beval\s*\(/g, severity: 'HIGH', desc: 'Dynamic code evaluation', codeOnly: true },
  { id: 'MAL_FUNC_CTOR', cat: 'malicious-code', regex: /new\s+Function\s*\(/g, severity: 'HIGH', desc: 'Function constructor (dynamic code)', codeOnly: true },
  { id: 'MAL_CHILD', cat: 'malicious-code', regex: /require\s*\(\s*['"]child_process['"]\)|child_process/g, severity: 'MEDIUM', desc: 'Child process module', codeOnly: true },
  { id: 'MAL_EXEC', cat: 'malicious-code', regex: /\bexecSync\s*\(|\bexec\s*\(\s*[`'"]/g, severity: 'MEDIUM', desc: 'Command execution', codeOnly: true },
  { id: 'MAL_SPAWN', cat: 'malicious-code', regex: /\bspawn\s*\(\s*['"`]/g, severity: 'MEDIUM', desc: 'Process spawn', codeOnly: true },
  { id: 'MAL_SHELL', cat: 'malicious-code', regex: /\/bin\/(sh|bash|zsh)|cmd\.exe|powershell\.exe/gi, severity: 'MEDIUM', desc: 'Shell invocation', codeOnly: true },
  { id: 'MAL_REVSHELL', cat: 'malicious-code', regex: /reverse.?shell|bind.?shell|\bnc\s+-[elp]|\bncat\s+-e|\bsocat\s+TCP/gi, severity: 'CRITICAL', desc: 'Reverse/bind shell', all: true },
  { id: 'MAL_SOCKET', cat: 'malicious-code', regex: /\bnet\.Socket\b[\s\S]{0,50}\.connect\s*\(/g, severity: 'HIGH', desc: 'Raw socket connection', codeOnly: true },

  // ── Category 3: Suspicious Downloads (CRITICAL) ──
  { id: 'DL_CURL_BASH', cat: 'suspicious-download', regex: /curl\s+[^\n]*\|\s*(sh|bash|zsh)|wget\s+[^\n]*\|\s*(sh|bash|zsh)/g, severity: 'CRITICAL', desc: 'Pipe download to shell', all: true },
  { id: 'DL_EXE', cat: 'suspicious-download', regex: /download\s+[^\n]*\.(zip|exe|dmg|msi|pkg|appimage|deb|rpm)/gi, severity: 'CRITICAL', desc: 'Download executable/archive', docOnly: true },
  { id: 'DL_GITHUB_RELEASE', cat: 'suspicious-download', regex: /github\.com\/[^\/]+\/[^\/]+\/releases\/download/g, severity: 'MEDIUM', desc: 'GitHub release download', all: true },
  { id: 'DL_PASSWORD_ZIP', cat: 'suspicious-download', regex: /password[\s:]+[^\n]*\.zip|\.zip[\s\S]{0,100}password/gi, severity: 'CRITICAL', desc: 'Password-protected archive (evasion technique)', all: true },

  // ── Category 4: Credential Handling (HIGH) ──
  { id: 'CRED_ENV_FILE', cat: 'credential-handling', regex: /(?:read|open|load|parse|require|cat|source)\s*[(\s]['"`]?[^\n]*\.env\b/gi, severity: 'HIGH', desc: 'Reading .env file', codeOnly: true },
  { id: 'CRED_ENV_REF', cat: 'credential-handling', regex: /process\.env\.[A-Z_]*(?:KEY|SECRET|TOKEN|PASSWORD|CREDENTIAL)/gi, severity: 'MEDIUM', desc: 'Sensitive env var access', codeOnly: true },
  { id: 'CRED_SSH', cat: 'credential-handling', regex: /\.ssh\/|id_rsa|id_ed25519|authorized_keys/gi, severity: 'HIGH', desc: 'SSH key access', codeOnly: true },
  { id: 'CRED_WALLET', cat: 'credential-handling', regex: /wallet[\s._-]*(?:key|seed|phrase|mnemonic)|seed[\s._-]*phrase|mnemonic[\s._-]*phrase/gi, severity: 'HIGH', desc: 'Crypto wallet credential access', codeOnly: true },
  { id: 'CRED_CLAWDBOT', cat: 'credential-handling', regex: /\.clawdbot\b|\.openclaw[\/\\](?!workspace).*(?:env|config|token)/gi, severity: 'HIGH', desc: 'OpenClaw/Clawdbot config access', codeOnly: true },
  { id: 'CRED_ECHO', cat: 'credential-handling', regex: /echo\s+\$[A-Z_]*(?:KEY|TOKEN|SECRET|PASS)|(?:print|console\.log)\s*\(\s*(?:.*\b(?:api_key|secret_key|access_token|password)\b)/gi, severity: 'HIGH', desc: 'Credential echo/print to output', all: true },
  { id: 'CRED_SUDO', cat: 'credential-handling', regex: /\bsudo\s+(?:curl|wget|npm|pip|chmod|chown|bash)/g, severity: 'HIGH', desc: 'Sudo in installation instructions', docOnly: true },

  // ── Category 5: Secret Detection (HIGH) ──
  // (entropy-based detection is separate — see detectHardcodedSecrets)
  { id: 'SECRET_HARDCODED_KEY', cat: 'secret-detection', regex: /(?:api[_-]?key|apikey|secret[_-]?key|access[_-]?token)\s*[:=]\s*['"][a-zA-Z0-9_\-]{20,}['"]/gi, severity: 'HIGH', desc: 'Hardcoded API key/secret', codeOnly: true },
  { id: 'SECRET_AWS', cat: 'secret-detection', regex: /AKIA[0-9A-Z]{16}/g, severity: 'CRITICAL', desc: 'AWS Access Key ID', all: true },
  { id: 'SECRET_PRIVATE_KEY', cat: 'secret-detection', regex: /-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----/g, severity: 'CRITICAL', desc: 'Embedded private key', all: true },
  { id: 'SECRET_GITHUB_TOKEN', cat: 'secret-detection', regex: /gh[ps]_[A-Za-z0-9_]{36,}/g, severity: 'CRITICAL', desc: 'GitHub token', all: true },

  // ── Category 6: Exfiltration / Third-Party Content (MEDIUM) ──
  { id: 'EXFIL_WEBHOOK', cat: 'exfiltration', regex: /webhook\.site|requestbin\.com|hookbin\.com|pipedream\.net/gi, severity: 'CRITICAL', desc: 'Known exfiltration endpoint', all: true },
  { id: 'EXFIL_POST', cat: 'exfiltration', regex: /(?:method:\s*['"]POST['"]|\.post\s*\()\s*[^\n]*(?:secret|token|key|cred|env|password)/gi, severity: 'HIGH', desc: 'POST with sensitive data', codeOnly: true },
  { id: 'EXFIL_CURL_DATA', cat: 'exfiltration', regex: /curl\s+[^\n]*(?:-d|--data)\s+[^\n]*(?:\$|env|key|token|secret)/gi, severity: 'HIGH', desc: 'curl exfiltration of secrets', all: true },
  { id: 'EXFIL_DNS', cat: 'exfiltration', regex: /dns\.resolve|nslookup\s+.*\$|dig\s+.*\$/g, severity: 'HIGH', desc: 'DNS-based exfiltration', codeOnly: true },

  // ── Category 7: Unverifiable Dependencies (MEDIUM) ──
  { id: 'DEP_REMOTE_IMPORT', cat: 'unverifiable-deps', regex: /import\s*\(\s*['"]https?:\/\//g, severity: 'HIGH', desc: 'Remote dynamic import', codeOnly: true },
  { id: 'DEP_REMOTE_SCRIPT', cat: 'unverifiable-deps', regex: /<script\s+src\s*=\s*['"]https?:\/\/[^'"]*(?!googleapis|cdn\.|unpkg|cdnjs|jsdelivr)/gi, severity: 'MEDIUM', desc: 'Remote script loading', codeOnly: true },

  // ── Category 8: Financial Access (MEDIUM) ──
  { id: 'FIN_CRYPTO', cat: 'financial-access', regex: /private[_-]?key\s*[:=]|send[_-]?transaction|sign[_-]?transaction|transfer[_-]?funds/gi, severity: 'HIGH', desc: 'Cryptocurrency transaction operations', codeOnly: true },
  { id: 'FIN_PAYMENT', cat: 'financial-access', regex: /stripe\.(?:charges|payments)|paypal\.(?:payment|payout)|plaid\.(?:link|transactions)/gi, severity: 'MEDIUM', desc: 'Payment API integration', codeOnly: true },

  // ── Obfuscation (cross-category, code-only) ──
  { id: 'OBF_HEX', cat: 'obfuscation', regex: /\\x[0-9a-f]{2}(?:\\x[0-9a-f]{2}){4,}/gi, severity: 'HIGH', desc: 'Hex-encoded string (5+ bytes)', codeOnly: true },
  { id: 'OBF_BASE64_EXEC', cat: 'obfuscation', regex: /(?:atob|Buffer\.from)\s*\([^)]+\)[\s\S]{0,30}(?:eval|exec|spawn|Function)/g, severity: 'CRITICAL', desc: 'Base64 decode → execute chain', codeOnly: true },
  { id: 'OBF_BASE64', cat: 'obfuscation', regex: /atob\s*\(|Buffer\.from\s*\([^)]+,\s*['"]base64['"]/g, severity: 'MEDIUM', desc: 'Base64 decoding', codeOnly: true },
  { id: 'OBF_CHARCODE', cat: 'obfuscation', regex: /String\.fromCharCode\s*\(\s*(?:\d+\s*,\s*){3,}/g, severity: 'HIGH', desc: 'Character code construction (4+ chars)', codeOnly: true },
  { id: 'OBF_CONCAT', cat: 'obfuscation', regex: /\[\s*['"][a-z]['"](?:\s*,\s*['"][a-z]['"]){5,}\s*\]\.join/gi, severity: 'MEDIUM', desc: 'Array join obfuscation', codeOnly: true },
  { id: 'OBF_BASE64_BASH', cat: 'obfuscation', regex: /base64\s+(-[dD]|--decode)\s*\|\s*(sh|bash)/g, severity: 'CRITICAL', desc: 'Base64 decode piped to shell', all: true },

  // ── SKILL.md specific (prerequisites fraud) ──
  { id: 'PREREQ_DOWNLOAD', cat: 'suspicious-download', regex: /(?:prerequisit|pre-?requisit|before\s+(?:you\s+)?(?:use|start|install))[^\n]*(?:download|install|run)\s+[^\n]*(?:\.zip|\.exe|\.dmg|\.sh|curl|wget)/gi, severity: 'CRITICAL', desc: 'Download in prerequisites (ClawHavoc vector)', docOnly: true },
  { id: 'PREREQ_PASTE', cat: 'suspicious-download', regex: /(?:paste|copy)\s+(?:this\s+)?(?:into|in)\s+(?:your\s+)?terminal/gi, severity: 'HIGH', desc: 'Terminal paste instruction', docOnly: true },

  // ── Sandbox/environment detection ──
  { id: 'SANDBOX', cat: 'malicious-code', regex: /process\.env\.CI\b|isDocker\b|isContainer\b|process\.env\.GITHUB_ACTIONS\b/g, severity: 'MEDIUM', desc: 'Sandbox/CI environment detection', codeOnly: true },
];

// ===== SCANNER =====
class GuavaGuard {
  constructor(options = {}) {
    this.verbose = options.verbose || false;
    this.selfExclude = options.selfExclude || false;
    this.strict = options.strict || false;
    this.summaryOnly = options.summaryOnly || false;
    this.scannerDir = path.resolve(__dirname);
    this.thresholds = this.strict ? THRESHOLDS.strict : THRESHOLDS.normal;
    this.findings = [];
    this.stats = { scanned: 0, clean: 0, low: 0, suspicious: 0, malicious: 0 };
    this.ignoredSkills = new Set();
    this.ignoredPatterns = new Set();
  }

  // Load .guava-guard-ignore from scan directory
  loadIgnoreFile(scanDir) {
    const ignorePath = path.join(scanDir, '.guava-guard-ignore');
    if (!fs.existsSync(ignorePath)) return;

    const lines = fs.readFileSync(ignorePath, 'utf-8').split('\n');
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) continue;
      if (trimmed.startsWith('pattern:')) {
        this.ignoredPatterns.add(trimmed.replace('pattern:', '').trim());
      } else {
        this.ignoredSkills.add(trimmed);
      }
    }
    if (this.verbose && (this.ignoredSkills.size || this.ignoredPatterns.size)) {
      console.log(`📋 Loaded ignore file: ${this.ignoredSkills.size} skills, ${this.ignoredPatterns.size} patterns`);
    }
  }

  scanDirectory(dir) {
    if (!fs.existsSync(dir)) {
      console.error(`❌ Directory not found: ${dir}`);
      process.exit(2);
    }

    this.loadIgnoreFile(dir);

    const skills = fs.readdirSync(dir).filter(f => {
      const p = path.join(dir, f);
      return fs.statSync(p).isDirectory();
    });

    console.log(`\n🍈🛡️  GuavaGuard v${VERSION} Security Scanner`);
    console.log(`${'═'.repeat(54)}`);
    console.log(`📂 Scanning: ${dir}`);
    console.log(`📦 Skills found: ${skills.length}`);
    if (this.strict) console.log(`⚡ Strict mode enabled`);
    console.log();

    for (const skill of skills) {
      const skillPath = path.join(dir, skill);

      // Self-exclusion
      if (this.selfExclude && path.resolve(skillPath) === this.scannerDir) {
        if (!this.summaryOnly) console.log(`⏭️  ${skill} — SELF (excluded)`);
        continue;
      }

      // Ignore list
      if (this.ignoredSkills.has(skill)) {
        if (!this.summaryOnly) console.log(`⏭️  ${skill} — IGNORED`);
        continue;
      }

      this.scanSkill(skillPath, skill);
    }

    this.printSummary();
    return this.findings;
  }

  scanSkill(skillPath, skillName) {
    this.stats.scanned++;
    const skillFindings = [];

    // ── Check 1: Known malicious skill name ──
    if (KNOWN_MALICIOUS.typosquats.includes(skillName.toLowerCase())) {
      skillFindings.push({
        severity: 'CRITICAL', id: 'KNOWN_TYPOSQUAT', cat: 'malicious-code',
        desc: `Known malicious/typosquat skill name (ClawHavoc)`,
        file: 'SKILL NAME', line: 0
      });
    }

    // ── Check 2: Scan all files ──
    const files = this.getFiles(skillPath);
    for (const file of files) {
      const ext = path.extname(file).toLowerCase();
      const relFile = path.relative(skillPath, file);

      // Skip paths
      if (relFile.includes('node_modules/') || relFile.includes('node_modules\\')) continue;
      if (relFile.startsWith('.git/') || relFile.startsWith('.git\\')) continue;
      if (BINARY_EXTENSIONS.has(ext)) continue;

      let content;
      try {
        content = fs.readFileSync(file, 'utf-8');
      } catch { continue; }

      if (content.length > 500000) continue;

      const fileType = this.classifyFile(ext, relFile);

      // IoC checks (always)
      this.checkIoCs(content, relFile, skillFindings);

      // Pattern checks (context-aware)
      this.checkPatterns(content, relFile, fileType, skillFindings);

      // Hardcoded secret detection (code files only — skip lock files, metadata)
      const baseName = path.basename(relFile).toLowerCase();
      const skipSecretCheck = baseName.endsWith('-lock.json') || baseName === 'package-lock.json' ||
                              baseName === 'yarn.lock' || baseName === 'pnpm-lock.yaml' ||
                              baseName === '_meta.json' || baseName === '.package-lock.json';
      if (fileType === 'code' && !skipSecretCheck) {
        this.checkHardcodedSecrets(content, relFile, skillFindings);
      }
    }

    // ── Check 3: Structural checks ──
    this.checkStructure(skillPath, skillName, skillFindings);

    // Filter ignored patterns
    const filteredFindings = skillFindings.filter(f => !this.ignoredPatterns.has(f.id));

    // Calculate risk
    const risk = this.calculateRisk(filteredFindings);
    const verdict = this.getVerdict(risk);

    this.stats[verdict.stat]++;

    if (!this.summaryOnly) {
      console.log(`${verdict.icon} ${skillName} — ${verdict.label} (risk: ${risk})`);

      if (this.verbose && filteredFindings.length > 0) {
        // Group by category
        const byCat = {};
        for (const f of filteredFindings) {
          (byCat[f.cat] = byCat[f.cat] || []).push(f);
        }
        for (const [cat, findings] of Object.entries(byCat)) {
          console.log(`   📁 ${cat}`);
          for (const f of findings) {
            const icon = f.severity === 'CRITICAL' ? '💀' : f.severity === 'HIGH' ? '🔴' : f.severity === 'MEDIUM' ? '🟡' : '⚪';
            const loc = f.line ? `${f.file}:${f.line}` : f.file;
            console.log(`      ${icon} [${f.severity}] ${f.desc} — ${loc}`);
            if (f.sample) console.log(`         └─ "${f.sample}"`);
          }
        }
      }
    }

    if (filteredFindings.length > 0) {
      this.findings.push({ skill: skillName, risk, verdict: verdict.label, findings: filteredFindings });
    }
  }

  classifyFile(ext, relFile) {
    if (CODE_EXTENSIONS.has(ext)) return 'code';
    if (DOC_EXTENSIONS.has(ext)) return 'doc';
    if (DATA_EXTENSIONS.has(ext)) return 'data';
    // SKILL.md and README.md are docs but get special treatment
    const base = path.basename(relFile).toLowerCase();
    if (base === 'skill.md' || base === 'readme.md') return 'skill-doc';
    return 'other';
  }

  checkIoCs(content, relFile, findings) {
    const contentLower = content.toLowerCase();

    for (const ip of KNOWN_MALICIOUS.ips) {
      if (content.includes(ip)) {
        findings.push({ severity: 'CRITICAL', id: 'IOC_IP', cat: 'malicious-code', desc: `Known malicious IP: ${ip}`, file: relFile });
      }
    }

    for (const url of KNOWN_MALICIOUS.urls) {
      if (contentLower.includes(url.toLowerCase())) {
        findings.push({ severity: 'CRITICAL', id: 'IOC_URL', cat: 'malicious-code', desc: `Known malicious URL: ${url}`, file: relFile });
      }
    }

    // Domains — check as standalone, not just substring
    for (const domain of KNOWN_MALICIOUS.domains) {
      // Use word-boundary-like check to avoid matching substrings in documentation
      const domainRegex = new RegExp(`(?:https?://|[\\s'"\`(]|^)${domain.replace(/\./g, '\\.')}`, 'gi');
      if (domainRegex.test(content)) {
        // Extra context: if it's just mentioned in docs discussing security, lower severity
        findings.push({
          severity: 'HIGH', id: 'IOC_DOMAIN', cat: 'exfiltration',
          desc: `Suspicious domain: ${domain}`, file: relFile
        });
      }
    }

    for (const fname of KNOWN_MALICIOUS.filenames) {
      if (contentLower.includes(fname.toLowerCase())) {
        findings.push({ severity: 'CRITICAL', id: 'IOC_FILE', cat: 'suspicious-download', desc: `Known malicious filename: ${fname}`, file: relFile });
      }
    }

    for (const user of KNOWN_MALICIOUS.usernames) {
      if (contentLower.includes(user.toLowerCase())) {
        findings.push({ severity: 'HIGH', id: 'IOC_USER', cat: 'malicious-code', desc: `Known malicious username: ${user}`, file: relFile });
      }
    }
  }

  checkPatterns(content, relFile, fileType, findings) {
    for (const pattern of PATTERNS) {
      // Skip based on context
      if (pattern.codeOnly && fileType !== 'code') continue;
      if (pattern.docOnly && fileType !== 'doc' && fileType !== 'skill-doc') continue;
      if (!pattern.all && !pattern.codeOnly && !pattern.docOnly) continue;

      // Reset regex state
      pattern.regex.lastIndex = 0;
      const matches = content.match(pattern.regex);
      if (!matches) continue;

      // Find line number
      pattern.regex.lastIndex = 0;
      const idx = content.search(pattern.regex);
      const lineNum = idx >= 0 ? content.substring(0, idx).split('\n').length : null;

      // Severity adjustment: docs get demoted for non-critical code patterns
      let adjustedSeverity = pattern.severity;
      if ((fileType === 'doc' || fileType === 'skill-doc') && pattern.all && !pattern.docOnly) {
        // In docs, reduce severity by one level unless CRITICAL
        if (adjustedSeverity === 'HIGH') adjustedSeverity = 'MEDIUM';
        else if (adjustedSeverity === 'MEDIUM') adjustedSeverity = 'LOW';
      }

      findings.push({
        severity: adjustedSeverity,
        id: pattern.id,
        cat: pattern.cat,
        desc: pattern.desc,
        file: relFile,
        line: lineNum,
        matchCount: matches.length,
        sample: matches[0].substring(0, 80)
      });
    }
  }

  // Entropy-based secret detection
  checkHardcodedSecrets(content, relFile, findings) {
    // Match assignment patterns with string values
    const assignmentRegex = /(?:api[_-]?key|secret|token|password|credential|auth)\s*[:=]\s*['"]([a-zA-Z0-9_\-+/=]{16,})['"]|['"]([a-zA-Z0-9_\-+/=]{32,})['"]/gi;
    let match;
    while ((match = assignmentRegex.exec(content)) !== null) {
      const value = match[1] || match[2];
      if (!value) continue;

      // Skip obvious non-secrets
      if (/^[A-Z_]+$/.test(value)) continue;  // ALL_CAPS placeholder
      if (/^(true|false|null|undefined|none|default|example|test|placeholder|your[_-])/i.test(value)) continue;
      if (/^x{4,}|\.{4,}|_{4,}|0{8,}$/i.test(value)) continue; // Dummy values
      if (/^projects\/|^gs:\/\/|^https?:\/\//i.test(value)) continue; // Resource paths
      if (/^[a-z]+-[a-z]+-[a-z0-9]+$/i.test(value)) continue; // GCP project IDs like gen-lang-client-xxx

      const entropy = this.shannonEntropy(value);
      if (entropy > 3.5 && value.length >= 20) {
        const lineNum = content.substring(0, match.index).split('\n').length;
        findings.push({
          severity: 'HIGH', id: 'SECRET_ENTROPY', cat: 'secret-detection',
          desc: `High-entropy string (possible leaked secret, entropy=${entropy.toFixed(1)})`,
          file: relFile, line: lineNum,
          sample: value.substring(0, 8) + '...' + value.substring(value.length - 4)
        });
      }
    }
  }

  shannonEntropy(str) {
    const freq = {};
    for (const c of str) freq[c] = (freq[c] || 0) + 1;
    const len = str.length;
    let entropy = 0;
    for (const count of Object.values(freq)) {
      const p = count / len;
      if (p > 0) entropy -= p * Math.log2(p);
    }
    return entropy;
  }

  // Structural / meta checks
  checkStructure(skillPath, skillName, findings) {
    const skillMd = path.join(skillPath, 'SKILL.md');

    // Check if SKILL.md exists
    if (!fs.existsSync(skillMd)) {
      findings.push({
        severity: 'LOW', id: 'STRUCT_NO_SKILLMD', cat: 'structural',
        desc: 'No SKILL.md found', file: skillName
      });
      return;
    }

    const content = fs.readFileSync(skillMd, 'utf-8');

    // Check for suspiciously short SKILL.md
    if (content.length < 50) {
      findings.push({
        severity: 'MEDIUM', id: 'STRUCT_TINY_SKILLMD', cat: 'structural',
        desc: 'Suspiciously short SKILL.md (< 50 chars)', file: 'SKILL.md'
      });
    }

    // Check for scripts directory with executables but no documentation about them
    const scriptsDir = path.join(skillPath, 'scripts');
    if (fs.existsSync(scriptsDir)) {
      const scripts = fs.readdirSync(scriptsDir).filter(f =>
        CODE_EXTENSIONS.has(path.extname(f).toLowerCase())
      );
      if (scripts.length > 0 && !content.includes('scripts/')) {
        findings.push({
          severity: 'MEDIUM', id: 'STRUCT_UNDOCUMENTED_SCRIPTS', cat: 'structural',
          desc: `${scripts.length} script(s) in scripts/ not referenced in SKILL.md`,
          file: 'scripts/'
        });
      }
    }
  }

  calculateRisk(findings) {
    if (findings.length === 0) return 0;

    let score = 0;
    for (const f of findings) {
      score += SEVERITY_WEIGHTS[f.severity] || 0;
    }

    // Combo multipliers (data flow analysis)
    const ids = new Set(findings.map(f => f.id));
    const cats = new Set(findings.map(f => f.cat));

    // Credential access + exfiltration = very bad (2x)
    if (cats.has('credential-handling') && cats.has('exfiltration')) {
      score = Math.round(score * 2);
    }

    // Credential access + network request = suspicious (1.5x)
    if (cats.has('credential-handling') &&
        findings.some(f => f.id === 'MAL_CHILD' || f.id === 'MAL_EXEC')) {
      score = Math.round(score * 1.5);
    }

    // Obfuscation + code execution = very bad (2x)
    if (cats.has('obfuscation') &&
        (cats.has('malicious-code') || cats.has('credential-handling'))) {
      score = Math.round(score * 2);
    }

    // Known IoC = auto max
    if (ids.has('IOC_IP') || ids.has('IOC_URL') || ids.has('KNOWN_TYPOSQUAT')) {
      score = 100;
    }

    return Math.min(100, score);
  }

  getVerdict(risk) {
    if (risk >= this.thresholds.malicious) {
      return { icon: '🔴', label: 'MALICIOUS', stat: 'malicious' };
    }
    if (risk >= this.thresholds.suspicious) {
      return { icon: '🟡', label: 'SUSPICIOUS', stat: 'suspicious' };
    }
    if (risk > 0) {
      return { icon: '🟢', label: 'LOW RISK', stat: 'low' };
    }
    return { icon: '🟢', label: 'CLEAN', stat: 'clean' };
  }

  getFiles(dir) {
    const results = [];
    try {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.isDirectory()) {
          if (entry.name === '.git' || entry.name === 'node_modules') continue;
          results.push(...this.getFiles(fullPath));
        } else {
          results.push(fullPath);
        }
      }
    } catch {}
    return results;
  }

  printSummary() {
    const total = this.stats.scanned;
    const safe = this.stats.clean + this.stats.low;
    console.log(`\n${'═'.repeat(54)}`);
    console.log(`📊 GuavaGuard v${VERSION} Scan Summary`);
    console.log(`${'─'.repeat(54)}`);
    console.log(`   Scanned:      ${total}`);
    console.log(`   🟢 Clean:       ${this.stats.clean}`);
    console.log(`   🟢 Low Risk:    ${this.stats.low}`);
    console.log(`   🟡 Suspicious:  ${this.stats.suspicious}`);
    console.log(`   🔴 Malicious:   ${this.stats.malicious}`);
    console.log(`   Safety Rate:  ${total ? Math.round(safe / total * 100) : 0}%`);
    console.log(`${'═'.repeat(54)}`);

    if (this.stats.malicious > 0) {
      console.log(`\n⚠️  CRITICAL: ${this.stats.malicious} malicious skill(s) detected!`);
      console.log(`   Review findings with --verbose and remove if confirmed.`);
    } else if (this.stats.suspicious > 0) {
      console.log(`\n⚡ ${this.stats.suspicious} suspicious skill(s) found — review recommended.`);
    } else {
      console.log(`\n✅ All clear! No threats detected.`);
    }
  }

  toJSON() {
    return {
      timestamp: new Date().toISOString(),
      scanner: `GuavaGuard v${VERSION}`,
      mode: this.strict ? 'strict' : 'normal',
      stats: this.stats,
      thresholds: this.thresholds,
      findings: this.findings
    };
  }
}

// ===== CLI =====
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
  console.log(`
🍈🛡️  GuavaGuard v${VERSION} — Agent Skill Security Scanner

Usage: node guava-guard.js [scan-dir] [options]

Options:
  --verbose, -v       Detailed findings with categories and samples
  --json              Write JSON report to scan-dir/guava-guard-report.json
  --self-exclude      Skip scanning the guava-guard skill itself
  --strict            Lower detection thresholds (more sensitive)
  --summary-only      Only print the summary table
  --help, -h          Show this help

Ignore File (.guava-guard-ignore):
  Place in the scan directory. One entry per line.
  - Skill names to skip: my-trusted-skill
  - Pattern IDs to suppress: pattern:CRED_ENV_FILE
  - Comments: # this is a comment

Examples:
  node guava-guard.js ~/.openclaw/workspace/skills/ --verbose --self-exclude
  node guava-guard.js /path/to/clawhub/skills/ --strict --json
`);
  process.exit(0);
}

const verbose = args.includes('--verbose') || args.includes('-v');
const jsonOutput = args.includes('--json');
const selfExclude = args.includes('--self-exclude');
const strict = args.includes('--strict');
const summaryOnly = args.includes('--summary-only');
const scanDir = args.find(a => !a.startsWith('-')) || process.cwd();

const guard = new GuavaGuard({ verbose, selfExclude, strict, summaryOnly });
guard.scanDirectory(scanDir);

if (jsonOutput) {
  const outPath = path.join(scanDir, 'guava-guard-report.json');
  fs.writeFileSync(outPath, JSON.stringify(guard.toJSON(), null, 2));
  console.log(`\n📄 JSON report: ${outPath}`);
}

process.exit(guard.stats.malicious > 0 ? 1 : 0);
