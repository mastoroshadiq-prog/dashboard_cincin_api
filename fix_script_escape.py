import re

FILE = r'data/output/dashboard_cincin_api_ISO_TABBED_v10.html'

def main():
    with open(FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Kita mencari fungsi generateExecutiveReport
    start_fn = content.find("function generateExecutiveReport()")
    if start_fn == -1:
        print("Function not found!")
        return
        
    end_fn = content.find("function generateStrategicCommentary()", start_fn)
    
    # Ambil potongan kode fungsi tersebut
    func_code = content[start_fn:end_fn]
    
    # Di dalam potongan kode ini, kita cari </script> yang TIDAK di-escape
    # Kita ganti menjadi <\/script>
    
    # Regex lookbehind sulit di python standar jika panjang variable, jadi kita replace string literal saja.
    # Kita tahu formatnya di file source biasanya: </script>
    # Tapi kita tidak boleh replace </script> yang menutup tag HTML utama. 
    # Untungnya, generateExecutiveReport ada di DALAM tag <script> utama.
    # Jadi SEMUA </script> di dalam range `func_code` ADALAH ILEGAL (karena itu nested string).
    
    fixed_code = func_code.replace("</script>", "<\/script>")
    
    if fixed_code == func_code:
        print("No unescaped script tags found in the target function.")
        # Coba cek variasi lain?
    else:
        print(f"Fixed unescaped script tags inside generateExecutiveReport.")
        
    # Replace kembali ke content utama
    new_content = content[:start_fn] + fixed_code + content[end_fn:]
    
    with open(FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)
        
    print("✅ FIX APPLIED: Escaped nested closing script tags.")

if __name__ == "__main__":
    main()
