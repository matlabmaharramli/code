# Convertly Engine — Raster math diagrams → clean SVG

Drop in PNG/JPG photos or screenshots of geometry / math diagrams and Convertly Engine
produces clean, scalable **SVG** files. Geometry is recovered 100% offline with
computer vision; text labels are read by your choice of local AI model (or the bundled
Tesseract OCR). Everything runs locally — nothing is uploaded.

## How to run

1. Launch **`ConvertlyEngine.exe`** (inside the `ConvertlyEngine` folder), or `python app.py`.
2. **Add images…** — pick your diagram(s) (PNG or JPG; transparent PNGs are fine).
3. **Choose…** an output folder — *required*; the app will not convert until it is set.
4. (Optional) set stroke colour, stroke width, and the text model.
5. **Convert ▶**. When it finishes, a popup offers to **open the results in Convertly View**
   — a built-in review stage where you see each raster beside (or under) its generated SVG,
   drag endpoints to adjust lines/arcs/circles, draw any new component (lines, shapes,
   ticks, right-angles, arrows, braces, text), shade closed regions, and **Save**. It snaps
   to the existing geometry (and an optional fine grid), supports undo/redo, and starts the
   stroke-colour picker on the colour Convertly Engine generated with. (Or **Open output** to jump to
   the folder.

## Prerequisites & AI Configuration

The app does **not** bundle or force a specific AI model. It dynamically integrates with
whatever you have in your local **Ollama** install.

### Setup Instructions

1. **Install Ollama:** Download and install Ollama from [ollama.com](https://ollama.com).
2. **Pull a model** (any vision or text model you like), e.g.:
   * General vision: `ollama pull qwen2.5vl:7b` (or `qwen2.5vl:3b`, `minicpm-v`)
   * Document/OCR: `ollama pull glm-ocr`
3. **Run the app:** it auto-detects every installed Ollama model and lists them in the
   **Text model** dropdown. Pick one, or pick **“None”** to skip AI entirely.

> Geometry detection always works without any AI. A **vision** model (e.g. `qwen2.5vl`,
> `minicpm-v`, `glm-ocr`) gives the best reading of math, Greek letters (α, β, γ),
> fractions and handwriting. With **“None”** (or if Ollama is offline) the bundled
> **Tesseract** OCR reads the labels instead — so the app is fully functional with no AI.
> The dropdown status line always names the model that the next conversion will use.

## What it detects

**Lines & curves**
* **Circles** — centre + radius (validated by inked-perimeter coverage).
* **Straight lines** — triangle sides, chords, rays, tangents, secants, axes, cevians,
  diagonals. Endpoints are snapped to shared vertices; chords/tangents are extended onto
  circles; a single edge is never emitted as two stacked lines.
* **Angle arcs** — single, **double**, and **triple** concentric (equal-angle) marks.
* **Dashed lines** (straight).
* **Structural curly braces** (re-drawn as smooth béziers).

**Marks**
* **Right-angle squares** (□) at perpendicular corners / T-junctions.
* **Arrowheads** — solid filled triangles *and* open “V” heads; single- **and**
  double-headed lines.
* **Tick marks** — equal-length / equal-angle hashes on sides and arcs.
* **Point / dot markers** — at vertices, at line crossings, **and on circles** (a marked
  point, or where a secant/tangent meets the circle). Nodes are drawn at one **uniform
  radius** and **magnetically snapped** onto the exact geometry they mark — to a
  line↔line intersection, a line endpoint, a line edge, or a circle rim (in that order).

**Text**
* Math-typeset labels — variables italicised, degree signs, fractions, subscripts, etc.

### Polygons — what's covered

* **Outline (hollow) polygons of ANY kind** are fully reproduced, because each edge is a
  straight line: triangles, quadrilaterals (square, rectangle, parallelogram, trapezoid),
  pentagons, hexagons, arbitrary n-gons.
* **Solid-filled shapes** are emitted as a single filled `<polygon>` for **convex
  triangles** and **right-angle rectangles / squares** (e.g. physics blocks, solid
  markers).

## Best results & limitations

Convertly Engine is strongest on **clear, reasonably high-resolution, typeset** geometry
diagrams — that is its sweet spot, and it is reliable there. Be aware of the limits:

* **Resolution matters.** Very low-res or faint hand-drawn scans can lose small marks
  (tiny dots, thin ticks) — that is a resolution limit, not a bug.
* **A dot that sits *on* a line and is barely thicker than it** may be missed (it is
  almost indistinguishable from the line).
* **Hand-drawn circles** are reproduced as a best-fit circle; against a wobbly drawing the
  rendered circle can sit a couple of pixels off.
* **Not detected:** ellipses / ovals (no ellipse detection — a dashed or solid ellipse is
  not recognised as one); filled non-right quadrilaterals, filled pentagons-and-up, and
  filled circles; a **dashed *polygon*** is recovered as plain (solid) edges, not dashed.
* For unusual or busy figures, expect to occasionally tidy one element by hand. A
  near-correct SVG plus a few seconds of cleanup beats a wrong one.

## Notes

* Everything runs locally / offline. Nothing is uploaded.
* The **Tesseract** OCR engine (languages — Greek, Russian, Math, Azerbaijani) is bundled
  in the app folder; the AI model is **not** (Ollama manages models in its own store).

## Build from source (PyInstaller)

```
pyinstaller ConvertlyEngine.spec --noconfirm
```
Output: `dist/ConvertlyEngine/ConvertlyEngine.exe` (one-folder, windowed). Ship `README.txt`
alongside the `.exe`. The Ollama model is never bundled; the user supplies it through
their local Ollama.
