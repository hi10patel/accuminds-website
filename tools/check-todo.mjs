// Lists every placeholder still waiting for real content.
//   node tools/check-todo.mjs        exits 1 while anything is open
// Looks for "TODO" text and data-todo / data-todo-slot attributes.
import { readdir, readFile } from 'node:fs/promises';
import { extname, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = fileURLToPath(new URL('..', import.meta.url));
const SKIP_DIRS = new Set(['.git', 'node_modules', 'design', 'tools', 'vendor', '.claude']);
const EXTS = new Set(['.html', '.js', '.xml', '.txt', '.json', '.webmanifest']);
const PATTERN = /TODO|data-todo/;

async function* walk(dir) {
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    if (entry.isDirectory()) {
      if (!SKIP_DIRS.has(entry.name)) yield* walk(join(dir, entry.name));
    } else if (EXTS.has(extname(entry.name))) {
      yield join(dir, entry.name);
    }
  }
}

let count = 0;
for await (const file of walk(ROOT)) {
  const lines = (await readFile(file, 'utf8')).split(/\r?\n/);
  lines.forEach((line, i) => {
    if (!PATTERN.test(line)) return;
    count += 1;
    console.log(`${relative(ROOT, file)}:${i + 1}  ${line.trim().slice(0, 140)}`);
  });
}

console.log(count ? `\n${count} placeholder line(s) still open.` : 'No placeholders left.');
process.exitCode = count ? 1 : 0;
