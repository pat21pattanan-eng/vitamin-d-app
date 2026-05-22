import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json

def save_lead_to_google_sheets(name, contact, score, risk_level):
    try:
        scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        secret_info = json.loads(st.secrets["gcp_service_account_json"])
        credentials = Credentials.from_service_account_info(secret_info, scopes=scopes)
        client = gspread.authorize(credentials)
        sheet = client.open("Vitamin_D_Leads").sheet1
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row_to_append = [current_time, name, contact, score, risk_level]
        sheet.insert_row(row_to_append, 2, value_input_option="USER_ENTERED")
        return True
    except Exception as e:
        if "200" in str(e):
            return True
        st.error(f"❌ ระบบเชื่อมต่อ Google Sheets ขัดข้อง: {e}")
        return False


st.set_page_config(page_title="ประเมินภาวะขาดวิตามินดี", page_icon="☀️", layout="centered")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Sarabun', sans-serif;
    }

    /* ซ่อน default streamlit header */
    #MainMenu, footer, header { visibility: hidden; }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 680px;
    }

    /* Hero Banner */
    .hero-banner {
        background: linear-gradient(135deg, #D46B00 0%, #F0970A 45%, #D97706 100%);
        border-radius: 20px;
        padding: 3rem 2.5rem;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 32px rgba(180, 100, 0, 0.4);
    }
    .hero-banner h1 {
        color: white;
        font-size: 2.7rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 0 2px 12px rgba(0,0,0,0.35);
        line-height: 1.45;
        letter-spacing: -0.01em;
    }
    .hero-banner .hero-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        display: block;
        filter: drop-shadow(0 3px 6px rgba(0,0,0,0.2));
    }
    .hero-subtitle {
        color: rgba(255,255,255,0.95);
        font-size: 1rem;
        margin-top: 0.9rem;
        line-height: 1.7;
        text-shadow: 0 1px 6px rgba(0,0,0,0.25);
    }

    /* Stat pills */
    .stat-pill {
        display: inline-block;
        background: rgba(255,255,255,0.25);
        border: 1px solid rgba(255,255,255,0.4);
        border-radius: 20px;
        padding: 0.3rem 0.9rem;
        font-size: 0.85rem;
        color: white;
        font-weight: 600;
        margin-top: 0.75rem;
    }

    /* Disclaimer card */
    .disclaimer-card {
        background: #FFF8E7;
        border-left: 4px solid #FFB300;
        border-radius: 10px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 1.5rem;
        font-size: 0.82rem;
        color: #7B5B00;
        line-height: 1.6;
    }

    /* Section card */
    .section-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem 1.75rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 2px 16px rgba(0,0,0,0.06);
        border: 1px solid #F0F0F0;
    }
    .section-title {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        font-size: 1.15rem;
        font-weight: 700;
        color: #B45309;
        background: linear-gradient(90deg, #FFF7ED, #FFFBF0);
        border-left: 4px solid #F97316;
        border-radius: 0 10px 10px 0;
        margin-bottom: 1.1rem;
        padding: 0.65rem 1rem;
    }
    .section-icon {
        font-size: 1.2rem;
        flex-shrink: 0;
    }

    /* Result Cards */
    .result-high {
        background: linear-gradient(135deg, #FFF0F0, #FFE8E8);
        border: 2px solid #FF4444;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .result-mid {
        background: linear-gradient(135deg, #FFFBF0, #FFF3D0);
        border: 2px solid #FFB300;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .result-low {
        background: linear-gradient(135deg, #F0FFF4, #E8FFE8);
        border: 2px solid #22C55E;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .result-badge {
        display: inline-block;
        padding: 0.3rem 1rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
    }
    .badge-high { background: #FF4444; color: white; }
    .badge-mid  { background: #FFB300; color: white; }
    .badge-low  { background: #22C55E; color: white; }

    .result-title {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .result-high .result-title { color: #C00000; }
    .result-mid .result-title  { color: #7B5B00; }
    .result-low .result-title  { color: #15803D; }

    /* Score bar */
    .score-bar-wrap {
        background: #EEEEEE;
        border-radius: 999px;
        height: 10px;
        margin: 0.75rem 0;
        overflow: hidden;
    }
    .score-bar-fill-high { background: linear-gradient(90deg, #FF8C00, #FF4444); border-radius: 999px; height: 10px; }
    .score-bar-fill-mid  { background: linear-gradient(90deg, #FFD700, #FFB300); border-radius: 999px; height: 10px; }
    .score-bar-fill-low  { background: linear-gradient(90deg, #86EFAC, #22C55E); border-radius: 999px; height: 10px; }

    /* Product recommendation box */
    .product-box {
        background: white;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-top: 0.75rem;
        display: flex;
        gap: 0.75rem;
        align-items: flex-start;
    }
    .product-icon { font-size: 1.6rem; flex-shrink: 0; margin-top: 0.1rem; }
    .product-text { font-size: 0.88rem; line-height: 1.65; color: #333; }
    .product-text strong { color: #1A1A1A; }

    /* Submit button override */
    .stButton > button[kind="primaryFormSubmit"],
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #FF8C00, #FFD700) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        width: 100% !important;
        box-shadow: 0 4px 16px rgba(255,140,0,0.35) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button[kind="primaryFormSubmit"]:hover,
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(255,140,0,0.45) !important;
    }

    /* Question label */
    .question-label {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        font-size: 1.05rem;
        font-weight: 700;
        color: #C2410C;
        background: linear-gradient(90deg, #FFF4ED, #FFFAF7);
        border-radius: 8px;
        padding: 0.45rem 0.75rem;
        margin-bottom: 0.5rem;
        margin-top: 0.75rem;
    }
    .question-label .q-icon { font-size: 1.25rem; }
    .question-label .q-num {
        font-size: 0.78rem;
        font-weight: 700;
        background: #F97316;
        color: white;
        border-radius: 50%;
        width: 1.5rem;
        height: 1.5rem;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }

    /* Radio & checkbox tweaks */
    .stRadio > div { gap: 0.4rem; }
    .stRadio label, .stCheckbox label {
        font-size: 0.93rem !important;
    }

    /* Input fields */
    .stTextInput > div > div > input {
        border-radius: 10px !important;
        border: 1.5px solid #E0E0E0 !important;
        padding: 0.6rem 0.9rem !important;
        font-size: 0.93rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #FFB300 !important;
        box-shadow: 0 0 0 3px rgba(255,179,0,0.15) !important;
    }

    /* Divider */
    hr { border-color: #F5F5F5 !important; margin: 1rem 0 !important; }

    /* Success / info messages */
    .stSuccess, .stInfo { border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)


# ── Hero Banner ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <span class="hero-icon">☀️</span>
    <h1>เช็คลิสต์ประเมินความเสี่ยง<br>ภาวะขาดวิตามินดี</h1>
    <p class="hero-subtitle">คนไทยกว่า <strong>45%</strong> มีภาวะขาดวิตามินดีโดยไม่รู้ตัว<br>ทำแบบประเมินนี้เพื่อรู้ระดับความเสี่ยงของคุณ</p>
    <span class="stat-pill">⏱ ใช้เวลาเพียง 2 นาที</span>
</div>
""", unsafe_allow_html=True)

# ── Disclaimer ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="disclaimer-card">
    ⚠️ <strong>หมายเหตุ:</strong> แบบประเมินนี้เป็นเพียงการคัดกรองเบื้องต้น ไม่ใช่การวินิจฉัยโรค
    ควรปรึกษาเภสัชกรหรือแพทย์ก่อนใช้ผลิตภัณฑ์ โดยเฉพาะผู้มีโรคประจำตัว ใช้ยาเป็นประจำ ตั้งครรภ์ หรือให้นมบุตร
</div>
""", unsafe_allow_html=True)


# ── Form ──────────────────────────────────────────────────────────────────────

# ส่วนที่ 0: ข้อมูลส่วนตัว
st.markdown("""
<div class="section-title">
    <span class="section-icon">👤</span> ข้อมูลเบื้องต้น
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    name = st.text_input("ชื่อ-นามสกุล / ชื่อเล่น *", placeholder="กรอกชื่อของคุณ")
with col2:
    phone = st.text_input("เบอร์โทร / LINE ID", placeholder="(ไม่บังคับ)")

st.markdown("<hr>", unsafe_allow_html=True)

# ส่วนที่ 1: พฤติกรรมและปัจจัยเสี่ยง
st.markdown("""
<div class="section-title">
    <span class="section-icon">🌿</span> ส่วนที่ 1 — พฤติกรรมและปัจจัยเสี่ยง
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="question-label"><span class="q-num">1</span><span class="q-icon">☀️</span>พฤติกรรมการโดนแสงแดดของคุณเป็นอย่างไร?</div>', unsafe_allow_html=True)
q1 = st.radio(
    "q1", ["ทำกิจกรรมกลางแจ้งเป็นประจำ", "ทำงานออฟฟิศ หรืออยู่ในร่มตลอดวัน"],
    horizontal=False, label_visibility="collapsed"
)

st.markdown('<div class="question-label"><span class="q-num">2</span><span class="q-icon">🧴</span>การใช้ครีมกันแดดหรือการปกป้องผิวของคุณ?</div>', unsafe_allow_html=True)
q2 = st.radio(
    "q2", ["ไม่ค่อยทาครีมกันแดด", "ทาครีมกันแดดเป็นประจำทุกวัน หรือใส่เสื้อแขนยาวเสมอ"],
    label_visibility="collapsed"
)

st.markdown('<div class="question-label"><span class="q-num">3</span><span class="q-icon">🎂</span>อายุของคุณ?</div>', unsafe_allow_html=True)
q3 = st.radio(
    "q3", ["อายุน้อยกว่า 50 ปี", "อายุ 50 ปีขึ้นไป"],
    horizontal=True, label_visibility="collapsed"
)

st.markdown('<div class="question-label"><span class="q-num">4</span><span class="q-icon">🪞</span>โทนสีผิวของคุณ?</div>', unsafe_allow_html=True)
q4 = st.radio(
    "q4", ["ผิวขาว หรือ ขาวเหลือง", "ผิวคล้ำ หรือ สีผิวเข้ม"],
    horizontal=True, label_visibility="collapsed"
)

st.markdown('<div class="question-label"><span class="q-num">5</span><span class="q-icon">⚖️</span>น้ำหนักตัวของคุณอยู่ในเกณฑ์ใด?</div>', unsafe_allow_html=True)
q5 = st.radio(
    "q5", ["น้ำหนักปกติ (BMI 18.5–22.9)", "น้ำหนักเกิน / อ้วน (BMI 23 ขึ้นไป)"],
    horizontal=False, label_visibility="collapsed",
    help="วิตามินดีละลายได้ในไขมัน ร่างกายที่มีไขมันสะสมมากจะ 'กักเก็บ' วิตามินดีไว้ในเนื้อเยื่อ ทำให้ระดับในเลือดต่ำลง"
)

st.markdown("<hr>", unsafe_allow_html=True)

# ส่วนที่ 2: สัญญาณเตือน
st.markdown("""
<div class="section-title">
    <span class="section-icon">🩺</span> ส่วนที่ 2 — สัญญาณเตือนจากร่างกาย
</div>
<p style="font-size:0.88rem;color:#666;margin-bottom:0.75rem;">✔ เลือกทุกอาการที่ตรงกับคุณในช่วง 1–3 เดือนที่ผ่านมา</p>
""", unsafe_allow_html=True)

any_symptom = any(st.session_state.get(k, False) for k in ['s1', 's2', 's3', 's4', 's5'])
s6_checked  = st.session_state.get('s6', False)

col_a, col_b = st.columns(2)
with col_a:
    s1 = st.checkbox("😴  อ่อนเพลียเรื้อรัง",            key='s1', disabled=s6_checked)
    s2 = st.checkbox("💪  ปวดเมื่อย / กล้ามเนื้ออ่อนแรง", key='s2', disabled=s6_checked)
    s3 = st.checkbox("🤧  ป่วยบ่อย / ภูมิต้านทานต่ำ",     key='s3', disabled=s6_checked)
with col_b:
    s4 = st.checkbox("😔  อารมณ์แปรปรวน / หดหู่",         key='s4', disabled=s6_checked)
    s5 = st.checkbox("💇  ผมร่วงผิดปกติ",                  key='s5', disabled=s6_checked)

st.markdown("<hr>", unsafe_allow_html=True)
s6 = st.checkbox("✅  ปัจจุบันยังไม่พบอาการผิดปกติใดๆ ข้างต้นเลย", key='s6', disabled=any_symptom)

st.markdown("<br>", unsafe_allow_html=True)
submitted = st.button("📊  ดูผลประเมินของฉัน", type="primary", use_container_width=True)


# ── Result ────────────────────────────────────────────────────────────────────
if submitted:
    if not name:
        st.warning("⚠️ รบกวนกรอกชื่อของคุณด้วยนะครับ")
    elif s6 and (s1 or s2 or s3 or s4 or s5):
        st.warning("⚠️ คุณเลือกทั้ง 'ไม่พบอาการ' และเลือกอาการอื่นพร้อมกัน รบกวนตรวจสอบอีกครั้งนะครับ")
    else:
        score = 0
        if q1 == "ทำงานออฟฟิศ หรืออยู่ในร่มตลอดวัน": score += 2
        if q2 == "ทาครีมกันแดดเป็นประจำทุกวัน หรือใส่เสื้อแขนยาวเสมอ": score += 1
        if q3 == "อายุ 50 ปีขึ้นไป": score += 1
        if q4 == "ผิวคล้ำ หรือ สีผิวเข้ม": score += 1
        if q5 == "น้ำหนักเกิน / อ้วน (BMI 23 ขึ้นไป)": score += 1
        if s1: score += 1
        if s2: score += 1
        if s3: score += 1
        if s4: score += 1
        if s5: score += 1

        max_score = 10
        bar_pct = int(score / max_score * 100)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown(f"### 🎯 ผลประเมินของคุณ: **{name}**")

        if score >= 5:
            risk_level = "ความเสี่ยงสูง (Nat D 5000 IU)"
            st.markdown(f"""
            <div class="result-high">
                <span class="result-badge badge-high">🔴 ความเสี่ยงสูง</span>
                <div class="result-title">ร่างกายมีแนวโน้มเข้าสู่ "ภาวะขาดวิตามินดี"</div>
                <div style="font-size:0.82rem;color:#888;margin-bottom:0.25rem;">คะแนน {score} / {max_score}</div>
                <div class="score-bar-wrap">
                    <div class="score-bar-fill-high" style="width:{bar_pct}%"></div>
                </div>
                <div class="product-box">
                    <span class="product-icon">💊</span>
                    <div class="product-text">
                        <strong>แนะนำ Nat D 5000 IU (สูตรฟื้นฟูเร่งด่วน)</strong><br>
                        เสริมวิตามินดี 3 <strong>Nat D 5000 IU</strong> วันละ 1 เม็ด ต่อเนื่อง 8–12 สัปดาห์
                        เพื่อดึงระดับวิตามินดีให้ฟื้นตัวได้ไวที่สุดครับ
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        elif score >= 2:
            risk_level = "ความเสี่ยงปานกลาง (Nat D 1000 IU / 5000 IU)"
            st.markdown(f"""
            <div class="result-mid">
                <span class="result-badge badge-mid">🟡 ความเสี่ยงปานกลาง</span>
                <div class="result-title">ร่างกายอาจมีภาวะ "พร่องวิตามินดี" ซ่อนอยู่</div>
                <div style="font-size:0.82rem;color:#888;margin-bottom:0.25rem;">คะแนน {score} / {max_score}</div>
                <div class="score-bar-wrap">
                    <div class="score-bar-fill-mid" style="width:{bar_pct}%"></div>
                </div>
                <div class="product-box">
                    <span class="product-icon">💊</span>
                    <div class="product-text">
                        <strong>แนะนำ Nat D 1000 IU (สูตรป้องกัน)</strong><br>
                        เสริม <strong>Nat D 1000 IU</strong> ทุกวัน หรือ <strong>Nat D 5000 IU</strong> สัปดาห์ละ 1–2 เม็ด
                        ป้องกันอาการอ่อนเพลียและเสริมภูมิต้านทานครับ
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        else:
            risk_level = "ความเสี่ยงต่ำ"
            st.markdown(f"""
            <div class="result-low">
                <span class="result-badge badge-low">🟢 ความเสี่ยงต่ำ</span>
                <div class="result-title">สุขภาพและไลฟ์สไตล์ของคุณอยู่ในเกณฑ์ดี 🎉</div>
                <div style="font-size:0.82rem;color:#888;margin-bottom:0.25rem;">คะแนน {score} / {max_score}</div>
                <div class="score-bar-wrap">
                    <div class="score-bar-fill-low" style="width:{max(bar_pct,8)}%"></div>
                </div>
                <div class="product-box">
                    <span class="product-icon">💊</span>
                    <div class="product-text">
                        <strong>แนะนำ Nat D 1000 IU (สูตรบำรุงรักษา)</strong><br>
                        เสริม <strong>Nat D 1000 IU</strong> วันละ 1 เม็ด หรือวันเว้นวัน
                        เพื่อคงระดับวิตามินดีให้แข็งแรงในระยะยาวครับ
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with st.spinner("⏳ กำลังบันทึกข้อมูล..."):
            success = save_lead_to_google_sheets(name, phone, score, risk_level)
            if success:
                st.success("✅ บันทึกข้อมูลสำเร็จ! สามารถนำผลประเมินนี้ปรึกษาเภสัชกรที่ร้านยาได้เลยครับ")
