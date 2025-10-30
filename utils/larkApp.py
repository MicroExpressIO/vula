import json, sys, os
import logging
import lark_oapi as lark
from lark_oapi.api.wiki.v2 import *
from lark_oapi.api.docx.v1 import *

# for token_access_id operations
from lark_oapi.api.auth.v3 import * 
# for delete node
from lark_oapi.api.drive.v1 import *


cur_dir = os.path.dirname(os.path.abspath(__file__))
par_dir = os.path.dirname(cur_dir)
sys.path.append(par_dir)
import utils.fileops as fops
from config.config import config

logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )

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
        
        self.clientDrive = lark.Client.builder() \
            .enable_set_token(True) \
            .log_level(lark.LogLevel.DEBUG) \
            .build()
    
    def getTenantAccessToken(self) -> str:
        logging.debug("Enter getTenantAccessToken()")
        # 构造请求对象
        request: InternalTenantAccessTokenRequest = InternalTenantAccessTokenRequest.builder() \
        .request_body(InternalTenantAccessTokenRequestBody.builder()
            .app_id(self.myappID)
            .app_secret(self.myappSecret)
            .build()) \
        .build()

        # 发起请求
        response: InternalTenantAccessTokenResponse = self.client.auth.v3.tenant_access_token.internal(request)

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.auth.v3.tenant_access_token.internal failed, code: \
                {response.code}, msg: {response.msg}, log_id:  \
                {response.get_log_id()},  \
                resp: \n{json.dumps(json.loads(response.raw.content), indent=4, \
                ensure_ascii=False)}")
            return

        # 处理业务结果
        logging.debug(f"{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        res = json.loads(response.raw.content)
        
        logging.debug(f"tenant_access_token is:  {res['tenant_access_token']}")

        return res['tenant_access_token']

    #this can get both tenant and app token
    def getAppAccessToken(self) -> str:  
        # 构造请求对象
        request: InternalAppAccessTokenRequest = InternalAppAccessTokenRequest.builder() \
            .request_body(InternalAppAccessTokenRequestBody.builder()
                .app_id(self.myappID)
                .app_secret(self.myappSecret)
                .build()) \
            .build()

        # 发起请求
        response: InternalAppAccessTokenResponse = self.client.auth.v3.app_access_token.internal(request)

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.auth.v3.app_access_token.internal failed, code: \
                {response.code}, msg: {response.msg}, \
                log_id: {response.get_log_id()}, \
                resp: \n{json.dumps(json.loads(response.raw.content), \
                indent=4, ensure_ascii=False)}"
            )
            logging.error("getAppAccessToken() failed")
            return

        # 处理业务结果
        #lark.logger.info(lark.JSON.marshal(response.data, indent=4))    
        logging.debug(f"{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
        res = json.loads(response.raw.content)
        logging.debug(f"app_access_token is:  {res['app_access_token']}")

        return res["app_access_token"] 

    def removeNode(self, page_token:str) -> bool: 
        logging.debug("Enter removeNode()")

        # retrieve app token
        app_token = self.getAppAccessToken()
        tenant_token = self.getTenantAccessToken()
        
        # 构造请求对象
        request: DeleteFileRequest = DeleteFileRequest.builder() \
            .file_token(page_token) \
            .type("docx") \
            .build()

        # 发起请求
        option = lark.RequestOption.builder().user_access_token(tenant_token).build()
        response: DeleteFileResponse = self.clientDrive.drive.v1.file.delete(request, option)

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.drive.v1.file.delete failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            logging.error("removeNode() failed")
            return

        # 处理业务结果
        # lark.logger.info(lark.JSON.marshal(response.data, indent=4))
        if response.code == 0:
            return True
        return False

    def getListOfWikiSpace(self) -> str:
        logging.debug("Enter getListOfWikiSpace()")

        # 创建client
        #client = self.createClient(self.myappID, self.myappSecret)

        request: ListSpaceRequest = ListSpaceRequest.builder() \
            .build()

        # 发起请求
        response: ListSpaceResponse = self.client.wiki.v2.space.list(request)

        # 处理失败返回
        if not response.success():
            logging.error(
                f"client.wiki.v2.space.list failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return None

        # 处理业务结果
        logging.info(lark.JSON.marshal(response.data, indent=4))

        resp_list = json.loads(lark.JSON.marshal(response.data))
        page_token = resp_list["page_token"]
        tmp_val = page_token.split("||", 1)
        if len(tmp_val) >1 :
            page_token = tmp_val[1]
        logging.debug(f"page_token: {page_token}")
        logging.debug("Leave getListOfWikiSpace()")
        return page_token
    
    def listNodeOfWikiSpace(self, parent_token, page_token) -> list:
        logging.debug("Enter listNodeOfWikiSpace()")

        space_id = self.getListOfWikiSpace()
        logging.info(f"space_id: {space_id}")

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
            logging.error(
                f"client.wiki.v2.space.list failed, code: {response.code}, \
                msg: {response.msg}, log_id: {response.get_log_id()}, \
                resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return None

        # 处理业务结果
        #logging.debug(lark.JSON.marshal(response.data, indent=4))

        resp_list = json.loads(lark.JSON.marshal(response.data))

        if "items" not in resp_list:
            return False, "", None
        
        page_items = resp_list["items"]
        
        has_more = resp_list['has_more']
        page_token = resp_list['page_token']

        # retrieve "title" and its "node_token"
        pages_info = []
        key_to_extract = ["title", "node_token"]
        pages_info = [{key: d[key] for key in key_to_extract if key in d } for d in page_items ]
        logging.debug(f"pages_info: {pages_info}")

        logging.debug("Leave listNodeOfWikiSpace()")

        #if page_list is None:
        if pages_info is None:
            return has_more, page_token, None
        else:
            #return has_more, page_token, page_list
            return has_more, page_token, pages_info
       
    def createNode(self, space_id, parent_id, page_title: str) -> str:
        logging.debug("createNode()")
        # 构造请求对象
        request: CreateSpaceNodeRequest = CreateSpaceNodeRequest.builder() \
            .space_id(space_id) \
            .request_body(Node.builder()
                .obj_type("docx")
                .parent_node_token(parent_id)
                .node_type("origin")
                .title(page_title)
                .creator("HuideYin")
                .build()) \
            .build()

        # 发起请求
        response: CreateSpaceNodeResponse = self.client.wiki.v2.space_node.create(request)

        # 处理失败返回
        if not response.success():
            logging.error(
                f"client.wiki.v2.space_node.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return None

        # 处理业务结果
        logging.info(lark.JSON.marshal(response.data, indent=4))
        resp = json.loads(lark.JSON.marshal(response.data))
        new_node_token = resp["node"]["node_token"]
        print(f"new_node_token: {new_node_token}")
        return new_node_token

    #def recycleNode(self, page_id, page_title: str) -> str:
    def recycleNode(self, page_id) -> bool:
        logging.debug("Enter recycleNode()")

        # 构造请求对象
        space_id  = self.getListOfWikiSpace()
        #app_token = self.getAppAccessToken()
        #tenant_token = self.getTenantAccessToken()
        
        request: MoveSpaceNodeRequest = MoveSpaceNodeRequest.builder() \
            .space_id(space_id) \
            .node_token(page_id) \
            .request_body(MoveSpaceNodeRequestBody.builder()
                .target_parent_token(config.page_kb_recycle)
                .target_space_id(space_id)
                .build()) \
        .build()

        # 发起请求
        #option = lark.RequestOption.builder().app_access_token(app_token).build()
        #response: MoveSpaceNodeResponse = self.client.wiki.v2.space_node.move(request, option)
        response: MoveSpaceNodeResponse = self.client.wiki.v2.space_node.move(request)

        # 处理失败返回
        if not response.success():
            lark.logger.error(
                f"client.wiki.v2.space_node.move failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return

        # 处理业务结果
        #lark.logger.info(lark.JSON.marshal(response.data, indent=4))
        if response.code == 0:
            return True
        return False

    #def convertMarkdown(self, freport:str):
    def convertMarkdownHtml(self, docFormat: str, vulReport: str):
        logging.debug("Enter convertMarkdown()  ")

        #client = createClient(myappID, myappSecret)
        # format = {"markdown", "html"}

        """
        util_fops = fops.FOPS()
        body_content = util_fops.read_from_file(freport)
        """
        body_content = vulReport
        
        # 构造请求对象
        request: ConvertDocumentRequest = ConvertDocumentRequest.builder() \
            .request_body(ConvertDocumentRequestBody.builder()
                .content_type(docFormat)
                .content(f"""{body_content}""")
                .build()) \
            .build()

        # 发起请求
        response: ConvertDocumentResponse = self.client.docx.v1.document.convert(request)
        if not response.success():
            logging.error(
                f"client.docx.v1.document.convert failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return None, None

        logging.debug("# Start 处理业务结果")
        #logging.info(lark.JSON.marshal(response.data, indent=4))
        
        resp = json.loads(lark.JSON.marshal(response.data, indent=4))
        first_level_block_ids = resp["first_level_block_ids"]
        blocks = resp["blocks"]
        return blocks, first_level_block_ids

    def createNestBlocks(self, doc_id: str, children_ids: list, block_desendants) -> bool:
        logging.debug("Enter createNestBlocks()")

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
            logging.error(
                f"client.docx.v1.document_block_descendant.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return False

        # 处理业务结果
        logging.info(lark.JSON.marshal(response.data, indent=4))
        return True
    
    def createBlocks(self, doc_id: str, blocks) -> bool:
        logging.debug("Enter createBlocks()")

        #client = createClient(myappID, myappSecret)

        '''request: CreateDocumentBlockDescendantRequest = CreateDocumentBlockDescendantRequest.builder() \
            .document_revision_id(-1) \
            .document_id(doc_id) \
            .block_id(doc_id) \
            .request_body(CreateDocumentBlockDescendantRequestBody.builder()
                .children_id(children_ids)
                .index(0)
                .descendants(block_desendants)
                .build()) \
            .build()'''
        
        request: CreateDocumentBlockChildrenRequest = CreateDocumentBlockChildrenRequest.builder() \
            .document_revision_id(-1) \
            .document_id(doc_id) \
            .block_id(doc_id) \
            .request_body(CreateDocumentBlockChildrenRequestBody.builder()
                .children(blocks)
                .index(0)
                .build()) \
            .build()
        response: CreateDocumentBlockDescendantResponse = self.client.docx.v1.document_block_descendant.create(request)

        if not response.success():
            logging.error(
                f"client.docx.v1.document_block_descendant.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}, resp: \n{json.dumps(json.loads(response.raw.content), indent=4, ensure_ascii=False)}")
            return False

        # 处理业务结果
        logging.info(lark.JSON.marshal(response.data, indent=4))
        return True

    def createWikiPage(self, page_title:str, page_content: str) -> bool:  # example - how to call funcs
        space_id = self.getListOfWikiSpace()
        if space_id is None:
            logging.error("Retrieve space ID failed! quite...")
            return False
        node_id = self.createNode(space_id, self.parent_node_token, page_title)
        if node_id is None:
            logging.error("Create wiki node failed!")
            return False
        
        response_blocks, response_first_level_block_ids = self.convertMarkdownHtml("markdown", page_content)
        #response_blocks, response_first_level_block_ids = self.convertMarkdownHtml("html", page_content)

        if response_blocks is None or response_first_level_block_ids is None:
            return False
        return self.createNestBlocks(node_id, response_first_level_block_ids, response_blocks)

#############
# test cases
#############
class TestLarkAPP:
    def __init__(self, bot_id, bot_secret, parent_page ):
        self.bot_id = bot_id
        self.bot_secret = config.bot_secret
        self.parent_page = config.page_doubao_high
        
        self.larkapp = LarkAPP(self.bot_id, self.bot_secret, self.parent_page)
    
    def testListNodeOfWikispace(self):

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
            has_more, page_token, page_list = self.larkapp.listNodeOfWikiSpace(config.page_doubao_medium, page_token)
            
            if page_list is not None:
                sum_pagelist.extend(page_list)

            print(f"has_more: {has_more}")
            print(f"page_token: {page_token}")

        logging.info(f"\n#########\n sum_pagelist\n\n\n\n\n\n{sum_pagelist}")


        if target_title in sum_pagelist:
            print(f"\n###########\nyes\n############")
        else:
            print(f"\n###########\nno\n############")
        
        for x in sum_pagelist:
            print(f"\n###\n{x}")


    def test_convertMarkdownHtml(self):
        #larkapp = LarkAPP(config.bot_id, config.bot_secret, config.pagetoken_cve_high)
        page_title = "CVE-2024-36971"
        '''space_id = larkapp.getListOfWikiSpace()
        if space_id is None:
            logging.error("Retrieve space ID failed! quite...")
            return False
        node_id = larkapp.createNode(space_id, page_title)
        if node_id is None:
            logging.error("Create wiki node failed!")
            return False
        '''
        #space_id="7045970518410821634"
        pnode_id="Tl2iwsj0citq7HkAFFwcJmhUnLd"
        freport = "/home/huideyin/src/vula/output/CVE-2024-36971.md"
        util_fops = fops.FOPS()
        body_content = util_fops.read_from_file(freport)

        res_blks, res_blk_ids = self.larkapp.convertMarkdownHtml("markdown", body_content)
        
        #if response_blocks is None or response_first_level_block_ids is None:
        #    return False
        #return self.createNestBlocks(node_id, response_first_level_block_ids, response_blocks)
        #logging.debug("\n\n###########################\n\n")
        #logging.debug(f" res blks: {res_blks} \n")
        #logging.debug(f" \n\n")
        #logging.debug(f" res blk ids: {res_blk_ids} \n")

        if res_blks is None or res_blk_ids is None:
            return False
            
        return self.larkapp.createNestBlocks(pnode_id, res_blk_ids, res_blks)
        #return larkapp.createBlocks(pnode_id, res_blks)

    def test_getTenantAccessToken(self):
        x = self.larkapp.getTenantAccessToken()
        print(f"tenant_access_token is: {x}")
    
    def test_getAppAccessToken(self):
        x = self.larkapp.getAppAccessToken()
        print(f"app_access_token: {x}")

    def test_removeNode(self):
        page_token="FBVYwhDPkiWNdpk8fB6cE4menHg"
        ret = self.larkapp.removeNode(page_token)
        if ret:
            print ("true")
        else:
            print("false")

    def test_recycleNode(self):
        page_token="Tl2iwsj0citq7HkAFFwcJmhUnLd"
        ret = self.larkapp.recycleNode(page_token)
        if ret:
            print ("true")
        else:
            print("false")
 

#'''
if __name__ == "__main__":
    testLarkApp = TestLarkAPP(  config.bot_id, 
                                config.bot_secret, 
                                config.pagetoken_cve_high )
    logging.debug("est")
    #testLarkApp.test_getTenantAccessToken()
    #testLarkApp.test_getAppAccessToken()
    #testLarkApp.test_convertMarkdownHtml()
    #testLarkApp.test_removeNode() # waiting for 1.0.4 to be released
    #testLarkApp.test_recycleNode()
    #testLarkApp.test_removeNode()
#'''
