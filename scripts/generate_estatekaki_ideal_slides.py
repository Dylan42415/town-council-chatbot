"""
EstateKaki Ideal Presentation Deck Generator
Generates an 8-slide, beautifully formatted 16:9 widescreen presentation:
output/slides/EstateKaki_Showcase_Ideal.pptx

Preserves the friendly, approachable aesthetic of EstateKaki while correcting
all factual errors, properly taking credit for voice memos and multilingual support,
and giving the team a natural, effortless script to present.
"""

from __future__ import annotations

import os
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "output" / "slides"
OUT_DIR.mkdir(parents=True, exist_ok=True)
PPTX_PATH = OUT_DIR / "EstateKaki_Showcase_Ideal.pptx"

# Color Palette (Friendly EstateKaki Navy & Pastel Accents)
BG_DARK = RGBColor(19, 30, 51)      # #131E33 - Deep Friendly Navy
CARD_BG = RGBColor(28, 44, 73)      # #1C2C49 - Navy Card
CARD_ALT = RGBColor(38, 59, 97)     # #263B61 - Lighter Navy Card
WHITE = RGBColor(248, 249, 250)     # Clean text
MUTED = RGBColor(176, 192, 214)     # Secondary body text

# Pastel Accents (Matching Canva Aesthetic)
YELLOW_ACCENT = RGBColor(254, 211, 105) # #FED369 - Soft Yellow
PEACH_ACCENT = RGBColor(250, 177, 160)  # #FAB1A0 - Soft Coral / Peach
MINT_ACCENT = RGBColor(85, 239, 196)    # #55EFC4 - Soft Mint
BLUE_BUBBLE = RGBColor(43, 110, 180)   # #2B6EB4 - Resident Telegram Bubble
GREEN_DONE = RGBColor(46, 204, 113)    # Resolved status green
AMBER = RGBColor(243, 156, 18)

FONT_FAMILY = "Calibri"


def set_bg(slide, color=BG_DARK):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_card(slide, left, top, width, height, fill=CARD_BG, border=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    if border:
        shape.line.color.rgb = border
        shape.line.width = Pt(1.5)
    else:
        shape.line.fill.background()
    return shape


def add_header(slide, title, category, slide_num):
    tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(10), Inches(0.35))
    p_c = tb_cat.text_frame.paragraphs[0]
    p_c.text = category.upper()
    p_c.font.name = FONT_FAMILY
    p_c.font.size = Pt(11)
    p_c.font.bold = True
    p_c.font.color.rgb = YELLOW_ACCENT

    tb_t = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(10.5), Inches(0.75))
    p_t = tb_t.text_frame.paragraphs[0]
    p_t.text = title
    p_t.font.name = FONT_FAMILY
    p_t.font.size = Pt(28)
    p_t.font.bold = True
    p_t.font.color.rgb = WHITE

    if slide_num:
        tb_n = slide.shapes.add_textbox(Inches(11.8), Inches(0.45), Inches(0.8), Inches(0.4))
        p_n = tb_n.text_frame.paragraphs[0]
        p_n.text = slide_num
        p_n.alignment = PP_ALIGN.RIGHT
        p_n.font.name = FONT_FAMILY
        p_n.font.size = Pt(12)
        p_n.font.color.rgb = MUTED


def add_speaker_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


