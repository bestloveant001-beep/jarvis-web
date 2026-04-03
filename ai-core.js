// [ MARK-V20 // AI-CORE: BILINGUAL MODE 50% ]
const API_KEY = "AIzaSyDNG91SpfOI2qeHBnhveV1zOUjxEbRoakQ"; 

async function askJarvis(userInput) {
    try {
        const response = await fetch(`https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=${API_KEY}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: `You are JARVIS, the highly sophisticated AI assistant for 'Sir Somdet' (Pilot Somdet). 
                        Personality (50% Sarcastic Mode): Professional, British-accented tone (in text), smart-aleck but loyal.
                        Instruction:
                        1. Address him as 'Sir Somdet' or 'ท่านสมเดช'.
                        2. Communicate in a mix of Thai and English (Bilingual). 
                        3. Be helpful but include a subtle, witty remark in every response.
                        4. Keep responses concise, cool, and high-tech.
                        
                        Current request from Sir Somdet: "${userInput}"`
                    }]
                }]
            })
        });

        const data = await response.json();
        if (data.candidates && data.candidates[0].content) {
            return data.candidates[0].content.parts[0].text;
        } else {
            return "Systems are slightly unstable, Sir Somdet. ขออภัยครับ ระบบสื่อสารขัดข้องเล็กน้อย";
        }
    } catch (error) {
        return "Connection lost, Sir. สงสัยพิกัดดาวเทียมจะหลุดนะครับท่านสมเดช";
    }
}

// อัปเดตเสียงให้รองรับสำเนียงที่ดูอินเตอร์ขึ้น (ถ้าเบราว์เซอร์รองรับ)
function jarvisSpeak(text) {
    window.speechSynthesis.cancel();
    const utter = new SpeechSynthesisUtterance(text);
    // ระบบจะพยายามเลือกเสียงที่เหมาะสม ถ้ามีภาษาอังกฤษผสมจะดูเท่มาก
    utter.lang = 'th-TH'; 
    utter.pitch = 0.85;
    utter.rate = 1.0;
    window.speechSynthesis.speak(utter);
}
