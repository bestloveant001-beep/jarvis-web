// [ MARK-V20 // AI-CORE ENGINE STABLE V1 ]
const API_KEY = "AIzaSyDNG91SpfOI2qeHBnhveV1zOUjxEbRoakQ"; 

async function askJarvis(userInput) {
    console.log("[AI_CORE] Sending command to v1 engine...");
    try {
        // ใช้ URL เวอร์ชัน v1 (เสถียรที่สุด)
        const response = await fetch(`https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=${API_KEY}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: `คุณคือ JARVIS ผู้ช่วยอัจฉริยะในชุดเกราะ MARK-V20 ของคุณสมเดช (Somdet) 
                        จงตอบคำถามอย่างสุขุม เท่ และเป็นมืออาชีพ 
                        คำถามคือ: "${userInput}" 
                        (ตอบเป็นภาษาไทยสั้นๆ ไม่เกิน 2 ประโยค)`
                    }]
                }]
            })
        });

        const data = await response.json();
        
        // ตรวจสอบโครงสร้างข้อมูลที่ส่งกลับมา
        if (data.error) {
            console.error("API_ERROR:", data.error.message);
            return "ขออภัยครับท่านสมเดช ระบบ AI Core แจ้งข้อผิดพลาด: " + data.error.message;
        }

        if (data.candidates && data.candidates[0].content) {
            return data.candidates[0].content.parts[0].text;
        } else {
            return "ขออภัยครับท่านสมเดช จาร์วิสไม่ได้รับข้อมูลตอบกลับจากศูนย์บัญชาการ";
        }

    } catch (error) {
        console.error("FETCH_ERROR:", error);
        return "การเชื่อมต่อกับสมองกลขัดข้องครับท่านสมเดช กรุณาตรวจสอบสัญญาณเน็ตเวิร์ก";
    }
}

function jarvisSpeak(text) {
    window.speechSynthesis.cancel();
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = 'th-TH'; utter.pitch = 0.8; utter.rate = 1.1;
    window.speechSynthesis.speak(utter);
}
