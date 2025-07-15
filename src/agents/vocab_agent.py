from langchain_core.messages import AIMessage  # 导入 AI 消息类

from .session_history import get_session_history  # 导入用于处理会话历史的方法
from .agent_base import AgentBase  # 导入基础代理类
from utils.logger import LOG  # 导入日志记录模块

class VocabAgent(AgentBase):
    """
    词汇学习代理类，负责处理与用户的对话。
    继承自 AgentBase 基类。
    """
    def __init__(self, session_id=None):
        # 加载工业术语提示文件（新增）
        super().__init__(
            name="industrial_terms",
            prompt_file="prompts/industrial_terms_prompt.txt",  # 工业术语学习提示
            session_id=session_id
        )

    def restart_session(self, session_id=None):
        """
        重新启动会话，清除会话历史。

        参数:
            session_id (str, optional): 会话的唯一标识符。如果未提供，将使用当前会话 ID。

        返回:
            str: 返回清空后的会话历史，作为初始的 AI 消息。
        """
        # 如果没有传递 session_id，则使用实例中的 session_id
        if session_id is None:
            session_id = self.session_id

        # 获取该会话的历史记录对象
        history = get_session_history(session_id)
        # 清除该会话的历史记录
        history.clear()
        # 记录清除后的会话历史到日志中
        LOG.debug(f"[history][{session_id}]:{history}")

        # 返回清空后的会话历史记录
        return history


