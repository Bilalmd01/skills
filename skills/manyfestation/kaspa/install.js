#!/usr/bin/env node
/**
 * Kaspa Wallet CLI - Node.js Installer
 * Downloads official WASM SDK from https://github.com/kaspanet/rusty-kaspa/releases
 * Self-bootstrapping: auto-installs dependencies if missing
 */

import { existsSync, mkdirSync, rmSync, writeFileSync, readdirSync, renameSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { execSync } from 'child_process';
import { Readable } from 'stream';

const __dirname = dirname(fileURLToPath(import.meta.url));
const SDK_DIR = join(__dirname, 'wasm-sdk');
const GITHUB_API = 'https://api.github.com/repos/kaspanet/rusty-kaspa/releases/latest';

// Auto-install dependencies if missing
async function ensureDependencies() {
  try {
    await import('unzipper');
  } catch {
    console.log('Installing dependencies...');
    execSync('npm install', { cwd: __dirname, stdio: 'inherit' });
  }
}

async function main() {
  console.log('==========================================');
  console.log('  Kaspa Wallet CLI - Official SDK Setup');
  console.log('==========================================\n');

  try {
    // Ensure dependencies are installed
    await ensureDependencies();
    const { Extract } = await import('unzipper');

    // Step 1: Fetch release info
    console.log('[1/3] Fetching latest SDK release info...');
    const release = await fetch(GITHUB_API, {
      headers: { 'User-Agent': 'kaspa-wallet-installer' }
    }).then(r => r.json());

    const version = release.tag_name;
    const sdkUrl = `https://github.com/kaspanet/rusty-kaspa/releases/download/${version}/kaspa-wasm32-sdk-${version}.zip`;
    console.log(`  Version: ${version}`);
    console.log(`  URL: ${sdkUrl}`);

    // Step 2: Download SDK
    console.log('\n[2/3] Downloading official Kaspa WASM SDK...');
    const response = await fetch(sdkUrl);
    if (!response.ok) throw new Error(`Download failed: ${response.status}`);

    const contentLength = response.headers.get('content-length');
    const totalMB = contentLength ? (parseInt(contentLength) / 1024 / 1024).toFixed(1) : '?';
    console.log(`  Size: ${totalMB} MB`);

    // Step 3: Extract SDK
    console.log('\n[3/3] Extracting SDK...');

    // Remove old SDK
    if (existsSync(SDK_DIR)) {
      rmSync(SDK_DIR, { recursive: true, force: true });
    }
    mkdirSync(SDK_DIR, { recursive: true });

    // Convert web stream to Node.js stream and extract
    const nodeStream = Readable.fromWeb(response.body);
    await new Promise((resolve, reject) => {
      nodeStream
        .pipe(Extract({ path: SDK_DIR }))
        .on('close', resolve)
        .on('error', reject);
    });

    // Handle nested directory (zip extracts to kaspa-wasm32-sdk-vX.X.X/)
    const entries = readdirSync(SDK_DIR);
    const nestedDir = entries.find(e => e.startsWith('kaspa'));
    if (nestedDir) {
      const nestedPath = join(SDK_DIR, nestedDir);
      for (const file of readdirSync(nestedPath)) {
        renameSync(join(nestedPath, file), join(SDK_DIR, file));
      }
      rmSync(nestedPath, { recursive: true, force: true });
    }

    // Save version
    writeFileSync(join(SDK_DIR, 'VERSION'), version);

    // Verify
    const nodejsPath = join(SDK_DIR, 'nodejs', 'kaspa');
    if (existsSync(nodejsPath)) {
      console.log(`  Extracted to: ${SDK_DIR}`);
      console.log(`  Node.js bindings: ${nodejsPath}`);
    } else {
      console.log('  WARNING: nodejs/kaspa directory not found');
    }

    console.log('\n==========================================');
    console.log('  Installation Complete!');
    console.log('==========================================');
    console.log(`\nSDK Version: ${version}`);
    console.log(`SDK Location: ${SDK_DIR}`);
    console.log('\nUsage:');
    console.log('  ./kaswallet.sh help');
    console.log('  ./kaswallet.sh balance kaspa:...');
    console.log('  ./kaswallet.sh info\n');

  } catch (err) {
    console.error('\nERROR:', err.message);
    process.exit(1);
  }
}

main();
