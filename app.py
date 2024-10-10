import torch
import gradio as gr
from transformers import pipeline
from api import *

MODEL_NAME = "razhan/whisper-small-ckb"

device = 0 if torch.cuda.is_available() else "cpu"

pipe = pipeline(
    task="automatic-speech-recognition",
    model=MODEL_NAME,
    chunk_length_s=30,
    device=device,
)

pipe.model.config.forced_decoder_ids = pipe.tokenizer.get_decoder_prompt_ids(task="transcribe")


def transcribe(microphone, file_upload):
    warn_output = ""

    if microphone and file_upload:
        warn_output = (
            "WARNING: Microphone recording will be used, uploaded file will be discarded.\n"
        )
    elif not microphone and not file_upload:
        return "ERROR: You have to either use the microphone or upload an audio file"

    file = microphone if microphone else file_upload
    text = pipe(file)["text"]
    api_resp = send_to_claude(text)

    return warn_output + text + api_resp


demo = gr.Blocks()

mf_transcribe = gr.Interface(
    fn=transcribe,
    inputs=[
        gr.Audio(source="microphone", type="filepath", optional=True),
        gr.Audio(source="upload", type="filepath", optional=True),
    ],
    outputs="text",
    layout="horizontal",
    theme="huggingface",
    title="Whisper Central Kurdish‌ (Sorani) Demo: Transcribe Audio",
    description=(
        "Transcribe long-form microphone or audio inputs with the click of a button! Demo uses the fine-tuned"
        f" checkpoint [{MODEL_NAME}](https://huggingface.co/{MODEL_NAME}) and 🤗 Transformers to transcribe audio files"
        " of arbitrary length."
    ),
    allow_flagging="never",
)

with demo:
    gr.TabbedInterface([mf_transcribe], ["Transcribe Audio"])

demo.launch(share=True)
