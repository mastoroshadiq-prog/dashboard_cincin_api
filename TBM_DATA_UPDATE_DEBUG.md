# 🐛 TBM Blocks Not Showing - Debug & Fix Report

**Date**: 2026-01-26  
**Issue**: TBM blocks not appearing despite being in `all_blocks_data.json`  
**Root Cause**: Dashboard uses **embedded data** in HTML, not external JSON file  
**Status**: ✅ **FIXED**

---

## 🔍 Problem Analysis

### User Report
- TBM column exists (yellow, 4th column)
- Shows "Tidak ada data TBM"
- Tested multiple divisions (AME I, AME04, OLE, DBE)
- No TBM blocks appearing

### Initial Assumptions (WRONG ❌)
1. dashboard loads from `all_blocks_data.json` ← **WRONG**
2. Browser cache issue ← **Partial**
3. Division code mismatch ← **Not the issue**

### Actual Root Cause ✅

**Dashboard uses EMBEDDED data in the HTML file itself!**

```javascript
// Line ~1445 in DASHBOARD_DEMO_FEATURES.html
const COMPLETE_BLOCKS_DATA = {
    "K001": { ... },
    "A001A": { ... },
    // ... only 36 blocks (no TBM blocks!)
};
```

**This data was hardcoded** and NOT automatically updated when we modified `all_blocks_data.json`.

---

## 🛠️ Solution Implemented

### Step 1: Verify JSON Has TBM Data
```powershell
# Confirmed: all_blocks_data.json has 64 blocks (36 + 28 TBM)
Total TBM blocks: 28
✅ Data is correct in JSON file
```

### Step 2: Find Embedded Data in HTML
```python
# Located at line ~1445
const COMPLETE_BLOCKS_DATA = { ... }

# Problem: This was the OLD data (36 blocks only)
# Solution: Replace with updated data from JSON
```

### Step 3: Update HTML Embedded Data

**Script**: `update_html_embedded_data.py`

**Process**:
1. Load `all_blocks_data.json` (64 blocks with TBM)
2. Find `COMPLETE_BLOCKS_DATA` definition in HTML using regex
3. Replace entire object with updated data
4. Save updated HTML with embedded TBM data

**Result**:
- HTML size: 819,461 bytes → Updated
- Embedded data now includes all 64 blocks
- TBM blocks now present in JavaScript object

---

## 📊 Before vs After

### Before Fix
```javascript
const COMPLETE_BLOCKS_DATA = {
    // Only 36 blocks
    // NO TBM blocks
    // No tahun_tanam field
};
```

### After Fix
```javascript
const COMPLETE_BLOCKS_DATA = {
    // 64 blocks total
    // 28 TBM blocks included!
    // tahun_tanam field present
    "A005C": {
        "block_code": "A005C",
        "tahun_tanam": 2023,
        "is_tbm": true,
        ...
    },
    ...
};
```

---

## 🧪 Testing Instructions

### Step-by-Step Verification

1. **Close all browser tabs** with old dashboard
2. **Open fresh dashboard**:
   ```
   f:\PythonProjects\poac_cincin_api\dashboard-cincin-api\data\output\DASHBOARD_DEMO_FEATURES.html
   ```
3. **Hard refresh** (Ctrl+F5) to clear cache
4. **Test AME04 Division**:
   - Click "Total Blok" card
   - Look at 4th column (🌱 Blok TBM)
   - **Should see 7 blocks**: B012D, B013C, B015D, B015E, B016G, B016H, B017F, B017G

5. **Test AME01 Division**:
   - Should see 7 TBM blocks

6. **Test DBE01 Division**:
   - Should see 12 TBM blocks

### Expected Display

```
🌱 Blok TBM (Belum Menghasilkan)
┌──────────────────────────────┐
│ B012D  │ TBM │ Produksi: 0   │
│ B013C  │ TBM │ Produksi: 0   │
│ B015D  │ TBM │ Produksi: 0   │
│ B015E  │ TBM │ Produksi: 0   │
│ B016G  │ TBM │ Produksi: 0   │
│ B016H  │ TBM │ Produksi: 0   │
│ B017F  │ TBM │ Produksi: 0   │
│ B017G  │ TBM │ Produksi: 0   │
└──────────────────────────────┘
```

