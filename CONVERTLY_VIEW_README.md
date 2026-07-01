# Convertly View — CAD-lite SVG editor (Convertly Engine review stage + standalone)

Human-in-the-loop review/finishing for vector diagrams. It shows the raster (PNG) beside
**or under** its **SVG**, perfectly aligned, and lets you step through a batch
adjusting, drawing, and saving each one. Everything runs locally in your browser — nothing
is uploaded.

**Two ways to run:**
* **From Convertly Engine (integrated):** after a conversion, Convertly Engine pops up *"Open the results
  in Convertly View?"* and launches this editor **in-process**, handing over the exact
  PNG↔SVG pairs (a *manifest*). Edit any diagram and **Save** to write the SVG back to your
  output folder. Re-openable any time via the **✎ Open in Convertly View** button.
* **Standalone:** `python smart_editor.py --input <folder> --output <folder>` over any
  folder of PNGs (+ optional matching SVGs).

---

## The workspace

Two views, toggled with the **⇆ View** button (or **Tab**):

* **Side-by-side** (default) — full raster on the left, the editable SVG on the right (with
  a faint raster underlay for tracing).
* **Overlay** — the SVG drawn directly on top of the full-strength raster, with the vectors
  **tinted blue** so they stand out from the original black ink (great for checking the
  vectorisation lines up).

The **Raster** slider fades the underlay; at its **minimum the raster disappears entirely**.

> Convertly Engine emits an opaque white page background in every SVG. The editor makes it transparent
> while you work (so the raster shows through and shading is visible) and **restores the
> white background when you Save**.

## The toolbar (two rows)

**Row 1 — workflow:** Select · Undo ↩ / Redo ↪ · ‹ Prev / *n‑of‑n* / Next › · Clean · Delete
· ⇆ View · Raster slider · **⤓ Save**.

**Row 2 — drawing tools + style:** the draw tools, the tick-count selector, the font-size
box, the **stroke colour / width** and **fill colour** pickers, and the **snap grid** toggle
+ spacing.

## Editing existing parts (Select tool, `V`)

Click any component to select it (it gets a blue glow + draggable handles):

* **Lines / dashed lines** — drag an endpoint to extend, shorten or rotate (`x1/y1/x2/y2`
  update live).
* **Circles / ellipses** — drag the east/south handles to set **`rx` / `ry`** independently
  (a `<circle>` auto-converts to an `<ellipse>` the moment they differ).
* **Polygons** — drag any vertex.
* **Text** — click to select & move it; **double-click to edit the words**.
* **Drag the body** of anything to move it. **Delete** removes the selection; **Esc**
  deselects.

