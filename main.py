const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 8080;
const DB_FILE = 'chat_history.json';

app.use(bodyParser.json());
app.use(express.static('public'));

// --- 🤖 JARVIS LOGIC CORE (JavaScript Edition) ---
function jarvisLogic(input, device = {}) {
    const ui = input.toLowerCase();
    const batt = device.battery || "Unknown";
    const lat = device.lat || "0";
    const time = device.time || "Unknown";

    if (ui.includes("สวัสดี") || ui.includes("ตื่น")) {
        return `สวัสดีครับท่านสมเดช ระบบ JARVIS-JS ออนไลน์ 100% พลังงานอุปกรณ์อยู่ที่ ${batt} พร้อมปฏิบัติการครับ`;
    }
    if (ui.includes("สถานะ") || ui.includes("พลังงาน")) {
        return `รายงานสถานะ: พลังงานหลัก ${batt}, ระบบประมวลผล Node.js เสถียร, ขณะนี้เวลา ${time} ครับ`;
    }
    if (ui.includes("พิกัด") || ui.includes("ตำแหน่ง")) {
        return lat !== "0" ? `ล็อคพิกัดดาวเทียม: ละติจูด ${lat} พื้นที่โดยรอบปลอดภัยครับท่าน` : "เซนเซอร์ GPS ขัดข้อง กรุณาตรวจสอบการอนุญาตสิทธิ์ครับ";
    }
    return `รับทราบครับท่านสมเดช คำสั่ง '${input}' ได้รับการยืนยัน ผมกำลังประมวลผลผ่าน JS-Core ครับ`;
}

// --- 📁 HISTORY MANAGEMENT ---
function getHistory() {
    if (!fs.existsSync(DB_FILE)) return [];
    try { return JSON.parse(fs.readFileSync(DB_FILE, 'utf8')); }
    catch (e) { return []; }
}

function saveHistory(history) {
    fs.writeFileSync(DB_FILE, JSON.stringify(history, null, 2), 'utf8');
}

// --- 📡 API ROUTES ---
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

app.get('/api/history', (req, res) => {
    res.json(getHistory());
});

app.post('/api/ask', (req, res) => {
    const { message, device } = req.body;
    let history = getHistory();
    const reply = jarvisLogic(message, device);
    
    history.push({ u: message, j: reply });
    if (history.length > 15) history.shift();
    
    saveHistory(history);
    res.json({ reply });
});

app.listen(PORT, () => {
    console.log(`[JARVIS] Core active on port ${PORT}`);
});
        from flask import Flask, render_template_string, request, redirect, session
import os
import google.generativeai as genai

app = Flask(__name__)
app.secret_key = "ironman_secret" # สำหรับระบบ Login

# --- 🔐 SECURITY ---
USERS = {"ADMIN": "159753"}
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyD-mgndxGz8Ddfy83JWoDohZwGQ_wRzrt4")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- 🎨 HTML TEMPLATE (รวมหน้า Login & Dashboard) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>J.A.R.V.I.S. OS</title>
    <style>
        body { background: #00050a; color: cyan; font-family: sans-serif; text-align: center; padding: 20px; }
        .card { background: #0a192f; border: 1px solid #1e3a8a; padding: 20px; border_radius: 15px; margin-top: 20px; }
        input { width: 80%; padding: 10px; margin: 10px; background: #000; color: cyan; border: 1px solid cyan; }
        button { background: cyan; color: black; padding: 10px 20px; border: none; font-weight: bold; cursor: pointer; }
        .chat-box { height: 200px; overflow-y: scroll; text-align: left; background: #050a14; padding: 10px; border: 1px solid #1e3a8a; }
    </style>
</head>
<body>
    {% if not logged_in %}
        <h1>SECURE LOGIN</h1>
        <form method="POST" action="/login">
            <input type="text" name="user" placeholder="IDENTITY"><br>
            <input type="password" name="pass" placeholder="ACCESS CODE"><br>
            <button type="submit">AUTHENTICATE</button>
        </form>
    {% else %}
        <h1>J.A.R.V.I.S. ONLINE</h1>
        <div class="card">
            <h3>SYSTEM STATUS</h3>
            <p>CPU: 32% | NET: SECURE</p>
            <a href="/logout" style="color:red">LOGOUT</a>
        </div>
        <div class="card">
            <h3>AI CONSOLE</h3>
            <div class="chat-box" id="chat">
                {% for msg in chat_history %}
                    <p><b>{{ msg.role }}:</b> {{ msg.text }}</p>
                {% endfor %}
            </div>
            <form method="POST" action="/chat">
                <input type="text" name="msg" placeholder="Command...">
                <button type="submit">SEND</button>
            </form>
        </div>
    {% endif %}
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE, logged_in=session.get('user'), chat_history=session.get('chat', []))

@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('user')
    pw = request.form.get('pass')
    if user in USERS and USERS[user] == pw:
        session['user'] = user
        session['chat'] = []
    return redirect('/')

@app.route('/chat', methods=['POST'])
def chat():
    msg = request.form.get('msg')
    if msg and session.get('user'):
        resp = model.generate_content(msg)
        history = session.get('chat', [])
        history.append({"role": "SIR", "text": msg})
        history.append({"role": "JARVIS", "text": resp.text})
        session['chat'] = history
    return redirect('/')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
    
