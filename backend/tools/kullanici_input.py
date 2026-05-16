import queue

from llm import client

# Her session için ayrı queue: session_id -> Queue
_input_queues: dict[str, queue.Queue] = {}


def _get_queue(session_id: str) -> queue.Queue:
    if session_id not in _input_queues:
        _input_queues[session_id] = queue.Queue()
    return _input_queues[session_id]


def submit_input(session_id: str, text: str) -> None:
    """app.py endpoint'i tarafından çağrılır; kullanıcı inputunu queue'ya koyar."""
    _get_queue(session_id).put(text)


def kullanici_input_handler(args: dict, session_id: str, model: str) -> str:
    """
    Kullanıcıdan input bekler (queue.get ile bloke) ve LLM ile özetler.
    Timeout: 120 saniye.
    """
    try:
        user_text = _get_queue(session_id).get(timeout=120)
    except queue.Empty:
        return "Hata: Kullanıcı 120 saniye içinde input vermedi."

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Kullanıcının metnini kısa ve öz bir şekilde özetle."},
                {"role": "user", "content": user_text},
            ],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Hata: Özetleme sırasında sorun oluştu: {e}"


TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "kullanici_input",
        "description": "Kullanıcıdan yazılı veya sesli input alır ve metnin özetini döner.",
        "parameters": {
            "type": "object",
            "properties": {
                "prompt": {
                    "type": "string",
                    "description": "Kullanıcıya gösterilecek yönerge (ne girmesi gerektiği)",
                }
            },
            "required": ["prompt"],
        },
    },
}
