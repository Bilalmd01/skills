---
name: zhipu-search
description: |
  智谱AI网络搜索工具，提供灵活的搜索引擎调用能力。
  
  Use when:
  - 需要搜索网络信息获取最新数据
  - 需要特定搜索引擎（搜狗、夸克、智谱搜索）
  - 需要按时间范围、域名过滤搜索结果
  - 需要控制搜索结果数量和详细程度
  
  支持搜索引擎：search_std(基础版)、search_pro(高阶版)、search_pro_sogou(搜狗)、search_pro_quark(夸克)
  支持参数：搜索意图识别、结果数量、时间过滤、域名过滤、内容长度控制
metadata:
  {
    "openclaw":
      {
        "requires": { "env": ["ZHIPU_API_KEY"] },
      },
  }
---

# 智谱搜索 (Zhipu Search)

通过智谱AI API进行网络搜索，支持多种搜索引擎和灵活的参数配置。

## 快速使用

### 基础搜索

```python
# 使用默认参数搜索
search_query = "OpenClaw 最新版本"
search_engine = "search_std"
```

### 高级搜索（完整参数）

```python
search_query = "人工智能发展趋势"      # 必填，最多70字符
search_engine = "search_pro"          # 必填：search_std/search_pro/search_pro_sogou/search_pro_quark
search_intent = true                  # 可选，默认false，是否进行搜索意图识别
count = 20                            # 可选，默认10，范围1-50
search_domain_filter = "example.com"  # 可选，限定域名白名单
search_recency_filter = "oneWeek"     # 可选：oneDay/oneWeek/oneMonth/oneYear/noLimit
content_size = "high"                 # 可选：medium/high，控制内容详细程度
request_id = "unique-request-id"      # 可选，唯一请求标识
user_id = "user-123456"               # 可选，终端用户ID（6-128字符）
```

## 调用方式

### 方式1：直接调用脚本（推荐）

```bash
python scripts/zhipu_search.py \
  --query "搜索内容" \
  --engine search_pro \
  --count 10
```

### 方式2：使用OpenClaw工具调用

系统会自动根据需求选择合适的参数调用搜索功能。

## API 参数说明

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| search_query | string | ✅ | - | 搜索内容，建议≤70字符 |
| search_engine | enum | ✅ | - | search_std/search_pro/search_pro_sogou/search_pro_quark |
| search_intent | boolean | - | false | 是否进行搜索意图识别 |
| count | integer | - | 10 | 返回结果数量，1-50 |
| search_domain_filter | string | - | - | 限定白名单域名 |
| search_recency_filter | enum | - | noLimit | oneDay/oneWeek/oneMonth/oneYear/noLimit |
| content_size | enum | - | - | medium/high，控制内容长度 |
| request_id | string | - | - | 唯一请求标识 |
| user_id | string | - | - | 终端用户ID（6-128字符） |

## 搜索引擎选择指南

| 引擎 | 适用场景 |
|------|----------|
| search_std | 基础搜索，常规问答 |
| search_pro | 高阶搜索，需要更精准结果 |
| search_pro_sogou | 搜狗搜索，国内内容 |
| search_pro_quark | 夸克搜索，特定场景 |

## 返回结果结构

```json
{
  "id": "task-id",
  "created": 1704067200,
  "request_id": "request-id",
  "search_intent": [
    {
      "query": "原始搜索query",
      "intent": "SEARCH_ALL",
      "keywords": "改写后的关键词"
    }
  ],
  "search_result": [
    {
      "title": "标题",
      "content": "内容摘要",
      "link": "结果链接",
      "media": "网站名称",
      "icon": "网站图标",
      "refer": "角标序号",
      "publish_date": "发布时间"
    }
  ]
}
```

## 环境要求

- 环境变量 `ZHIPU_API_KEY` 必须已配置
- Python 3.7+
- requests 库

## 注意事项

1. search_query 建议控制在70字符以内
2. search_pro_sogou 的 count 必须是 10/20/30/40/50 之一
3. user_id 如果提供，长度必须在6-128字符之间
4. 搜索意图识别会增加响应时间，但能提升搜索结果相关性
