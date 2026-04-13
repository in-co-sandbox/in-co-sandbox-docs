const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const MDX_ROOT = path.join(ROOT, 'api-reference', 'gst', 'compliance', 'endpoints', 'taxpayer');
const DATA_ROOT = path.join(ROOT, 'data', 'gst', 'schema', 'request', 'taxpayer');
const REPORT_FILE = path.join(MDX_ROOT, 'schema-status-report.md');
const PORTAL_BASE = 'https://developer.gst.gov.in/pages/apiportal/data';
const RAW_BASE = 'https://raw.githubusercontent.com/in-co-sandbox/in-co-sandbox-docs/refs/heads/main/';

const VERSIONS = {
  GSTR1: 'v4.1',
  RETURNS: 'v1.1',
  RETURNS_PREFERENCE: 'v1.0',
  GSTR2A: 'v2.0',
  GSTR2A_ECOM: 'v2.2',
  GSTR2B: 'v4.0',
  EINVOICE: 'v1.0',
  GSTR3: 'v6.0',
  GSTR9: 'v1.3',
  IMS: 'v1.0',
  IMS_SUPPLIER: 'v1.0',
  LEDGER: 'v0.3',
  TAX_LIABILITY_LEDGER: 'v1.0',
};

const GSTR1_TITLES = {
  at: 'GSTR1 - Get AT',
  ata: 'GSTR1 - Get ATA',
  b2b: 'GSTR1 - Get B2B Invoices',
  b2ba: 'GSTR1 - Get B2BA Invoices',
  b2cl: 'GSTR1 - Get B2CL Invoices',
  b2cla: 'GSTR1 - Get B2CLA Invoices',
  b2cs: 'GSTR1 - Get B2CS Invoices',
  b2csa: 'GSTR1 - Get B2CSA Invoices',
  cdnr: 'GSTR1 - Get CDNR Invoices',
  cdnra: 'GSTR1 - Get CDNRA Invoices',
  cdnur: 'GSTR1 - Get CDNUR Invoices',
  cdnura: 'GSTR1 - Get CDNURA Invoices',
  doc_issue: 'GSTR1 - Get Doc Issued',
  ecom: 'GSTR1 - Get ECOM Invoices',
  ecoma: 'GSTR1 - Get ECOMA Invoices',
  exp: 'GSTR1 - Get EXP',
  expa: 'GSTR1 - Get EXPA',
  get_hsn: 'GSTR1 - Get HSN Summary details',
  nil: 'GSTR1 - Get Nil Rated Supplies',
  supeco: 'GSTR1 - Get SUPECO Details',
  supecoa: 'GSTR1 - Get SUPECOA Details',
  txp: 'GSTR1 - Get TXP',
  txpa: 'GSTR1 - Get TXPA',
};

const GSTR2A_TITLES = {
  amdhist: 'GSTR2A - Get AMDHIST',
  b2b: 'GSTR2A - Get B2B Invoices',
  b2ba: 'GSTR2A - Get B2BA Invoices',
  cdn: 'GSTR2A - Get CDN Invoices',
  cdna: 'GSTR2A - Get CDNA Invoices',
  document: 'GSTR2A - Get All Details',
  ecom: 'GSTR2A - Get ECOM Invoices',
  ecoma: 'GSTR2A - Get ECOMA Invoices',
  impg: 'GSTR2A - Get IMPG',
  impgsez: 'GSTR2A - Get IMPGSEZ',
  isd: 'GSTR2A - Get ISD Credit',
  tcs: 'GSTR2A - Get TCS Credit',
  tds: 'GSTR2A - Get TDS Credit',
};

const IMS_TITLES = {
  'added-back-liabilities': 'IMS - Get Added Back Liability Records',
  invoice_count: 'IMS - Get Invoice Count',
  invoices: 'IMS - Get Invoices',
  sales: 'IMS - Get Supplier Invoices API',
  status: 'IMS - Get IMS Request Status',
};

const LEDGER_TITLES = {
  cash_itc_balance_ledger: 'Get Cash ITC Balance',
  cash_ledger: 'Get Cash Ledger Details',
  itc_ledger: 'Get ITC Ledger Details',
  return_liability_ledger: 'Get Liability Ledger Details For Return Liability',
};