def build_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: Title Slide (Cover)
    # =========================================================================
    s1 = prs.slides.add_slide(layout)
    set_bg(s1)

    # Left content
    add_card(s1, Inches(0.8), Inches(1.1), Inches(3.2), Inches(0.4), CARD_ALT, None)
    tb_badge = s1.shapes.add_textbox(Inches(0.85), Inches(1.1), Inches(3.1), Inches(0.38))
    tb_badge.text_frame.paragraphs[0].text = "TOWN COUNCIL RESIDENT ASSISTANT"
    tb_badge.text_frame.paragraphs[0].font.size = Pt(11)
    tb_badge.text_frame.paragraphs[0].font.bold = True
    tb_badge.text_frame.paragraphs[0].font.color.rgb = YELLOW_ACCENT

    tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(1.7), Inches(6.8), Inches(1.5))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p1 = tf1.paragraphs[0]
    p1.text = "EstateKaki"
    p1.font.size = Pt(50)
    p1.font.bold = True
    p1.font.color.rgb = WHITE

    tb_sub = s1.shapes.add_textbox(Inches(0.8), Inches(3.3), Inches(6.6), Inches(1.8))
    tf_sub = tb_sub.text_frame
    tf_sub.word_wrap = True
    p_sub = tf_sub.paragraphs[0]
    p_sub.text = (
        "A zero-install Telegram assistant that answers residents from official "
        "Town Council documents, never guesses, handles voice & photos, and turns "
        "fault reports into tracked tickets staff can close."
    )
    p_sub.font.size = Pt(17)
    p_sub.font.color.rgb = MUTED

    add_card(s1, Inches(0.8), Inches(5.6), Inches(6.6), Inches(0.8), CARD_ALT, MINT_ACCENT)
    tb_pill = s1.shapes.add_textbox(Inches(1.0), Inches(5.7), Inches(6.2), Inches(0.6))
    p_pill = tb_pill.text_frame.paragraphs[0]
    p_pill.text = "✨ No app to install. Residents are already on Telegram!"
    p_pill.font.size = Pt(14)
    p_pill.font.bold = True
    p_pill.font.color.rgb = MINT_ACCENT

    # Right Content: Simulated Telegram Mobile Experience
    add_card(s1, Inches(7.9), Inches(1.1), Inches(4.6), Inches(5.5), CARD_BG)

    # Bubbles
    add_card(s1, Inches(8.4), Inches(1.6), Inches(3.8), Inches(0.7), BLUE_BUBBLE)
    tb_b1 = s1.shapes.add_textbox(Inches(8.5), Inches(1.65), Inches(3.6), Inches(0.6))
    tb_b1.text_frame.word_wrap = True
    tb_b1.text_frame.paragraphs[0].text = "Resident: Corridor light's out again at Blk 802"
    tb_b1.text_frame.paragraphs[0].font.size = Pt(11)
    tb_b1.text_frame.paragraphs[0].font.color.rgb = WHITE

    add_card(s1, Inches(8.4), Inches(2.5), Inches(3.8), Inches(0.7), BLUE_BUBBLE)
    tb_b2 = s1.shapes.add_textbox(Inches(8.5), Inches(2.55), Inches(3.6), Inches(0.6))
    tb_b2.text_frame.word_wrap = True
    tb_b2.text_frame.paragraphs[0].text = "🎙️ [Voice Memo (12s)]: Auntie say lift jerky jerky..."
    tb_b2.text_frame.paragraphs[0].font.size = Pt(11)
    tb_b2.text_frame.paragraphs[0].font.color.rgb = WHITE

    add_card(s1, Inches(8.1), Inches(3.4), Inches(4.2), Inches(1.2), CARD_ALT)
    tb_b3 = s1.shapes.add_textbox(Inches(8.2), Inches(3.45), Inches(4.0), Inches(1.1))
    tb_b3.text_frame.word_wrap = True
    p_b3 = tb_b3.text_frame.paragraphs[0]
    p_b3.text = "EstateKaki Bot:\nTicket #TC-802 opened · Electrical & Lift Maintenance.\nDispatched to King Wan Electrical (SLA: < 4h)."
    p_b3.font.size = Pt(11)
    p_b3.font.color.rgb = WHITE

    add_card(s1, Inches(8.1), Inches(4.8), Inches(4.2), Inches(0.65), CARD_ALT, GREEN_DONE)
    tb_b4 = s1.shapes.add_textbox(Inches(8.2), Inches(4.85), Inches(4.0), Inches(0.55))
    tb_b4.text_frame.paragraphs[0].text = "✅ Resolved by Staff. Resident notified automatically."
    tb_b4.text_frame.paragraphs[0].font.size = Pt(11)
    tb_b4.text_frame.paragraphs[0].font.bold = True
    tb_b4.text_frame.paragraphs[0].font.color.rgb = GREEN_DONE

    add_speaker_notes(
        s1,
        "Good morning everyone. Today we are presenting EstateKaki—an intelligent, zero-install Telegram assistant "
        "designed specifically for Singapore Town Councils. "
        "Residents don't want to download another bulky mobile app. They are already on Telegram. "
        "EstateKaki lets them type, send photos, or even leave voice memos in Singlish. "
        "The bot grounds every answer in official council by-laws, routes emergencies with zero delay, "
        "and automatically files tracked tickets for estate staff."
    )

    # =========================================================================
    # SLIDE 2: Problem Statement
    # =========================================================================
    s2 = prs.slides.add_slide(layout)
    set_bg(s2)
    add_header(s2, "Same questions daily, and reports that go missing", "The Municipal Reality", "02 / 08")

    problems = [
        ("Repeat Questions", YELLOW_ACCENT, [
            "Bulky item removal, renovation hours, corridor rules, BBQ pit deposits.",
            "Town Council staff answer the exact same 10 routine questions dozens of times every day.",
            "Staff time is tied up repeating basic rules rather than fixing estate issues."
        ]),
        ("Lost Reports & Scattered Channels", PEACH_ACCENT, [
            "Faults come in through scattered emails, phone hotlines, and manual counter visits.",
            "No automated tracking ticket is issued, making follow-ups painful for both residents and officers.",
            "Critical details (exact block number, photos) are often missing."
        ]),
        ("AI Guessing is Dangerous", MINT_ACCENT, [
            "A chatbot that makes up a fake fine, wrong booking fee, or inaccurate emergency advice is worse than no bot.",
            "In municipal governance, every answer must be 100% grounded in verified council by-laws.",
            "The system must know its limits and escalate to staff when unsure."
        ]),
    ]

    for idx, (title, accent, bullets) in enumerate(problems):
        left_pos = Inches(0.8 + idx * 4.0)
        add_card(s2, left_pos, Inches(1.6), Inches(3.75), Inches(4.4), CARD_BG)
        add_card(s2, left_pos + Inches(0.2), Inches(1.85), Inches(3.35), Inches(0.4), CARD_ALT)
        tb_pt = s2.shapes.add_textbox(left_pos + Inches(0.25), Inches(1.87), Inches(3.25), Inches(0.35))
        p_pt = tb_pt.text_frame.paragraphs[0]
        p_pt.text = title
        p_pt.font.bold = True
        p_pt.font.size = Pt(13)
        p_pt.font.color.rgb = accent

        tb_b = s2.shapes.add_textbox(left_pos + Inches(0.2), Inches(2.4), Inches(3.35), Inches(3.4))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        for i, text in enumerate(bullets):
            p = tf_b.paragraphs[0] if i == 0 else tf_b.add_paragraph()
            p.text = "• " + text
            p.font.size = Pt(12)
            p.font.color.rgb = MUTED

    add_card(s2, Inches(0.8), Inches(6.25), Inches(11.75), Inches(0.75), CARD_ALT, MINT_ACCENT)
    tb_s2_bot = s2.shapes.add_textbox(Inches(1.0), Inches(6.3), Inches(11.3), Inches(0.65))
    tb_s2_bot.text_frame.paragraphs[0].text = "🎯 Our Solution: A bot that answers strictly from verified council documents, never guesses, and handles life-safety with zero latency."
    tb_s2_bot.text_frame.paragraphs[0].font.size = Pt(13)
    tb_s2_bot.text_frame.paragraphs[0].font.bold = True
    tb_s2_bot.text_frame.paragraphs[0].font.color.rgb = WHITE

    add_speaker_notes(
        s2,
        "Why did we build EstateKaki? Because Town Councils face three chronic pain points: "
        "First, repetitive inquiries about renovation hours and bulky items eat up hours of staff time. "
        "Second, maintenance complaints arrive across phone calls and emails with missing block numbers and no tracking. "
        "And third, ordinary AI chatbots hallucinate—which is disastrous when dealing with municipal by-laws. "
        "So we built EstateKaki to answer only what the council officially wrote down."
    )

    # =========================================================================
    # SLIDE 3: System Flow (One message in, three ways out)
    # =========================================================================
    s3 = prs.slides.add_slide(layout)
    set_bg(s3)
    add_header(s3, "One message in, three ways out", "Triage & Routing Architecture", "03 / 08")

    # Left: Resident Intake
    add_card(s3, Inches(0.8), Inches(1.6), Inches(2.6), Inches(4.4), CARD_BG)
    tb_int = s3.shapes.add_textbox(Inches(0.95), Inches(1.8), Inches(2.3), Inches(3.9))
    tf_int = tb_int.text_frame
    tf_int.word_wrap = True
    p_i1 = tf_int.paragraphs[0]
    p_i1.text = "📱 Resident"
    p_i1.font.bold = True
    p_i1.font.size = Pt(16)
    p_i1.font.color.rgb = WHITE
    p_i2 = tf_int.add_paragraph()
    p_i2.text = (
        "\n• Plain chat on Telegram\n"
        "• Voice Memos (Whisper)\n"
        "• Defect Photos (Vision)\n"
        "• Natural Singlish\n"
        "• Zero installation"
    )
    p_i2.font.size = Pt(12)
    p_i2.font.color.rgb = MUTED

    # Center: Guard & Router
    add_card(s3, Inches(3.7), Inches(1.6), Inches(3.2), Inches(4.4), CARD_ALT, YELLOW_ACCENT)
    tb_grd = s3.shapes.add_textbox(Inches(3.85), Inches(1.8), Inches(2.9), Inches(3.9))
    tf_grd = tb_grd.text_frame
    tf_grd.word_wrap = True
    p_g1 = tf_grd.paragraphs[0]
    p_g1.text = "⚡ Guard + Router"
    p_g1.font.bold = True
    p_g1.font.size = Pt(16)
    p_g1.font.color.rgb = YELLOW_ACCENT
    p_g2 = tf_grd.add_paragraph()
    p_g2.text = (
        "\n1. Emergency Screen:\n"
        "Instant regex checks before any LLM call (<5ms).\n\n"
        "2. Multilingual Check:\n"
        "Catches English, Chinese, Malay & Tamil distress terms.\n\n"
        "3. Intent Classifier:\n"
        "Routes to Life-Safety vs By-Law RAG vs Fault Ticket."
    )
    p_g2.font.size = Pt(11)
    p_g2.font.color.rgb = WHITE

    # Right: 3 Outcomes
    branches = [
        ("🚨 Life-Safety Emergency", PEACH_ACCENT, "Bypasses all AI models instantly (<5ms). Replies immediately with 995 (SCDF), 999 (Police) & 1767. Zero waiting."),
        ("📖 Grounded By-Law Query", YELLOW_ACCENT, "Answers strictly from ingested council documents with exact clause citations. If not sure, it hands off to human staff."),
        ("🛠️ Tracked Fault Report", MINT_ACCENT, "Collects block location and defect photo. Opens a tracked ticket in SQLite and syncs directly to Trello with SLA countdowns."),
    ]
    top_pos = 1.6
    for title, color, desc in branches:
        add_card(s3, Inches(7.2), Inches(top_pos), Inches(5.3), Inches(1.35), CARD_BG, color)
        tb_br = s3.shapes.add_textbox(Inches(7.35), Inches(top_pos + 0.08), Inches(5.0), Inches(1.2))
        tf_br = tb_br.text_frame
        tf_br.word_wrap = True
        p_bt = tf_br.paragraphs[0]
        p_bt.text = title
        p_bt.font.bold = True
        p_bt.font.size = Pt(13)
        p_bt.font.color.rgb = color
        p_bd = tf_br.add_paragraph()
        p_bd.text = desc
        p_bd.font.size = Pt(11)
        p_bd.font.color.rgb = WHITE
        top_pos += 1.52

    # Bottom Callout
    add_card(s3, Inches(0.8), Inches(6.25), Inches(11.75), Inches(0.75), CARD_ALT)
    tb_s3_bot = s3.shapes.add_textbox(Inches(1.0), Inches(6.3), Inches(11.3), Inches(0.65))
    tb_s3_bot.text_frame.paragraphs[0].text = "🔄 Everything lands on the staff operations dashboard, and every status update syncs back directly to the resident on Telegram."
    tb_s3_bot.text_frame.paragraphs[0].font.size = Pt(12)
    tb_s3_bot.text_frame.paragraphs[0].font.bold = True
    tb_s3_bot.text_frame.paragraphs[0].font.color.rgb = MINT_ACCENT

    add_speaker_notes(
        s3,
        "Here is how EstateKaki operates: One message in, three ways out. "
        "A resident sends a message via Telegram. "
        "Before any AI model is even invoked, our deterministic emergency guard checks the message in less than 5 milliseconds. "
        "If it is a fire, gas leak, or trapped lift, it skips AI completely and gives emergency numbers. "
        "If it is a by-law question, our Semantic RAG answers with citations. "
        "If it is a maintenance issue, it collects location and photos and files a work order."
    )

    # =========================================================================
    # SLIDE 4: Real Scenarios (Three messages, three outcomes)
    # =========================================================================
    s4 = prs.slides.add_slide(layout)
    set_bg(s4)
    add_header(s4, "Three messages, three outcomes", "Real Resident Scenarios", "04 / 08")

    cols_s4 = [
        ("ASK (BY-LAWS)", YELLOW_ACCENT, [
            ("Resident Query:", "\"Can I put shoe racks along the corridor?\"", BLUE_BUBBLE),
            ("EstateKaki Reply:", "\"Yes, provided a clear escape passage of at least 1.2 metres is maintained.\n\nSource: Common Corridor Safety By-Laws (Clause 4.2).\"", CARD_ALT),
            ("Key Advantage:", "Grounded answer with exact by-law citation and resident feedback buttons. Zero guesswork.", None),
        ]),
        ("REPORT (FAULT TICKET)", MINT_ACCENT, [
            ("Resident Query:", "\"There's a sofa blocking the corridor staircase at Blk 802\"", BLUE_BUBBLE),
            ("EstateKaki Reply:", "\"Ticket #TC-204 opened under Waste & Conservancy. Photo verified. Dispatched to conservancy team (SLA: < 4h).\"", CARD_ALT),
            ("Key Advantage:", "Collects location and photo, tags severity, files SQLite ticket, and syncs to staff Trello board.", None),
        ]),
        ("EMERGENCY (SAFETY BYPASS)", PEACH_ACCENT, [
            ("Resident Query:", "\"I smell a gas leak in my block corridor!\"", BLUE_BUBBLE),
            ("EstateKaki Reply:", "\"🚨 DANGER: Evacuate immediately. Call SCDF at 995 and CityGas at 1800-752-1800. Do not operate electrical switches.\"", CARD_ALT),
            ("Key Advantage:", "Caught by regex pre-filter before any model call. Zero token cost, zero waiting, zero prompt injection risk.", None),
        ]),
    ]

    for idx, (head, accent, steps) in enumerate(cols_s4):
        left_pos = Inches(0.8 + idx * 4.0)
        add_card(s4, left_pos, Inches(1.6), Inches(3.75), Inches(4.4), CARD_BG)
        add_card(s4, left_pos + Inches(0.2), Inches(1.85), Inches(3.35), Inches(0.35), CARD_ALT)
        tb_ch = s4.shapes.add_textbox(left_pos + Inches(0.25), Inches(1.87), Inches(3.25), Inches(0.3))
        tb_ch.text_frame.paragraphs[0].text = head
        tb_ch.text_frame.paragraphs[0].font.bold = True
        tb_ch.text_frame.paragraphs[0].font.size = Pt(12)
        tb_ch.text_frame.paragraphs[0].font.color.rgb = accent

        top_inner = 2.35
        for lbl, val, box_color in steps:
            if box_color:
                add_card(s4, left_pos + Inches(0.2), Inches(top_inner), Inches(3.35), Inches(0.95), box_color)
                tb_box = s4.shapes.add_textbox(left_pos + Inches(0.25), Inches(top_inner + 0.05), Inches(3.25), Inches(0.85))
                tf_box = tb_box.text_frame
                tf_box.word_wrap = True
                p_l = tf_box.paragraphs[0]
                p_l.text = lbl
                p_l.font.size = Pt(9.5)
                p_l.font.bold = True
                p_l.font.color.rgb = YELLOW_ACCENT if box_color == BLUE_BUBBLE else MINT_ACCENT
                p_v = tf_box.add_paragraph()
                p_v.text = val
                p_v.font.size = Pt(10)
                p_v.font.color.rgb = WHITE
                top_inner += 1.05
            else:
                tb_adv = s4.shapes.add_textbox(left_pos + Inches(0.2), Inches(top_inner), Inches(3.35), Inches(0.85))
                tf_adv = tb_adv.text_frame
                tf_adv.word_wrap = True
                p_al = tf_adv.paragraphs[0]
                p_al.text = lbl
                p_al.font.bold = True
                p_al.font.size = Pt(10)
                p_al.font.color.rgb = WHITE
                p_av = tf_adv.add_paragraph()
                p_av.text = val
                p_av.font.size = Pt(10)
                p_av.font.color.rgb = MUTED

    add_card(s4, Inches(0.8), Inches(6.25), Inches(11.75), Inches(0.75), CARD_ALT)
    tb_s4_bot = s4.shapes.add_textbox(Inches(1.0), Inches(6.3), Inches(11.3), Inches(0.65))
    tb_s4_bot.text_frame.paragraphs[0].text = "💡 Ask it something random outside the rules, and it says: \"I am not sure based on council by-laws. Let me connect you with an estate officer.\""
    tb_s4_bot.text_frame.paragraphs[0].font.size = Pt(12)
    tb_s4_bot.text_frame.paragraphs[0].font.bold = True
    tb_s4_bot.text_frame.paragraphs[0].font.color.rgb = YELLOW_ACCENT

    add_speaker_notes(
        s4,
        "Here are three live examples that demonstrate the system in action: "
        "First, when someone asks about corridor shoe racks, it cites the exact 1.2-meter escape passage rule. "
        "Second, when a resident reports a discarded sofa, it collects a photo, confirms block details, and creates a work order. "
        "Third, when someone reports smelling gas, it triggers our emergency safety pre-filter instantly without waiting for an LLM."
    )

    # =========================================================================
    # SLIDE 5: Operations Console (Tickets move, residents get told)
    # =========================================================================
    s5 = prs.slides.add_slide(layout)
    set_bg(s5)
    add_header(s5, "Tickets move, residents get told", "Live Operations & Kanban Workflow", "05 / 08")

    kanban_cols = [
        ("OPEN", YELLOW_ACCENT, "3", [
            ("#3 Sofa blocking staircase", "Waste & Conservancy · High · Toa Payoh", "4h SLA"),
            ("#6 Dark staircase landing", "Lighting Services · Medium · Woodlands", "24h SLA"),
            ("#8 Rubbish chute jammed", "Sanitary Services · High · Queenstown", "4h SLA"),
        ]),
        ("IN PROGRESS", PEACH_ACCENT, "2", [
            ("#2 Pothole at carpark entrance", "Roads & Civil Works · High · Tampines", "Contractor On-Site"),
            ("#7 Dripping pipe in void deck", "Plumbing & Drainage · Med · Sengkang", "Dispatched (Hai Yong)"),
        ]),
        ("RESOLVED", GREEN_DONE, "2", [
            ("#1 Corridor light replaced", "Electrical · Blk 802 · Done in 45m", "King Wan Electrical"),
            ("#4 Fallen tree branch cleared", "Horticulture · Blk 104 · Cleared", "Town Team Verified"),
        ]),
    ]

    for idx, (col_name, accent, count, cards) in enumerate(kanban_cols):
        left_pos = Inches(0.8 + idx * 4.0)
        add_card(s5, left_pos, Inches(1.6), Inches(3.75), Inches(4.4), CARD_BG)

        # Header Badge
        add_card(s5, left_pos + Inches(0.2), Inches(1.85), Inches(3.35), Inches(0.4), CARD_ALT)
        tb_kh = s5.shapes.add_textbox(left_pos + Inches(0.3), Inches(1.87), Inches(3.15), Inches(0.35))
        p_kh = tb_kh.text_frame.paragraphs[0]
        p_kh.text = f"{col_name}   ({count})"
        p_kh.font.bold = True
        p_kh.font.size = Pt(13)
        p_kh.font.color.rgb = accent

        top_k = 2.45
        for card_title, card_sub, sla_info in cards:
            add_card(s5, left_pos + Inches(0.2), Inches(top_k), Inches(3.35), Inches(1.05), CARD_ALT)
            tb_kc = s5.shapes.add_textbox(left_pos + Inches(0.25), Inches(top_k + 0.05), Inches(3.25), Inches(0.95))
            tf_kc = tb_kc.text_frame
            tf_kc.word_wrap = True
            p_kt = tf_kc.paragraphs[0]
            p_kt.text = card_title
            p_kt.font.bold = True
            p_kt.font.size = Pt(11)
            p_kt.font.color.rgb = WHITE
            p_ks = tf_kc.add_paragraph()
            p_ks.text = card_sub
            p_ks.font.size = Pt(9.5)
            p_ks.font.color.rgb = MUTED
            p_sla = tf_kc.add_paragraph()
            p_sla.text = "⏱️ " + sla_info
            p_sla.font.size = Pt(9.5)
            p_sla.font.bold = True
            p_sla.font.color.rgb = accent
            top_k += 1.15

    add_card(s5, Inches(0.8), Inches(6.25), Inches(11.75), Inches(0.75), CARD_ALT, GREEN_DONE)
    tb_s5_bot = s5.shapes.add_textbox(Inches(1.0), Inches(6.3), Inches(11.3), Inches(0.65))
    tb_s5_bot.text_frame.paragraphs[0].text = "🔔 Two-Way Resident Feedback Loop: When staff click 'Resolve' on the dashboard, the resident instantly receives a Telegram notification with the resolution notes."
    tb_s5_bot.text_frame.paragraphs[0].font.size = Pt(12)
    tb_s5_bot.text_frame.paragraphs[0].font.bold = True
    tb_s5_bot.text_frame.paragraphs[0].font.color.rgb = WHITE

    add_speaker_notes(
        s5,
        "Slide 5 shows the estate officer's operational view. "
        "Notice our live Kanban board: tickets move seamlessly from Open to In Progress to Resolved. "
        "Each ticket is tagged with a priority SLA and matched to our term contractors. "
        "Crucially, this is a closed loop: when an estate officer clicks 'Resolve' on the dashboard, "
        "the resident immediately gets a notification on Telegram letting them know the issue was fixed."
    )

    # =========================================================================
    # SLIDE 6: Lossless Ingestion & Semantic RAG (MarkItDown & Table Preservation)
    # =========================================================================
    s6 = prs.slides.add_slide(layout)
    set_bg(s6)
    add_header(s6, "Lossless Ingestion Pipeline & Semantic RAG", "Microsoft MarkItDown & Cross-Page Table Preservation", "06 / 08")

    rag_cards = [
        ("1. MarkItDown PDF Ingestion", YELLOW_ACCENT, [
            "Converts PDF council handbooks into clean Markdown using Microsoft's MarkItDown library.",
            "Strips raw PDF visual bloat, fonts, and headers, cutting LLM input tokens by >80%.",
            "Ensures clean markdown structure (#, ##) for fast, deterministic vector indexing."
        ]),
        ("2. Cross-Page Table Healing", PEACH_ACCENT, [
            "Detects sentences and tables split across physical page breaks and auto-heals them.",
            "100% Table Atomicity Shield: regex protects tables (|---|) from being cut down the middle.",
            "13 out of 13 tariff and fee tables preserved as indivisible units with zero row/column loss."
        ]),
        ("3. Two-Stage Semantic Chunking", MINT_ACCENT, [
            "Stage 1: Splits strictly by `#`, `##`, `###` markdown header hierarchy.",
            "Stage 2: Breaks long sections only at natural sentence meaning shifts (cosine distance).",
            "Context Breadcrumbs: Stamps every chunk with [Town Council > By-Laws > Facility]."
        ]),
    ]

    for idx, (title, accent, bullets) in enumerate(rag_cards):
        left_pos = Inches(0.8 + idx * 4.0)
        add_card(s6, left_pos, Inches(1.6), Inches(3.75), Inches(4.4), CARD_BG)
        add_card(s6, left_pos + Inches(0.2), Inches(1.85), Inches(3.35), Inches(0.4), CARD_ALT)
        tb_eh = s6.shapes.add_textbox(left_pos + Inches(0.25), Inches(1.87), Inches(3.25), Inches(0.35))
        p_eh = tb_eh.text_frame.paragraphs[0]
        p_eh.text = title
        p_eh.font.bold = True
        p_eh.font.size = Pt(12)
        p_eh.font.color.rgb = accent

        tb_eb = s6.shapes.add_textbox(left_pos + Inches(0.2), Inches(2.4), Inches(3.35), Inches(3.4))
        tf_eb = tb_eb.text_frame
        tf_eb.word_wrap = True
        for i, text in enumerate(bullets):
            p = tf_eb.paragraphs[0] if i == 0 else tf_eb.add_paragraph()
            p.text = "• " + text
            p.font.size = Pt(11.5)
            p.font.color.rgb = MUTED

    add_card(s6, Inches(0.8), Inches(6.25), Inches(11.75), Inches(0.75), CARD_ALT, MINT_ACCENT)
    tb_s6_bot = s6.shapes.add_textbox(Inches(1.0), Inches(6.3), Inches(11.3), Inches(0.65))
    tb_s6_bot.text_frame.paragraphs[0].text = "🎯 Benchmark Audit Across 145 Chunks: 100% RAG Hit Rate @ 3, 0.9222 MRR, 100% table preservation, and 0 hallucinated phone numbers."
    tb_s6_bot.text_frame.paragraphs[0].font.size = Pt(12)
    tb_s6_bot.text_frame.paragraphs[0].font.bold = True
    tb_s6_bot.text_frame.paragraphs[0].font.color.rgb = WHITE

    add_speaker_notes(
        s6,
        "Slide 6 covers our ingestion and Semantic RAG pipeline. "
        "Standard RAG fails on council documents because tables get sliced in half and PDF formatting wastes tokens. "
        "We built a three-step solution: "
        "First, we ingest PDFs with Microsoft MarkItDown, stripping visual bloat and cutting token costs by over 80%. "
        "Second, we heal sentences and tables split across page transitions, guaranteeing 100% table atomicity. "
        "Third, our Two-Stage Chunker splits by headers and semantic meaning shifts, tagging each chunk with full breadcrumb context. "
        "In our benchmark of 145 chunks, we achieved a 100% Hit Rate @ 3 and preserved all 13 fee tables intact."
    )

    # =========================================================================
    # SLIDE 7: Human-in-the-Loop Living Policy Copilot
    # =========================================================================
    s7 = prs.slides.add_slide(layout)
    set_bg(s7)
    add_header(s7, "Human-in-the-Loop Policy & By-Law Copilot", "Surgical Living Document Maintenance & Visual Diffs", "07 / 08")

    # Left: Officer Flow & Surgical Reconciliation
    add_card(s7, Inches(0.8), Inches(1.6), Inches(5.7), Inches(4.5), CARD_BG)
    add_card(s7, Inches(1.0), Inches(1.85), Inches(5.3), Inches(0.4), CARD_ALT)
    tb_c1_h = s7.shapes.add_textbox(Inches(1.1), Inches(1.87), Inches(5.1), Inches(0.35))
    tb_c1_h.text_frame.paragraphs[0].text = "NATURAL LANGUAGE BY-LAW AMENDMENT"
    tb_c1_h.text_frame.paragraphs[0].font.bold = True
    tb_c1_h.text_frame.paragraphs[0].font.size = Pt(12)
    tb_c1_h.text_frame.paragraphs[0].font.color.rgb = YELLOW_ACCENT

    # Officer Prompt Box
    add_card(s7, Inches(1.0), Inches(2.4), Inches(5.3), Inches(0.95), CARD_ALT)
    tb_pr = s7.shapes.add_textbox(Inches(1.1), Inches(2.43), Inches(5.1), Inches(0.9))
    tf_pr = tb_pr.text_frame
    tf_pr.word_wrap = True
    p_pr1 = tf_pr.paragraphs[0]
    p_pr1.text = "💬 Officer Natural Language Prompt:"
    p_pr1.font.bold = True
    p_pr1.font.size = Pt(10)
    p_pr1.font.color.rgb = YELLOW_ACCENT
    p_pr2 = tf_pr.add_paragraph()
    p_pr2.text = "\"When booking a barbecue pit, Resident shall deposit from $150 to $300\""
    p_pr2.font.italic = True
    p_pr2.font.size = Pt(10.5)
    p_pr2.font.color.rgb = WHITE

    # 3 Bullet highlights
    tb_c1 = s7.shapes.add_textbox(Inches(1.0), Inches(3.45), Inches(5.3), Inches(2.5))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True
    c1_bullets = [
        ("🎯 AST Clause Targeting: ", "Navigates directly to Recreational Facilities > Barbecue Area (Clause 5), filtering out static application forms."),
        ("✂️ Surgical Line Reconciliation: ", "Eliminates phantom LLM diffs! Snaps untouched lines back character-for-character."),
        ("💰 >90% Output Token Reduction: ", "Replaces only the target phrase instead of rewriting the entire 60-line section."),
    ]
    for i, (head, text) in enumerate(c1_bullets):
        p = tf_c1.paragraphs[0] if i == 0 else tf_c1.add_paragraph()
        r1 = p.add_run()
        r1.text = head
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = WHITE
        r2 = p.add_run()
        r2.text = text
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = MUTED

    # Right: GitHub-Style Diff & Governance
    add_card(s7, Inches(6.8), Inches(1.6), Inches(5.75), Inches(4.5), CARD_BG)
    add_card(s7, Inches(7.0), Inches(1.85), Inches(5.35), Inches(0.4), CARD_ALT)
    tb_c2_h = s7.shapes.add_textbox(Inches(7.1), Inches(1.87), Inches(5.15), Inches(0.35))
    tb_c2_h.text_frame.paragraphs[0].text = "GOVERNANCE, AUDIT TRAIL & INSTANT ROLLBACK"
    tb_c2_h.text_frame.paragraphs[0].font.bold = True
    tb_c2_h.text_frame.paragraphs[0].font.size = Pt(12)
    tb_c2_h.text_frame.paragraphs[0].font.color.rgb = PEACH_ACCENT

    # Visual Diff Box
    add_card(s7, Inches(7.0), Inches(2.4), Inches(5.35), Inches(1.25), CARD_ALT)
    tb_df = s7.shapes.add_textbox(Inches(7.1), Inches(2.45), Inches(5.15), Inches(1.15))
    tf_df = tb_df.text_frame
    tf_df.word_wrap = True
    p_df1 = tf_df.paragraphs[0]
    p_df1.text = "🔍 GitHub-Style Visual Diff Preview:"
    p_df1.font.bold = True
    p_df1.font.size = Pt(10.5)
    p_df1.font.color.rgb = WHITE

    p_del = tf_df.add_paragraph()
    p_del.text = "- 5. When booking BBQ pit, deposit sum of $150.00 per pit..."
    p_del.font.size = Pt(10)
    p_del.font.color.rgb = PEACH_ACCENT

    p_add = tf_df.add_paragraph()
    p_add.text = "+ 5. When booking BBQ pit, deposit sum of $300.00 per pit..."
    p_add.font.size = Pt(10)
    p_add.font.color.rgb = MINT_ACCENT

    p_df2 = tf_df.add_paragraph()
    p_df2.text = "✨ Surgical Output: Exactly +1 Addition, -1 Deletion (0 Spurious Micro-Diffs)"
    p_df2.font.size = Pt(9.5)
    p_df2.font.color.rgb = MUTED

    # Governance Bullets
    tb_gov = s7.shapes.add_textbox(Inches(7.0), Inches(3.8), Inches(5.35), Inches(2.1))
    tf_gov = tb_gov.text_frame
    tf_gov.word_wrap = True
    gov_points = [
        ("• Automated Backups: ", "Timestamped snapshot taken before any handbook write."),
        ("• Immutable Audit Log: ", "JSON log stores officer intent, raw prompt, and exact diff."),
        ("• One-Click Rollback: ", "Instantly restores original rules if an amendment is rescinded."),
        ("• Hot Vector Re-Indexing: ", "RAG updates immediately with zero server downtime."),
    ]
    for i, (head, text) in enumerate(gov_points):
        p = tf_gov.paragraphs[0] if i == 0 else tf_gov.add_paragraph()
        r1 = p.add_run()
        r1.text = head
        r1.font.bold = True
        r1.font.size = Pt(10.5)
        r1.font.color.rgb = WHITE
        r2 = p.add_run()
        r2.text = text
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = MUTED

    # Bottom Callout
    add_card(s7, Inches(0.8), Inches(6.25), Inches(11.75), Inches(0.75), CARD_ALT, MINT_ACCENT)
    tb_s7_bot = s7.shapes.add_textbox(Inches(1.0), Inches(6.3), Inches(11.3), Inches(0.65))
    tb_s7_bot.text_frame.paragraphs[0].text = "🧑‍💼 Full Human Oversight: AI acts strictly as an assistant drafter; Town Council estate officers review visual diffs and approve before changes go live."
    tb_s7_bot.text_frame.paragraphs[0].font.size = Pt(12)
    tb_s7_bot.text_frame.paragraphs[0].font.bold = True
    tb_s7_bot.text_frame.paragraphs[0].font.color.rgb = WHITE

    add_speaker_notes(
        s7,
        "Slide 7 presents our Human-in-the-Loop Living Policy Copilot. "
        "By-laws aren't static; councils frequently update booking fees or deposit rules. "
        "Instead of manually editing messy text files, estate officers type a plain English instruction: "
        "'When booking a barbecue pit, Resident shall deposit from $150 to $300'. "
        "Our AST engine locates the exact clause, performs surgical phrase replacement, and shows a color-coded GitHub diff. "
        "Officers review and approve the change with 1 click, backed by automated backups, immutable audit logging, and instant rollback."
    )

    # =========================================================================
    # SLIDE 8: Built Today, and What's Next (The Truth!)
    # =========================================================================
    s8 = prs.slides.add_slide(layout)
    set_bg(s8)
    add_header(s8, "Built today, and what's next", "Achievements & Future Roadmap", "08 / 08")

    # Metrics Column (Left)
    metrics_s8 = [
        ("9", "Council Handbooks", "Ingested & semantically chunked"),
        ("10", "Municipal Trades", "Auto-matched to term contractors"),
        ("100%", "Table Preservation", "13/13 tariff & fee tables intact"),
        ("305", "Automated Tests", "Passing with zero test failures"),
    ]
    top_m = 1.6
    for val, lbl, sub in metrics_s8:
        add_card(s8, Inches(0.8), Inches(top_m), Inches(3.6), Inches(1.0), CARD_BG)
        tb_m = s8.shapes.add_textbox(Inches(0.95), Inches(top_m + 0.05), Inches(3.3), Inches(0.9))
        tf_m = tb_m.text_frame
        tf_m.word_wrap = True
        p_m = tf_m.paragraphs[0]
        r_val = p_m.add_run()
        r_val.text = f"{val}  "
        r_val.font.bold = True
        r_val.font.size = Pt(20)
        r_val.font.color.rgb = YELLOW_ACCENT
        r_lbl = p_m.add_run()
        r_lbl.text = f"—  {lbl}\n"
        r_lbl.font.bold = True
        r_lbl.font.size = Pt(11)
        r_lbl.font.color.rgb = WHITE
        r_sub = p_m.add_run()
        r_sub.text = sub
        r_sub.font.size = Pt(10)
        r_sub.font.color.rgb = MUTED
        top_m += 1.12

    # Center: Built Today (Claiming his real achievements!)
    add_card(s8, Inches(4.7), Inches(1.6), Inches(4.2), Inches(4.4), CARD_BG, MINT_ACCENT)
    tb_bt = s8.shapes.add_textbox(Inches(4.9), Inches(1.8), Inches(3.8), Inches(4.0))
    tf_bt = tb_bt.text_frame
    tf_bt.word_wrap = True
    p_bt_t = tf_bt.paragraphs[0]
    p_bt_t.text = "✅ Built Today (In Production)"
    p_bt_t.font.bold = True
    p_bt_t.font.size = Pt(15)
    p_bt_t.font.color.rgb = MINT_ACCENT

    built_items = [
        "Multimodal Voice Memos (Whisper Audio Transcription)",
        "Multilingual Emergency Screen (EN, ZH, MS, TA)",
        "Automated PDF-to-Markdown Ingestion & Healing",
        "Deterministic Safety Bypass (<5ms zero latency)",
        "Computer Vision Defect Severity Assessment",
        "Trello Kanban Integration with Live SLA Badges",
        "Two-Way Resident Telegram Notification Loop",
    ]
    for b_item in built_items:
        p = tf_bt.add_paragraph()
        p.text = "• " + b_item
        p.font.size = Pt(11)
        p.font.color.rgb = WHITE

    # Right: Real Next Steps (Future Roadmap)
    add_card(s8, Inches(9.2), Inches(1.6), Inches(3.35), Inches(4.4), CARD_BG, PEACH_ACCENT)
    tb_nx = s8.shapes.add_textbox(Inches(9.4), Inches(1.8), Inches(2.95), Inches(4.0))
    tf_nx = tb_nx.text_frame
    tf_nx.word_wrap = True
    p_nx_t = tf_nx.paragraphs[0]
    p_nx_t.text = "🔮 Future Roadmap"
    p_nx_t.font.bold = True
    p_nx_t.font.size = Pt(15)
    p_nx_t.font.color.rgb = PEACH_ACCENT

    next_items = [
        "Municipal ERP & SAP Integration for auto-invoicing",
        "IoT Water Tank & Pump Telemetry auto-reporting",
        "WhatsApp Business API Multi-Channel Deployment",
        "Geospatial Heatmap Dashboard for estate clusters",
        "Singpass Resident Identity Verification",
    ]
    for n_item in next_items:
        p = tf_nx.add_paragraph()
        p.text = "• " + n_item
        p.font.size = Pt(11)
        p.font.color.rgb = MUTED

    # Bottom Callout / Conclusion
    add_card(s8, Inches(0.8), Inches(6.25), Inches(11.75), Inches(0.75), CARD_ALT)
    tb_s8_bot = s8.shapes.add_textbox(Inches(1.0), Inches(6.3), Inches(11.3), Inches(0.65))
    tb_s8_bot.text_frame.paragraphs[0].text = "🎉 Summary: EstateKaki transforms municipal service delivery—giving residents instant 24/7 answers while automating contractor work orders for estate staff. Thank you!"
    tb_s8_bot.text_frame.paragraphs[0].font.size = Pt(12)
    tb_s8_bot.text_frame.paragraphs[0].font.bold = True
    tb_s8_bot.text_frame.paragraphs[0].font.color.rgb = YELLOW_ACCENT

    add_speaker_notes(
        s8,
        "To conclude: EstateKaki is not just an idea—it is a working platform. "
        "We have already built voice memo transcription, multilingual emergency screening, automated PDF ingestion, "
        "and two-way Telegram status updates, backed by 305 passing tests. "
        "Our future roadmap targets enterprise ERP integration and IoT telemetry. "
        "Thank you very much, and we are now ready for your questions!"
    )

    prs.save(PPTX_PATH)
    print(f"Presentation successfully saved to: {PPTX_PATH}")
    return PPTX_PATH


if __name__ == "__main__":
    build_deck()
