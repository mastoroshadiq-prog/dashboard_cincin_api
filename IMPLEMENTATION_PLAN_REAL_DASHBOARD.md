# IMPLEMENTATION PLAN: Prototype → Real Dashboard
**Date:** 14 Januari 2026  
**Target:** dashboard_cincin_api_INTERACTIVE_FULL.html  
**Source:** PROTOTYPE_3_ENHANCEMENTS.html (approved features)

---

## 🎯 **FEATURES TO IMPLEMENT:**

### **Feature 1: Before/After Treatment Comparison Chart**
- **Location:** Below COI section (after ROI metrics)
- **Type:** Bar chart with 2 datasets (Red vs Green)
- **Data:** Year 0-3 comparison
- **Summary boxes:** 3 boxes (TANPA, DENGAN, SAVINGS)

### **Feature 2: Section Rename**
- **Target:** "ESTIMASI KERUGIAN BLOK" → "STATISTIK BLOK"
- **Keep position:** PAPARAN (Red) LEFT, STATISTIK (Blue) RIGHT
- **No swap needed:** Current layout is correct

### **Feature 3: Enhanced Modal Charts**
#### **3.1: 3-Year Trend Chart**
- Dual-line comparison (TANPA vs DENGAN)
- Click-to-table with SIDE-BY-SIDE format
- Rich tooltips with 4 metrics

#### **3.2: Pie Chart (Treatment Cost)**
- Distinct colors (Red→Blue spectrum)
- Labels on segments (Value + %)
- Enhanced legend with values

---

## 📋 **IMPLEMENTATION STEPS:**

### **STEP 1: Backup Current Dashboard**
```bash
cp dashboard_cincin_api_INTERACTIVE_FULL.html dashboard_cincin_api_INTERACTIVE_FULL_BACKUP.html
```

### **STEP 2: Feature 2 - Rename Section**
**Simple text replacement:**
- Find: "ESTIMASI KERUGIAN BLOK"
- Replace: "STATISTIK BLOK"
- **Estimated time:** 5 minutes

### **STEP 3: Feature 1 - Treatment Comparison Chart**
**Insert location:** After ROI section, before block detail cards

**Components to add:**
1. Chart container HTML
2. Summary boxes (3 columns)
3. Chart.js initialization
4. Data arrays

**Files to extract from prototype:**
- Lines ~125-163 (Feature 1 HTML)
- Lines ~239-304 (Feature 1 JavaScript)

**Estimated time:** 30-45 minutes

### **STEP 4: Feature 3 - Enhanced Modal Charts**
**Modals to enhance:**
1. ✅ Current Loss - Keep existing (already has table)
2. ✅ 3-Year Projection - Enhance with dual-line + click-to-table
3. ✅ Treatment Cost - Enhance with labeled pie
4. ✅ Savings - Keep existing
5. ✅ ROI - Keep existing

**For 3-Year Modal:**
- Replace chart code (lines ~360-401 in prototype)
- Add click handler (lines ~new handler)
- Add data display container

**For Pie Modal:**
- Replace chart code (lines ~403-441 in prototype)
- Update colors, labels, legend

**Estimated time:** 1-2 hours

### **STEP 5: Testing & Verification**
**Test checklist:**
- [ ] Feature 1: Chart displays correctly
- [ ] Feature 1: Summary boxes show correct values
- [ ] Feature 2: "STATISTIK BLOK" title visible
- [ ] Feature 3: 3-year chart has dual lines
- [ ] Feature 3: Click shows side-by-side table
- [ ] Feature 3: Pie chart has distinct colors + labels
- [ ] No console errors
- [ ] All existing features still work

**Estimated time:** 30 minutes

---

## ⏱️ **TOTAL ESTIMATED TIME:** 2.5-3 hours

---

## 🚀 **EXECUTION APPROACH:**

**Option A: All at once (recommended)**
- Implement all 3 features in one session
- Single commit after full testing
- **Pros:** Clean, atomic change
- **Cons:** Longer before seeing results

**Option B: Incremental**
- Feature 2 → commit → test
- Feature 1 → commit → test  
- Feature 3 → commit → test
- **Pros:** See progress, easier debugging
- **Cons:** Multiple commits

**RECOMMENDATION:** Option A (all at once) since features are independent and prototype is tested.

---

## 📝 **IMPLEMENTATION SCRIPT:**

I'll create Python scripts to:
1. Backup dashboard
2. Apply Feature 2 (rename)
3. Insert Feature 1 (chart + boxes)
4. Enhance Feature 3 (modals)
5. Verify no syntax errors

**Ready to proceed?**
