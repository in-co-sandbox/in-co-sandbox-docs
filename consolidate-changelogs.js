#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Month name to number mapping
const monthOrder = {
  'january': 1, 'february': 2, 'march': 3, 'april': 4,
  'may': 5, 'june': 6, 'july': 7, 'august': 8,
  'september': 9, 'october': 10, 'november': 11, 'december': 12
};

function capitalizeMonth(month) {
  return month.charAt(0).toUpperCase() + month.slice(1);
}

function extractUpdatesFromFile(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const updates = content.match(/<Update[\s\S]*?<\/Update>/g) || [];
  return updates;
}

function getAllMonthlyChangelogs() {
  const changelogs = {};
  const years = ['2022', '2023', '2024', '2025'];
  
  years.forEach(year => {
    const dir = `changelog/${year}`;
    if (!fs.existsSync(dir)) return;
    
    const files = fs.readdirSync(dir).filter(f => f.endsWith('.mdx'));
    
    files.forEach(file => {
      const monthName = path.basename(file, '.mdx').toLowerCase();
      const filePath = `${dir}/${file}`;
      const updates = extractUpdatesFromFile(filePath);
      
      if (updates.length > 0) {
        if (!changelogs[year]) changelogs[year] = {};
        changelogs[year][monthName] = updates;
      }
    });
  });
  
  return changelogs;
}

function sortUpdatesByDate(updates) {
  return updates.sort((a, b) => {
    const dateA = parseInt(a.match(/label="[A-Z][a-z]+ (\d+)(?:st|nd|rd|th)/)?.[1] || 0);
    const dateB = parseInt(b.match(/label="[A-Z][a-z]+ (\d+)(?:st|nd|rd|th)/)?.[1] || 0);
    return dateB - dateA; // Descending (newest first)
  });
}

function buildChangelogContent(changelogs) {
  const frontmatter = `---
title: "Changelog"
description: "Changelog for Sandbox APIs"
---
`;
  
  let content = frontmatter;
  
  // Sort years in descending order (newest first)
  const years = Object.keys(changelogs).sort((a, b) => parseInt(b) - parseInt(a));
  
  years.forEach(year => {
    content += `## ${year}\n`;
    
    // Sort months in descending order (newest first)
    const months = Object.keys(changelogs[year]).sort((a, b) => {
      return monthOrder[b] - monthOrder[a];
    });
    
    months.forEach(month => {
      content += `### ${capitalizeMonth(month)}\n`;
      
      const updates = sortUpdatesByDate(changelogs[year][month]);
      content += updates.join('\n\n') + '\n\n';
    });
  });
  
  return content;
}

function consolidateChangelogs() {
  console.log('📂 Scanning for monthly changelog files...\n');
  
  const changelogs = getAllMonthlyChangelogs();
  
  let totalUpdates = 0;
  let totalMonths = 0;
  
  Object.keys(changelogs).forEach(year => {
    const months = Object.keys(changelogs[year]);
    totalMonths += months.length;
    months.forEach(month => {
      const updateCount = changelogs[year][month].length;
      totalUpdates += updateCount;
      console.log(`  ✓ ${year}/${month}: ${updateCount} updates`);
    });
  });
  
  console.log(`\n📊 Summary:`);
  console.log(`   - ${Object.keys(changelogs).length} years`);
  console.log(`   - ${totalMonths} months`);
  console.log(`   - ${totalUpdates} total updates\n`);
  
  console.log('🔨 Building consolidated changelog.mdx...');
  const content = buildChangelogContent(changelogs);
  
  // Backup existing changelog.mdx if it exists
  if (fs.existsSync('changelog.mdx')) {
    const backupName = `changelog.mdx.backup.${Date.now()}`;
    fs.copyFileSync('changelog.mdx', backupName);
    console.log(`📦 Backed up existing changelog.mdx to ${backupName}`);
  }
  
  fs.writeFileSync('changelog.mdx', content);
  console.log('✅ Successfully wrote changelog.mdx');
  console.log('\n🎉 Consolidation complete!');
}

// Run consolidation
consolidateChangelogs();

