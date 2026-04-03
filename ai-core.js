// [ MARK-V20 // WEB-CORE: GEMINI-2.5-STABLE ]
const JARVIS_CONFIG = {
    apiKey: "วาง API Key ของท่านที่นี่",
    model: "gemini-2.5-flash",
    personality: "45% Sarcastic, British Tone, Bilingual (TH/EN)"
};

async function askJarvis(query) {
    const endpoint = `https://generativelanguage.googleapis.com/v1beta/models/${JARVIS_CONFIG.model}:generateContent?key=${JARVIS_CONFIG.apiKey}`;
    
    try {
        const response = await fetch(endpoint, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                contents: [{
                    parts: [{
                        text: `Role: JARVIS for Sir Somdet. Personality: ${JARVIS_CONFIG.personality}. Task: Respond to "${query}" and always provide web links for facts.`
                    }]
                }]
            })
        });

        const data = await response.json();
        return data.candidates[0].content.parts[0].text;
    } catch (err) {
        return "Sir, the mainframe is unresponsive. Check the power core (API Key).";
    }
}
    
