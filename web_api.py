from fastapi import FastAPI

app = FastAPI(
        # docs_url=None, 
        # redoc_url=None
    )


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/get_video_text_content")
def get_video_text_content_(video_url: str) -> str:
    from skills import get_video_text_content

    return get_video_text_content(video_url)


