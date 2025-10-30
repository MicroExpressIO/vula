import os

import time
from datetime import datetime

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
                )


class FOPS:
    def __init__(self):
        self.fops = []

    def read_from_file(self, fpath: str) -> str:
        # read text info from given file
        # return a str
        fcontent = ""
        try:
            if not os.path.exists(fpath):
                return None
            with open(fpath, 'r', encoding='utf-8') as file:
                fcontent = file.read()
        except FileNotFoundError:
            print(f"Error find file")
        except Exception as e:
            print(f"Excpetion found: {e}")
        return fcontent

    def write_if_not_exists(self, file_path: str, content: str) -> bool:
        """
        Write content to a file if it does not already exist.
        
        :param file_path: Path to the file where content should be written.
        :param content: Content to write to the file.
        """
        try:

            if os.path.exists(file_path):
                print(f"File '{file_path}' already exists. Skipping write operation.")
                return False
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
                print(f"Content written to '{file_path}'.")
                return True
        except Exception as e:
            print(f"Error writing to file '{file_path}': {e}")
            return False   
        except IOError as e:
            print(f"IOError while writing to file '{file_path}': {e}")
            return False
     
    def rewrite_if_exists(self, file_path: str, content: str) -> bool:
        """
        Write content to a file if it does not already exist.
        
        :param file_path: Path to the file where content should be written.
        :param content: Content to write to the file.
        """
        try:

            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Remove existed file {file_path} . ")
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
                print(f"Content written to '{file_path}'.")
                return True
        except Exception as e:
            print(f"Error writing to file '{file_path}': {e}")
            return False   
        except IOError as e:
            print(f"IOError while writing to file '{file_path}': {e}")
            return False

    ### get file modfication timestamp in seconds
    def get_modification_timestamp(self, filepath: str):
        if os.path.exists(filepath):
            return os.path.getmtime(filepath)
        else:
            logging.error(f"Error: File not found at {filepath}")

    ### If the target file newer than existed
    def is_file_newer(self, ts_existed, new_file: str) -> bool:
        tar_timestamp = self.get_modification_timestamp(new_file)
        return True if tar_timestamp > ts_existed else False

class TestFOPS:
    def __init__(self, tpath):
        self.path=tpath

    def test_get_timestamp(self):
        testFops = FOPS()
        tpath="/home/huideyin/src/tmp/link"
        spath="/home/huideyin/src/tmp/links"
        tret = testFops.get_modification_timestamp(tpath)
        sret = testFops.get_modification_timestamp(spath)
        logging.debug(f"\n sret: {sret}\n tret: {tret}")
        if sret > tret:
            logging.debug("sret larger")
        else:
            logging.debug("sret smaller")

    def test_if_filenewer(self):
        testFops = FOPS()
        spath="/home/huideyin/src/tmp/link"
        tpath="/home/huideyin/src/tmp/tlink"
        sret = testFops.get_modification_timestamp(spath)
        ret = testFops.is_file_newer(sret, tpath)
        if ret:
            logging.debug("\n\nnewer\n")
        else:
            logging.debug("\nolder\n")
    


if __name__ == "__main__" :
    test=TestFOPS("/home/huide")
    #test.test_get_timestamp()
    test.test_if_filenewer()
