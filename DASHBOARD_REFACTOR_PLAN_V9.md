# Dashboard Refactoring Implementation Plan
**Version:** 9.0 Major Refactoring  
**Date:** 2026-01-29  
**Objective:** Simplify popup, move sections to main dashboard for better UX

---

## 🎯 **GOAL:**

Transform the current **overloaded popup** into a **clean, focused interface** by:
1. Moving **Visual Analysis** (5 category cards) → Main Dashboard
2. Moving **Loss Analysis** (metrics + breakdowns) → Main Dashboard  
3. Moving **5-Year Trend Analysis** → Main Dashboard
4. Simplifying **Popup** to show only production trend lists
5. Creating **NEW Block Detail Drilldown Modal** for per-block insights

---

## 📊 **CURRENT STATE vs TARGET STATE:**

### **CURRENT (v8.8.2):**
```
Main Dashboard:
├─ Division Selector
├─ Top 4 Metrics (Total Blocks, Area, Avg Yield, Critical)
├─ Historical Trends Chart
└─ [Empty space below]

Popup "Tren Produksi Per Blok" (OVERLOADED):
├─ 5 Category Cards (Visual Analysis)
├─ Loss Analysis Dashboard
│   ├─ 4 Metrics (Gap Yield, Kerugian, Ganoderma, SPH)
│   ├─ Ganoderma Breakdown Chart
│   └─ SPH Distribution Chart
├─ 5-Year Trend Analysis
│   ├─ Multi-line Chart
│   ├─ Scenario Toggles
│   └─ Key Insights
└─ Block Lists (by category)
```

### **TARGET (v9.0):**
```
Main Dashboard (ENHANCED):
├─ Division Selector
├─ Top 4 Metrics (Total Blocks, Area, Avg Yield, Critical)
├─ Historical Trends Chart
├─ ✨ NEW: Production Trend Overview (5 category cards)
├─ ✨ NEW: Loss Analysis Dashboard (full section)
└─ ✨ NEW: 5-Year Trend Analysis (full chart + insights)

Popup "Tren Produksi" (SIMPLIFIED):
├─ Header (Division info)
├─ Search Box
└─ Block Lists (categorized)
    └─ Click block → NEW Drilldown Modal

✨ NEW: Block Detail Drilldown Modal:
├─ Block Header (Name, Area, Yield)
├─ Production Matrix (2023-2025 data)
├─ Risk Matrix (Ganoderma × SPH)
└─ Visual Charts:
    ├─ Attack Rate Trend 
    ├─ Yield Performance
    └─ SPH Evolution
```

---

## 🚀 **IMPLEMENTATION PHASES:**

### **PHASE 1: Move Sections to Main Dashboard** ⏳
**Status:** Planned  
**Risk:** Medium (large file, complex structure)

**Steps:**
1. ✅ Create backup (`DASHBOARD_DEMO_FEATURES_BEFORE_REFACTOR.html`)
2. 📝 Extract Visual Analysis section (lines 18697-18773)
3. 📝 Extract Loss Analysis section (lines 18776-18985)
4. 📝 Extract 5-Year Trend section (lines 18987-19086)
5. 📝 Insert all 3 sections into main dashboard (after line 466)
6. ✅ Test: Verify sections render correctly on main page
7. ✅ Test: Verify JavaScript functions still work (charts, sliders)

**Files to modify:**
- `data/output/DASHBOARD_DEMO_FEATURES.html` (main file)

**Line ranges:**
- Insertion point: After line 466 (`<div class="max-w-7xl mx-auto space-y-8">`)
- Extraction points:
  - Visual: 18697-18773 (77 lines)
  - Loss: 18776-18985 (210 lines)
  - Trend: 18987-19086 (100 lines)

---

### **PHASE 2: Simplify Popup** ⏳
**Status:** Planned  
**Risk:** Low

**Steps:**
1. 📝 Remove Visual Analysis from popup (replace with comment)
2. 📝 Remove Loss Analysis from popup (replace with  comment)
3. 📝 Remove 5-Year Trend from popup (replace with comment)
4. 📝 Update popup title: "Tren Produksi Per Blok" → "Production Trend - Block Lists"
5. ✅ Test: Verify popup still opens correctly
6. ✅ Test: Verify block lists still show correctly
7. ✅ Test: Verify search function still works

**Expected result:**
- Popup becomes lightweight (only header + search + lists)
- Faster loading time
- Clearer focus on block selection

---

### **PHASE 3: Create Block Drilldown Modal** ⏳
**Status:** Planned  
**Risk:** High (new feature, requires data integration)

