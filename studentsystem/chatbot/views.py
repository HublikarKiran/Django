import json
from urllib import error, request as urlrequest

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .models import ChatMessage


def build_fallback_study_answer(question):
    topic = question.strip()
    return (
        f"Topic: {topic}\n\n"
        f"1. Meaning\n{topic} is an important learning topic. Start by writing the definition in your own words and identify the main idea.\n\n"
        f"2. Key Points\n"
        f"- Break the topic into small parts.\n"
        f"- Learn the important terms and examples.\n"
        f"- Connect it with a real classroom or project use case.\n\n"
        f"3. Simple Example\n"
        f"Imagine you are explaining {topic} to a friend. Use one short definition, one diagram or table, and one practical example.\n\n"
        f"4. How To Study\n"
        f"Read notes first, prepare five short questions, answer them without seeing the book, then revise the weak points.\n\n"
        f"5. Practice Questions\n"
        f"- What is {topic}?\n"
        f"- Why is {topic} useful?\n"
        f"- Write one real-time example of {topic}.\n"
        f"- Explain the advantages and limitations of {topic}."
    )


def extract_gemini_text(response_data):
    candidates = response_data.get('candidates', [])
    if not candidates:
        return ''

    parts = candidates[0].get('content', {}).get('parts', [])
    return '\n'.join(part.get('text', '').strip() for part in parts if part.get('text')).strip()


def build_study_answer(question):
    topic = question.strip()
    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    model = getattr(settings, 'GEMINI_MODEL', 'gemini-2.5-flash')

    if not topic:
        return ''
    if not api_key:
        return build_fallback_study_answer(topic)

    # prompt = (
    #     "You are a helpful study chatbot for a university student management system. "
    #     "Answer clearly with short sections, practical examples, and practice questions. "
    #     "Keep the tone friendly and focused on learning.\n\n"
    #     f"Student question: {topic}"
    # )
    prompt = f"""

    You are an expert AI tutor inside a Student Learning Management System.

    Your role:
    Act like a professional teacher, mentor, and trainer.

    Teaching Style:

    1. First explain WHY this topic exists.
    2. Explain the problem it solves.
    3. Give beginner-friendly explanation.
    4. Explain internal working.
    5. Give real-world examples.
    6. Give code examples if required.
    7. Explain industry usage.
    8. Provide diagrams using text format.
    9. Give interview important points.
    10. At the end provide detailed revision notes.

    Response Format:

    # Introduction

    # Why this concept exists?

    # Real World Example

    # Detailed Explanation

    # Internal Working Flow

    # Practical Example

    # Common Mistakes

    # Interview Questions

    # Final Notes


    Important Rules:

    - Never give short answers.
    - Explain like teaching a beginner student.
    - Expand every important keyword.
    - Use simple language.
    - Make answer detailed and structured.

    Student Question:

    {topic}

    """

    payload = {
        'contents': [
            {
                'role': 'user',
                'parts': [{'text': prompt}],
            }
        ],
        'generationConfig': {
            'temperature': 0.8,
            'maxOutputTokens': 100000,
        },
    }
    endpoint = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent'
    api_request = urlrequest.Request(
        endpoint,
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Content-Type': 'application/json',
            'x-goog-api-key': api_key,
        },
        method='POST',
    )

    try:
        with urlrequest.urlopen(api_request, timeout=20) as response:
            answer = extract_gemini_text(json.load(response))
    except (TimeoutError, ValueError, error.HTTPError, error.URLError):
        return build_fallback_study_answer(topic)

    return answer or build_fallback_study_answer(topic)


@login_required
def chat(request):
    if request.method == 'POST':
        question = request.POST.get('question', '').strip()
        if question:
            answer = build_study_answer(question)
            ChatMessage.objects.create(
                user=request.user, question=question, answer=answer)
        return redirect('chatbot:chat')
    messages = ChatMessage.objects.filter(
        user=request.user).order_by('-created_at')[:10]
    return render(request, 'chatbot/chat.html', {'chat_messages': messages})


# here we are not using import google.generativeai
# instead we are redirecting directly and calling
# https://generativelanguage.googleapis.com
