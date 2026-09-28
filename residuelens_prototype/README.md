# ResidueLens — Iteration 3 Prototype Pack

5 张 390×844 高保真 SVG 屏 + 自动连线的 Figma 插件。**v3：对照 `NithishK5/residuelens` 仓库 `Litmus-Mobile` 真实源码 + 真实运行渲染双重校准**——本包数据是在本机实际跑起该 App（RN-web export + Postgres + FastAPI 播种 `data/gold` 数据集）后，从运行时截图逐项核对的结果。

## 文件结构

```
figma_prototypes/
  1_home_screen.svg        Home（DashboardHero：问候+副标题+胶囊搜索 → Scan/Type code/Browse → Your basket → What we hold → 来源分布）
  2_packaged_scan.svg      包装蔬菜快扫（取景器 + 底部结果 sheet，结果=Spinach PLU 3332，与详情页数据一致）
  3_washing_estimate.svg   Spinach 详情页（WHAT TO DO + 34px 双行标题 + accent 标尺 + WashComparison Vinegar 49% + 成分行）
  4_explore_discovery.svg  Explore（同龄适龄探索，用真实设计语言渲染的新特性屏）
  5_my_basket.svg          Basket（5 items + 双 CoverageMeasure 轨道 + 频率 chips 换行 + 4 条真实食材行）
ResidueLens_BrandNew_Plugin/
  manifest.json
  code.js                  内嵌全部 5 张 SVG，一键生成画板+连线
previews/                  PNG 预览（cairosvg 渲染）+ contact_sheet.png
gen_svgs.py                从真实设计 token 重新生成 5 张 SVG
build_plugin.py            由 figma_prototypes/*.svg 重新生成 code.js
```

## 使用（Figma 桌面端或 Web）

1. Figma → **Plugins → Development → Import plugin from manifest…**
2. 选择 `ResidueLens_BrandNew_Plugin/manifest.json`
3. **Plugins → Development → ResidueLens — Prototype Journey Builder** 运行一次
4. 画布自动生成 5 个 390×844 画板（Epic 9/8/10 已标在画板名里），15 个透明热区已连好 NAVIGATE 跳转，并在第 1 屏创建 Flow Starting Point：**`Iteration 3: Tutor Presentation Journey`**
5. 右上角 **▶ Present** 直接演示

## 热区连线图（15 条）

| From | 热区 | To |
|---|---|---|
| Home | Scan 卡片 | Packaged Scan |
| Home | Spinach 图块（Your basket） | Washing Estimate |
| Home | "See all" | My Basket |
| Home | 底栏 Learn | Explore (Epic 10) |
| Packaged Scan | 左上角 × | Home |
| Packaged Scan | View produce details | Washing Estimate |
| Packaged Scan | Add to basket | My Basket |
| Washing Estimate | 左上角 `<` | Home |
| Washing Estimate | 底栏 Basket | My Basket |
| Explore | Sweet potato "View the evidence" | Washing Estimate |
| Explore | 底栏 Basket | My Basket |
| Explore | 底栏 Home | Home |
| My Basket | Spinach 行 | Washing Estimate |
| My Basket | 底栏 Home | Home |
| My Basket | 底栏 Learn | Explore (Epic 10) |

## 与真实 App 运行时的对照（已验证）

运行时环境：Postgres:18 + `alembic upgrade head` + `load_gold.py`（66 食材）+ FastAPI :8000 + Expo web dev server。以下数值全部取自真实数据/真实渲染：

- **Home**："Good Morning/Evening, You"（按时间变化）、YOUR BASKET 卡 "5 items saved · Four of them have no Australian results."、覆盖图 4/62/0（Australia/overseas/none）、来源分布 79% US only · 16% US and UK · 4% UK only
- **Spinach 详情**："Wash under running water"（真实 lede，`actionPrimary` 取分号前段）、standfirst 用真实 washReductionMedian **42%**、"LIMITED EVIDENCE · 1 STUDY"（mono 下划线）、WashComparison 方法按 median 排序 **Vinegar 49%**（40–67% across studies）、灰底 "Limited evidence · 1 study" 徽标、成分行 Indoxacarb 67% / Pyraclostrobin 63% / Thiamethoxam 61%…
- **Basket**：1 of 5 tested in Australia（accentMid 1/5 填充）、3 of 5 with washing study（accentSoft 3/5）、"2 items have neither yet."、chips All 5 / Often 2 / Sometimes 2 / Rarely 1 / Not marked 0（换两行）、真实行 Blueberry 42 · 无清洗研究 / Spinach 55 · 42% / Apple 54 · tested in Australia · 38% / Tomato 56 · 48%
- **底栏**：3 Tab Home / Basket / Learn（RootNavigator.js），无第 4 Tab
- **食材图标**：与 App `glyphs.generated.js` 同一份 Noto Emoji 矢量数据（16 个，含 tomato）

## 再生成

```bash
python3 gen_svgs.py        # 重建 figma_prototypes/*.svg
python3 build_plugin.py    # 重新内嵌进 ResidueLens_BrandNew_Plugin/code.js
```
