import gradio as gr
from tabs.scenario_tab import create_scenario_tab
from tabs.vocab_tab import create_vocab_tab  # 保留场景和词汇标签
from utils.logger import LOG

def main():
    with gr.Blocks(title="LanguageMentor 电解铝培训助手") as language_mentor_app:
        create_scenario_tab()  # 场景标签保留
        create_vocab_tab()     # 词汇标签保留
        # 移除原对话标签的调用：create_conversation_tab()

    # 启动应用
    language_mentor_app.launch(share=True, server_name="0.0.0.0")

if __name__ == "__main__":
    main()
