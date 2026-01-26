try:
    import fpdf
    print("FPDF Available")
except ImportError:
    print("FPDF Not Available")

try:
    import reportlab
    print("ReportLab Available")
except ImportError:
    print("ReportLab Not Available")

try:
    import matplotlib.pyplot as plt
    print("Matplotlib Available")
except ImportError:
    print("Matplotlib Not Available")
