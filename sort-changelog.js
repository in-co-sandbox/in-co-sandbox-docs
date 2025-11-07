#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Get file path from command line argument
const filePath = process.argv[2];

if (!filePath) {
  console.log('Usage: node sort-changelog.js <file.mdx>');
  console.log('   or: node sort-changelog.js --all  (sorts all changelog files including changelog.mdx)');
  process.exit(1);
}

function sortSimpleChangelog(file) {
  // For monthly changelog files (changelog/2024/november.mdx)
  const content = fs.readFileSync(file, 'utf-8');
  
  // Extract frontmatter and updates
  const frontmatterMatch = content.match(/^---\n[\s\S]*?\n---\n/);
  const frontmatter = frontmatterMatch ? frontmatterMatch[0] : '';
  const updates = content.slice(frontmatter.length).match(/<Update[\s\S]*?<\/Update>/g) || [];
  
  if (updates.length === 0) {
    console.log(`⚠️  No <Update> blocks found in ${path.basename(file)}`);
    return;
  }
  
  // Sort updates by date (extract day number from label)
  const sorted = updates.sort((a, b) => {
    const dateA = parseInt(a.match(/label="[A-Z][a-z]+ (\d+)(?:st|nd|rd|th)/)?.[1] || 0);
    const dateB = parseInt(b.match(/label="[A-Z][a-z]+ (\d+)(?:st|nd|rd|th)/)?.[1] || 0);
    return dateB - dateA; // Descending (newest first)
  });
  
  // Write back
  fs.writeFileSync(file, frontmatter + '\n' + sorted.join('\n\n') + '\n');
  console.log(`✅ Sorted ${sorted.length} updates in ${path.basename(file)} (newest first)`);
}

function sortMainChangelog(file) {
  // For the main changelog.mdx file with year/month sections
  const content = fs.readFileSync(file, 'utf-8');
  
  // Extract frontmatter
  const frontmatterMatch = content.match(/^---\n[\s\S]*?\n---\n/);
  const frontmatter = frontmatterMatch ? frontmatterMatch[0] : '';
  const afterFrontmatter = content.slice(frontmatter.length);
  
  // Split by year headers (## YYYY)
  const yearSections = afterFrontmatter.split(/(?=^## \d{4}$)/m);
  
  let totalUpdates = 0;
  const processedSections = yearSections.map(yearSection => {
    if (!yearSection.trim()) return yearSection;
    
    // Split by month headers (### Month)
    const monthSections = yearSection.split(/(?=^### [A-Z])/m);
    
    const processedMonths = monthSections.map(monthSection => {
      if (!monthSection.includes('<Update')) return monthSection;
      
      // Extract updates from this month
      const updates = monthSection.match(/<Update[\s\S]*?<\/Update>/g) || [];
      if (updates.length === 0) return monthSection;
      
      totalUpdates += updates.length;
      
      // Sort updates by date
      const sorted = updates.sort((a, b) => {
        const dateA = parseInt(a.match(/label="[A-Z][a-z]+ (\d+)(?:st|nd|rd|th)/)?.[1] || 0);
        const dateB = parseInt(b.match(/label="[A-Z][a-z]+ (\d+)(?:st|nd|rd|th)/)?.[1] || 0);
        return dateB - dateA; // Descending (newest first)
      });
      
      // Rebuild month section with sorted updates
      const monthHeaderMatch = monthSection.match(/^### [A-Z][a-z]+\n/);
      const monthHeader = monthHeaderMatch ? monthHeaderMatch[0] : '';
      
      return monthHeader + sorted.join('\n\n') + '\n';
    });
    
    return processedMonths.join('');
  });
  
  // Write back
  fs.writeFileSync(file, frontmatter + processedSections.join(''));
  console.log(`✅ Sorted ${totalUpdates} updates in ${path.basename(file)} (newest first per month)`);
}

function sortChangelogFile(file) {
  try {
    // Check if this is the main changelog.mdx
    if (path.basename(file) === 'changelog.mdx') {
      sortMainChangelog(file);
    } else {
      sortSimpleChangelog(file);
    }
  } catch (error) {
    console.error(`❌ Error processing ${file}:`, error.message);
  }
}

function getAllChangelogFiles() {
  const files = [];
  
  // Add main changelog.mdx first
  if (fs.existsSync('changelog.mdx')) {
    files.push('changelog.mdx');
  }
  
  // Add monthly changelog files
  const years = ['2022', '2023', '2024'];
  years.forEach(year => {
    const dir = `changelog/${year}`;
    if (fs.existsSync(dir)) {
      const yearFiles = fs.readdirSync(dir)
        .filter(f => f.endsWith('.mdx'))
        .map(f => `${dir}/${f}`);
      files.push(...yearFiles);
    }
  });
  
  return files;
}

// Handle --all flag
if (filePath === '--all') {
  const changelogFiles = getAllChangelogFiles();
  console.log(`📂 Found ${changelogFiles.length} changelog files\n`);
  changelogFiles.forEach(sortChangelogFile);
  console.log('\n🎉 All done!');
} else {
  // Single file
  sortChangelogFile(filePath);
}

