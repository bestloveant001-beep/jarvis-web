// [ MARK-V20 // AI-CORE: GEMINI-2.5-FLASH-WEB-STABLE ]
const API_KEY = "AIzaSyCKBgkwZTM7xasWwIsivVTQ24MclNPgvUM"; 

async function askJarvis(userInput) {
    // อัปเกรดเป็น Gemini 2.5 Flash เรียบร้อย
    const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${API_KEY}`;
    
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: `You are JARVIS, the ultra-advanced AI for Sir Somdet. Personality: 50% Sarcastic, high-tech British tone. Response: Mix Thai and English naturally. User Prompt: ${userInput}`
                    }]
                }]
            })
        });

        const data = await response.json();
        
        if (data.candidates && data.candidates[0].content) {
            return data.candidates[0].content.parts[0].text;
        } 
        
        if (data.error) {
            return `Sir, Mainframe Error: ${data.error.message}`;
        }

        return "Systems are slightly unstable, Sir Somdet.";
    } catch (error) {
        return "Connection lost, Sir. Check your network.";
    }
}
