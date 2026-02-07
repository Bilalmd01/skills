/**
 * Janitor Skill - Example Usage
 */

const Janitor = require('./janitor');

async function example() {
  console.log('=== Janitor Skill Example ===\n');

  // Create janitor instance
  const janitor = new Janitor({
    enabled: true,
    unusedFileAgeDays: 7
  });

  // Example 1: Run cleanup
  console.log('1. Running cleanup...');
  const result = await janitor.cleanup();
  console.log('   Result:', result);
  console.log('');

  // Example 2: Get statistics
  console.log('2. Getting statistics...');
  const stats = janitor.getStats();
  console.log('   Stats:', stats);
  console.log('');

  // Example 3: Generate report
  console.log('3. Generating report...');
  await janitor.report();
  console.log('');

  console.log('=== Example Complete ===');
  console.log('\nFor more features, visit: https://github.com/openclaw/janitor');
}

// Run example
example().catch(console.error);
