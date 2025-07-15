# tabs/scenario_tab.py

import gradio as gr
from agents.scenario_agent import ScenarioAgent
from utils.logger import LOG

# 初始化场景代理（全局作用域，确保 start_new_scenario_chatbot 可访问）
agents = {
    "electrolysis_worker": ScenarioAgent("electrolysis_worker"),  # 电解铝事故模拟
    "equipment_maintenance": ScenarioAgent("equipment_maintenance"),  # 电解铝设备维护
}

def get_page_desc(scenario):
    try:
        with open(f"content/page/{scenario}.md", "r", encoding="utf-8") as file:
            scenario_intro = file.read().strip()
        return scenario_intro
    except FileNotFoundError:
        LOG.error(f"场景介绍文件 content/page/{scenario}.md 未找到！")
        return "场景介绍文件未找到。"
    
# 获取场景介绍并启动新会话的函数
def start_new_scenario_chatbot(scenario):
    # 直接访问全局 agents 字典
    initial_ai_message = agents[scenario].start_new_session()  # 启动新会话并获取初始AI消息

    return gr.Chatbot(
        value=[{"role": "assistant", "content": initial_ai_message}],
        height=600,
        type="messages"
    )

# 场景代理处理函数，根据选择的场景调用相应的代理
def handle_scenario(user_input, chat_history, scenario):
    bot_message = agents[scenario].chat_with_history(user_input)  # 获取场景代理的回复
    LOG.info(f"[ChatBot]: {bot_message}")  # 记录场景代理的回复
    return bot_message  # 返回场景代理的回复

def create_scenario_tab():
    with gr.Tab("场景"):  # 场景标签
        gr.Markdown("## 选择一个场景完成目标和挑战")  # 场景选择说明

        # 创建单选框组件
        # 初始化场景代理（仅保留电解铝相关场景）
        agents = {
            "electrolysis_worker": ScenarioAgent("electrolysis_worker"),  # 电解铝事故模拟
            "equipment_maintenance": ScenarioAgent("equipment_maintenance"),  # 电解铝设备维护
        }

        # 单选框选项明确行业属性
        scenario_radio = gr.Radio(
            choices=[
                ("电解铝事故模拟", "electrolysis_worker"),
                ("电解铝设备维护模拟", "equipment_maintenance"),
            ],
            label="场景"
        )

        # 聊天机器人占位符调整
        scenario_chatbot = gr.Chatbot(
            placeholder="<strong>电解铝培训助手 小智</strong><br><br>选择场景后开始模拟操作吧！",
            height=600,
            type="messages"
        )

        scenario_intro = gr.Markdown()  # 场景介绍文本组件


        # 更新场景介绍并在场景变化时启动新会话
        scenario_radio.change(
            fn=lambda s: (get_page_desc(s), start_new_scenario_chatbot(s)),  # 更新场景介绍和聊天机器人
            inputs=scenario_radio,  # 输入为选择的场景
            outputs=[scenario_intro, scenario_chatbot],  # 输出为场景介绍和聊天机器人组件
        )

        # 场景聊天界面
        gr.ChatInterface(
            fn=handle_scenario,  # 处理场景聊天的函数
            chatbot=scenario_chatbot,  # 聊天机器人组件
            additional_inputs=scenario_radio,  # 额外输入为场景选择
            #clear_btn="清除历史记录",  # 清除历史记录按钮文本
            submit_btn="发送",  # 发送按钮文本
        )

        # retry_btn=None,  # 不显示重试按钮
        # undo_btn=None,  # 不显示撤销按钮
        # clear_btn="清除历史记录",  # 清除历史记录按钮文本
        # submit_btn="发送",  # 发送按钮文本
    #)