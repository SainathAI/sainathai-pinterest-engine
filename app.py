import gradio as gr

def test():
    return {"ok": True}

with gr.Blocks() as demo:
    out = gr.JSON()
    btn = gr.Button("Ping")
    btn.click(fn=test, inputs=None, outputs=out)

if __name__ == "__main__":
    demo.launch()
