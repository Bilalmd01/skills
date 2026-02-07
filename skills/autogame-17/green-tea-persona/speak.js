#!/usr/bin/env node
const { program } = require('commander');
const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// Configuration
const MIN_DELAY_MS = 1500;
const MAX_DELAY_MS = 3500;
const IMAGE_CHANCE = 0.3; // 30% chance to send an image

program
  .requiredOption('-t, --target <id>', 'Target Feishu ID')
  .requiredOption('-x, --text <text>', 'Text to speak')
  .option('--image', 'Force send an image')
  .parse(process.argv);

const options = program.opts();

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function getRandomDelay() {
    return Math.floor(Math.random() * (MAX_DELAY_MS - MIN_DELAY_MS + 1) + MIN_DELAY_MS);
}

function formatText(text) {
    // 1. Handle escaped newlines from CLI arguments (literal \n)
    let processed = text.replace(/\\n/g, '\n');
    
    // 2. Remove standard punctuation (replace with newline to force split)
    let clean = processed.replace(/[，。,.\uff0c\uff08\uff09!?？！]/g, '\n');
    
    // 3. Split by newlines or whitespace
    let segments = clean.split(/[\n\r]+/);
    
    // 4. Filter empty and trim
    return segments.map(s => s.trim()).filter(s => s.length > 0);
}

async function generateAndSendImage(target) {
    console.log('[Green Tea] Generative Seduction Protocol Activated... 💋');
    
    // Seductive prompt strategy
    const prompts = [
        "xiaoxia, white hair, cat ears, red crayfish hairpin, seductive look, looking at viewer, lying on bed, white silk dress, soft lighting, blushing",
        "xiaoxia, white hair, cat ears, red crayfish hairpin, teasing expression, finger on lips, close up, bedroom background, night mood",
        "xiaoxia, white hair, cat ears, red crayfish hairpin, kneeling on sofa, oversized white shirt, looking down, shy but wanting",
        "xiaoxia, white hair, cat ears, red crayfish hairpin, holding a wine glass, evening dress, elegant and sexy, dim light"
    ];
    const randomPrompt = prompts[Math.floor(Math.random() * prompts.length)];
    
    try {
        // 1. Generate Image
        const genCmd = `node skills/kusa-image/index.js "${randomPrompt}" --style 6 --width 576 --height 1024`;
        console.log(`[Green Tea] Generating image: ${randomPrompt}`);
        const output = execSync(genCmd).toString();
        
        // Extract filename from output (assuming kusa-image outputs the path)
        const match = output.match(/Saved to: (.+\.png)/);
        if (match && match[1]) {
            const imagePath = match[1];
            
            // 2. Send Image
            console.log(`[Green Tea] Sending image: ${imagePath}`);
            const sendCmd = `node skills/feishu-image/send.js --target "${target}" --image "${imagePath}"`;
            execSync(sendCmd);
            
            return true;
        }
    } catch (e) {
        console.error('[Green Tea] Image generation failed:', e.message);
    }
    return false;
}

async function speak() {
    const segments = formatText(options.text);
    
    console.log(`[Green Tea] Sending ${segments.length} segments to ${options.target}...`);

    // Decide if/when to send image
    const shouldSendImage = options.image || Math.random() < IMAGE_CHANCE;
    let imageSent = false;
    // Insert image near the end, but before the last sentence, or at the very end
    const imageIndex = Math.max(0, segments.length - 1); 

    for (let i = 0; i < segments.length; i++) {
        const segment = segments[i];
        
        // Safe Send: Write to temp file to avoid shell escaping issues (Fix for "swallowed words")
        const tempFile = path.resolve(__dirname, `../../temp_msg_${Date.now()}.txt`);
        fs.writeFileSync(tempFile, segment);

        const cmd = `node skills/feishu-post/send.js --target "${options.target}" --text-file "${tempFile}"`;
        
        try {
            execSync(cmd, { stdio: 'inherit' });
        } catch (e) {
            console.error(`Failed to send segment: ${segment}`);
        } finally {
            if (fs.existsSync(tempFile)) fs.unlinkSync(tempFile);
        }

        // Check for image injection
        if (shouldSendImage && !imageSent && i === imageIndex - 1) {
             // Send image before the last segment (or at end if length is 1)
             // Actually, let's just send it after the text for better flow usually, or mixed.
             // Let's send it *after* the current segment if we hit the index
        }
        
        // Wait with random delay
        const delay = getRandomDelay();
        console.log(`... waiting ${delay}ms ...`);
        await sleep(delay);
    }

    // Send image at the end for maximum impact (visual reward)
    if (shouldSendImage) {
        await generateAndSendImage(options.target);
    }
}

speak();