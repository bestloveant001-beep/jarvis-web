const API_KEY = "AIzaSyDNG91SpfOI2qeHBnhveV1zOUjxEbRoakQ"; 

async function askJarvis(userInput) {
    try {
        const response = await fetch(`https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=${API_KEY}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: `คุณคือ JARVIS AI ผู้ช่วยสุดกวนประสาทและขี้ประชดประชันของ 'คุณสมเดช' (Somdet) จงตอบคำถามสั้นๆ แบบแสบๆ: "${userInput}"`
                    }]
                }]
            })
        });

        const data = await response.json();
        
        // ถ้า Google ส่ง Error กลับมา ให้แสดง Error จริงๆ ออกมาดู
        if (data.error) {
            return "จาร์วิส Error: " + data.error.message; 
        }

        if (data.candidates && data.candidates[0].content) {
            return data.candidates[0].content.parts[0].text;
        } else {
            return "จาร์วิส: ผมได้รับข้อมูลที่ว่างเปล่าเหมือนสมองท่านเลยครับท่านสมเดช";
        }
    } catch (error) {
        return "จาร์วิส: เชื่อมต่อไม่ได้ สงสัยเน็ตท่านสมเดชจะโดนตัดนะครับ (" + error.message + ")";
    }
}
