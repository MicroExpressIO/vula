"""
在使用大模型时，可以通过以下方式实现访问外部网络：

通过API联网调用：
1. 创建bot时选择相关配置开启联网能力。
    a. 具体来说，先创建一个应用，然后在控制台里开启联网功能。同时可参考以下文档了解更多详情：
https://cloud.bytedance.net/docs/ark/docs/664afad9e16ff302cb5c0706/674e783f4238d802790991e1?x-resource-account=public&x-bc-region-id=bytedance

https://cloud.bytedance.net/docs/ark/docs/664afad9e16ff302cb5c0706/667ecff27749010250657855?x-resource-account=public&x-bc-region-id=bytedance [citation: 3]

    b. 使用联网搜索工具：在生成模型响应时，可利用方舟大模型内置工具实现联网搜索功能。

示例代码如下：
```
--header "Authorization: Bearer <ARK_API_KEY>" \
--header 'Content-Type: application/json' \
--header 'ark-beta-web-search: true' \
--data '{
    "model": "doubao-seed-1-6-250615",
    "stream": true,
    "tools": [
        {"type": "web_search"}
    ],
    "input": [
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text": "今天有什么热点新闻"
                }
            ]
        }
    ]
}'
[citation: 1]
```

2. 使用联网内容插件：
    该插件支持实时搜索互联网公开域网页资源和字节系的图文、视频资源，
    帮助大语言模型获取最新、专业的信息。其支持的搜索资源包括涵盖各领
    域丰富的互联网公开可搜索网页等多种类型，且各类型资源有相应的展示
    引用链接及计费说明。
    
    需注意默认限流为5QPS（账号维度），并且开启此插件时，Function 
    Calling功能不生效。具体可参考 联网内容插件产品计费.
总结：实现大模型访问外部网络可通过API配置、内置工具以及插件等方式，每种方式各有特点和适用场景，使用者可根据自身需求选择合适的方法，并注意相关的限制条件和使用说明。

联网内容插件产品计费: [https://cloud.bytedance.net/docs/ark/docs/664afad9e16ff302cb5c0706/674e783f4238d802790991dd]
"""


from openai import OpenAI
import os, sys
from pathlib import Path
cur_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(cur_dir)
pp_dir = os.path.dirname(par_dir)
prj_dir = Path(__file__).resolve().parent.parent.parent
print(f" prj_dir: {prj_dir}")
print(f" par_dir: {par_dir}")
print(f" pp_dir: {pp_dir}")


sys.path.append(pp_dir)
from config.config import config

# 从环境变量中获取您的API KEY，配置方法见：https://www.volcengine.com/docs/82379/1399008

client = OpenAI(
    #base_url='https://ark-cn-beijing.bytedance.net/api/v3',
    base_url=config.doubao_url,
    api_key=config.gpt_key
)

tools = [{
    "type": "web_search",
}]

# 创建一个对话请求
response = client.responses.create(
    model=config.gpt_model,
    input=[{"role": "user", "content": "北京的天气怎么样？"}],
    tools=tools,
)

print(response)