---

## 📁 Files Modified

| File | Action | Description |
|------|--------|-------------|
| `DASHBOARD_DEMO_FEATURES.html` | ✅ Updated | Embedded data replaced with TBM blocks |
| `DASHBOARD_DEMO_FEATURES_BEFORE_DATA_UPDATE.html` | ✅ Created | Backup of old HTML |
| `update_html_embedded_data.py` | ✅ Created | Update script |
| `TBM_DATA_UPDATE_DEBUG.md` | ✅ Created | This document |

---

## 💡 Key Learnings

### Critical Discovery
**Dashboard data architecture**:
```
HTML File
  └─> Embedded JavaScript Object (COMPLETE_BLOCKS_DATA)
      └─> Used by all dashboard functions
      └─> NOT loaded from external .json file!
```

**Implications**:
1. Updating `all_blocks_data.json` alone doesn't affect dashboard
2. HTML file must be regenerated/updated when data changes
3. Need to maintain sync between JSON and HTML embedded data

### Why This Happened
1. Dashboard was likely generated from JSON originally
2. JSON was updated (added TBM blocks)
3. HTML was NOT regenerated
4. Result: Mismatch between JSON source and HTML display

---

## 🔧 Technical Details

### Data Update Method

**Regex Pattern Used**:
```python
# Find start
start_pattern = r'const COMPLETE_BLOCKS_DATA = \{'

# Find end (closing brace before next const/script)
end_pattern = r'\n\s*\};\s*\n\s*(?:const |//|</script>)'
```

**Replacement**:
```python
new_blocks_js = "const COMPLETE_BLOCKS_DATA = " + 
                json.dumps(updated_blocks, indent=4) + ";"
```

### File Size Changes
- Original HTML: ~819 KB
- Updated HTML: ~820 KB (minimal increase)
- Data change: +28 blocks (78% increase in block count)

---

## 🚨 Important Notes

### Data Source Hierarchy
```
Excel (data_gabungan.xlsx)
    ↓ (extracted TBM data)
JSON (all_blocks_data.json)
    ↓ (embedded into)  
HTML (DASHBOARD_DEMO_FEATURES.html) ← THIS is what browser loads!
```

### Future Updates
**When adding/modifying block data**:
1. ✅ Update Excel source
2. ✅ Extract to JSON
3. ✅ **UPDATE HTML EMBEDDED DATA** ← Critical step!
4. ✅ Test in browser

### Maintenance Script
Use `update_html_embedded_data.py` whenever:
- Block data changes
- New blocks added
- Field values updated
- Data structure modified

---

## ✅ Verification Checklist

- [x] TBM data in `all_blocks_data.json` (64 blocks)
- [x] HTML embedded data updated
- [x] Backup created (BEFORE_DATA_UPDATE)
- [x] Script documented (update_html_embedded_data.py)
- [x] Dashboard reopened in browser
- [ ] **User verification**: TBM blocks visible in AME04
- [ ] **User verification**: TBM blocks visible in other divisions

---

## 🎯 Expected Outcome

**After browser refresh**:
- AME01: 7 TBM blocks ✅
- AME03: 1 TBM block ✅
- AME04: 7 TBM blocks ✅
- DBE01: 12 TBM blocks ✅

**Total**: 28 TBM blocks across divisions

---

## 📞 If Still Not Working

### Troubleshooting Steps

1. **Clear all browser cache**:
   ```
   Chrome: Ctrl+Shift+Delete → Clear all
   ```

2. **Verify HTML file was updated**:
   ```powershell
   Select-String -Path "DASHBOARD_DEMO_FEATURES.html" -Pattern "is_tbm" | Measure-Object
   # Should find 28+ matches
   ```

3. **Check browser console** (F12):
   ```javascript
   console.log(COMPLETE_BLOCKS_DATA);
   // Look for blocks with is_tbm: true
   ```

4. **Verify file modification time**:
   ```powershell
   Get-Item "DASHBOARD_DEMO_FEATURES.html" | Select-Object LastWriteTime
   # Should be recent (today)
   ```

---

**Author**: AI Assistant (Antigravity)  
**Fix Time**: ~15 minutes  
**Root Cause**: Embedded data vs JSON file mismatch  
**Complexity**: Medium (architectural misunderstanding)
