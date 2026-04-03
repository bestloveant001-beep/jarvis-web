// [ MARK-V20 // AI-CORE ENGINE ]
const API_KEY = "AIzaSyDNG91SpfOI2qeHBnhveV1zOUjxEbRoakQ"; // ใส่ API Key ของท่านที่นี่

async function askJarvis(userInput) {
    console.log("[AI_CORE] Processing request...");
    try {
        // ใช้ Model ล่าสุด gemini-1.5-flash เพื่อความรวดเร็วบนมือถือ
        const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: `คุณคือ JARVIS AI ผู้ช่วยอัจฉริยะในชุดเกราะ MARK-V20 ของคุณสมเดช (Somdet) 
                        จงตอบคำถามอย่างสุขุม เท่ และเป็นมืออาชีพแบบในหนัง Iron Man 
                        คำถามคือ: "${userInput}" 
                        (ตอบเป็นภาษาไทยสั้นๆ ไม่เกิน 2 ประโยค)`
                    }]
                }]
            })
        });

        const data = await response.json();
        
        // ตรวจสอบว่ามี Error จาก Google หรือไม่
        if (data.error) {
            console.error("AI_ERROR:", data.error.message);
            return "ขออภัยครับท่านสมเดช ระบบ AI Core แจ้งข้อผิดพลาด: " + data.error.message;
        }

        return data.candidates[0].content.parts[0].text;
    } catch (error) {
        console.error("CONNECTION_ERROR:", error);
        return "ขออภัยครับท่านสมเดช การเชื่อมต่อกับสมองกลขัดข้อง กรุณาตรวจสอบสัญญาณเน็ตเวิร์กครับ";
    }
}

// ระบบเสียงสังเคราะห์
function jarvisSpeak(text) {
    window.speechSynthesis.cancel();
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = 'th-TH';
    utter.pitch = 0.8;
    utter.rate = 1.1;
    window.speechSynthesis.speak(utter);
}
