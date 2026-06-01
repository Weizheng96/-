import sys, io, pdfplumber
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
pdf = pdfplumber.open("d:/project/高价值专利检测/专利集/CN107634908B/候选/08-agora-rtc/agora_sd-rtn_whitepaper.pdf")
for i, p in enumerate(pdf.pages):
    print(f"--- p{i+1} ---")
    print(p.extract_text() or "(empty)")
pdf.close()
