#!/usr/bin/env python3
"""
Generates high-resolution QR codes, PNG poster, PDF poster, and printable HTML poster
for Stitch Waste attendance check-in at NPCL KP-4, Greater Noida.
Location: https://www.google.com/maps/place/NPCL+(Corporate+Office+KP-4)/@28.487329,77.5332451,113m/
(28.4875107, 77.5333647)
"""

import os
import sys
import base64
import qrcode
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

FONT_BOLD = "/home/rahul/.local/share/fonts/microsoft/NirmalaB.ttf"
FONT_REG = "/home/rahul/.local/share/fonts/microsoft/Nirmala.ttf"

TARGET_URL = "https://githubuser45566.github.io/attendance-checkin/?site=npcl_kp4"
COMPANY_NAME = "Stitch Waste"
SITE_NAME = "NPCL KP-4, Greater Noida"
SITE_ADDRESS = "NPCL Corporate Office, Knowledge Park IV, Greater Noida, UP 201310"

def generate_qr(target_url, filename="npcl_kp4_qr.png"):
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

def generate_png_poster(target_url, company_name=COMPANY_NAME, site_name=SITE_NAME, site_address=SITE_ADDRESS):
    qr_filename = "npcl_kp4_qr.png"
    qr_path = generate_qr(target_url, qr_filename)

    width, height = 1240, 1754
    img = Image.new("RGB", (width, height), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    f_badge = ImageFont.truetype(FONT_BOLD, 16)
    f_title = ImageFont.truetype(FONT_BOLD, 46)
    f_sub = ImageFont.truetype(FONT_BOLD, 26)
    f_site = ImageFont.truetype(FONT_BOLD, 22)
    f_addr = ImageFont.truetype(FONT_REG, 17)

    f_caption_1 = ImageFont.truetype(FONT_BOLD, 22)
    f_caption_2 = ImageFont.truetype(FONT_BOLD, 18)

    f_sec_title = ImageFont.truetype(FONT_BOLD, 24)
    f_step_num = ImageFont.truetype(FONT_BOLD, 22)
    f_step_title = ImageFont.truetype(FONT_BOLD, 20)
    f_step_desc = ImageFont.truetype(FONT_REG, 17)

    f_notice_title = ImageFont.truetype(FONT_BOLD, 19)
    f_notice_body1 = ImageFont.truetype(FONT_REG, 16)
    f_notice_body2 = ImageFont.truetype(FONT_BOLD, 16)
    f_footer = ImageFont.truetype(FONT_REG, 15)

    # 1. Outer Frame Border
    draw.rounded_rectangle([30, 30, width - 30, height - 30], radius=24, outline="#D1D7DB", width=3)

    # 2. Badge (Top Centered)
    badge_text = "OFFICIAL SITE ATTENDANCE"
    b_box = draw.textbbox((0, 0), badge_text, font=f_badge)
    bw, bh = b_box[2] - b_box[0], b_box[3] - b_box[1]
    bx = (width - bw) // 2
    by = 65
    draw.rounded_rectangle([bx - 18, by - 6, bx + bw + 18, by + bh + 8], radius=14, fill="#E8F5E9")
    draw.text((bx, by), badge_text, fill="#075E54", font=f_badge)

    # 3. Company Title
    t_box = draw.textbbox((0, 0), company_name, font=f_title)
    draw.text(((width - (t_box[2] - t_box[0])) // 2, 115), company_name, fill="#075E54", font=f_title)

    # 4. Hindi Subtitle
    sub_text = "दैनिक उपस्थिति एवं लोकेशन चेक-इन"
    s_box = draw.textbbox((0, 0), sub_text, font=f_sub)
    draw.text(((width - (s_box[2] - s_box[0])) // 2, 180), sub_text, fill="#111B21", font=f_sub)

    # 5. Site Name & Address
    site_str = f"Site: {site_name}"
    site_box = draw.textbbox((0, 0), site_str, font=f_site)
    draw.text(((width - (site_box[2] - site_box[0])) // 2, 224), site_str, fill="#075E54", font=f_site)

    addr_str = site_address
    addr_box = draw.textbbox((0, 0), addr_str, font=f_addr)
    draw.text(((width - (addr_box[2] - addr_box[0])) // 2, 256), addr_str, fill="#667781", font=f_addr)

    # Header Divider Line
    draw.line([70, 290, width - 70, 290], fill="#E9EDEF", width=2)

    # 6. QR Code Card Container
    card_x1, card_y1, card_x2, card_y2 = 320, 315, 920, 905
    draw.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=20, fill="#FAFAFA", outline="#E0E0E0", width=2)

    qr_img = Image.open(qr_path).convert('RGB')
    qr_size = 460
    qr_img = qr_img.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
    qrx = (width - qr_size) // 2
    qry = card_y1 + 25
    img.paste(qr_img, (qrx, qry))

    cap1 = "SCAN WITH ANY SMARTPHONE CAMERA"
    c1_box = draw.textbbox((0, 0), cap1, font=f_caption_1)
    draw.text(((width - (c1_box[2] - c1_box[0])) // 2, qry + qr_size + 18), cap1, fill="#075E54", font=f_caption_1)

    cap2 = "कैमरा या गूगल लेंस से स्कैन करें"
    c2_box = draw.textbbox((0, 0), cap2, font=f_caption_2)
    draw.text(((width - (c2_box[2] - c2_box[0])) // 2, qry + qr_size + 50), cap2, fill="#667781", font=f_caption_2)

    # 7. Steps Section
    steps_x = 100
    steps_y = 945
    draw.text((steps_x, steps_y), "3 Simple Steps / 3 आसान चरण:", fill="#111B21", font=f_sec_title)

    steps = [
        (
            "1",
            "1. Scan QR Code (क्यूआर कोड स्कैन करें)",
            "Open phone camera or Google Lens and point at this QR code."
        ),
        (
            "2",
            "2. Allow GPS Location (लोकेशन की अनुमति दें)",
            "Browser will automatically verify your presence at NPCL KP-4."
        ),
        (
            "3",
            "3. Send to Attendance Group (व्हाट्सएप ग्रुप में भेजें)",
            "Tap PUNCH IN or OUT, select your Attendance Group, and tap Send."
        )
    ]

    sy = steps_y + 45
    for num, title, desc in steps:
        cx, cy, r = steps_x + 22, sy + 22, 22
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill="#128C7E")
        n_box = draw.textbbox((0, 0), num, font=f_step_num)
        nw, nh = n_box[2] - n_box[0], n_box[3] - n_box[1]
        draw.text((cx - nw // 2, cy - nh // 2 - 2), num, fill="#FFFFFF", font=f_step_num)

        tx = steps_x + 60
        draw.text((tx, sy + 2), title, fill="#111B21", font=f_step_title)
        draw.text((tx, sy + 30), desc, fill="#667781", font=f_step_desc)
        sy += 85

    # 8. Strict Notice Box
    ny1 = 1325
    ny2 = 1490
    nx1, nx2 = 80, width - 80
    draw.rounded_rectangle([nx1, ny1, nx2, ny2], radius=14, fill="#FFF3E0")
    draw.rectangle([nx1, ny1, nx1 + 8, ny2], fill="#FF9800")

    draw.text((nx1 + 24, ny1 + 16), "Strict Attendance Policy / सख्त उपस्थिति नियम:", fill="#E65100", font=f_notice_title)
    notice_l1 = "Every employee must punch from their own mobile phone. Proxy attendance is strictly prohibited."
    notice_l2 = "प्रत्येक कर्मचारी अपने ही फोन से पंच करें। प्रॉक्सी हाजिरी सिस्टम द्वारा स्वतः खारिज कर दी जाएगी।"
    draw.text((nx1 + 24, ny1 + 52), notice_l1, fill="#BF360C", font=f_notice_body1)
    draw.text((nx1 + 24, ny1 + 86), notice_l2, fill="#BF360C", font=f_notice_body2)

    # 9. Footer
    draw.line([70, 1530, width - 70, 1530], fill="#E9EDEF", width=2)
    footer_t1 = f"Automated WhatsApp Attendance & Verification System • {company_name}"
    f1_box = draw.textbbox((0, 0), footer_t1, font=f_footer)
    draw.text(((width - (f1_box[2] - f1_box[0])) // 2, 1555), footer_t1, fill="#8696A0", font=f_footer)

    footer_t2 = f"Direct Link: {target_url}"
    f2_box = draw.textbbox((0, 0), footer_t2, font=f_footer)
    draw.text(((width - (f2_box[2] - f2_box[0])) // 2, 1585), footer_t2, fill="#128C7E", font=f_footer)

    out_png = os.path.join(OUTPUT_DIR, "npcl_kp4_attendance_poster.png")
    img.save(out_png, "PNG", quality=95)
    print(f"[✓] Generated High-Res PNG Poster at: {out_png}")
    return out_png

def generate_pdf_poster(target_url, company_name=COMPANY_NAME, site_name=SITE_NAME):
    png_path = os.path.join(OUTPUT_DIR, "npcl_kp4_attendance_poster.png")
    if not os.path.exists(png_path):
        generate_png_poster(target_url, company_name, site_name)

    out_pdf = os.path.join(OUTPUT_DIR, "npcl_kp4_attendance_poster.pdf")
    c = canvas.Canvas(out_pdf, pagesize=A4)
    page_w, page_h = A4

    c.drawImage(png_path, 0, 0, width=page_w, height=page_h)
    c.showPage()
    c.save()
    print(f"[✓] Generated Printable PDF Poster at: {out_pdf}")
    return out_pdf

def generate_html_poster(target_url, company_name=COMPANY_NAME, site_name=SITE_NAME, site_address=SITE_ADDRESS):
    qr_filename = "npcl_kp4_qr.png"
    qr_path = generate_qr(target_url, qr_filename)

    with open(qr_path, "rb") as f:
        qr_base64 = base64.b64encode(f.read()).decode("utf-8")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Attendance QR Poster - {company_name} ({site_name})</title>
  <style>
    @page {{
      size: A4 portrait;
      margin: 10mm;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Segoe UI', 'Nirmala UI', -apple-system, Roboto, 'Noto Sans Devanagari', sans-serif;
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
      width: 190mm;
      max-width: 100%;
      min-height: 277mm;
      background: #ffffff;
      padding: 28px 36px;
      border-radius: 12px;
      box-shadow: 0 4px 20px rgba(0,0,0,0.08);
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
      padding-bottom: 14px;
    }}
    .badge {{
      display: inline-block;
      background: #e8f5e9;
      color: #075e54;
      font-size: 13px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 1px;
      padding: 4px 14px;
      border-radius: 20px;
      margin-bottom: 8px;
    }}
    h1 {{
      font-size: 32px;
      color: #075e54;
      font-weight: 800;
      letter-spacing: 0.5px;
      margin-bottom: 2px;
    }}
    h2 {{
      font-size: 20px;
      color: #111b21;
      font-weight: 600;
      margin-bottom: 6px;
    }}
    .site-tag {{
      font-size: 15px;
      color: #075e54;
      font-weight: 700;
    }}
    .site-addr {{
      font-size: 12px;
      color: #667781;
      margin-top: 2px;
    }}
    .qr-container {{
      background: #fafafa;
      border: 2px solid #e0e0e0;
      border-radius: 16px;
      padding: 16px;
      text-align: center;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      box-shadow: inset 0 2px 6px rgba(0,0,0,0.02);
      margin: 10px 0;
    }}
    .qr-container img {{
      width: 320px;
      height: 320px;
      display: block;
    }}
    .qr-caption {{
      font-size: 15px;
      font-weight: 800;
      color: #075e54;
      margin-top: 10px;
      letter-spacing: 0.5px;
    }}
    .qr-subcaption {{
      font-size: 13px;
      color: #667781;
      font-weight: 600;
      margin-top: 2px;
    }}
    .steps-container {{
      width: 100%;
      background: #f7f9fa;
      border-radius: 12px;
      padding: 16px 20px;
      border: 1px solid #e9edef;
    }}
    .steps-title {{
      font-size: 16px;
      font-weight: 700;
      color: #111b21;
      margin-bottom: 12px;
    }}
    .step-item {{
      display: flex;
      align-items: flex-start;
      margin-bottom: 10px;
    }}
    .step-item:last-child {{
      margin-bottom: 0;
    }}
    .step-num {{
      background: #128c7e;
      color: white;
      width: 26px;
      height: 26px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 14px;
      flex-shrink: 0;
      margin-right: 12px;
      margin-top: 2px;
    }}
    .step-text h4 {{
      font-size: 14px;
      font-weight: 700;
      color: #111b21;
      margin-bottom: 2px;
    }}
    .step-text p {{
      font-size: 12px;
      color: #667781;
    }}
    .notice-box {{
      width: 100%;
      background: #fff3e0;
      border-left: 5px solid #ff9800;
      border-radius: 8px;
      padding: 10px 16px;
      font-size: 12px;
      color: #bf360c;
      line-height: 1.4;
    }}
    .footer {{
      text-align: center;
      width: 100%;
      font-size: 12px;
      color: #8696a0;
      border-top: 1px solid #e9edef;
      padding-top: 10px;
    }}
    .footer-url {{
      color: #128C7E;
      font-weight: 600;
      margin-top: 3px;
      font-size: 11px;
    }}
    @media print {{
      body {{
        background: transparent !important;
        padding: 0 !important;
      }}
      .poster {{
        border: none !important;
        box-shadow: none !important;
        width: 100% !important;
        min-height: auto !important;
        height: 100% !important;
        padding: 0 !important;
        page-break-inside: avoid !important;
        page-break-after: avoid !important;
      }}
    }}
  </style>
</head>
<body>
  <div class="poster">
    <div class="header">
      <div class="badge">Official Site Attendance</div>
      <h1>{company_name}</h1>
      <h2>दैनिक उपस्थिति एवं लोकेशन चेक-इन</h2>
      <div class="site-tag">Site: <strong>{site_name}</strong></div>
      <div class="site-addr">{site_address}</div>
    </div>

    <div class="qr-container">
      <img src="data:image/png;base64,{qr_base64}" alt="Scan for Attendance">
      <div class="qr-caption">SCAN WITH ANY SMARTPHONE CAMERA</div>
      <div class="qr-subcaption">कैमरा या गूगल लेंस से स्कैन करें</div>
    </div>

    <div class="steps-container">
      <div class="steps-title">3 Simple Steps / 3 आसान चरण:</div>
      
      <div class="step-item">
        <div class="step-num">1</div>
        <div class="step-text">
          <h4>1. Scan QR Code (क्यूआर कोड स्कैन करें)</h4>
          <p>Open phone camera or Google Lens and point at this code.</p>
        </div>
      </div>

      <div class="step-item">
        <div class="step-num">2</div>
        <div class="step-text">
          <h4>2. Allow GPS Location (लोकेशन की अनुमति दें)</h4>
          <p>Browser will automatically verify your presence at NPCL KP-4.</p>
        </div>
      </div>

      <div class="step-item">
        <div class="step-num">3</div>
        <div class="step-text">
          <h4>3. Send to Attendance Group (व्हाट्सएप ग्रुप में भेजें)</h4>
          <p>Tap PUNCH IN or OUT, select your Attendance Group, and tap Send.</p>
        </div>
      </div>
    </div>

    <div class="notice-box">
      <strong>Strict Attendance Policy / सख्त उपस्थिति नियम:</strong><br>
      Every employee must punch from their own mobile phone. Proxy attendance is strictly prohibited.<br>
      प्रत्येक कर्मचारी अपने ही फोन से पंच करें। प्रॉक्सी हाजिरी सिस्टम द्वारा स्वतः खारिज कर दी जाएगी।
    </div>

    <div class="footer">
      Automated WhatsApp Attendance & Verification System • {company_name}
      <div class="footer-url">{target_url}</div>
    </div>
  </div>
</body>
</html>
"""
    out_html = os.path.join(OUTPUT_DIR, "npcl_kp4_attendance_poster.html")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[✓] Generated Self-Contained Printable Poster at: {out_html}")
    return out_html

def generate_all():
    print("=" * 60)
    print(f"Generating NPCL KP-4 Attendance Poster Suite for {COMPANY_NAME}...")
    print(f"Site: {SITE_NAME} ({SITE_ADDRESS})")
    print(f"Target URL: {TARGET_URL}")
    print("=" * 60)
    generate_qr(TARGET_URL)
    generate_png_poster(TARGET_URL)
    generate_pdf_poster(TARGET_URL)
    generate_html_poster(TARGET_URL)
    print("=" * 60)
    print("[✓] All NPCL KP-4 formats generated successfully!")
    print("=" * 60)

if __name__ == "__main__":
    generate_all()
