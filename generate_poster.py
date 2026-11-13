#!/usr/bin/env python3
"""
Generates high-resolution QR codes, PNG poster, PDF poster, and printable HTML poster
for Stitch Waste employee attendance check-in.
"""

import os
import sys
import qrcode
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

FONT_LATIN_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_LATIN_REG = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FONT_DEVA_BOLD = "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Bold.ttf"
FONT_DEVA_REG = "/usr/share/fonts/truetype/noto/NotoSansDevanagari-Regular.ttf"

def generate_qr(target_url, filename="qr_code.png"):
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=12,
        border=2,
    )
    qr.add_data(target_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="#075E54", back_color="white").convert('RGB')
    out_path = os.path.join(OUTPUT_DIR, filename)
    img.save(out_path)
    print(f"[✓] Generated QR code at: {out_path}")
    return out_path

def generate_png_poster(target_url, company_name="Stitch Waste", site_name="Devasya"):
    qr_filename = "qr_code.png"
    qr_path = generate_qr(target_url, qr_filename)

    width, height = 1240, 1754
    img = Image.new("RGB", (width, height), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    f_badge = ImageFont.truetype(FONT_LATIN_BOLD, 16)
    f_title = ImageFont.truetype(FONT_LATIN_BOLD, 46)
    f_sub = ImageFont.truetype(FONT_DEVA_BOLD, 26)
    f_site = ImageFont.truetype(FONT_LATIN_REG, 20)
    f_site_b = ImageFont.truetype(FONT_LATIN_BOLD, 20)

    f_caption_1 = ImageFont.truetype(FONT_LATIN_BOLD, 20)
    f_caption_2 = ImageFont.truetype(FONT_DEVA_REG, 17)

    f_sec_title = ImageFont.truetype(FONT_DEVA_BOLD, 22)
    f_step_num = ImageFont.truetype(FONT_LATIN_BOLD, 22)
    f_step_title = ImageFont.truetype(FONT_DEVA_BOLD, 20)
    f_step_desc = ImageFont.truetype(FONT_LATIN_REG, 16)

    f_notice_title = ImageFont.truetype(FONT_DEVA_BOLD, 17)
    f_notice_body = ImageFont.truetype(FONT_LATIN_REG, 15)
    f_footer = ImageFont.truetype(FONT_LATIN_REG, 15)

    # 1. Outer Frame Border
    draw.rounded_rectangle([25, 25, width - 25, height - 25], radius=24, outline="#D1D7DB", width=2)

    # 2. Badge (Top Centered)
    badge_text = "OFFICIAL DUTY ATTENDANCE"
    b_box = draw.textbbox((0, 0), badge_text, font=f_badge)
    bw, bh = b_box[2] - b_box[0], b_box[3] - b_box[1]
    bx = (width - bw) // 2
    by = 55
    draw.rounded_rectangle([bx - 16, by - 6, bx + bw + 16, by + bh + 8], radius=14, fill="#E8F5E9")
    draw.text((bx, by), badge_text, fill="#075E54", font=f_badge)

    # 3. Company Title
    t_box = draw.textbbox((0, 0), company_name, font=f_title)
    tw = t_box[2] - t_box[0]
    draw.text(((width - tw) // 2, 105), company_name, fill="#075E54", font=f_title)

    # 4. Hindi Subtitle
    sub_text = "दैनिक उपस्थिति एवं लोकेशन चेक-इन"
    s_box = draw.textbbox((0, 0), sub_text, font=f_sub)
    sw = s_box[2] - s_box[0]
    draw.text(((width - sw) // 2, 175), sub_text, fill="#111B21", font=f_sub)

    # 5. Site Name
    site_str = f"Site / Duty Location: {site_name}"
    site_box = draw.textbbox((0, 0), site_str, font=f_site)
    sitew = site_box[2] - site_box[0]
    draw.text(((width - sitew) // 2, 225), site_str, fill="#667781", font=f_site)

    # Header Divider Line
    draw.line([60, 275, width - 60, 275], fill="#E9EDEF", width=2)

    # 6. QR Code Card Container
    card_x1, card_y1, card_x2, card_y2 = 320, 305, 920, 895
    draw.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=20, fill="#FAFAFA", outline="#E0E0E0", width=2)

    qr_img = Image.open(qr_path).convert('RGB')
    qr_size = 460
    qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
    qrx = (width - qr_size) // 2
    qry = card_y1 + 25
    img.paste(qr_img, (qrx, qry))

    cap1 = "📲 SCAN WITH ANY SMARTPHONE CAMERA"
    c1_box = draw.textbbox((0, 0), cap1, font=f_caption_1)
    draw.text(((width - (c1_box[2] - c1_box[0])) // 2, qry + qr_size + 18), cap1, fill="#075E54", font=f_caption_1)

    cap2 = "कैमरा या गूगल लेंस से स्कैन करें"
    c2_box = draw.textbbox((0, 0), cap2, font=f_caption_2)
    draw.text(((width - (c2_box[2] - c2_box[0])) // 2, qry + qr_size + 48), cap2, fill="#667781", font=f_caption_2)

    # 7. Steps Section
    steps_x = 90
    steps_y = 935

    draw.text((steps_x, steps_y), "📋 3 Simple Steps / 3 आसान चरण:", fill="#111B21", font=f_sec_title)

    steps = [
        (
            "1",
            "1. Scan QR Code (क्यूआर कोड स्कैन करें)",
            "Open phone camera or Google Lens and point at this QR code."
        ),
        (
            "2",
            "2. Allow GPS Location (लोकेशन की अनुमति दें)",
            "Browser will verify your presence at the official duty site."
        ),
        (
            "3",
            "3. Tap Punch In & Send (पंच इन दबाकर भेजें)",
            "WhatsApp opens directly with your live location. Tap Send."
        )
    ]

    sy = steps_y + 45
    for num, title, desc in steps:
        # Green Circle with Number
        cx, cy, r = steps_x + 22, sy + 22, 22
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#128C7E")
        n_box = draw.textbbox((0, 0), num, font=f_step_num)
        nw, nh = n_box[2] - n_box[0], n_box[3] - n_box[1]
        draw.text((cx - nw // 2, cy - nh // 2 - 2), num, fill="#FFFFFF", font=f_step_num)

        # Title & Description
        tx = steps_x + 60
        draw.text((tx, sy + 2), title, fill="#111B21", font=f_step_title)
        draw.text((tx, sy + 28), desc, fill="#667781", font=f_step_desc)

        sy += 75

    # 8. Strict Notice Box
    ny1 = 1290
    ny2 = 1435
    nx1, nx2 = 80, width - 80
    draw.rounded_rectangle([nx1, ny1, nx2, ny2], radius=12, fill="#FFF3E0")
    draw.rectangle([nx1, ny1, nx1 + 8, ny2], fill="#FF9800")

    draw.text((nx1 + 24, ny1 + 16), "⚠️ Strict Attendance Policy / सख्त उपस्थिति नियम:", fill="#E65100", font=f_notice_title)
    notice_line1 = "Every employee must punch from their own mobile phone. Proxy attendance is strictly prohibited."
    notice_line2 = "प्रत्येक कर्मचारी अपने ही फोन से पंच करें। प्रॉक्सी हाजिरी सिस्टम द्वारा स्वतः खारिज कर दी जाएगी।"
    draw.text((nx1 + 24, ny1 + 48), notice_line1, fill="#BF360C", font=f_notice_body)
    draw.text((nx1 + 24, ny1 + 76), notice_line2, fill="#BF360C", font=f_notice_title)

    # 9. Footer
    draw.line([60, 1510, width - 60, 1510], fill="#E9EDEF", width=2)

    footer_t1 = f"Automated WhatsApp Attendance & Verification System • {company_name}"
    f1_box = draw.textbbox((0, 0), footer_t1, font=f_footer)
    draw.text(((width - (f1_box[2] - f1_box[0])) // 2, 1530), footer_t1, fill="#8696A0", font=f_footer)

    footer_t2 = f"Direct Check-In Web App: {target_url}"
    f2_box = draw.textbbox((0, 0), footer_t2, font=f_footer)
    draw.text(((width - (f2_box[2] - f2_box[0])) // 2, 1560), footer_t2, fill="#128C7E", font=f_footer)

    out_png = os.path.join(OUTPUT_DIR, "attendance_poster.png")
    img.save(out_png, "PNG", quality=95)
    print(f"[✓] Generated High-Res PNG Poster at: {out_png}")
    return out_png

def generate_pdf_poster(target_url, company_name="Stitch Waste", site_name="Devasya"):
    png_path = os.path.join(OUTPUT_DIR, "attendance_poster.png")
    if not os.path.exists(png_path):
        generate_png_poster(target_url, company_name, site_name)

    out_pdf = os.path.join(OUTPUT_DIR, "attendance_poster.pdf")
    c = canvas.Canvas(out_pdf, pagesize=A4)
    page_w, page_h = A4

    c.drawImage(png_path, 0, 0, width=page_w, height=page_h)
    c.showPage()
    c.save()
    print(f"[✓] Generated Vector Printable PDF Poster at: {out_pdf}")
    return out_pdf

def generate_html_poster(target_url, company_name="Stitch Waste", site_name="Devasya"):
    qr_filename = "qr_code.png"
    generate_qr(target_url, qr_filename)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Attendance QR Poster - {company_name}</title>
  <style>
    @page {{
      size: A4 portrait;
      margin: 15mm;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Segoe UI', -apple-system, Roboto, Helvetica, Arial, sans-serif;
    }}
    body {{
      background: #f0f2f5;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      padding: 20px;
    }}
    .poster {{
      width: 210mm;
      min-height: 297mm;
      background: #ffffff;
      padding: 30px 40px;
      border-radius: 12px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.1);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      border: 1px solid #d1d7db;
    }}
    .header {{
      text-align: center;
      width: 100%;
      border-bottom: 2px solid #e9edef;
      padding-bottom: 18px;
    }}
    .badge {{
      display: inline-block;
      background: #e8f5e9;
      color: #075e54;
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      padding: 5px 14px;
      border-radius: 20px;
      margin-bottom: 8px;
    }}
    .header h1 {{
      font-size: 38px;
      font-weight: 800;
      color: #075E54;
      margin-bottom: 4px;
    }}
    .header h2 {{
      font-size: 20px;
      font-weight: 600;
      color: #111b21;
    }}
    .qr-container {{
      background: #f8f9fa;
      padding: 24px;
      border-radius: 16px;
      border: 2px dashed #075E54;
      text-align: center;
      margin: 20px 0;
      box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }}
    .qr-container img {{
      width: 240px;
      height: 240px;
      display: block;
      margin: 0 auto;
    }}
    .qr-caption {{
      margin-top: 14px;
      font-size: 15px;
      font-weight: 700;
      color: #075E54;
      letter-spacing: 0.5px;
    }}
    .steps-container {{
      width: 100%;
      background: #ffffff;
      border-radius: 10px;
      padding: 10px 0;
    }}
    .steps-title {{
      font-size: 16px;
      font-weight: 700;
      color: #111b21;
      margin-bottom: 14px;
    }}
    .step-item {{
      display: flex;
      align-items: flex-start;
      margin-bottom: 14px;
      gap: 14px;
    }}
    .step-num {{
      background: #128C7E;
      color: white;
      width: 32px;
      height: 32px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 15px;
      flex-shrink: 0;
    }}
    .step-text h4 {{
      font-size: 15px;
      font-weight: 700;
      color: #111b21;
    }}
    .step-text p {{
      font-size: 13px;
      color: #667781;
      margin-top: 2px;
    }}
    .notice-box {{
      width: 100%;
      background: #fff3e0;
      border-left: 5px solid #ff9800;
      padding: 12px 16px;
      border-radius: 8px;
      font-size: 12px;
      color: #e65100;
      line-height: 1.4;
      margin-top: 15px;
    }}
    .footer {{
      width: 100%;
      text-align: center;
      font-size: 12px;
      color: #8696a0;
      border-top: 1px solid #e9edef;
      padding-top: 12px;
    }}
    @media print {{
      body {{
        background: white;
        padding: 0;
      }}
      .poster {{
        border: none;
        box-shadow: none;
        width: 100%;
        min-height: 100%;
        padding: 20px;
      }}
    }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="header">
      <div class="badge">Official Duty Attendance</div>
      <h1>{company_name}</h1>
      <h2>दैनिक उपस्थिति एवं लोकेशन चेक-इन</h2>
      <div style="font-size: 13px; color: #667781; margin-top: 4px;">Site / Location: <strong>{site_name}</strong></div>
    </div>

    <div class="qr-container">
      <img src="{qr_filename}" alt="Scan for Attendance">
      <div class="qr-caption">📲 SCAN WITH ANY SMARTPHONE CAMERA</div>
      <div style="font-size: 12px; color: #667781; margin-top: 2px;">कैमरा या गूगल लेंस से स्कैन करें</div>
    </div>

    <div class="steps-container">
      <div class="steps-title">📋 3 Simple Steps / 3 आसान चरण:</div>
      
      <div class="step-item">
        <div class="step-num">1</div>
        <div class="step-text">
          <h4>Scan QR Code (क्यूआर कोड स्कैन करें)</h4>
          <p>Open phone camera or Google Lens and point at this code.</p>
        </div>
      </div>

      <div class="step-item">
        <div class="step-num">2</div>
        <div class="step-text">
          <h4>Allow GPS Location (लोकेशन की अनुमति दें)</h4>
          <p>Browser will verify your presence at the duty site.</p>
        </div>
      </div>

      <div class="step-item">
        <div class="step-num">3</div>
        <div class="step-text">
          <h4>Tap "Punch In" & Send (पंच इन दबाकर भेजें)</h4>
          <p>WhatsApp will open directly with your live location. Tap Send.</p>
        </div>
      </div>
    </div>

    <div class="notice-box">
      ⚠️ <strong>Strict Policy / सख्त नियम:</strong> Every employee must punch from their own mobile phone. Proxy attendance is automatically detected and rejected by the attendance server.
    </div>

    <div class="footer">
      Automated WhatsApp Attendance & Verification System • {company_name}
    </div>
  </div>
</body>
</html>
"""
    out_html = os.path.join(OUTPUT_DIR, "attendance_poster.html")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[✓] Generated Printable Poster at: {out_html}")
    return out_html

def generate_all(target_url, company_name="Stitch Waste", site_name="Devasya"):
    print("=" * 60)
    print(f"Generating Complete Attendance Poster Suite for {company_name}...")
    print(f"Target URL: {target_url}")
    print("=" * 60)
    generate_qr(target_url)
    generate_png_poster(target_url, company_name, site_name)
    generate_pdf_poster(target_url, company_name, site_name)
    generate_html_poster(target_url, company_name, site_name)
    print("=" * 60)
    print("[✓] All formats generated successfully!")
    print("=" * 60)

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://githubuser45566.github.io/attendance-checkin/"
    generate_all(url)
