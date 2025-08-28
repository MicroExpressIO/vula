import os

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
     