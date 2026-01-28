# CHECKPOINT 9: Info Icons Implementation Plan

## User Request
1. **Problem:** Cannot click [i] icon in tooltip because tooltip disappears when mouse moves
2. **Solution Needed:** Move methodology link to static position (chart header)
3. **Enhancement:** Add [i] info icons throughout dashboard for contextual help

## Implementation Strategy

### Phase 1: Fix Methodology Access
- [x] Remove "ℹ️ Lihat metodologi estimasi" from tooltip footer
- [ ] Add static info button to Trend Chart section header
- [ ] Make button always accessible (not dependent on hover)

### Phase 2: Add Info Icons to All Metrics
- [ ] Quick Metrics (Total Blocks, Area, Yield, Critical)
- [ ] Ganoderma Attack Rate
- [ ] SPH (Stand Per Hectare)
- [ ] Risk Classification
- [ ] Production metrics

### Phase 3: Create Reusable InfoIcon Component
```html
<span class="info-icon" 
      onclick="showInfoModal('metric_name')"
      title="Click for details">
    ℹ️
</span>
```

### Phase 4: Build Modal System
Each metric will have dedicated info content explaining:
- What it measures
- Why it matters
- How it's calculated
- Interpretation guidelines

## Metrics to Document

1. **Total Blocks** - Explanation of block categorization
2. **Total Area** - Produktif vs non-produktif
3. **Average Yield** - T/Ha calculation and industry benchmark
4. **Critical Blocks** - Risk threshold explanation
5. **Ganoderma %** - Disease severity levels
6. **SPH** - Optimal density ranges (130-143)
7. **Gap Production** - Loss calculation methodology
8. **Risk Classification** - Tinggi/Sedang/Rendah criteria
9. **Trend Analysis** - Data sources and estimation methods

## Files to Modify
- `DASHBOARD_DEMO_FEATURES.html` - Main dashboard file

## Success Criteria
- ✅ All info icons clickable without disappearing
- ✅ Each metric has clear, concise explanation
- ✅ Methodology modal accessible from chart header
- ✅ Consistent UX across all info icons
- ✅ Mobile-friendly design