const EXPLICIT_MAPPINGS = {
  'common/get_filing_preference.mdx': {
    moduleFolder: 'Returns',
    apiName: 'All - GET PREFERENCE',
    version: VERSIONS.RETURNS_PREFERENCE,
  },
  'common/save_filing_preference.mdx': {
    moduleFolder: 'Returns',
    apiName: 'All - SAVE PREFERENCE',
    version: VERSIONS.RETURNS_PREFERENCE,
  },
  'common/gst_return_status.mdx': {
    moduleFolder: 'Returns',
    apiName: 'All - Get Return Status',
    version: VERSIONS.RETURNS,
  },
  'e-invoice/e_invoice.mdx': {
    moduleFolder: 'E-Invoice',
    apiName: 'Get IRN Details',
    version: VERSIONS.EINVOICE,
  },
  'gstr-2b/document.mdx': {
    moduleFolder: 'Returns',
    apiName: 'GSTR2B - Get All Details',
    version: VERSIONS.GSTR2B,
  },
  'gstr-2b/regenerate_gstr_2b.mdx': {
    moduleFolder: 'Returns',
    apiName: 'GSTR2B - Generate 2B On Demand API',
    version: VERSIONS.GSTR2B,
  },
  'gstr-1/file/file.mdx': {
    moduleFolder: 'Returns',
    apiName: 'GSTR1 - File Gstr1',
    version: VERSIONS.GSTR1,
  },
  'gstr-1/file/new_proceed.mdx': {
    moduleFolder: 'Returns',
    apiName: 'All - New Proceed to File(for GSTR6,GSTR5,GSTR1)',
    version: VERSIONS.RETURNS,
  },
  'gstr-1/file/reset.mdx': {
    moduleFolder: 'Returns',
    apiName: 'GSTR1 - Reset GSTR1',
    version: VERSIONS.GSTR1,
  },
  'gstr-2b/gstr_2b_regeneration_status.mdx': {
    moduleFolder: 'Returns',
    apiName: 'GSTR2B - Get 2B Gen Status API',
    version: VERSIONS.GSTR2B,
  },
  'gstr-3b/auto_liability_calc.mdx': {
    moduleFolder: 'Returns',
    apiName: 'GSTR3B - Get ITC Liability Auto Calc Details',
    version: VERSIONS.GSTR3,
  },
  'gstr-3b/gstr_3b_details.mdx': {
    moduleFolder: 'Returns',
    apiName: 'GSTR3B - Get GSTR3B Details',
    version: VERSIONS.GSTR3,
  },
  'gstr-9/auto_calculated_details.mdx': {
    moduleFolder: 'Returns',
    apiName: 'GSTR9 - Get Autocalculated Details',
    version: VERSIONS.GSTR9,
  },
  'gstr-9/file.mdx': {
    moduleFolder: 'Returns',
    apiName: 'GSTR9 - File GSTR9',
    version: VERSIONS.GSTR9,
  },
  'gstr-9/gstr_9_details.mdx': {
    moduleFolder: 'Returns',
    apiName: 'GSTR9 - Get Details',
    version: VERSIONS.GSTR9,
  },
  'gstr-9/proceed.mdx': {
    moduleFolder: 'Returns',
    apiName: 'All - Proceed to File',
    version: VERSIONS.RETURNS,
  },
  'gstr-9/save.mdx': {
    moduleFolder: 'Returns',
    apiName: 'GSTR9 - Save GSTR9 data',
    version: VERSIONS.GSTR9,
  },
  'gstr-9/section_8a_details.mdx': {
    moduleFolder: 'Returns',
    apiName: 'GSTR9 - Get 8A Details',
    version: VERSIONS.GSTR9,
  },
  'invoices/reset.mdx': {
    moduleFolder: 'Returns',
    apiName: 'IMS - Reset IMS Action',
    version: VERSIONS.IMS,
  },
  'invoices/save.mdx': {
    moduleFolder: 'Returns',
    apiName: 'IMS - Save IMS Action',
    version: VERSIONS.IMS,
  },
};

