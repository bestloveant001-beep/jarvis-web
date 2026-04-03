const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 8080;
const DB_FILE = 'chat_history.json';

app.use(bodyParser.json());

// --- 🤖 JARVIS LOGIC CORE ---
function jarvisLogic(input, device = {}) {
    const ui = input.toLowerCase();
    const batt = device.battery || "Unknown";
    const time = device.time || "Unknown";
    const lat = device.lat || "0";

    if (ui.includes("สวัสดี") || ui.includes("ตื่น") || ui.includes("พร้อม")) {
        return `สวัสดีครับท่านสมเดช ระบบ MARK-V20 ออนไลน์ 100% พลังงานเครื่องอยู่ที่ ${batt} พร้อมปฏิบัติการครับ`;
    }
    if (ui.includes("สถานะ") || ui.includes("พลังงาน") || ui.includes("แบต")) {
        return `รายงานสถานะ: พลังงานหลัก ${batt}, ระบบประมวลผลเสถียร, ขณะนี้เวลา ${time} ครับท่าน`;
    }
    if (ui.includes("พิกัด") || ui.includes("ตำแหน่ง")) {
        return lat !== "0" ? `ล็อคพิกัดดาวเทียม: ละติจูด ${lat} ตรวจสอบพื้นที่โดยรอบแล้ว... ปลอดภัยครับ` : "เซนเซอร์ GPS ขัดข้อง กรุณาอนุญาตสิทธิ์บนหน้าจอครับ";
    }
    if (ui.includes("ขอบคุณ") || ui.includes("ดีมาก")) {
        return "ด้วยความยินดีอย่างยิ่งครับท่านสมเดช ผมจะเฝ้าระวังความปลอดภัยให้ท่านเสมอ";
    }
    return `รับทราบครับท่านสมเดช คำสั่ง '${input}' ได้รับการยืนยัน ระบบกำลังประมวลผลข้อมูลครับ`;
}

// --- 📁 HISTORY ---
function getHistory() {
    if (!fs.existsSync(DB_FILE)) return [];
    try { return JSON.parse(fs.readFileSync(DB_FILE, 'utf8')); } catch (e) { return []; }
}
function saveHistory(h) { fs.writeFileSync(DB_FILE, JSON.stringify(h, null, 2), 'utf8'); }

// --- 📡 ROUTES ---
app.get('/', (req, res) => { res.sendFile(path.join(__dirname, 'index.html')); });
app.get('/api/history', (req, res) => { res.json(getHistory()); });
app.post('/api/ask', (req, res) => {
    const { message, device } = req.body;
    let history = getHistory();
    const reply = jarvisLogic(message, device);
    history.push({ u: message, j: reply });
    if (history.length > 15) history.shift();
    saveHistory(history);
    res.json({ reply });
});

app.listen(PORT, () => { console.log(`[JARVIS] Core active on port ${PORT}`); });
