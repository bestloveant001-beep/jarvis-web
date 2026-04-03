// [ MARK-V20 // AI-CORE: BILINGUAL FINAL STABLE ]
const API_KEY = "AIzaSyDNG91SpfOI2qeHBnhveV1zOUjxEbRoakQ"; 

async function askJarvis(userInput) {
    console.log("[AI_CORE] Initiating Neural Link...");
    try {
        const response = await fetch(`https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key=${API_KEY}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: `You are JARVIS, a bilingual AI for Sir Somdet. 
                        Personality: 50% sarcastic, British-style, very smart. 
                        Response: mix Thai and English. 
                        Current user prompt: "${userInput}"`
                    }]
                }]
            })
        });

        const data = await response.json();
        
        // ถ้าเชื่อมต่อสำเร็จ จะต้องมีข้อมูล candidates
        if (data.candidates && data.candidates[0].content) {
            return data.candidates[0].content.parts[0].text;
        } 
        
        // ถ้า Google ส่ง Error กลับมา
        if (data.error) {
            return `Sir, the mainframe says: ${data.error.message}`;
        }

        return "Systems are slightly unstable, Sir Somdet. (No data returned)";
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