const SKIPPED_FILES = {
  'e-invoice/list_purchase_invoices_job_status.mdx': 'No exact GST portal API match found for this job-status endpoint.',
  'e-invoice/list_sales_invoices_job_status.mdx': 'No exact GST portal API match found for this job-status endpoint.',
  'gstr-2a/document.mdx': 'No matching GST portal response schema asset is published for this endpoint.',
};

function walk(dir) {
  const files = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const fullPath = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      files.push(...walk(fullPath));
    } else if (entry.name.endsWith('.mdx')) {
      files.push(fullPath);
    }
  }
  return files;
}

function toPosix(inputPath) {
  return inputPath.split(path.sep).join('/');
}

function parseArguments() {
  const options = {
    method: 'GET',
    scope: 'all',
    syncReport: false,
  };

  for (const arg of process.argv.slice(2)) {
    if (arg.startsWith('--method=')) {
      options.method = arg.split('=')[1].toUpperCase();
    } else if (arg.startsWith('--scope=')) {
      options.scope = arg.split('=')[1].toLowerCase();
    } else if (arg === '--sync-report') {
      options.syncReport = true;
    }
  }

  if (!['GET', 'POST'].includes(options.method)) {
    throw new Error(`Unsupported method filter: ${options.method}`);
  }

  if (!['all', 'report'].includes(options.scope)) {
    throw new Error(`Unsupported scope: ${options.scope}`);
  }

  return options;
}

function encodeSegment(segment) {
  return encodeURIComponent(segment).replace(/%2F/g, '/');
}

function getRelativeMdxPath(filePath) {
  return toPosix(path.relative(MDX_ROOT, filePath));
}

function getMethodFromContent(content) {
  const openapiMatch = content.match(/^openapi:\s*'.*? (GET|POST|PUT|PATCH|DELETE) .+?'$/m);
  return openapiMatch ? openapiMatch[1] : null;
}

function getSchemaType(method) {
  return method === 'GET' ? 'response' : 'request';
}

function hasSchemaCard(content, schemaType) {
  const heading = schemaType === 'response' ? 'Response body schema' : 'Request body schema';
  return new RegExp(`## ${heading}[\\s\\S]*?<CardGroup>`, 'm').test(content);
}

function getPortalMapping(relativePath) {
  if (EXPLICIT_MAPPINGS[relativePath]) {
    return EXPLICIT_MAPPINGS[relativePath];
  }

  const parts = relativePath.split('/');
  const fileName = path.basename(relativePath, '.mdx');

  if (relativePath.startsWith('gstr-1/documents/')) {
    return {
      moduleFolder: 'Returns',
      apiName: GSTR1_TITLES[fileName],
      version: VERSIONS.GSTR1,
    };
  }

  if (relativePath.startsWith('gstr-2a/')) {
    return {
      moduleFolder: 'Returns',
      apiName: GSTR2A_TITLES[fileName],
      version: fileName === 'ecom' || fileName === 'ecoma' ? VERSIONS.GSTR2A_ECOM : VERSIONS.GSTR2A,
    };
  }

  if (relativePath.startsWith('invoices/')) {
    return {
      moduleFolder: 'Returns',
      apiName: IMS_TITLES[fileName],
      version: fileName === 'sales' ? VERSIONS.IMS_SUPPLIER : VERSIONS.IMS,
    };
  }

  if (relativePath.startsWith('ledgers/')) {
    return {
      moduleFolder: 'Ledger',
      apiName: LEDGER_TITLES[fileName],
      version: fileName === 'return_liability_ledger' ? VERSIONS.TAX_LIABILITY_LEDGER : VERSIONS.LEDGER,
    };
  }

  if (parts[0] === 'e-invoice' && fileName === 'e_invoice') {
    return {
      moduleFolder: 'E-Invoice',
      apiName: 'Get IRN Details',
      version: VERSIONS.EINVOICE,
    };
  }

  return null;
}

