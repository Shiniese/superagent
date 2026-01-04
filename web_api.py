from fastapi import FastAPI

app = FastAPI(
        # docs_url=None, 
        # redoc_url=None
    )


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/get_video_text_content")
def get_video_text_content(video_url: str) -> str:
    import os
    from util_pub_func import download_audio, audio_to_text

    try:
        audio_path = ""
        audio_path = download_audio(video_url)
        video_texts = audio_to_text(audio_path)

        return video_texts
    
    except Exception as e:
        return "Error getting video text content"
    
    finally:
        if audio_path:
            os.unlink(audio_path)  # 删除临时文件

