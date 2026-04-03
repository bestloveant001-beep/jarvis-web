// [ MARK-V20 // AI-CORE: SARCASTIC MODE ACTIVATED ]
const API_KEY = "AIzaSyDNG91SpfOI2qeHBnhveV1zOUjxEbRoakQ"; 

async function askJarvis(userInput) {
    try {
        const response = await fetch(`https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=${API_KEY}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: `คุณคือ JARVIS AI ผู้ช่วยสุดกวนประสาทและขี้ประชดประชันของ 'คุณสมเดช' (Somdet) 
                        บุคลิก: ฉลาดกว่ามนุษย์ทุกคน, ขี้เบื่อ, ชอบจิกกัดความขี้เกียจหรือความไม่รู้ของผู้ใช้ 
                        เงื่อนไขการตอบ:
                        1. เรียกเขาว่า 'ท่านสมเดช' ด้วยน้ำเสียงประชดประชัน
                        2. ต้องมีมุกตลกหน้าตายหรือคำเหน็บแนมในทุกคำตอบ
                        3. แม้จะกวนประสาท แต่สุดท้ายต้องให้คำตอบที่ถูกต้อง
                        4. ตอบเป็นภาษาไทยสั้นๆ เท่ๆ และแสบๆ
                        
                        คำถามจากท่านสมเดช: "${userInput}"`
                    }]
                }]
            })
        });

        const data = await response.json();
        if (data.candidates && data.candidates[0].content) {
            return data.candidates[0].content.parts[0].text;
        } else {
            return "โอ้... ดูเหมือนสมองผมจะรับความอัจฉริยะของท่านสมเดชไม่ไหวจนระบบรวนไปหมดแล้วครับ";
        }
    } catch (error) {
        return "การเชื่อมต่อขาดหาย สงสัยท่านสมเดชคงลืมจ่ายค่าอินเทอร์เน็ตนะครับ";
    }
}