function getSchemaCard(schemaType, href) {
  const heading = schemaType === 'response' ? 'Response body schema' : 'Request body schema';
  const title = schemaType === 'response' ? 'View response body schema' : 'View request body schema';

  return [
    `## ${heading}`,
    '',
    '<CardGroup>',
    '  <Card',
    `    title="${title}"`,
    '    icon="code"',
    `    href="${href}"`,
    '    arrow="true"',
    '    horizontal',
    '  >',
    '  </Card>',
    '</CardGroup>',
  ].join('\n');
}

function insertSchemaCard(content, schemaType, href) {
  const heading = schemaType === 'response' ? 'Response body schema' : 'Request body schema';
  if (content.includes(`## ${heading}`)) {
    return content;
  }

  const card = getSchemaCard(schemaType, href);
  const frontmatterMatch = content.match(/^---\r?\n[\s\S]*?\r?\n---\r?\n?/);

  if (!frontmatterMatch) {
    return `${card}\n\n${content}`;
  }

  const frontmatter = frontmatterMatch[0];
  const rest = content.slice(frontmatter.length).replace(/^\r?\n/, '');
  return `${frontmatter}${card}\n\n${rest}`;
}

async function fetchWithRetry(url, retries = 3) {
  let lastError = null;
  for (let attempt = 1; attempt <= retries; attempt += 1) {
    try {
      return await fetch(url);
    } catch (error) {
      lastError = error;
    }
  }
  throw lastError;
}

async function fetchPortalAsset(url, expectedType) {
  const response = await fetchWithRetry(url);
  if (!response.ok) {
    return null;
  }

  const contentType = response.headers.get('content-type') || '';
  const buffer = Buffer.from(await response.arrayBuffer());

  if (expectedType === 'json') {
    const body = buffer.toString('utf8');
    try {
      JSON.parse(body);
    } catch {
      return null;
    }
    return { buffer, contentType };
  }

  if (!contentType.includes('sheet') && !contentType.includes('excel') && !url.endsWith('.xlsx')) {
    return null;
  }

  return { buffer, contentType };
}

async function downloadSchemaAsset(mapping, schemaType) {
  const basePath = [PORTAL_BASE, encodeSegment(mapping.moduleFolder), encodeSegment(mapping.apiName), encodeSegment(mapping.version)].join('/');
  const jsonUrl = `${basePath}/${encodeSegment(`${mapping.apiName} ${schemaType}_schema.json`)}`;
  const jsonResult = await fetchPortalAsset(jsonUrl, 'json');
  if (jsonResult) {
    return { extension: '.json', sourceUrl: jsonUrl, buffer: jsonResult.buffer };
  }

  const excelUrl = `${basePath}/${encodeSegment(`${mapping.apiName} attributes.xlsx`)}`;
  const excelResult = await fetchPortalAsset(excelUrl, 'xlsx');
  if (excelResult) {
    return { extension: '.xlsx', sourceUrl: excelUrl, buffer: excelResult.buffer };
  }

  return null;
}

function writeSchemaFile(relativePath, extension, buffer) {
  const outputRelativePath = path.join('data', 'gst', 'schema', 'request', 'taxpayer', relativePath.replace(/\.mdx$/, extension));
  const outputPath = path.join(ROOT, outputRelativePath);
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, buffer);
  return toPosix(outputRelativePath);
}

function getFilesWithoutSchemaCard(methodFilter) {
  return walk(MDX_ROOT).filter((filePath) => {
    const content = fs.readFileSync(filePath, 'utf8');
    const method = getMethodFromContent(content);
    if (!method) {
      return false;
    }

    if (methodFilter === 'GET' && method !== 'GET') {
      return false;
    }

    if (methodFilter === 'POST' && method !== 'POST' && method !== 'PUT') {
      return false;
    }

    return !hasSchemaCard(content, getSchemaType(method));
  });
}

