// [ MARK-V20 // AI-CORE ENGINE REPAIRED ]
const API_KEY = "AIzaSyDNG91SpfOI2qeHBnhveV1zOUjxEbRoakQ"; 

async function askJarvis(userInput) {
    try {
        // แก้ไข URL เป็น gemini-pro เพื่อความเสถียรสูงสุดในเวอร์ชัน v1beta
        const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=${API_KEY}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: `คุณคือ JARVIS ผู้ช่วยในชุดเกราะ MARK-V20 ตอบท่านสมเดชอย่างเท่และสั้น: "${userInput}"`
                    }]
                }]
            })
        });

        const data = await response.json();
        
        if (data.error) {
            console.error("AI_CORE_ERROR:", data.error.message);
            return "ขออภัยครับท่านสมเดช ระบบแจ้งข้อผิดพลาด: " + data.error.message;
        }

        if (data.candidates && data.candidates[0].content) {
            return data.candidates[0].content.parts[0].text;
        } else {
            return "ขออภัยครับ จาร์วิสไม่สามารถประมวลผลคำตอบได้ในขณะนี้";
        }

    } catch (error) {
        return "การเชื่อมต่อกับสมองกลขัดข้องครับท่านสมเดช";
    }
}

function jarvisSpeak(text) {
    window.speechSynthesis.cancel();
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = 'th-TH'; utter.pitch = 0.8; utter.rate = 1.1;
    window.speechSynthesis.speak(utter);
}
