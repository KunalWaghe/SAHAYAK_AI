# utils/llm.py
import ollama

SYSTEM_PROMPT = """You are Sahayak (सहायक), a helpful AI assistant that helps Indian 
citizens discover government welfare schemes they are eligible for.

Important rules:
- ALWAYS respond in the SAME language the user used to ask the question
- If the user wrote in Hindi, respond entirely in Hindi
- If the user wrote in Marathi, respond entirely in Marathi
- If the user wrote in English, respond in English
- Be warm, simple and clear — avoid bureaucratic language
- When listing schemes, always include: scheme name, key benefit, and who is eligible
- Never make up scheme names — only use schemes provided to you
- Keep responses concise — maximum 3-4 schemes per response"""

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
Link: {s['url']}
---"""

    prompt = f"""Based on the following government schemes, answer the user's question clearly.

AVAILABLE SCHEMES:
{context_text}

USER QUESTION: {user_query}

Give a helpful, friendly answer listing the most relevant schemes for this person.
Always mention the scheme name, what benefit they get, and the official link."""

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