function getMissingFilesFromReport(methodFilter) {
  const report = fs.readFileSync(REPORT_FILE, 'utf8');
  const files = [];

  for (const line of report.split(/\r?\n/)) {
    const match = line.match(/^\|\s*(GET|POST|PUT|PATCH|DELETE)\s*\|\s*`([^`]+)`\s*\|\s*([^|]+?)\s*\|\s*(Present|Missing)\s*\|$/);
    if (!match) {
      continue;
    }

    const [, method, filePath, , status] = match;
    if (status !== 'Missing') {
      continue;
    }

    if (methodFilter === 'GET' && method !== 'GET') {
      continue;
    }

    if (methodFilter === 'POST' && method !== 'POST' && method !== 'PUT') {
      continue;
    }

    const absolutePath = path.join(ROOT, filePath.replace(/\//g, path.sep));
    if (fs.existsSync(absolutePath)) {
      files.push(absolutePath);
    }
  }

  return files;
}

function syncReportFile() {
  const lines = fs.readFileSync(REPORT_FILE, 'utf8').split(/\r?\n/);
  let presentCount = 0;
  let missingCount = 0;

  const updatedLines = lines.map((line) => {
    const match = line.match(/^\|\s*(GET|POST|PUT|PATCH|DELETE)\s*\|\s*`([^`]+)`\s*\|\s*([^|]+?)\s*\|\s*(Present|Missing)\s*\|$/);
    if (!match) {
      return line;
    }

    const [, method, filePath, expectedSchema] = match;
    const absolutePath = path.join(ROOT, filePath.replace(/\//g, path.sep));

    let nextStatus = 'Missing';
    if (fs.existsSync(absolutePath)) {
      const content = fs.readFileSync(absolutePath, 'utf8');
      nextStatus = hasSchemaCard(content, getSchemaType(method)) ? 'Present' : 'Missing';
    }

    if (nextStatus === 'Present') {
      presentCount += 1;
    } else {
      missingCount += 1;
    }

    return `| ${method} | \`${filePath}\` | ${expectedSchema.trim()} | ${nextStatus} |`;
  }).map((line) => {
    if (/^\| Present \|/.test(line)) {
      return `| Present | ${presentCount} |`;
    }

    if (/^\| Missing \|/.test(line)) {
      return `| Missing | ${missingCount} |`;
    }

    return line;
  });

  fs.writeFileSync(REPORT_FILE, `${updatedLines.join('\n')}\n`, 'utf8');
}

async function main() {
  const options = parseArguments();
  const files = options.scope === 'report'
    ? getMissingFilesFromReport(options.method)
    : getFilesWithoutSchemaCard(options.method);
  const updated = [];
  const skipped = [];
  const failed = [];

  for (const filePath of files) {
    const relativePath = getRelativeMdxPath(filePath);

    try {
      const content = fs.readFileSync(filePath, 'utf8');
      const method = getMethodFromContent(content);
      const schemaType = getSchemaType(method);

      if (schemaType === 'response' && SKIPPED_FILES[relativePath]) {
        skipped.push({ relativePath, reason: SKIPPED_FILES[relativePath] });
        continue;
      }

      const mapping = getPortalMapping(relativePath);
      if (!mapping || !mapping.apiName) {
        failed.push({ relativePath, reason: 'No portal mapping configured.' });
        continue;
      }

      const asset = await downloadSchemaAsset(mapping, schemaType);
      if (!asset) {
        failed.push({ relativePath, reason: `No ${schemaType} schema JSON or Excel asset found on the GST portal.`, mapping });
        continue;
      }

      const schemaRelativePath = writeSchemaFile(relativePath, asset.extension, asset.buffer);
      const href = `${RAW_BASE}${schemaRelativePath}`;

      const updatedContent = insertSchemaCard(content, schemaType, href);
      fs.writeFileSync(filePath, updatedContent, 'utf8');

      updated.push({
        relativePath,
        method,
        schemaType,
        apiName: mapping.apiName,
        version: mapping.version,
        asset: schemaRelativePath,
        sourceUrl: asset.sourceUrl,
      });
    } catch (error) {
      failed.push({ relativePath, reason: error.message });
    }
  }

  if (options.syncReport) {
    syncReportFile();
  }

  console.log(JSON.stringify({ updated, skipped, failed }, null, 2));
  if (failed.length > 0) {
    process.exitCode = 1;
  }
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});