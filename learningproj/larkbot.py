
import json

import lark_oapi as lark
from lark_oapi.api.wiki.v2 import *

grandparent_node_token="WxEtwrfXhiJCY2kWfWacT68CnEf"
parent_node_token="N3J6wdHt4i3CEFk5DPfcRSwgntQ"

def create_lark_wiki(title: str, content: str) -> None:

    client = lark.Client.builder() \
        .app_id("cli_a8faaf83d234100e") \
        .app_secret("yuEEbIk8bDDGyZEoB9abUT2Wd4hUFjbD") \
        .log_level(lark.LogLevel.DEBUG) \
        .build()
    

    # 构造请求对象
    request: CreateSpaceNodeRequest = CreateSpaceNodeRequest.builder() \
        .space_id("") \
        .request_body(Node.builder()
            .obj_type("doc")
            .parent_node_token(parent_node_token)
            .node_type("origin")
            .origin_node_token(parent_node_token)
            .title(title)
            .build()) \
        .build()

    # 发起请求
    #response: CreateSpaceNodeResponse = client.wiki.v2.space_node.create(request)

    # 发起请求
    option = lark.RequestOption.builder().user_access_token("u-ghWmx_FGxcXGTt68twSf5r5giNJx41Erqi0051c02703").build()
    response: CreateSpaceNodeResponse = client.wiki.v2.space_node.create(request, option)


    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.wiki.v2.space_node.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))

#def main():
    #create_lark_wiki("larkbot", "This is a test content for larkbot wiki page.")


# SDK 使用说明: https://open.feishu.cn/document/uAjLw4CM/ukTMukTMukTM/server-side-sdk/python--sdk/preparations-before-development
# 以下示例代码默认根据文档示例值填充，如果存在代码问题，请在 API 调试台填上相关必要参数后再复制代码使用
def main():
    # 创建client
    # 使用 user_access_token 需开启 token 配置, 并在 request_option 中配置 token
    client = lark.Client.builder() \
        .enable_set_token(True) \
        .app_id("cli_a8faaf83d234100e") \
        .app_secret("yuEEbIk8bDDGyZEoB9abUT2Wd4hUFjbD") \
        .log_level(lark.LogLevel.DEBUG) \
        .build()
    
    # 构造请求对象
    request: CreateSpaceNodeRequest = CreateSpaceNodeRequest.builder() \
        .space_id("222") \
        .request_body(Node.builder()
            .obj_type("doc")
            .parent_node_token(parent_node_token)
            .node_type("origin")
            .title("test lark bot")
            .build()) \
        .build()

    # 发起请求
    option_user = lark.RequestOption.builder().user_access_token("u-ghWmx_FGxcXGTt68twSf5r5giNJx41Erqi0051c02703").build()
    option_tenant = lark.RequestOption.builder().tenant_access_token("t-g1047v4XIG6QSQXKPG32VH6RE7PIFSADD347ISWY").build()
    response: CreateSpaceNodeResponse = client.wiki.v2.space_node.create(request, option_tenant)

    # 处理失败返回
    if not response.success():
        lark.logger.error(
            f"client.wiki.v2.space_node.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        return

    # 处理业务结果
    lark.logger.info(lark.JSON.marshal(response.data, indent=4))

if __name__ == "__main__":
    main()