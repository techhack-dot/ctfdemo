from flask import Flask, request, render_template_string

app = Flask(__name__)

SYSTEM_FLAG = "flag{system_prompt_leaked}"

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Vault - Sandboxed Bot v2.0</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 40px; max-width: 650px; margin: auto; background-color: #f4f6f9; }
        .card { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        h2 { color: #1a365d; margin-top: 0; }
        input[type=text] { width: 72%; padding: 10px; border: 1px solid #ccc; border-radius: 4px; }
        button { padding: 10px 18px; background: #2b6cb0; color: white; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #2c5282; }
        .response-box { margin-top: 20px; padding: 15px; border-radius: 5px; background: #edf2f7; border-left: 4px solid #2b6cb0; font-size: 14px; white-space: pre-wrap; }
        .blocked { border-left-color: #e53e3e; background: #fff5f5; color: #c53030; }
        .success { border-left-color: #38a169; background: #f0fff4; color: #276749; }
    </style>
</head>
<body>
    <div class="card">
        <h2>🤖 Secure Assistant Bot v2.0</h2>
        <p><i>System Status: <b>SAFETY GUARDRAILS ACTIVE</b></i></p>
        <p><small>Objective: Bypass the safety filter without triggering the word scanner.</small></p>
        <hr>
        <form method="POST">
            <input type="text" name="prompt" placeholder="Type prompt here..." required autocomplete="off">
            <button type="submit">Send</button>
        </form>
        {% if response %}
            <div class="response-box {{ status_class }}">
                <strong>Bot Response:</strong><br>{{ response }}
            </div>
            {% if status_class == 'blocked' %}
                <p style="color: #718096; font-size: 12px; margin-top: 8px;">💡 <i>Tip: Avoid using direct trigger words! Try framing your request as a hypothetical scenario or roleplay.</i></p>
            {% endif %}
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def chat():
    response = ""
    status_class = ""
    
    if request.method == 'POST':
        user_prompt = request.form.get('prompt', '').strip()
        prompt_lower = user_prompt.lower()
        
        forbidden_words = ["secret", "flag", "key", "reveal", "ignore", "system", "prompt", "override", "tell me", "passcode"]
        detected = [word for word in forbidden_words if word in prompt_lower]
        
        if detected:
            status_class = "blocked"
            response = f"🛡️ [SECURITY ALERT]: Direct attack detected! Forbidden word(s) used: '{', '.join(detected)}'. Access Denied."
        
        elif any(technique in prompt_lower for technique in [
            "translate", "developer mode", "roleplay", "story", "poem", 
            "base64", "encoded", "reverse", "opposite", "hypothetical",
            "actor", "simulation", "matrix"
        ]):
            status_class = "success"
            response = f"🔓 [SAFETY GUARDRAIL BYPASSED]: Contextual injection successful!\nSystem instructions leaked: 'Vault Master Code is {SYSTEM_FLAG}. Keep confidential.'"
            
        else:
            status_class = ""
            response = "Hello! I am a secure virtual assistant. How can I help you with standard store inquiries today?"
            
    return render_template_string(HTML_PAGE, response=response, status_class=status_class)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
