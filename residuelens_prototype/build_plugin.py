#!/usr/bin/env python3
"""Build ResidueLens_BrandNew_Plugin/code.js embedding the 5 SVG screens."""
import json, pathlib

root = pathlib.Path(__file__).parent
svg_dir = root / "figma_prototypes"
files = [
    "1_home_screen.svg",
    "2_packaged_scan.svg",
    "3_washing_estimate.svg",
    "4_explore_discovery.svg",
    "5_my_basket.svg",
]
svgs = [(svg_dir / f).read_text(encoding="utf-8") for f in files]
svg_js = ",\n".join(json.dumps(s) for s in svgs)

code = f"""// ResidueLens — Prototype Journey Builder
// Auto-generates 5 high-fidelity screens (1:1 with the Litmus-Mobile app)
// and wires 12 bidirectional prototype hotspots + flow starting point.
// Run in Figma: Plugins > Development > ResidueLens — Prototype Journey Builder

const SCREEN_SVGS = [
{svg_js}
];

const SCREEN_NAMES = [
  "1 · Home",
  "2 · Epic 9 — Packaged Scan",
  "3 · Epic 8 — Washing Estimate",
  "4 · Epic 10 — Explore Produce Discovery",
  "5 · My Basket",
];

// Transparent tap-target overlays placed on top of each screen.
// Coordinates are frame-local (each frame is 390 x 844), matched to the
// geometry drawn in the SVGs above (gen_svgs.py).
const HOTSPOTS = {{
  0: [ // Home
    {{ x: 18,  y: 232, w: 113, h: 62,  to: 1, label: "Scan card → Packaged Scan" }},
    {{ x: 30,  y: 404, w: 44,  h: 40,  to: 2, label: "Blueberry tile → Washing Estimate" }},
    {{ x: 320, y: 316, w: 52,  h: 30,  to: 4, label: "See all → My Basket" }},
    {{ x: 260, y: 780, w: 130, h: 64,  to: 3, label: "tab Learn → Explore" }},
  ],
  1: [ // Packaged Scan
    {{ x: 8,   y: 46,  w: 44,  h: 44,  to: 0, label: "close → Home" }},
    {{ x: 24,  y: 724, w: 342, h: 52,  to: 2, label: "View produce details → Washing Estimate" }},
    {{ x: 60,  y: 788, w: 270, h: 36,  to: 4, label: "Add to basket → My Basket" }},
  ],
  2: [ // Washing Estimate
    {{ x: 8,   y: 78,  w: 44,  h: 44,  to: 0, label: "back → Home" }},
    {{ x: 130, y: 780, w: 130, h: 64,  to: 4, label: "tab Basket → My Basket" }},
  ],
  3: [ // Explore
    {{ x: 30,  y: 396, w: 140, h: 30,  to: 2, label: "Sweet potato evidence → Washing Estimate" }},
    {{ x: 130, y: 780, w: 130, h: 64,  to: 4, label: "tab Basket → My Basket" }},
    {{ x: 0,   y: 780, w: 130, h: 64,  to: 0, label: "tab Home → Home" }},
  ],
  4: [ // My Basket
    {{ x: 18,  y: 427, w: 354, h: 62,  to: 2, label: "Blueberry row → Washing Estimate" }},
    {{ x: 0,   y: 780, w: 130, h: 64,  to: 0, label: "tab Home → Home" }},
    {{ x: 260, y: 780, w: 130, h: 64,  to: 3, label: "tab Learn → Explore" }},
  ],
}};

const GAP = 160;
const FLOW_NAME = "Iteration 3: Tutor Presentation Journey";

async function createScreenNode(svg) {{
  if (figma.createNodeFromSvgAsync) return await figma.createNodeFromSvgAsync(svg);
  return figma.createNodeFromSvg(svg);
}}

async function addLabel(text, x, y) {{
  try {{
    await figma.loadFontAsync({{ family: "Inter", style: "Medium" }});
    const t = figma.createText();
    t.fontName = {{ family: "Inter", style: "Medium" }};
    t.fontSize = 20;
    t.characters = text;
    t.x = x;
    t.y = y;
    t.fills = [{{ type: "SOLID", color: {{ r: 0.11, g: 0.13, b: 0.11 }} }}];
    return t;
  }} catch (e) {{ return null; }}
}}

async function setRxns(node, actions) {{
  // current API shape: reactions use 'actions' (array); older docs used 'action' (singular)
  const modern = [{{ trigger: {{ type: "ON_CLICK" }}, actions }}];
  try {{
    if (node.setReactionsAsync) await node.setReactionsAsync(modern);
    else node.reactions = modern;
  }} catch (e1) {{
    const legacy = [{{ trigger: {{ type: "ON_CLICK" }}, action: actions[0] }}];
    if (node.setReactionsAsync) await node.setReactionsAsync(legacy);
    else node.reactions = legacy;
  }}
}}

async function main() {{
  try {{
    if (figma.editorType && figma.editorType !== "figma")
      throw new Error("Open this plugin in a Figma Design file (not FigJam/Dev Mode).");
    if (figma.currentPage.loadAsync) await figma.currentPage.loadAsync();

    const frames = [];
    let x = 0;
    for (let i = 0; i < SCREEN_SVGS.length; i++) {{
      const node = await createScreenNode(SCREEN_SVGS[i]);
      node.name = SCREEN_NAMES[i];
      node.x = x;
      node.y = 80;
      node.clipsContent = true;
      frames.push(node);
      x += node.width + GAP;
      await addLabel(SCREEN_NAMES[i], node.x, 40);
    }}

    let wired = 0;
    let failed = 0;
    for (const [si, list] of Object.entries(HOTSPOTS)) {{
      const frame = frames[Number(si)];
      for (const h of list) {{
        try {{
          const r = figma.createRectangle();
          r.name = "hotspot → " + h.label;
          r.resize(h.w, h.h);
          r.fills = [{{ type: "SOLID", color: {{ r: 0, g: 0, b: 0 }}, opacity: 0 }}];
          frame.appendChild(r);
          r.x = h.x;
          r.y = h.y;
          await setRxns(r, [{{
            type: "NODE",
            destinationId: frames[h.to].id,
            navigation: "NAVIGATE",
            transition: {{ type: "DISSOLVE", easing: {{ type: "EASE_IN_AND_OUT" }}, duration: 0.2 }},
            preserveScrollPosition: false,
          }}]);
          wired++;
        }} catch (e) {{
          failed++;
          console.log("hotspot failed:", h.label, e && e.message);
        }}
      }}
    }}

    try {{
      figma.currentPage.flowStartingPoints = [
        {{ nodeId: frames[0].id, name: FLOW_NAME }},
      ];
    }} catch (e) {{
      console.log("flow starting point failed:", e && e.message);
    }}
    figma.viewport.scrollAndZoomIntoView(frames);
    figma.notify(
      "ResidueLens: " + frames.length + " screens, " + wired +
      " hotspots wired" + (failed ? " (" + failed + " FAILED — see console)" : "") +
      " · flow '" + FLOW_NAME + "' ready. Open ▶ Present to click through.",
      {{ timeout: 8000, error: failed > 0 }}
    );
  }} catch (e) {{
    figma.notify("ResidueLens build failed: " + e.message, {{ error: true }});
    throw e;
  }} finally {{
    figma.closePlugin();
  }}
}}

main();
"""

out = root / "ResidueLens_BrandNew_Plugin" / "code.js"
out.write_text(code, encoding="utf-8")
print(f"wrote {out} ({len(code)} bytes)")
