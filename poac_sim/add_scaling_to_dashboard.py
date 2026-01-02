import re

# Read the complete file
with open('data/output/dashboard_cincin_api_complete.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find line 101 and add scaling buttons
for i, line in enumerate(lines):
    if i == 100:  # Line 101 (0-indexed = 100)
        # Insert scaling buttons before this line
        scaling_buttons = '''                        <!-- 3 SCALING BUTTONS -->
                        <div class="flex bg-white/10 p-1 rounded-lg gap-1">
                            <button onclick="setScale('block')" id="scale-block" class="px-4 py-1.5 rounded-md text-xs font-black transition-all bg-white text-slate-900 shadow-lg">2 Blok Sampel</button>
                            <button onclick="setScale('division')" id="scale-division" class="px-4 py-1.5 rounded-md text-xs font-black transition-all text-white opacity-60 hover:opacity-100">Skala Divisi</button>
                            <button onclick="setScale('estate')" id="scale-estate" class="px-4 py-1.5 rounded-md text-xs font-black transition-all text-white opacity-60 hover:opacity-100">Skala Kebun (20%)</button>
                        </div>
'''
        lines.insert(i, scaling_buttons)
        break

# Update metric values to have IDs (line 109, 118, 127)
for i, line in enumerate(lines):
    if '<span class="text-4xl">47.7</span>' in line:
        lines[i] = line.replace('<span class="text-4xl">47.7</span>', '<span class="text-4xl" id="area-value">47.7</span>')
    if '<span class="text-4xl text-red-400 font-black">Rp 1.208</span>' in line:
        lines[i] = line.replace('<span class="text-4xl text-red-400 font-black">Rp 1.208</span>', '<span class="text-4xl text-red-400 font-black" id="loss-value">Rp 1.208</span>')
    if '<span class="text-4xl text-emerald-400 font-black">Rp 0.1</span>' in line:
        lines[i] = line.replace('<span class="text-4xl text-emerald-400 font-black">Rp 0.1</span>', '<span class="text-4xl text-emerald-400 font-black" id="mitigation-value">Rp 0.1</span>')

# Add area note after line 111
for i, line in enumerate(lines):
    if i == 111 and '</div>' in line and 'HA</span>' in lines[i-1]:
        lines.insert(i+1, '                            <p class="text-[10px] text-white opacity-90 mt-1 font-black tracking-tighter" id="area-note" style="display: none;"></p>\n')
        break

# Add estate warning before "Kartu Bukti Ilmiah" section
for i, line in enumerate(lines):
    if '<!-- Kartu Bukti Ilmiah -->' in line:
        warning_div = '''                    <!-- Warning for Estate Scale -->
                    <div id="estate-warning" class="mt-8 p-6 bg-red-600/20 border-2 border-red-500/50 rounded-2xl flex items-start gap-4 shadow-xl" style="display: none;">
                        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="text-red-400 shrink-0 mt-1"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/><path d="m9 12 2 2 4-4"/></svg>
                        <div>
                            <h4 class="text-lg font-black text-white uppercase tracking-tighter">Peringatan Interpretasi Data:</h4>
                            <p class="text-base text-white font-bold leading-relaxed">Angka <span class="text-red-400 font-black px-1.5 bg-black/40 rounded">Rp 56.1 Miliar</span> didasarkan pada asumsi bahwa <span class="underline decoration-red-500 decoration-2 underline-offset-4 font-black">HANYA 20% (2.200 Ha)</span> dari total 11.000 Ha kebun yang memiliki kondisi kritis serupa dengan sampel. Laporan ini tidak merepresentasikan kerugian untuk luasan 11.000 Ha secara keseluruhan.</p>
                        </div>
                    </div>

'''
        lines.insert(i, warning_div)
        break

# Add JavaScript for scaling before showTab function
for i, line in enumerate(lines):
    if 'function showTab(tabName)' in line:
        js_code = '''        // Data for 3 scales
        const scaleData = {
            block: { area: '47.7', loss: '1.208', mitigation: '0.1', showNote: false, note: '' },
            division: { area: '750', loss: '19.1', mitigation: '1.57', showNote: false, note: '' },
            estate: { area: '2,200', loss: '56.1', mitigation: '4.6', showNote: true, note: 'Subset 2.200 Ha dari 11.000 Ha Kebun' }
        };

        function setScale(scale) {
            // Update button states
            document.getElementById('scale-block').className = 'px-4 py-1.5 rounded-md text-xs font-black transition-all ' + (scale === 'block' ? 'bg-white text-slate-900 shadow-lg' : 'text-white opacity-60 hover:opacity-100');
            document.getElementById('scale-division').className = 'px-4 py-1.5 rounded-md text-xs font-black transition-all ' + (scale === 'division' ? 'bg-white text-slate-900 shadow-lg' : 'text-white opacity-60 hover:opacity-100');
            document.getElementById('scale-estate').className = 'px-4 py-1.5 rounded-md text-xs font-black transition-all ' + (scale === 'estate' ? 'bg-white text-slate-900 shadow-lg' : 'text-white opacity-60 hover:opacity-100');
            
            // Update values
            const data = scaleData[scale];
            document.getElementById('area-value').textContent = data.area;
            document.getElementById('loss-value').textContent = 'Rp ' + data.loss;
            document.getElementById('mitigation-value').textContent = 'Rp ' + data.mitigation;
            
            // Show/hide note and warning
            const noteEl = document.getElementById('area-note');
            const warningEl = document.getElementById('estate-warning');
            if (data.showNote) {
                noteEl.textContent = data.note;
                noteEl.style.display = 'block';
                noteEl.className = 'text-[10px] text-white opacity-90 mt-1 font-black underline decoration-red-500 tracking-tighter';
                warningEl.style.display = 'flex';
            } else {
                noteEl.style.display = 'none';
                warningEl.style.display = 'none';
            }
        }

'''
        lines.insert(i, js_code)
        break

# Write the updated content
with open('data/output/dashboard_cincin_api_final.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('✅ Dashboard with 3-button scaling feature created successfully!')
print('📁 File: data/output/dashboard_cincin_api_final.html')
print('🔥 Features: Complete dashboard + Cincin Api maps + 3-button scaling (2 Blok / Divisi / Kebun 20%)')
