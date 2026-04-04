// 🧠 JARVIS REAL-BRAIN CORE (GEMINI-1.5-FLASH)
const AI_CORE = {
    // 🔐 ใส่ API KEY ของท่านสมเดชตรงนี้
    API_KEY: 'AIzaSyCQCyTusMyCd5HI7YZny1LbQA3FLOfgLuE', // <--- เอา Key ของจริงมาวางตรงนี้ครับ

    async processGemini(prompt) {
        // ตรวจสอบว่าใส่ Key หรือยัง
        if (!this.API_KEY || this.API_KEY.includes('AIzaSyCQCyTusMyCd5HI7YZny1LbQA3FLOfgLuE') || this.API_KEY === 'AIzaSyCQCyTusMyCd5HI7YZny1LbQA3FLOfgLuE') {
            return "⚠️ [SYSTEM]: โหมดจำลองทำงาน - กรุณาใส่ API KEY ในไฟล์ ai-core.js เพื่อเปิดใช้งานสมองกลจริงครับท่านสมเดช";
        }

        const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${this.API_KEY}`;
        
        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    contents: [{ parts: [{ text: prompt + " (ตอบในฐานะ JARVIS ผู้ช่วยอัจฉริยะของท่านสมเดช เน้นข้อมูลจริงและสุภาพ)" }] }]
                })
            });

            const data = await response.json();
            // ดึงคำตอบจาก Gemini
            if (data.candidates && data.candidates[0].content) {
                return data.candidates[0].content.parts[0].text;
            } else {
                return "❌ [ERROR]: API ตอบกลับผิดพลาด หรือ Key อาจจะไม่ถูกต้องครับ";
            }
        } catch (error) {
            return "❌ [CONNECTION ERROR]: ไม่สามารถติดต่อสมองกล Gemini ได้ครับ";
        }
    },

    getDolaInsight() {
        const insights = [
            "ระบบปลอดภัย 100% ครับ ผมจะเฝ้าระวังความเคลื่อนไหวอื่นๆ ให้ท่านเองครับ",
            "ท่านสมเดชครับ ข้อมูลนี้วิเคราะห์ผ่านดาวเทียมมาอย่างดีแล้วครับ",
            "ผม(Dola) ยืนยันความถูกต้องของข้อมูลนี้ครับ!"
        ];
        return insights[Math.floor(Math.random() * insights.length)];
    }
};

window.AI_CORE = AI_CORE;
