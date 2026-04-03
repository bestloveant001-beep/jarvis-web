// [ MARK-V20 // AI-CORE: JS-WEB-STABLE ]
const API_KEY = "AIzaSyDNG91SpfOI2qeHBnhveV1zOUjxEbRoakQ"; 

async function askJarvis(userInput) {
    console.log("[AI_CORE] Initiating Neural Link via v1beta...");
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}`;
    
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: `You are JARVIS, a bilingual AI for Sir Somdet (Pilot Somdet). 
                        Personality (50% Sarcastic): Professional, British-style, smart-aleck but loyal. 
                        Response: Mix Thai and English. Be cool and concise. 
                        User Prompt: "${userInput}"`
                    }]
                }]
            })
        });

        const data = await response.json();
        if (data.candidates && data.candidates[0].content) {
            return data.candidates[0].content.parts[0].text;
        } 
        return data.error ? `Mainframe Error: ${data.error.message}` : "Systems unstable, Sir.";
    } catch (error) {
        return "Connection lost, Sir Somdet. สัญญาณขาดหายครับ";
    }
}
