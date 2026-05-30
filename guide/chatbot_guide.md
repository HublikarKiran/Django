# Chatbot App Guide

The chatbot app gives students a simple study assistant.

URL:

```text
/chatbot/
```

Enter a topic and submit. The app saves the question and creates a detailed learning answer locally, so it works without an external AI key.

API endpoint:

```text
/api/chat-messages/
```

POST JSON:

```json
{
  "question": "Explain operating system scheduling"
}
```
