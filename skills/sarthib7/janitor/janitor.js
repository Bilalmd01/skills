/**
 * Janitor - Lightweight AI Agent Cleanup Skill for ClawHub.ai
 *
 * Minimal version with core cleanup features.
 * For advanced features, see: https://github.com/openclaw/janitor
 */

const fs = require('fs');
const path = require('path');
const os = require('os');

class Janitor {
  constructor(config = {}) {
    this.config = {
      enabled: true,
      unusedFileAgeDays: 7,
      ...config
    };

    this.stats = {
      totalCleanups: 0,
      totalFilesDeleted: 0,
      totalSpaceSaved: 0
    };
  }

  /**
   * Main cleanup method - removes cache, logs, and temp files
   */
  async cleanup(workingDir = process.cwd()) {
    console.log('🧹 Janitor: Starting cleanup...');
    const startTime = Date.now();

    let filesDeleted = 0;
    let spaceSaved = 0;

    // Clean cache directories
    const cacheTargets = [
      path.join(workingDir, 'node_modules', '.cache'),
      path.join(workingDir, '.cache'),
      path.join(workingDir, 'dist'),
      path.join(workingDir, 'coverage'),
      path.join(workingDir, 'tmp')
    ];

    for (const target of cacheTargets) {
      if (fs.existsSync(target)) {
        const result = this._cleanDir(target, 2);
        filesDeleted += result.files;
        spaceSaved += result.bytes;
      }
    }

    // Clean .DS_Store files (macOS)
    const dsResult = this._cleanDSStore(workingDir);
    filesDeleted += dsResult.files;

    // Clean old logs
    const logResult = this._cleanOldLogs(workingDir);
    filesDeleted += logResult.files;
    spaceSaved += logResult.bytes;

    // Free memory
    this._freeMemory();

    // Update stats
    this.stats.totalCleanups++;
    this.stats.totalFilesDeleted += filesDeleted;
    this.stats.totalSpaceSaved += spaceSaved;

    const duration = Date.now() - startTime;
    const result = {
      filesDeleted,
      spaceSaved: this._formatBytes(spaceSaved),
      duration: `${duration}ms`,
      memoryFreed: true
    };

    console.log(`✅ Cleanup complete: ${filesDeleted} files, ${result.spaceSaved} saved`);
    return result;
  }

  /**
   * Clean directory recursively (limited depth for safety)
   */
  _cleanDir(dirPath, maxDepth = 2, currentDepth = 0) {
    let filesDeleted = 0;
    let bytesFreed = 0;

    if (currentDepth >= maxDepth || !fs.existsSync(dirPath)) {
      return { files: 0, bytes: 0 };
    }

    try {
      const files = fs.readdirSync(dirPath);

      for (const file of files) {
        const filePath = path.join(dirPath, file);

        try {
          const stats = fs.statSync(filePath);

          if (stats.isFile()) {
            bytesFreed += stats.size;
            fs.unlinkSync(filePath);
            filesDeleted++;
          } else if (stats.isDirectory()) {
            const result = this._cleanDir(filePath, maxDepth, currentDepth + 1);
            filesDeleted += result.files;
            bytesFreed += result.bytes;

            try {
              fs.rmdirSync(filePath);
            } catch (e) {
              // Directory not empty, skip
            }
          }
        } catch (e) {
          continue;
        }
      }
    } catch (e) {
      // Directory access error, skip
    }

    return { files: filesDeleted, bytes: bytesFreed };
  }

  /**
   * Clean .DS_Store files (macOS metadata)
   */
  _cleanDSStore(baseDir) {
    let filesDeleted = 0;

    const findAndDelete = (dir, depth = 0) => {
      if (depth > 3) return;

      try {
        const files = fs.readdirSync(dir);

        for (const file of files) {
          const filePath = path.join(dir, file);

          if (file === '.DS_Store') {
            try {
              fs.unlinkSync(filePath);
              filesDeleted++;
            } catch (e) {}
          } else {
            try {
              const stats = fs.statSync(filePath);
              if (stats.isDirectory() && !this._isProtected(filePath)) {
                findAndDelete(filePath, depth + 1);
              }
            } catch (e) {}
          }
        }
      } catch (e) {}
    };

    findAndDelete(baseDir);
    return { files: filesDeleted };
  }

  /**
   * Clean old log files (>7 days)
   */
  _cleanOldLogs(baseDir) {
    let filesDeleted = 0;
    let bytesFreed = 0;
    const maxAgeDays = 7;

    const searchLogs = (dir, depth = 0) => {
      if (depth > 2) return;

      try {
        const files = fs.readdirSync(dir);

        for (const file of files) {
          const filePath = path.join(dir, file);

          if (file.endsWith('.log')) {
            try {
              const stats = fs.statSync(filePath);
              const ageMs = Date.now() - stats.mtime.getTime();
              const ageDays = ageMs / (1000 * 60 * 60 * 24);

              if (ageDays > maxAgeDays) {
                bytesFreed += stats.size;
                fs.unlinkSync(filePath);
                filesDeleted++;
              }
            } catch (e) {}
          } else {
            try {
              const stats = fs.statSync(filePath);
              if (stats.isDirectory() && !this._isProtected(filePath)) {
                searchLogs(filePath, depth + 1);
              }
            } catch (e) {}
          }
        }
      } catch (e) {}
    };

    searchLogs(baseDir);
    return { files: filesDeleted, bytes: bytesFreed };
  }

  /**
   * Check if path is protected (should not delete)
   */
  _isProtected(filePath) {
    const protectedPaths = [
      'node_modules',
      '.git',
      'src',
      'package.json',
      'README.md',
      '.env'
    ];

    return protectedPaths.some(name => filePath.includes(name));
  }

  /**
   * Free up memory
   */
  _freeMemory() {
    if (global.gc) {
      global.gc();
      console.log('   🗑️  Memory freed');
    }
  }

  /**
   * Format bytes to human-readable
   */
  _formatBytes(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
  }

  /**
   * Get current stats
   */
  getStats() {
    const memUsed = process.memoryUsage();
    return {
      totalCleanups: this.stats.totalCleanups,
      totalFilesDeleted: this.stats.totalFilesDeleted,
      totalSpaceSaved: this._formatBytes(this.stats.totalSpaceSaved),
      memoryUsage: {
        heapUsed: this._formatBytes(memUsed.heapUsed),
        heapTotal: this._formatBytes(memUsed.heapTotal)
      }
    };
  }

  /**
   * Generate report
   */
  async report() {
    const stats = this.getStats();

    console.log('\n📊 Janitor Report:');
    console.log(`   Total Cleanups: ${stats.totalCleanups}`);
    console.log(`   Files Deleted: ${stats.totalFilesDeleted}`);
    console.log(`   Space Saved: ${stats.totalSpaceSaved}`);
    console.log(`   Memory (Heap): ${stats.memoryUsage.heapUsed}`);
    console.log('\n   💡 For advanced features (backup, scheduling, etc.):');
    console.log('      https://github.com/openclaw/janitor\n');

    return {
      timestamp: new Date().toISOString(),
      status: 'healthy',
      stats
    };
  }
}

module.exports = Janitor;
