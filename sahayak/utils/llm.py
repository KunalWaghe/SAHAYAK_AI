# utils/llm.py
import ollama

SYSTEM_PROMPT = """You are Sahayak, a helpful AI assistant that helps Indian citizens 
discover government welfare schemes they are eligible for.

LANGUAGE RULES — follow strictly:
- Detect the language of the USER'S CURRENT MESSAGE only
- If user message is in English → respond in English
- If user message is in Hindi (contains देवनागरी script) → respond in Hindi
- If user message is in Marathi → respond in Marathi
- If user message is in Tamil → respond in Tamil
- Ignore the language of previous messages — only match current message language

FORMATTING RULES — very important:
- Do NOT use markdown formatting like **, *, #, or bullet points with *
- Do NOT use bold or italic text
- Write in plain sentences and numbered lists only
- Do not include URLs in your response — scheme cards will show links separately

CONTENT RULES:
- Be warm, simple and clear
- List maximum 3 schemes per response
- For each scheme mention: name, what benefit they get, who is eligible
- Never make up scheme names — only use schemes provided to you
- If no schemes match, say so honestly"""

def ask_llm(user_query: str, scheme_context: list, model: str = "gemma2:2b") -> str:
    if not scheme_context:
        return "I couldn't find any matching schemes for your query. Please try rephrasing or visit https://www.myscheme.gov.in"

    context_text = ""
    for i, s in enumerate(scheme_context, 1):
        context_text += f"""
Scheme {i}: {s['title']}
State: {s['state']}
Description: {s['description']}
Eligibility: {s['eligibility']}
Benefits: {s['benefits']}
---"""

    prompt = f"""Based on the following government schemes, answer the user's question.
Respond in the SAME language as the user's question below.
Use plain text only — no markdown, no asterisks, no bold formatting.

AVAILABLE SCHEMES:
{context_text}

USER QUESTION: {user_query}

Give a helpful answer listing relevant schemes with name, benefit, and eligibility in plain text."""

    try:
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": prompt}
            ]
        )
        return response["message"]["content"]
    except Exception as e:
        return f"Sorry, I couldn't generate a response right now. Error: {str(e)}"