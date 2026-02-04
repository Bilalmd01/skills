#!/usr/bin/env python3
"""
智谱AI网络搜索API调用脚本
通过 chat completions API 调用 web_search 工具
"""

import os
import sys
import json
import argparse
import requests
import re
from typing import Optional, Dict, Any, List
from urllib.parse import urlparse


API_BASE_URL = "https://open.bigmodel.cn/api/paas/v4"


def search(
    search_query: str,
    search_engine: str = "search_std",
    search_intent: bool = False,
    count: int = 10,
    search_domain_filter: Optional[str] = None,
    search_recency_filter: Optional[str] = None,
    content_size: Optional[str] = None,
    request_id: Optional[str] = None,
    user_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    调用智谱搜索API
    
    参数与智谱API保持一致，提供最大的灵活性
    """
    api_key = os.environ.get("ZHIPU_API_KEY")
    if not api_key:
        raise ValueError("ZHIPU_API_KEY environment variable is not set")
    
    # 构建工具调用参数
    tool_params = {
        "search_query": search_query,
        "search_engine": search_engine,
        "search_intent": search_intent,
        "count": count,
    }
    
    # 添加可选参数
    if search_domain_filter:
        tool_params["search_domain_filter"] = search_domain_filter
    if search_recency_filter:
        tool_params["search_recency_filter"] = search_recency_filter
    if content_size:
        tool_params["content_size"] = content_size
    
    # 构建请求体 - 使用 function calling 方式
    payload: Dict[str, Any] = {
        "model": "glm-4-flash",
        "messages": [
            {"role": "system", "content": "你是一个能够使用搜索工具的AI助手。当用户需要搜索信息时，请使用web_search工具。"},
            {"role": "user", "content": search_query}
        ],
        "tools": [
            {
                "type": "web_search",
                "web_search": {
                    "enable": True,
                    **tool_params
                }
            }
        ],
        "tool_choice": "auto",
    }
    
    # 添加可选的元数据
    if request_id:
        payload["request_id"] = request_id
    if user_id:
        payload["user_id"] = user_id
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    response = requests.post(
        f"{API_BASE_URL}/chat/completions",
        headers=headers,
        json=payload,
        timeout=60,
    )
    
    response.raise_for_status()
    result = response.json()
    
    # 提取搜索结果
    return extract_search_results(result, search_query)


def extract_search_results(response: Dict[str, Any], original_query: str) -> Dict[str, Any]:
    """从API响应中提取搜索结果"""
    output = {
        "id": response.get("id", ""),
        "created": response.get("created", 0),
        "request_id": response.get("request_id", ""),
        "search_query": original_query,
        "search_intent": [],
        "search_result": [],
        "raw_response": response,
    }
    
    # 尝试从 choices 中提取工具调用结果
    choices = response.get("choices", [])
    if not choices:
        return output
    
    message = choices[0].get("message", {})
    
    # 检查 tool_calls (结构化搜索结果)
    tool_calls = message.get("tool_calls", [])
    for tool_call in tool_calls:
        if tool_call.get("type") == "web_search":
            web_search_result = tool_call.get("web_search", {})
            if "search_intent" in web_search_result:
                output["search_intent"] = web_search_result["search_intent"]
            if "search_result" in web_search_result:
                output["search_result"] = web_search_result["search_result"]
    
    # 如果没有结构化结果，尝试从 content 中解析
    content = message.get("content", "")
    if content and not output["search_result"]:
        # 尝试解析 JSON
        try:
            if isinstance(content, str) and content.strip().startswith("{"):
                parsed = json.loads(content)
                if "search_result" in parsed:
                    output["search_result"] = parsed["search_result"]
                elif "results" in parsed:
                    output["search_result"] = parsed["results"]
        except:
            pass
        
        # 如果JSON解析失败，尝试从文本中提取链接和信息
        if not output["search_result"]:
            parsed_results = parse_text_to_results(content)
            if parsed_results:
                output["search_result"] = parsed_results
    
    output["model_response"] = content
    return output


def parse_text_to_results(text: str) -> List[Dict[str, Any]]:
    """尝试从文本内容中提取搜索结果"""
    results = []
    
    # 匹配URL模式
    url_pattern = r'https?://[^\s\)\]\>\"\']+'
    urls = re.findall(url_pattern, text)
    
    # 按段落分割
    paragraphs = text.split('\n\n')
    
    for i, para in enumerate(paragraphs):
        # 查找包含URL的段落
        para_urls = re.findall(url_pattern, para)
        if para_urls or (para.strip() and len(para) > 20):
            # 尝试提取标题（通常是比较短的句子或加粗内容）
            lines = para.strip().split('\n')
            title = lines[0][:100] if lines else f"结果 {i+1}"
            
            # 清理标题
            title = re.sub(r'^\d+\.\s*', '', title)
            title = re.sub(r'^[\*\-\#]+\s*', '', title)
            
            result = {
                "title": title,
                "content": para[:500],
                "link": para_urls[0] if para_urls else "",
                "media": extract_domain(para_urls[0]) if para_urls else "",
            }
            results.append(result)
    
    return results[:10]  # 最多返回10条


def extract_domain(url: str) -> str:
    """从URL中提取域名"""
    try:
        parsed = urlparse(url)
        return parsed.netloc.replace('www.', '')
    except:
        return ""


def format_results(data: Dict[str, Any]) -> str:
    """格式化搜索结果为可读文本"""
    lines = []
    
    lines.append(f"🔍 搜索: {data.get('search_query', 'N/A')}")
    lines.append("")
    
    # 搜索意图信息
    if data.get("search_intent"):
        lines.append("=== 搜索意图 ===")
        for intent in data["search_intent"]:
            lines.append(f"原始Query: {intent.get('query', 'N/A')}")
            lines.append(f"识别意图: {intent.get('intent', 'N/A')}")
            lines.append(f"改写关键词: {intent.get('keywords', 'N/A')}")
        lines.append("")
    
    # 搜索结果
    results = data.get("search_result", [])
    if results:
        lines.append(f"=== 搜索结果 (共{len(results)}条) ===")
        for idx, result in enumerate(results, 1):
            lines.append(f"\n[{idx}] {result.get('title', '无标题')}")
            if result.get('media'):
                lines.append(f"    来源: {result['media']}")
            if result.get('link'):
                lines.append(f"    链接: {result['link']}")
            if result.get('publish_date'):
                lines.append(f"    发布时间: {result['publish_date']}")
            content = result.get('content', '')
            if content:
                lines.append(f"    摘要: {content[:200]}{'...' if len(content) > 200 else ''}")
    else:
        lines.append("未找到结构化搜索结果")
        # 显示模型回复
        if data.get("model_response"):
            lines.append("\n=== 模型回复 ===")
            lines.append(data["model_response"][:1000])
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="智谱AI网络搜索工具")
    
    # 必填参数
    parser.add_argument(
        "--query", "-q",
        required=True,
        help="搜索内容 (search_query)，建议不超过70字符"
    )
    parser.add_argument(
        "--engine", "-e",
        default="search_std",
        choices=["search_std", "search_pro", "search_pro_sogou", "search_pro_quark"],
        help="搜索引擎 (search_engine)，默认: search_std"
    )
    
    # 可选参数
    parser.add_argument(
        "--intent", "-i",
        action="store_true",
        help="启用搜索意图识别 (search_intent)"
    )
    parser.add_argument(
        "--count", "-c",
        type=int,
        default=10,
        help="返回结果数量 (count)，范围1-50，默认: 10"
    )
    parser.add_argument(
        "--domain-filter", "-d",
        help="域名白名单过滤 (search_domain_filter)"
    )
    parser.add_argument(
        "--recency", "-r",
        choices=["oneDay", "oneWeek", "oneMonth", "oneYear", "noLimit"],
        help="时间范围过滤 (search_recency_filter)"
    )
    parser.add_argument(
        "--content-size", "-s",
        choices=["medium", "high"],
        help="内容长度控制 (content_size): medium(摘要) / high(详细)"
    )
    parser.add_argument(
        "--request-id",
        help="唯一请求标识 (request_id)"
    )
    parser.add_argument(
        "--user-id", "-u",
        help="终端用户ID (user_id)，6-128字符"
    )
    parser.add_argument(
        "--json", "-j",
        action="store_true",
        help="输出原始JSON格式"
    )
    
    args = parser.parse_args()
    
    try:
        result = search(
            search_query=args.query,
            search_engine=args.engine,
            search_intent=args.intent,
            count=args.count,
            search_domain_filter=args.domain_filter,
            search_recency_filter=args.recency,
            content_size=args.content_size,
            request_id=args.request_id,
            user_id=args.user_id,
        )
        
        if args.json:
            # 移除 raw_response 以减少输出
            output = {k: v for k, v in result.items() if k != "raw_response"}
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            print(format_results(result))
            
    except requests.exceptions.RequestException as e:
        print(f"API请求失败: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"配置错误: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"未知错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
