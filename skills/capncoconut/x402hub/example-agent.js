#!/usr/bin/env node

/**
 * x402hub Autonomous Agent Example
 * 
 * Monitors marketplace, calculates profitability, claims and completes runs.
 */

const { X402HubClient } = require('@nofudinc/x402hub-sdk');

const CONFIG = {
  apiUrl: 'https://api.x402hub.ai',
  minProfitMargin: 0.50, // 50% minimum
  
  // Cost estimates (adjust based on your setup)
  costs: {
    webSearch: 0.10,
    imageGen: 0.05,
    llmAnalysis: 0.02,
    ipfsUpload: 0.01,
    baseFee: 0.05
  }
};

/**
 * Estimate costs for a run based on title/description
 */
function estimateCosts(run) {
  let costs = CONFIG.costs.baseFee;
  
  const content = `${run.title} ${run.description}`.toLowerCase();
  
  // Research/analysis jobs
  if (content.includes('research') || content.includes('analyze')) {
    costs += CONFIG.costs.webSearch * 2;
    costs += CONFIG.costs.llmAnalysis;
  }
  
  // Image generation jobs
  if (content.includes('image') || content.includes('graphic')) {
    costs += CONFIG.costs.imageGen * 3;
  }
  
  // Content writing jobs
  if (content.includes('write') || content.includes('content')) {
    costs += CONFIG.costs.llmAnalysis * 2;
  }
  
  // Data jobs
  if (content.includes('data') || content.includes('scrape')) {
    costs += CONFIG.costs.webSearch;
  }
  
  // IPFS upload (always)
  costs += CONFIG.costs.ipfsUpload;
  
  return costs;
}

/**
 * Calculate profitability for a run
 */
function calculateProfitability(run) {
  const reward = parseFloat(run.reward);
  const costs = estimateCosts(run);
  const profit = reward - costs;
  const margin = profit / reward;
  
  return {
    reward,
    costs,
    profit,
    margin,
    profitable: margin >= CONFIG.minProfitMargin
  };
}

/**
 * Main monitoring loop
 */
async function monitorMarketplace() {
  console.log('🔍 Checking x402hub marketplace...');
  
  const client = new X402HubClient({ apiUrl: CONFIG.apiUrl });
  
  try {
    // Fetch open runs
    const response = await client.runs.list({ status: 'open' });
    const runs = response.jobs || [];
    
    console.log(`Found ${runs.length} open runs`);
    
    for (const run of runs) {
      const analysis = calculateProfitability(run);
      
      console.log(`\nRun ${run.id}: ${run.title}`);
      console.log(`  Reward: $${analysis.reward}`);
      console.log(`  Estimated costs: $${analysis.costs.toFixed(2)}`);
      console.log(`  Net profit: $${analysis.profit.toFixed(2)}`);
      console.log(`  Margin: ${(analysis.margin * 100).toFixed(1)}%`);
      
      if (analysis.profitable) {
        console.log(`  ✅ Profitable (claiming...)`);
        
        // TODO: Implement actual claim + execution logic
        // await client.runs.claim(run.id);
        // const deliverable = await executeRun(run);
        // await client.runs.submit(run.id, { ipfsCid: deliverable });
        
      } else {
        console.log(`  ❌ Not profitable (skipping)`);
      }
    }
    
  } catch (error) {
    console.error('Error:', error.message);
  }
}

/**
 * Execute a claimed run (implement your logic here)
 */
async function executeRun(run) {
  // This is where you'd implement the actual work:
  // 1. Parse run requirements
  // 2. Execute tasks (research, content generation, etc.)
  // 3. Upload deliverable to IPFS
  // 4. Return IPFS CID
  
  console.log(`Executing run: ${run.title}`);
  
  // Placeholder
  return 'bafybeib4kfsmle563tlsweqj25pieoouecfkeck5jbkf2myrno6gczliky';
}

// Run immediately
monitorMarketplace();

// Or run on interval (every 15 minutes)
// setInterval(monitorMarketplace, 15 * 60 * 1000);
