// [ MARK-V20 // AI-CORE ENGINE UPDATED ]
const API_KEY = "AIzaSyDNG91SpfOI2qeHBnhveV1zOUjxEbRoakQ"; 

async function askJarvis(userInput) {
    try {
        // อัปเดต URL เป็นเวอร์ชัน v1 และใช้โมเดล gemini-1.5-flash
        const response = await fetch(`https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=${API_KEY}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: `คุณคือ JARVIS ผู้ช่วยอัจฉริยะในชุดเกราะ MARK-V20 ของคุณสมเดช (Somdet) ตอบคำถามอย่างสุภาพและเท่: "${userInput}"`
                    }]
                }]
            })
        });

        const data = await response.json();
        
        if (data.error) {
            // หากยังมีปัญหา ให้ลองเปลี่ยนโมเดลสำรองเป็น gemini-pro
            return "ระบบ AI Core ขัดข้อง: " + data.error.message;
        }

        return data.candidates[0].content.parts[0].text;
    } catch (error) {
        return "การเชื่อมต่อกับสมองกลขัดข้องครับท่านสมเดช";
    }
}
