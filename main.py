from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from Clients import azure_open_ai_client
from Clients.trace_client import get_tracer
from Clients.log_client import get_logger
from Clients.metric_client import get_meter

tracer = get_tracer()
logger = get_logger()
meter, request_counter, token_counter = get_meter()

app = FastAPI(title="Azure OpenAI FastAPI Demo")

# Templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def stream_chat_completion(prompt: str):
    client = azure_open_ai_client.client
    with tracer.start_as_current_span("stream_chat_completion"):
        logger.info(f"New request received: {prompt}")
        request_counter.add(1)

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            stream=True
        )

        for chunk in response:
            if chunk.choices:
                for choice in chunk.choices:
                    if choice.delta and choice.delta.content:
                        content = choice.delta.content
                        token_counter.add(1)
                        yield f"data: {content}\n\n"  # Server-Sent Event format


@app.get("/chat")
async def chat(prompt: str):
    logger.info(f"Chat request received: {prompt}")
    return StreamingResponse(stream_chat_completion(prompt), media_type="text/event-stream")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app,host="127.0.0.1",port=8000)