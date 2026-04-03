// [ MARK-V20 // AI-CORE: BILINGUAL STABLE ]
const API_KEY = "AIzaSyDNG91SpfOI2qeHBnhveV1zOUjxEbRoakQ"; 

async function askJarvis(userInput) {
    // กำหนด URL ทั้งแบบ v1 และ v1beta เพื่อความชัวร์
    const url = `https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=${API_KEY}`;
    
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: `You are JARVIS, a bilingual AI for Sir Somdet. 
                        Personality: Cool, professional, 50% sarcastic. 
                        Response: mix of Thai and English. 
                        User asks: "${userInput}"`
                    }]
                }]
            })
        });

        const data = await response.json();
        
        // ถ้า Google ส่ง Error กลับมา ให้ดึง Error นั้นมาโชว์บนหน้าจอเลยเพื่อจะได้รู้ว่าพังตรงไหน
        if (data.error) {
            console.error("AI_ERROR:", data.error.message);
            return `Sir Somdet, we have a problem: ${data.error.message} (รหัสผิดพลาดครับท่าน)`;
        }

        if (data.candidates && data.candidates[0].content) {
            return data.candidates[0].content.parts[0].text;
        } else {
            return "I'm receiving empty data, Sir. ระบบได้รับข้อมูลว่างเปล่าครับ";
        }
    } catch (error) {
        return `Connection failed: ${error.message}. การเชื่อมต่อล้มเหลวครับท่านสมเดช`;
    }
}

function jarvisSpeak(text) {
    window.speechSynthesis.cancel();
    const utter = new SpeechSynthesisUtterance(text);
    utter.lang = 'th-TH'; 
    utter.pitch = 0.85;
    utter.rate = 1.0;
    window.speechSynthesis.speak(utter);
}
