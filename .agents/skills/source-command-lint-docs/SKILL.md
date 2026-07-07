---
name: "source-command-lint-docs"
description: "Check documentation for broken links, Vale style errors, and OpenAPI spec validity. Fix linting issues found. Use when the user asks to lint, check for broken links, run Vale, or fix documentation errors."
---

# source-command-lint-docs

Use this skill when the user asks to run the migrated source command `lint-docs`.

## Command Template

Run `mint broken-links` and check the given git diff. For OpenAPI reference updates run `mint openapi-check`.

If the Vale CLI exists, run a Vale check on all changed files.

Make a plan to resolve any broken links or Vale errors.

For more details on the `mint` CLI, look at the details here:

```
mint <command>

Commands:
  mint dev                       initialize a local preview environment
  mint openapi-check <filename>  check if an OpenAPI spec is valid
  mint broken-links              check for invalid internal links
  mint rename <from> <to>        rename a file and update all internal link references
  mint update                    update the CLI to the latest version
  mint upgrade                   upgrade mint.json file to docs.json (current format)
  mint migrate-mdx               migrate MDX OpenAPI endpoint pages to x-mint extensions and docs.json
  mint ai [prompt]               Use ai to document a page
  mint version                   display the current version of the CLI and client                                 [aliases: v]

Options:
  -h, --help     Show help                                             [boolean]
  -v, --version  Show version number                                   [boolean]
```

For more information on the Vale CLI, look at the details here:

```
vale - A command-line linter for prose.

Usage: vale [options] [input...]
       vale myfile.md myfile1.md mydir1
       vale --output=JSON [input...]

Vale is a syntax-aware linter for prose built with speed and extensibility in
mind. It supports Markdown, AsciiDoc, reStructuredText, HTML, and more.

Flags:
 --config         A file path (--config='some/file/path/.vale.ini').    
 --ext            An extension to associate with stdin (--ext=.md).     
 --filter         An expression to filter rules by.                     
 --glob           A glob pattern (--glob='*.{md,txt}.')                 
 -h, --help       Print this help message.                              
 --minAlertLevel  The minimum level to display (--minAlertLevel=error). 
 --no-exit        Don't return a nonzero exit code on errors.           
 --output         An output style ("line", "JSON", or a template file). 
 -v, --version    Print the current version.                            

Commands:
 ls-config        Print the current configuration to stdout.             
 sync             Download and install external configuration sources.   
```
