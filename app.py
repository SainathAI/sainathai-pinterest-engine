import gradio as gr

def test():
    return {"ok": True}

with gr.Blocks() as demo:
    out = gr.JSON()
    gr.Button("Ping").click(lambda: test(), outputs=out)

demo.launch()
