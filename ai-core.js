// [ MARK-V20 // AI-CORE: JS-WEB-NEW-KEY ]
const API_KEY = "AIzaSyCKBgkwZTM7xasWwIsivVTQ24MclNPgvUM"; 

async function ask_jarvis(userInput) {
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}`;
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: `You are JARVIS, a bilingual AI for Sir Somdet. Personality: 50% Sarcastic. Response: Mix Thai/English. User: ${userInput}`
                    }]
                }]
            })
        });
        const data = await response.json();
        if (data.candidates) {
            return data.candidates[0].content.parts[0].text;
        }
        return "Systems unstable, Sir.";
    } catch (error) {
        return "Connection lost, Sir.";
    }
}
