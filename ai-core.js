// [ MARK-V20 // AI-CORE: BILINGUAL-STABLE-V2 ]
const API_KEY = "AIzaSyDNG91SpfOI2qeHBnhveV1zOUjxEbRoakQ"; 

async function askJarvis(userInput) {
    console.log("[AI_CORE] Testing connection via v1beta...");
    // สังเกตตรงนี้ต้องเป็น v1beta เท่านั้น
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}`;
    
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: `You are JARVIS, a bilingual AI for Sir Somdet. 
                        Personality: 50% sarcastic, British-style. 
                        Response: Thai and English mix. 
                        User: "${userInput}"`
                    }]
                }]
            })
        });

        const data = await response.json();
        
        if (data.candidates && data.candidates[0].content) {
            return data.candidates[0].content.parts[0].text;
        } 
        
        if (data.error) {
            return `Mainframe Error: ${data.error.message}`;
        }

        return "Systems unstable, Sir.";
    } catch (error) {
        return "Connection lost, Sir.";
    }
}
