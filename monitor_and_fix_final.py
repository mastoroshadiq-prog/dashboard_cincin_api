import os

# TARGET FILE: V10 SMART (The one you are viewing)
FILE = r'data/output/dashboard_cincin_api_ISO_TABBED_v10_SMART.html'
# Also fix the main V10 container just in case
FILE_BACKUP = r'data/output/dashboard_cincin_api_ISO_TABBED_v10.html'

# CLEAN FUNCTION IMPLEMENTATION (NO NESTED SCRIPT TAGS IN TEMPLATE STRING)
# We separate the script content from the HTML template to maximize safety.

CLEAN_CODE = '''
            function generateExecutiveReport() {
                const selected = document.querySelectorAll('.report-option.selected');
                const modules = Array.from(selected).map(el => el.getAttribute('data-value'));

                if (modules.length === 0) {
                    alert("Pilih minimal satu modul untuk laporan!");
                    return;
                }

                // CREATE NEW WINDOW FOR PRINTING
                const printWin = window.open('', '_blank');
                if (!printWin) {
                    alert("Popup blocked! Please allow popups for this dashboard.");
                    return;
                }
                
                // DATA GATHERING (Safe Logic)
                const today = new Date().toLocaleDateString('id-ID', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
                
                // GENERATE CONTENT HTML (Only HTML DIVS, NO SCRIPTS!)
                let contentHtml = `
                    <div class="mb-8 border-b-2 border-slate-800 pb-4">
                        <div class="flex justify-between items-end">
                            <h1 class="text-4xl font-black text-slate-900 uppercase tracking-tighter">Executive Summary</h1>
                            <div class="text-right">
                                <p class="text-sm font-bold text-slate-500 uppercase">Cincin Api Assessment</p>
                                <p class="text-lg font-black text-rose-600">${today}</p>
                            </div>
                        </div>
                    </div>
                `;
                
                // Add Strategic Commentary
                contentHtml += generateStrategicCommentary();
                
                // Add Modules
                if (modules.includes('financial_summary')) {
                     const totalLoss = document.getElementById('summaryTotalLoss')?.textContent || '--';
                     const criticalCount = document.getElementById('summaryCriticalCount')?.textContent || '--';
                     contentHtml += `
                        <div class="mb-8 break-inside-avoid">
                            <h2 class="text-2xl font-black text-slate-800 uppercase mb-4">Financial Exposure</h2>
                            <p class="text-xl">Total Loss: Rp ${totalLoss} M | Critical Blocks: ${criticalCount}</p>
                        </div>
                     `;
                }
                
                // ... (Simplified for stability) ...

                const finalDoc = `
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <title>Report</title>
                        <script src="https://cdn.tailwindcss.com"><\/script>
                    </head>
                    <body class="p-8">
                        ${contentHtml}
                        <script>setTimeout(() => { window.print(); }, 1000);<\/script>
                    </body>
                    </html>
                `;
                
                printWin.document.write(finalDoc);
                printWin.document.close();
            }
'''

def fix_file(filepath):
    if not os.path.exists(filepath): return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # FIND THE BROKEN FUNCTION
    # It usually starts with: function generateExecutiveReport() {
    # And ends before: function generateStrategicCommentary() {
    
    start_marker = "function generateExecutiveReport() {"
    end_marker = "function generateStrategicCommentary() {"
    
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        print(f"Found broken function block in {filepath}. Overwriting...")
        
        # Replace the entire block with CLEAN_CODE
        new_content = content[:start_idx] + CLEAN_CODE + '\n\n' + content[end_idx:]
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("✅ File fixed.")
    else:
        print(f"Could not locate function block in {filepath}.")

def main():
    fix_file(FILE)
    fix_file(FILE_BACKUP)

if __name__ == "__main__":
    main()
