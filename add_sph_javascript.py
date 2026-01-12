#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script untuk menambahkan JavaScript logic untuk update SPH Analysis
"""

import re

FILE_INPUT = r'data/output/dashboard_cincin_api_INTERACTIVE_FULL_WITH_SPH.html'
FILE_OUTPUT = r'data/output/dashboard_cincin_api_INTERACTIVE_FULL_WITH_SPH_COMPLETE.html'

# JavaScript function untuk update SPH analysis
SPH_UPDATE_FUNCTION = '''
    // ============================================
    // SPH ANALYSIS UPDATE FUNCTION
    // ============================================
    function updateSPHAnalysis(blockData, side = 'Left') {
        if (!blockData) return;
        
        const sphActual = blockData.sph || 0;
        const sphStandard = 136; // SPH standar untuk kelapa sawit
        const sphPercentage = (sphActual / sphStandard) * 100;
        
        // Update SPH values
        document.getElementById(`sphActual${side}`).textContent = sphActual.toFixed(2);
        document.getElementById(`sphStandard${side}`).textContent = sphStandard;
        
        // Determine status and color
        let statusText = '';
        let statusColor = '';
        let progressColor = '';
        
        if (sphActual < 100) {
            statusText = 'KRITIS - Sangat Rendah';
            statusColor = 'text-red-400';
            progressColor = 'bg-gradient-to-r from-red-600 to-red-500';
        } else if (sphActual < 120) {
            statusText = 'RENDAH - Perlu Perhatian';
            statusColor = 'text-orange-400';
            progressColor = 'bg-gradient-to-r from-orange-600 to-orange-500';
        } else if (sphActual < 130) {
            statusText = 'SEDANG - Dapat Ditingkatkan';
            statusColor = 'text-yellow-400';
            progressColor = 'bg-gradient-to-r from-yellow-600 to-yellow-500';
        } else if (sphActual <= 140) {
            statusText = 'OPTIMAL - Sesuai Standar';
            statusColor = 'text-emerald-400';
            progressColor = 'bg-gradient-to-r from-emerald-600 to-emerald-500';
        } else {
            statusText = 'TINGGI - Over Density';
            statusColor = 'text-blue-400';
            progressColor = 'bg-gradient-to-r from-blue-600 to-blue-500';
        }
        
        // Update status text
        const statusElement = document.getElementById(`sphStatusText${side}`);
        if (statusElement) {
            statusElement.textContent = statusText;
            statusElement.className = `text-xs font-black ${statusColor}`;
        }
        
        // Update progress bar
        const progressElement = document.getElementById(`sphProgress${side}`);
        if (progressElement) {
            const clampedPercentage = Math.min(Math.max(sphPercentage, 0), 100);
            progressElement.style.width = `${clampedPercentage}%`;
            progressElement.className = `h-full transition-all duration-500 rounded-full ${progressColor}`;
        }
        
        // Generate impact analysis text
        let impactText = '';
        const sphGap = sphStandard - sphActual;
        const sphGapPercent = ((sphGap / sphStandard) * 100).toFixed(1);
        
        if (sphActual < 100) {
            impactText = `⚠️ Kerapatan sangat rendah (${sphActual} pohon/ha). Defisit ${Math.abs(sphGap).toFixed(0)} pohon/ha (${Math.abs(sphGapPercent)}%) dari standar. Produktivitas berpotensi turun hingga 30-40%. Rekomendasi: Replanting atau interplanting segera.`;
        } else if (sphActual < 120) {
            impactText = `⚠️ Kerapatan di bawah optimal (${sphActual} pohon/ha). Defisit ${Math.abs(sphGap).toFixed(0)} pohon/ha (${Math.abs(sphGapPercent)}%). Potensi kehilangan produksi 15-25%. Pertimbangkan interplanting pada area kosong.`;
        } else if (sphActual < 130) {
            impactText = `ℹ️ Kerapatan mendekati standar (${sphActual} pohon/ha). Defisit ${Math.abs(sphGap).toFixed(0)} pohon/ha (${Math.abs(sphGapPercent)}%). Produktivitas dapat ditingkatkan 5-10% dengan optimasi kerapatan.`;
        } else if (sphActual <= 140) {
            impactText = `✅ Kerapatan optimal (${sphActual} pohon/ha). Sesuai standar industri (130-140 pohon/ha). Pertahankan kerapatan ini melalui perawatan rutin dan penggantian pohon mati.`;
        } else {
            const excess = (sphActual - sphStandard).toFixed(0);
            const excessPercent = ((excess / sphStandard) * 100).toFixed(1);
            impactText = `⚠️ Kerapatan terlalu tinggi (${sphActual} pohon/ha). Kelebihan ${excess} pohon/ha (+${excessPercent}%). Kompetisi nutrisi dan cahaya dapat menurunkan produktivitas per pohon. Pertimbangkan thinning selektif.`;
        }
        
        // Update impact text
        const impactElement = document.getElementById(`sphImpact${side}`);
        if (impactElement) {
            impactElement.innerHTML = impactText;
        }
    }
'''

def add_sph_javascript():
    print("Membaca file dashboard...")
    with open(FILE_INPUT, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Cari fungsi updateFinancialPanel atau lokasi yang tepat untuk insert function
    # Kita akan insert sebelum closing </script> tag terakhir
    
    # Cari script tag yang berisi updateFinancialPanel atau fungsi update lainnya
    script_pattern = r'(function updateFinancialPanel.*?)\s*(</script>)'
    
    matches = list(re.finditer(script_pattern, content, re.DOTALL))
    
    if matches:
        # Insert setelah fungsi updateFinancialPanel
        insert_pos = matches[0].end(1)
        new_content = content[:insert_pos] + '\n\n' + SPH_UPDATE_FUNCTION + '\n' + content[insert_pos:]
        print(f"✓ SPH function ditambahkan setelah updateFinancialPanel")
    else:
        # Fallback: insert sebelum </script> terakhir
        last_script_close = content.rfind('</script>')
        if last_script_close != -1:
            new_content = content[:last_script_close] + '\n' + SPH_UPDATE_FUNCTION + '\n' + content[last_script_close:]
            print(f"✓ SPH function ditambahkan sebelum </script> terakhir")
        else:
            print("ERROR: Tidak dapat menemukan lokasi untuk insert JavaScript")
            return
    
    # Sekarang tambahkan call ke updateSPHAnalysis di dalam updateFinancialPanel
    # Cari updateFinancialPanel function dan tambahkan call
    update_panel_pattern = r'(function updateFinancialPanel\([^)]*\)\s*{[^}]*)(}\s*$)'
    
    # Cari pattern yang lebih spesifik
    # Kita cari di mana finLossLeft di-update, lalu tambahkan updateSPHAnalysis setelahnya
    fin_loss_pattern = r'(document\.getElementById\(["\']finLossLeft["\']\)\.textContent\s*=\s*[^;]+;)'
    
    matches = list(re.finditer(fin_loss_pattern, new_content))
    
    if matches:
        # Insert setelah update finLossLeft
        insert_pos = matches[0].end()
        sph_call = '\n        updateSPHAnalysis(blockData, "Left");'
        new_content = new_content[:insert_pos] + sph_call + new_content[insert_pos:]
        print(f"✓ Call ke updateSPHAnalysis ditambahkan di updateFinancialPanel")
    else:
        print("⚠️  Tidak dapat menemukan lokasi untuk auto-call updateSPHAnalysis")
        print("    Anda perlu menambahkan manual: updateSPHAnalysis(blockData, 'Left');")
    
    # Tulis ke file output
    print(f"\nMenulis ke {FILE_OUTPUT}...")
    with open(FILE_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("\n" + "="*70)
    print("✅ SELESAI!")
    print("="*70)
    print("\nFungsi JavaScript untuk SPH Analysis telah ditambahkan:")
    print("  - updateSPHAnalysis(blockData, side)")
    print("  - Auto-update saat blok dipilih")
    print("  - Analisis status: Kritis, Rendah, Sedang, Optimal, Tinggi")
    print("  - Progress bar dengan warna dinamis")
    print("  - Rekomendasi berdasarkan kerapatan")
    print(f"\nFile output: {FILE_OUTPUT}")
    print("\nSilakan test dengan membuka file dan memilih blok!")

if __name__ == "__main__":
    add_sph_javascript()
