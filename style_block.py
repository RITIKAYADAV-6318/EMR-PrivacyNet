APP_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #061024 0%, #0a1f44 50%, #0d2a5c 100%);
}

.stApp, .stApp p, .stApp span, .stApp label, .stApp div {
    color: #eaf2fb;
}

header[data-testid="stHeader"] { display: none !important; }
div[data-testid="stToolbar"] { display: none !important; }
.custom-header, .custom-footer { z-index: 2147483647 !important; }

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #050d1f 0%, #0a1f44 100%);
}
section[data-testid="stSidebar"] * {
    color: #eaf2fb !important;
}
section[data-testid="stSidebar"] .streamlit-expanderHeader {
    background: rgba(255, 255, 255, 0.06);
    border-radius: 10px;
}

h1, h2, h3 {
    color: #ffffff;
    font-weight: 600;
}

.streamlit-expanderHeader {
    background: rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 14px;
    padding: 10px 16px;
    font-weight: 500;
    color: #ffffff;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.25);
}

.streamlit-expanderContent {
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border-radius: 0 0 14px 14px;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-top: none;
    padding: 18px;
}

.stButton > button {
    background: linear-gradient(135deg, #3b82c4 0%, #16447a 100%);
    color: #ffffff;
    border: none;
    border-radius: 10px;
    padding: 0.5em 1.3em;
    font-weight: 500;
    letter-spacing: 0.3px;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
    transition: all 0.2s ease;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
    background: linear-gradient(135deg, #4a94d8 0%, #1d529a 100%);
}

.stApp input {
    background: rgba(255, 255, 255, 0.08) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
}
.stApp input::placeholder {
    color: #b7c4d6 !important;
    opacity: 1;
}

[data-testid="stDataFrame"] {
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(10px);
    border-radius: 14px;
    padding: 6px;
}

.risk-badge-high {
    display: inline-block;
    background: rgba(220, 90, 90, 0.18);
    color: #ff9c9c;
    border: 1px solid rgba(220, 90, 90, 0.4);
    border-radius: 8px;
    padding: 3px 12px;
    font-weight: 600;
    font-size: 0.9em;
}
.risk-badge-low {
    display: inline-block;
    background: rgba(80, 200, 150, 0.15);
    color: #7fe3bb;
    border: 1px solid rgba(80, 200, 150, 0.4);
    border-radius: 8px;
    padding: 3px 12px;
    font-weight: 600;
    font-size: 0.9em;
}

.caution-note {
    color: #b7c4d6;
    font-size: 0.85em;
    font-style: italic;
}

.glass-card {
    background: rgba(255, 255, 255, 0.07);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 18px;
    padding: 26px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
    color: #eaf2fb;
}

.login-card {
    background: rgba(255, 255, 255, 0.06);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 14px;
    padding: 14px 20px 6px 20px;
    color: #eaf2fb;
}

.block-container {
    padding-top: 90px !important;
    padding-bottom: 80px !important;
}
</style>
"""

LOGIN_BG_HTML = """
<style>
.login-hero {
    position: relative;
    height: 320px;
    border-radius: 22px;
    overflow: hidden;
    background: linear-gradient(135deg, #050d1f 0%, #123a66 55%, #3b82c4 100%);
}
.login-hero svg { position: absolute; }
.floaty { animation: floaty 6s ease-in-out infinite; }
.floaty-slow { animation: floaty 9s ease-in-out infinite; }
.floaty-rev { animation: floaty-rev 7s ease-in-out infinite; }
@keyframes floaty { 0% { transform: translateY(0px) rotate(0deg); } 50% { transform: translateY(-18px) rotate(6deg); } 100% { transform: translateY(0px) rotate(0deg); } }
@keyframes floaty-rev { 0% { transform: translateY(0px) rotate(0deg); } 50% { transform: translateY(16px) rotate(-8deg); } 100% { transform: translateY(0px) rotate(0deg); } }
.pulse-line { stroke-dasharray: 500; stroke-dashoffset: 500; animation: drawline 3.5s ease-in-out infinite; }
@keyframes drawline { 0% { stroke-dashoffset: 500; } 50% { stroke-dashoffset: 0; } 100% { stroke-dashoffset: -500; } }
.login-title-overlay { position: relative; z-index: 2; text-align: center; padding-top: 55px; }
.login-title-overlay h1 { color: #ffffff; font-size: 2.3em; font-weight: 600; text-shadow: 0 2px 12px rgba(0,0,0,0.4); }
.login-title-overlay p { color: #cfe3f7; font-size: 1.05em; }
</style>
<div class="login-hero">
<svg width="100%" height="100%" viewBox="0 0 1200 320" preserveAspectRatio="xMidYMid slice">
<circle class="floaty-slow" cx="140" cy="70" r="46" fill="rgba(255,255,255,0.10)" />
<circle class="floaty" cx="1060" cy="60" r="30" fill="rgba(255,255,255,0.13)" />
<circle class="floaty-rev" cx="950" cy="220" r="55" fill="rgba(255,255,255,0.07)" />
<circle class="floaty" cx="220" cy="250" r="22" fill="rgba(255,255,255,0.12)" />
<g class="floaty" transform="translate(180,150)"><rect x="-6" y="-26" width="12" height="52" rx="4" fill="rgba(255,255,255,0.7)" /><rect x="-26" y="-6" width="52" height="12" rx="4" fill="rgba(255,255,255,0.7)" /></g>
<g class="floaty-rev" transform="translate(1000,150)"><rect x="-5" y="-22" width="10" height="44" rx="3" fill="rgba(255,255,255,0.6)" /><rect x="-22" y="-5" width="44" height="10" rx="3" fill="rgba(255,255,255,0.6)" /></g>
<g class="floaty-slow" transform="translate(650,55)"><rect x="-5" y="-20" width="10" height="40" rx="3" fill="rgba(255,255,255,0.5)" /><rect x="-20" y="-5" width="40" height="10" rx="3" fill="rgba(255,255,255,0.5)" /></g>
<path class="pulse-line" d="M0,270 L250,270 L280,210 L310,300 L340,240 L370,270 L1200,270" fill="none" stroke="rgba(255,255,255,0.5)" stroke-width="3" />
<circle class="floaty" cx="500" cy="180" r="4" fill="rgba(255,255,255,0.55)" />
<circle class="floaty-rev" cx="780" cy="100" r="5" fill="rgba(255,255,255,0.45)" />
<circle class="floaty-slow" cx="420" cy="85" r="3.5" fill="rgba(255,255,255,0.55)" />
</svg>
<div class="login-title-overlay"><h1>EMR-PrivacyNet</h1><p>Privacy-first electronic medical records, built for clinical decision support</p></div>
</div>
"""

HEADER_HTML = """<div class="custom-header" style="position:fixed;top:0;left:0;width:100%;z-index:2147483647;background:rgba(5,13,31,0.92);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-bottom:1px solid rgba(255,255,255,0.1);padding:14px 36px;display:flex;justify-content:space-between;align-items:center;"><div style="color:#ffffff;font-weight:600;font-size:1.15em;letter-spacing:0.3px;">EMR-PrivacyNet</div><div style="display:flex;gap:28px;"><a href="#about" style="color:#cfe3f7;text-decoration:none;font-weight:500;font-size:0.95em;">About</a><a href="#login-section" style="color:#cfe3f7;text-decoration:none;font-weight:500;font-size:0.95em;">Login</a><a href="#contact" style="color:#cfe3f7;text-decoration:none;font-weight:500;font-size:0.95em;">Contact</a></div></div>"""

FOOTER_HTML = """<div id="contact" class="custom-footer" style="position:fixed;bottom:0;left:0;width:100%;z-index:2147483647;background:rgba(5,13,31,0.95);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-top:1px solid rgba(255,255,255,0.1);padding:10px 36px;display:flex;justify-content:space-between;align-items:center;font-size:0.85em;color:#b7c4d6;"><div>EMR-PrivacyNet &nbsp;|&nbsp; Prototype built on synthetic data only</div><div>Contact: 3802719 &nbsp;|&nbsp; emr@gmail.com</div></div>"""

ABOUT_SECTION_HTML = """<div id="about" class="glass-card" style="margin-top:28px;"><h3 style="margin-top:0;">About EMR-PrivacyNet</h3><p>EMR-PrivacyNet is a prototype Electronic Medical Records system demonstrating how clinical workflows can be combined with privacy-preserving design and applied AI. It brings together role-based access control, patient data de-identification, full audit logging, and two AI-assisted features: a clinical note summarizer and an ML-based risk-flagging model.</p><p>Every record in this system is synthetic. No real patient information is used, stored, or displayed anywhere in this application. The project was built to explore healthcare informatics and clinical decision support in a privacy-conscious, responsibly scoped way.</p></div>"""