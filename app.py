import gradio as gr

def health():
    return {"ok": True}

with gr.Blocks() as demo:
    gr.Markdown("# Engine Test")
    out = gr.JSON()
    btn = gr.Button("Check")
    btn.click(lambda: health(), outputs=[out])

demo.launch()
