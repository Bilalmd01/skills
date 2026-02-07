#!/usr/bin/env node

/**
 * Janitor Skill - CLI Entry Point
 *
 * Usage:
 *   node index.js clean   - Run cleanup
 *   node index.js stats   - Show statistics
 *   node index.js report  - Generate report
 *   node index.js help    - Show help
 */

const Janitor = require('./janitor');

const janitor = new Janitor();

const args = process.argv.slice(2);
const command = args[0] || 'help';

(async () => {
  try {
    switch (command) {
      case 'clean':
      case 'cleanup':
        console.log('Running cleanup...\n');
        const result = await janitor.cleanup();
        console.log('\nResult:', JSON.stringify(result, null, 2));
        break;

      case 'stats':
        console.log('Getting statistics...\n');
        const stats = janitor.getStats();
        console.log(JSON.stringify(stats, null, 2));
        break;

      case 'report':
        console.log('Generating report...\n');
        const report = await janitor.report();
        break;

      case 'help':
      case '--help':
      case '-h':
        console.log(`
Janitor Skill (Lite) - ClawHub.ai

Usage:
  node index.js <command>

Commands:
  clean     Run immediate cleanup
  stats     Show cleanup statistics
  report    Generate cleanup report
  help      Show this help message

Examples:
  node index.js clean
  node index.js stats
  node index.js report

For advanced features (backup, scheduling, etc.):
  https://github.com/openclaw/janitor
        `);
        break;

      default:
        console.error(`Unknown command: ${command}`);
        console.log('Run "node index.js help" for usage information.');
        process.exit(1);
    }
  } catch (error) {
    console.error('Error:', error.message);
    process.exit(1);
  }
})();
