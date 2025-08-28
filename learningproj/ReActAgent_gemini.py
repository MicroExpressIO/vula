
import os
import sys
import json
import re
import requests
from typing import Dict, List, Any, Optional
from dataclasses import dataclass

# load config
cur_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(cur_dir)
sys.path.append(par_dir)
from config.config import config

# load LLM
from google import genai
from google.genai import types


@dataclass
class ToolResult:
    """工具执行结果"""
    success: bool
    result: str
    error: Optional[str] = None


class Tool:
    """工具基类"""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def execute(self, **kwargs) -> ToolResult:
        raise NotImplementedError


class SearchTool(Tool):
    """搜索工具 - 使用 DuckDuckGo API"""
    def __init__(self):
        super().__init__(
            name="search",
            description="在互联网上搜索信息。输入：查询关键词"
        )
    
    def execute(self, query: str) -> ToolResult:
        try:
            # 这里使用一个简单的搜索API示例
            # 实际使用时可以替换为真实的搜索API
            url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                # 简化处理，实际应用中需要更复杂的解析
                abstract = data.get('Abstract', '')
                if abstract:
                    return ToolResult(success=True, result=abstract)
                else:
                    return ToolResult(success=True, result=f"搜索到关于 '{query}' 的信息，但没有找到摘要")
            else:
                return ToolResult(success=False, result="", error="搜索请求失败")
                
        except Exception as e:
            return ToolResult(success=False, result="", error=str(e))


class CalculatorTool(Tool):
    """计算器工具"""
    def __init__(self):
        super().__init__(
            name="calculator",
            description="执行数学计算。输入：数学表达式"
        )
    
    def execute(self, expression: str) -> ToolResult:
        try:
            # 安全的数学计算
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in expression):
                return ToolResult(success=False, result="", error="包含不允许的字符")
            
            result = eval(expression)
            return ToolResult(success=True, result=str(result))
        except Exception as e:
            return ToolResult(success=False, result="", error=str(e))


class ReActAgent:
    """ReAct Agent 实现"""
    
    def __init__(self, llm_api_key: str, llm_model: str, tools: List[Tool], max_iterations: int = 10):
        self.llm_api_key = llm_api_key
        self.llm_model = llm_model
        self.tools = {tool.name: tool for tool in tools}
        self.max_iterations = max_iterations
        
        # ReAct 提示模板
        self.prompt_template = """You are a ReAct agent that can think and act to solve problems.

可用工具：
{tools_description}

请按照以下格式回答：
Thought: 我需要思考下一步要做什么
Action: 工具名称
Action Input: 工具的输入参数
Observation: 工具执行的结果

如果你已经有了最终答案，请以以下格式结束：
Thought: 我现在知道最终答案了
Final Answer: 最终答案

问题：{question}

让我们开始：
"""
    
    def _format_tools_description(self) -> str:
        """格式化工具描述"""
        descriptions = []
        for tool in self.tools.values():
            descriptions.append(f"- {tool.name}: {tool.description}")
        return "\n".join(descriptions)
    
    def _parse_action(self, text: str) -> tuple[Optional[str], Optional[str]]:
        """解析模型输出中的行动"""
        # 查找 Action 和 Action Input
        action_match = re.search(r'Action:\s*(.+)', text)
        action_input_match = re.search(r'Action Input:\s*(.+)', text)
        
        if action_match and action_input_match:
            action = action_match.group(1).strip()
            action_input = action_input_match.group(1).strip()
            return action, action_input
        
        return None, None
    
    def _is_final_answer(self, text: str) -> bool:
        """检查是否包含最终答案"""
        return "Final Answer:" in text
    
    def _extract_final_answer(self, text: str) -> str:
        """提取最终答案"""
        match = re.search(r'Final Answer:\s*(.+)', text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return "无法提取最终答案"
    
    def _call_llm(self, prompt: str) -> str:
        #client = genai.Client(api_key=config.gemini_key)
        client = genai.Client(api_key=self.llm_api_key)
        response = client.models.generate_content(
            model=self.llm_model,
            config=types.GenerateContentConfig(
                system_instruction="You are a ReAct agent that can think and act to solve problems.",
                max_output_tokens=500,
                temperature=0.7),
            contents=prompt
        )
        return response.text
        # 模拟LLM响应 - 实际使用时替换为OpenAI API、Claude API等
        # 这里为了演示，返回一个示例响应
        #return """Thought: 我需要搜索最新的天气信息
        #Action: search
        #Action Input: 今日天气预报"""
        #return response.text  
    
    def run(self, question: str) -> str:
        """运行ReAct循环"""
        # 构建初始提示
        tools_desc = self._format_tools_description()
        prompt = self.prompt_template.format(
            tools_description=tools_desc,
            question=question
        )
        
        print(f"Initial Prompt:\n{prompt}\n")

        conversation_history = prompt
        
        for iteration in range(self.max_iterations):
            print(f"\n--- Iteration {iteration + 1} ---")
            
            # 调用LLM
            #print(f"conversation_history:\n{conversation_history}\n ")
            response = self._call_llm(conversation_history)
            print(f"LLM Response: {response}\n end of LLM response\n")
            #print("end of LLM resonse\n")
            # 检查是否是最终答案
            if self._is_final_answer(response):
                final_answer = self._extract_final_answer(response)
                print(f"Final Answer: {final_answer}")
                return final_answer
            
            # 解析行动
            action, action_input = self._parse_action(response)
            
            if action and action_input:
                # 执行工具
                if action in self.tools:
                    tool_result = self.tools[action].execute(action_input)
                    
                    if tool_result.success:
                        observation = f"Observation: {tool_result.result}"
                    else:
                        observation = f"Observation: 工具执行失败 - {tool_result.error}"
                    
                    print(f"Tool Result: {observation}")
                    
                    # 更新对话历史
                    conversation_history += f"\n{response}\n{observation}\n"
                else:
                    observation = f"Observation: 工具 '{action}' 不存在"
                    print(f"Error: {observation}")
                    conversation_history += f"\n{response}\n{observation}\n"
            else:
                # 无法解析行动，继续对话
                print("无法解析行动，继续...")
                conversation_history += f"\n{response}\n"
        
        return "达到最大迭代次数，未能找到最终答案"


# 使用示例
def main():
    # 初始化工具
    tools = [
        SearchTool(),
        CalculatorTool()
    ]
    
    # 创建ReAct Agent
    agent = ReActAgent(
        llm_api_key=config.gemini_key,  # 替换为真实的API密钥
        llm_model=config.gemini_model,
        tools=tools,
        max_iterations=5
    )
    
    # 运行示例
    question = "今天天气怎么样？"
    result = agent.run(question)
    print(f"\n最终结果: {result}")


if __name__ == "__main__":
    main()