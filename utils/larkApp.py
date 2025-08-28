import json, sys, os
import lark_oapi as lark
from lark_oapi.api.wiki.v2 import *
from lark_oapi.api.docx.v1 import *
#from lark_oapi.api.drive.v1 import *


cur_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(cur_dir)
sys.path.append(par_dir)
import utils.fileops as fops
from config.config import config

class LarkAPP:
    def __init__(self, appID, appSec, pNode):

        #lark bot:
        self.myappID=appID
        self.myappSecret=appSec
        #lark doc:
        self.parent_node_token=pNode

        self.client = lark.Client.builder() \
            .app_id(self.myappID) \
            .app_secret(self.myappSecret) \
            .log_level(lark.LogLevel.DEBUG) \
            .build()

    """def createClient(self, appID: str, appSecret: str) -> lark.Client:
        client = lark.Client.builder() \
            .app_id(self.myappID) \
            .app_secret(self.myappSecret) \
            .log_level(lark.LogLevel.DEBUG) \
            .build()
        return client"""

    def getListOfWikiSpace(self) -> str:
        lark.logger.debug("Enter getListOfWikiSpace()")

        # 创建client
        #client = self.createClient(self.myappID, self.myappSecret)

        request: ListSpaceRequest = ListSpaceRequest.builder() \
            .build()

        # 发起请求
        response: ListSpaceResponse = self.client.wiki.v2.space.list(request)

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.wiki.v2.space.list failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return None

        # 处理业务结果
        lark.logger.info(lark.JSON.marshal(response.data, indent=4))

        resp_list = json.loads(lark.JSON.marshal(response.data))
        page_token = resp_list["page_token"]
        tmp_val = page_token.split("||", 1)
        if len(tmp_val) >1 :
            page_token = tmp_val[1]
        lark.logger.info(f"page_token: {page_token}")
        return page_token
    
    def listNodeOfWikiSpace(self, parent_token, page_token) -> list:
        lark.logger.debug("Enter listNodeOfWikiSpace()")

        space_id = self.getListOfWikiSpace()
        lark.logger.info(f"space_id: {space_id}")

        if page_token is not None:
            request: ListSpaceNodeRequest = ListSpaceNodeRequest.builder() \
                .space_id(space_id) \
                .page_size(50) \
                .parent_node_token(parent_token) \
                .page_token(page_token) \
                .build()
        else:
            request: ListSpaceNodeRequest = ListSpaceNodeRequest.builder() \
            .space_id(space_id) \
            .page_size(50) \
            .parent_node_token(parent_token) \
            .build()

        # send request
        response: ListSpaceNodeResponse = self.client.wiki.v2.space_node.list(request)

        # error handling
        if not response.success():
            lark.logger.error(
                f"client.wiki.v2.space.list failed, code: {response.code}, \
                msg: {response.msg}, log_id: {response.get_log_id()}, \
                resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return None

        # 处理业务结果
        #lark.logger.debug(lark.JSON.marshal(response.data, indent=4))

        resp_list = json.loads(lark.JSON.marshal(response.data))
        #lark.logger.info(f"\n\n####### listNode ###########\n\n\n\n{resp_list}")

        if "items" not in resp_list:
            return False, "", None
        
        page_items = resp_list["items"]

        #lark.logger.info(f"\n#########\n start: resp_list[items]\n\n\n\n\n\n")
        #lark.logger.info(resp_list["items"])
        #lark.logger.info(f"\n\n\n\n#########\n end of resp_list[items]\n")
        
        has_more = resp_list['has_more']
        page_token = resp_list['page_token']
        page_list = []
        for x in page_items:
            page_list.append(x["title"])
        if page_list is None:
            return has_more, page_token, None
        else:
            return has_more, page_token, page_list
       
    def createNode(self, page_id, page_title: str) -> str:
        lark.logger.debug("createNode()")

        #client = self.createClient(myappID, myappSecret)
        # 构造请求对象
        request: CreateSpaceNodeRequest = CreateSpaceNodeRequest.builder() \
            .space_id(page_id) \
            .request_body(Node.builder()
                .obj_type("docx")
                .parent_node_token(self.parent_node_token)
                .node_type("origin")
                .title(page_title)
                .creator("HuideYin")
                .build()) \
            .build()

        # 发起请求
        response: CreateSpaceNodeResponse = self.client.wiki.v2.space_node.create(request)

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.wiki.v2.space_node.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return None

        # 处理业务结果
        lark.logger.info(lark.JSON.marshal(response.data, indent=4))
        resp = json.loads(lark.JSON.marshal(response.data))
        new_node_token = resp["node"]["node_token"]
        print(f"new_node_token: {new_node_token}")
        return new_node_token


    #def convertMarkdown(self, freport:str):
    def convertMarkdown(self, vulReport: str):
        lark.logger.debug("Enter convertMarkdown()  ")

        #client = createClient(myappID, myappSecret)

        """
        util_fops = fops.FOPS()
        body_content = util_fops.read_from_file(freport)
        """
        body_content = vulReport
        
        # 构造请求对象
        request: ConvertDocumentRequest = ConvertDocumentRequest.builder() \
            .request_body(ConvertDocumentRequestBody.builder()
                .content_type("markdown")
                .content(f"""{body_content}""")
                .build()) \
            .build()

        # 发起请求
        response: ConvertDocumentResponse = self.client.docx.v1.document.convert(request)
        if not response.success():
            lark.logger.error(
                f"client.docx.v1.document.convert failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return None, None

        # 处理业务结果
        lark.logger.info(lark.JSON.marshal(response.data, indent=4))

        tmp_val = json.loads(lark.JSON.marshal(response.data))
        blocks = tmp_val["blocks"]
        first_level_block_ids = tmp_val["first_level_block_ids"]
        return blocks, first_level_block_ids

    def createNestBlocks(self, doc_id: str, children_ids: list, block_desendants) -> bool:
        lark.logger.debug("Enter createBlocks()")

        #client = createClient(myappID, myappSecret)

        request: CreateDocumentBlockDescendantRequest = CreateDocumentBlockDescendantRequest.builder() \
            .document_revision_id(-1) \
            .document_id(doc_id) \
            .block_id(doc_id) \
            .request_body(CreateDocumentBlockDescendantRequestBody.builder()
                .children_id(children_ids)
                .index(0)
                .descendants(block_desendants)
                .build()) \
            .build()
        
        response: CreateDocumentBlockDescendantResponse = self.client.docx.v1.document_block_descendant.create(request)

        if not response.success():
            lark.logger.error(
                f"client.docx.v1.document_block_descendant.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return False

        # 处理业务结果
        lark.logger.info(lark.JSON.marshal(response.data, indent=4))
        return True

    def createWikiPage(self, page_title:str, page_content: str) -> bool:  # example - how to call funcs
        page_id = self.getListOfWikiSpace()
        if page_id is None:
            lark.logger.error("Retrieve space ID failed! quite...")
            return False
        node_id = self.createNode(page_id, page_title)
        if node_id is None:
            lark.logger.error("Create wiki node failed!")
            return False
        
        response_blocks, response_first_level_block_ids = self.convertMarkdown(page_content)

        if response_blocks is None or response_first_level_block_ids is None:
            return False
        return self.createNestBlocks(node_id, response_first_level_block_ids, response_blocks)


def testListNodeOfWikispace():
    larkapp = LarkAPP(config.bot_id, config.bot_secret, config.page_doubao_high)

    #page_title="cve vulnerability analysis report-6"
    #freport = f"{par_dir}/output/CVE-2025-34027.md"
        
    #larkapp.createWikiPage(page_title, freport)
    ### 
    sum_pagelist = []
    page_token = None
    target_title = "6016913-Debian Security Update for linux (CVE-2024-53104)"
    
    has_more = True #, page_token, page_list = larkapp.listNodeOfWikiSpace(config.pagetoken_codewise)
    while has_more:
        #has_more, page_token, page_list = larkapp.listNodeOfWikiSpace(config.pagetoken_codewise, page_token)
        has_more, page_token, page_list = larkapp.listNodeOfWikiSpace(config.page_doubao_medium, page_token)
        
        if page_list is not None:
            sum_pagelist.extend(page_list)

        print(f"has_more: {has_more}")
        print(f"page_token: {page_token}")

    lark.logger.info(f"\n#########\n sum_pagelist\n\n\n\n\n\n{sum_pagelist}")


    if target_title in sum_pagelist:
        print(f"\n###########\nyes\n############")
    else:
        print(f"\n###########\nno\n############")
    
    for x in sum_pagelist:
        print(f"\n###\n{x}")

def testLarkApp():
    testListNodeOfWikispace()

"""
def main():
    testLarkApp()
if __name__ == "__main__":
    main()
"""    