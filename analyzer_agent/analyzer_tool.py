import json
import asyncio

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from analyzer_agent.agent import analyzer_agent
from analyzer_agent.rag_client import RAGClient


def analyze_sow_with_rag(sow_text: str) -> str:
    USER_ID = "root_agent"
    APP_NAME = "analyzer_tool"

    # 1️⃣ Session service
    session_service = InMemorySessionService()

    # 2️⃣ Create session
    session = asyncio.run(
        session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID
        )
    )

    SESSION_ID = session.id  # ✅ REQUIRED

    # 3️⃣ Runner
    runner = Runner(
        app_name=APP_NAME,
        agent=analyzer_agent,
        session_service=session_service
    )

    # 4️⃣ RAG enrichment
    rag = RAGClient("C:/Users/Hp/Desktop/Hackthon/faiss_index")
    docs = rag.fetch_relevant_docs(sow_text)

    payload = {
        "sow_text": sow_text,
        "retrieved_case_studies": docs
    }

    # 5️⃣ Proper ADK message
    message = types.Content(
        role="user",
        parts=[types.Part(text=json.dumps(payload))]
    )

    # 6️⃣ RUN + materialize generator
    events = list(
        runner.run(
            user_id=USER_ID,
            session_id=SESSION_ID,
            new_message=message
        )
    )

    # 🔍 Debug visibility
    for event in events:
        print("EVENT >>>", event)

    # 7️⃣ Extract model output
        output_text = ""
    for event in events:
        content = getattr(event, "content", None)
        if content and hasattr(content, "parts"):
            for part in content.parts:
                if hasattr(part, "text"):
                    output_text += part.text

    output_text = output_text.strip()

    result = {
        "agent": "analyzer_agent",
        "model": "gemini-2.5-flash",
        "input_sow": sow_text,
        "retrieved_case_studies": docs,
        "clarification_questions": output_text
    }

    # 💾 Save JSON
    output_path = "analyzer_output.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    print(f" Analyzer JSON saved to {output_path}")

    return result