**Steps:**
1. 📝 Design new modal template structure
2. 📝 Create `showBlockDetail(blockId)` JavaScript function
3. 📝 Add click handlers to block list items
4. 📝 Implement Production Matrix:
   - 2023, 2024, 2025 production data
   - Year-over-year change percentages
5. 📝 Implement Risk Matrix:
   - Ganoderma severity (Low/Medium/High)
   - SPH status (Below/Optimal/Above)
   - Combined risk score
6. 📝 Add 3 Chart.js visualizations:
   - Attack Rate trend line
   - Yield performance bars
   - SPH evolution line
7. 📝 Add actionable recommendations based on risk level
8. ✅ Test: Click block → modal opens with correct data
9. ✅ Test: Charts render correctly
10. ✅ Test: Close modal → returns to block list

**Data requirements:**
- Per-block historical data (2023-2025)
- Ganoderma stadium/attack rate data
- SPH data
- Treatment recommendations logic

---

## ⚠️ **RISKS & MITIGATION:**

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Regex extraction fails | Medium | High | Use line-based extraction with exact boundaries |
| JavaScript breaks after move | Medium | High | Keep all `id` attributes intact, test thoroughly |
| Charts don't render | Low | Medium | Verify Chart.js canvas IDs are unique |
| Popup becomes unusable | Low | High | Test popup separately after each phase |
| Performance degradation | Low | Medium | Monitor page load time, optimize if needed |

---

## ✅ **TESTING CHECKLIST:**

### **Phase 1 Tests:**
- [ ] Main dashboard loads without errors
- [ ] Visual Analysis cards show counts correctly
- [ ] Loss Analysis metrics calculate correctly
- [ ] 5-Year Trend chart renders with data
- [ ] All info icons (ℹ️) still work
- [ ] Slider for TBS price works
- [ ] Scenario toggles work
- [ ] Charts are interactive (tooltips, etc.)

### **Phase 2 Tests:**
- [ ] Popup opens when clicking "Total Blocks"
- [ ] Popup shows block lists correctly
- [ ] Search box filters blocks correctly
- [ ] Block counts match category cards
- [ ] Popup doesn't have visual glitches
- [ ] Close button works

### **Phase 3 Tests:**
- [ ] Click block → drilldown modal opens
- [ ] Block name/info shows correctly
- [ ] Production matrix has real data
- [ ] Risk matrix calculated correctly
- [ ] All 3 charts render with data
- [ ] Recommendations are relevant
- [ ] Close → returns to block list
- [ ] Navigate between blocks works

---

## 📦 **DELIVERABLES:**

1. **v9.0-main-dashboard-enhanced**
   - Visual Analysis on main dashboard
   - Loss Analysis on main dashboard
   - 5-Year Trend on main dashboard

2. **v9.1-popup-simplified**
   - Lightweight popup with only block lists
   - Improved search functionality

3. **v9.2-block-drilldown**
   - New modal for per-block details
   - Production matrix
   - Risk matrix
   - 3 visual charts
   - Action recommendations

---

## 🎯 **SUCCESS CRITERIA:**

✅ Main dashboard is information-rich (no need to click for key metrics)  
✅ Popup is fast and focused (lightweight, clear purpose)  
✅ Block drilldown provides deep insights (actionable intelligence)  
✅ No JavaScript errors  
✅ All existing features still work  
✅ User experience improved (less clicking, better information architecture)

---

## 📅 **TIMELINE:**

| Phase | Estimated Time | Priority |
|-------|----------------|----------|
| Phase 1 | 2-3 hours | HIGH |
| Phase 2 | 1 hour | HIGH |
| Phase 3 | 4-6 hours | MEDIUM |

**Total:** ~8-10 hours of development + testing

---

## 🔄 **ROLLBACK PLAN:**

If anything goes wrong:
```bash
# Restore from backup
git checkout v8.8.2-format-consistency

# Or use backup file
Copy-Item DASHBOARD_DEMO_FEATURES_BEFORE_REFACTOR.html DASHBOARD_DEMO_FEATURES.html
```

---

## 📝 **NOTES:**

- **File is large (19,887 lines, 962KB)** - be careful with regex operations
- **Many interdependencies** - JavaScript functions reference specific IDs
- **Chart.js canvases** - ensure unique IDs across main dashboard and modals
- **Data loading** - verify AME02 division data still loads correctly
- **Responsive design** - test on different screen sizes

---

## 🚀 **NEXT ACTION:**

**Option A (Incremental):** Implement Phase 1 step-by-step with manual edits and testing  
**Option B (Scripted):** Fix Python script to be more precise with line-based extraction  
**Option C (Hybrid):** Use script for extraction, manual verification for insertion

**Recommended:** Option A (safest for complex refactoring)