Editing is **snap-aware too** — a dragged endpoint snaps to other geometry's
endpoints/intersections/centres or **perpendicularly onto a nearby line** (the element being
dragged is excluded, so it can't collapse onto itself).

## Drawing tools

Drawn shapes go into the correct SVG layer and inherit the diagram's stroke, so a hand-drawn
part looks like a Convertly Engine-detected one. Keys in brackets.

| Tool | Key | How |
|---|---|---|
| **Line** / **Dashed** | `L` / `D` | click start, click end. Angle-snaps to 15° steps; shows length & angle. |
| **Arc** | `A` | 3-point: click start, click end, then click the apex. |
| **Circle** | `C` | press at the centre, drag out to the radius. |
| **Ellipse** | `E` | drag a bounding box (square box → circle). |
| **Point** | `P` | click to drop a node dot. |
| **Tick** | `K` | hover a side (it highlights), click to tick its midpoint. **×1 / ×2 / ×3** for equal-length marks. |
| **Right-angle** | `G` | click one side (it stays lit), then the second — a square mark is drawn at the corner. |
| **Arrow** | `W` | **drag from tail to tip** — the arrow is drawn from the exact start point, points the way you drag, and the tip snaps onto line ends. |
| **Brace** | `B` | click the two ends (same bézier Convertly Engine emits). |
| **Text** | `X` | click, type. Size from the font-size box (blank = match the diagram). |
| **Shade** | `H` | click inside a closed region (bounded by **lines or curves**) to shade it; the shade is selectable and deletable like any part. |

## Smart snapping & guides

* A global **snap engine** keeps every critical coordinate — line **endpoints, midpoints,
  intersections**, shape **centres** and **vertices** — and the cursor snaps to the nearest
  within **10 px** while drawing *or* editing. The array **rebuilds after every change**, so
  new shapes snap to ones you just drew.
* **Perpendicular-to-line** snapping lands a point cleanly *on* a line.
* **Fine snap grid** (toggle + spacing) quantises free points for symmetry/accuracy.
* **Angle snap** (15°) + a live **length / angle** readout while drawing lines and arrows.

## Style controls

* **Stroke colour** — starts on the colour **Convertly Engine generated the diagram in**, so
  new strokes match by default. A **Dimly** button quick-sets the brand colour `#B880FF`.
  **Stroke width** (blank = match the diagram). **Fill colour** for shades.
* Changing any of these also **retouches the currently selected element**.

## Symbols, background & branding

* **Symbol deck** — the **Ω Symbols** button opens a popover grid; click a math symbol
  (° √ π θ α…ω, ², ₁, ∠, ⊥, ≅, ≤, →, ∑, ∫, …) to copy it, then paste it into the **Text** tool.
* **White bg** toggle (row 1) — keep the white page background in the saved SVG, or turn it
  off to save a **transparent** SVG.
* **Powered by Dimly** — Convertly View is part of the Convertly suite by Dimly.

## Undo / Clean / Save

* **Undo / Redo** (`Ctrl+Z` / `Ctrl+Y`) — one step per draw/drag/delete/clean.
* **Clean All** — wipes every vector, leaving the empty aligned layer over the raster so you
  can trace by hand, then Save.
* **Save** (`Ctrl+S`) — writes the SVG to the output folder with all editor chrome stripped
  (handles, previews, snap markers, grid, hit-rect) and the white page background restored.

## Run (standalone)

```
cd "Smart Editor"
python smart_editor.py --input <folder-of-pngs> --output <folder-for-saved-svgs>
```
Both default to `./input` and `./output` next to the script. It prints a local URL and
opens your browser. A few sample pairs are in `input/`. Stop with Ctrl+C.

**Keys:** `← / →` prev / next image · `V L D A C E P K G W B X H` tools · `Ctrl+Z/Y`
undo/redo · `Del` delete · `Tab` view toggle · `Esc` deselect/cancel · `Ctrl+S` save.

## Safety / robustness

File I/O is the foundation, so it is tested before anything else. `python test_io.py` runs
25 checks: scanning/pairing, reads, blank-SVG sizing, save + atomic overwrite,
**path-traversal rejection**, oversized-payload rejection, a **file-handle-leak** check
(3000 ops then the temp dir must delete cleanly), and the server surviving **400 concurrent
requests** + a malformed POST without crashing.

* Every file access is context-managed (no dangling handles).
* Browser-supplied names are validated against the live directory listing, so a request can
  never escape the input/output folders.
* Saves are atomic (unique temp → `os.replace`, with a short retry for transient Windows
  sharing violations) and serialised against reads.

## Tests

| Suite | Covers | Result |
|---|---|---|
| `python test_io.py` | file I/O safety (above) | 25/25 |
| `node test_editor.js` | select / drag anchors / circle→ellipse / move / text | 25/25 |
| `node test_cad.js` | snapping + geometry math (heavy) | 35/35 |
| `node test_tools.js` | CAD tools + snap + style/grid/arrow/symbols | 52/52 |
| `python test_browser.py` | **real headless Edge** — DOM/CSS the node mocks can't catch | 38/38 |

`test_browser.py` is the one that catches browser-only bugs (CSS layering, pointer events,
the opaque page-bg hiding the raster, overlay opacity per mode, undo/redo, grid render,
stroke→selection, arrow shaft, save round-trip). Run it after any UI change.

## Files

```
smart_editor.py     backend: safe file I/O (Library) + stdlib HTTP server + API
test_io.py          I/O safety suite                              -> 25/25
test_editor.js      select / drag / morph / move / text           -> 25/25
test_cad.js         snapping + geometry math                      -> 35/35
test_tools.js       CAD tools + snap + style/grid/arrow           -> 52/52
test_browser.py     real-browser (Selenium/Edge) smoke test       -> 38/38
static/index.html   UI shell (two-row toolbar)
static/style.css    styling
static/app.js       front-end: rendering, batch queue, undo, grid, page-bg, tool wiring
static/editor.js    select / drag anchors / circle->ellipse / move / text / edit-snap
static/cad.js       Smart-Snapping engine + grid + all CAD draw tools
input/  output/     default folders (input has a few samples)
```

## API (for reference)

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/list` | items (name, image, has_input_svg, has_output_svg) + folders |
| GET | `/api/image?name=<stem>` | raster bytes |
| GET | `/api/svg?name=<stem>` | SVG text (saved > source > blank) + size |
| POST | `/api/save` | `{name, svg}` → write `<output>/<stem>.svg` |
