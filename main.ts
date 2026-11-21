// News image entry for 21 November 2026 (Node 22, standard library only).
//
// The image is pre-rendered and shipped beside this program as entry.png.
// This program only copies it, byte for byte, to the grader's output
// directory, so the run is deterministic and needs no network, no
// dependencies and no image library.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
// /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const source = join(dirname(fileURLToPath(import.meta.url)), 'entry.png');
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(outDir, { recursive: true });
copyFileSync(source, join(outDir, 'entry.png'));
