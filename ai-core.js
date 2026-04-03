// [ MARK-V20 // AI-CORE: BILINGUAL STABLE FINAL ]
const API_KEY = "AIzaSyDNG91SpfOI2qeHBnhveV1zOUjxEbRoakQ"; 

async function askJarvis(userInput) {
    console.log("[AI_CORE] Initiating Neural Link via v1beta...");
    try {
        // เปลี่ยนกลับมาใช้ v1beta ซึ่งรองรับ gemini-1.5-flash แน่นอนในตอนนี้
        const response = await fetch(`https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: `You are JARVIS, a bilingual AI for Sir Somdet. 
                        Personality: 50% sarcastic, British-style, very smart. 
                        Response: mix Thai and English. 
                        User Prompt: "${userInput}"`
                    }]
                }]
            })
        });

        const data = await response.json();
        
        // ตรวจสอบข้อมูล
        if (data.candidates && data.candidates[0].content) {
            return data.candidates[0].content.parts[0].text;
        } 
        
        if (data.error) {
            console.error("DEBUG_ERROR:", data.error.message);
            return `Sir, the mainframe says: ${data.error.message}`;
        }

        return "Systems are slightly unstable, Sir Somdet.";
    } catch (error) {
        return "Connection lost, Sir. Please check your network.";
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
