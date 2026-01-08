# ISO 31000 UI IMPLEMENTATION PLAN

**Objective:** Categorize Dashboard Components into 5 Pillars of ISO 31000.
**Approach:** Non-intrusive Visual Badging System.

---

## 🗺️ COMPONENT MAPPING

### 1. Risk Identification (Identifikasi)
*   Container: **Peta Kluster Cincin Api** (Line ~491)
    *   *Rationale:* Spatial identification of risk sources.
*   Container: **Analisis Kerapatan SPH** (Line ~1080)
    *   *Rationale:* Identification of root contact vectors.

### 2. Risk Analysis (Analisis)
*   Container: **Financial Simulator** (Line ~140)
    *   *Rationale:* Understanding financial consequence stability.
*   Container: **Vanishing Yield Explained** (Line ~835)
    *   *Rationale:* Analyzing severity & likelihood trend.
*   Container: **Estimasi Kerugian (Left Panel)** (Line ~222)
    *   *Rationale:* Quantifying the impact.

### 3. Risk Evaluation (Evaluasi)
*   Container: **Risk Matrix** (Line ~185)
    *   *Rationale:* Evaluating risk level against criteria (Likelihood vs Impact).
*   Container: **Risk Control Tower** (Line ~345)
    *   *Rationale:* Prioritization decision support.

### 4. Risk Treatment (Perlakuan)
*   Container: **Standard Protocols** (Line ~630)
    *   *Rationale:* Prescriptive mitigation options.

### 5. Monitoring & Review (Pemantauan)
*   Container: **Watchlist Table** (Inside Risk Control Tower)
    *   *Strategy:* Add specific sub-badge or header inside the Watchlist area.

---

## 🛠️ EXECUTION WALKTHROUGH

### Step 1: Define CSS Classes
Inject the following utility class into the `<style>` block (Line ~90):
```css
.iso-badge {
    position: absolute;
    top: 1.5rem;
    right: 1.5rem;
    padding: 0.35rem 0.85rem;
    border-radius: 9999px;
    font-size: 0.6rem;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    z-index: 50;
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255,255,255,0.15);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    pointer-events: none; /* Pass clicks through */
}
/* Color Variants */
.iso-phase-1 { background: rgba(99, 102, 241, 0.85); color: white; } /* Indigo */
.iso-phase-2 { background: rgba(59, 130, 246, 0.85); color: white; } /* Blue */
.iso-phase-3 { background: rgba(245, 158, 11, 0.85); color: white; } /* Amber */
.iso-phase-4 { background: rgba(16, 185, 129, 0.85); color: white; } /* Emerald */
.iso-phase-5 { background: rgba(100, 116, 139, 0.85); color: white; } /* Slate */
```

### Step 2: Inject HTML Badges
Iteratively go through each mapped container and insert the badge HTML as the **first child** (to ensure proper z-indexing context, though absolute positioning handles it).

### Step 3: Verify & Snapshot
Use Browser Subagent to capture screenshots of each section to ensure:
1.  Badges are visible.
2.  Badges do not obscure critical buttons (like "Close" or "Toggle").
3.  Design aesthetic is preserved.

---

## 🛡️ RISK MITIGATION (Development)
*   **Layout Shift:** Low risk (Absolute positioning).
*   **Interaction:** `pointer-events: none` ensures badges don't block clicks on elements below them.
