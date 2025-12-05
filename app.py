import gradio as gr

def test():
    return {"ok": True}

with gr.Blocks() as demo:
    out = gr.JSON()
    btn = gr.Button("Ping")
    # correct: pass function reference and outputs, don't call the function here
    btn.click(fn=test, inputs=None, outputs=out)

demo.launch()
