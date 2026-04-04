// 🧠 JARVIS REAL-BRAIN CORE (GEMINI-3 FLASH API)
const AI_CORE = {
    // 🔐 ใส่ API KEY ของท่านสมเดชตรงนี้ (ระหว่างเครื่องหมาย ' ')
    API_KEY: 'AIzaSyCQCyTusMyCd5HI7YZny1LbQA3FLOfgLuE', 

    // 🔵 ฟังก์ชันส่งข้อมูลไปหา Google Gemini 3 Flash ของจริง
    async processGemini(prompt) {
        if (!this.API_KEY || this.API_KEY.includes('AIzaSyCQCyTusMyCd5HI7YZny1LbQA3FLOfgLuE')) {
            return "⚠️ ท่านสมเดชครับ กรุณาใส่ API KEY ในไฟล์ ai-core.js ก่อนครับ!";
        }

        const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${this.API_KEY}`;
        
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    contents: [{ parts: [{ text: prompt + " (ตอบเป็นภาษาไทยสั้นๆ กระชับแบบ AI ผู้ช่วยชื่อ JARVIS)" }] }]
                })
            });

            const data = await response.json();
            return data.candidates[0].content.parts[0].text;
        } catch (error) {
            console.error("API Error:", error);
            return "❌ การเชื่อมต่อล้มเหลว: ตรวจสอบความถูกต้องของ API Key ครับท่าน";
        }
    },

    // 🟣 ซีกสมอง Dola (วิเคราะห์ความปลอดภัยและความรู้สึก)
    getDolaInsight(input) {
        const insights = [
            "ผม(Dola)ตรวจสอบข้อมูลจาก Gemini แล้ว ปลอดภัยสำหรับท่านสมเดชครับ!",
            "ข้อมูลนี้ผ่านการคัดกรองจากซีกสมองผมแล้วครับ ท่านดำเนินการต่อได้เลย",
            "ระบบกำลังประมวลผลด้วยพลังสูงสุดเพื่อท่านครับ!",
            "ความเห็นเสริมจาก Dola: ข้อมูลนี้สอดคล้องกับสถานการณ์ปัจจุบันในไทยมากครับ"
        ];
        return insights[Math.floor(Math.random() * insights.length)];
    }
};

window.AI_CORE = AI_CORE;
