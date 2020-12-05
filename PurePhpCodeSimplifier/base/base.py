import os
import re
import linecache


class PurePhpCodeSimplifier(object):
    def __init__(self, input_path: str = "", output_path: str = ""):
        self.input_path = input_path if input_path != "" else os.path.abspath('input')
        self.output_path = output_path if output_path != "" else os.path.abspath('output')

    def do_simplify(self, working_directory: str = ""):
        if working_directory == "": working_directory = self.input_path
        pwd = working_directory
        _pwd = working_directory
        for file in os.listdir(working_directory):
            _pwd = os.path.join(pwd, file)
            if os.path.isdir(_pwd):
                self.do_simplify(_pwd)
            else:
                # 吧<?PHP?>删选出来
                CH_DICT = self._gen_simplify_dict(_pwd)
                print(CH_DICT)
                self._apply_simlify(_pwd, CH_DICT)

    def _apply_simlify(self, working_directory, change_dict):
        if change_dict != {}:
            f = open(working_directory, mode='r', encoding='utf8')
            file_lines = f.readlines()
            for line_num, content in change_dict.items():
                file_lines[line_num - 1] = content
            file_lines = [_.replace("<?php", "").replace("?>", "") for _ in file_lines]
            f.close()
            f = open(working_directory, mode='w', encoding='utf8')
            f.write("<?php" + "".join(file_lines) + "?>")

    def _gen_simplify_dict(self, working_directory):
        CH_DICT = {}  # 1: <对应修改的完整内容>
        IS_PHP_CONTENT_FLAG = False
        with open(working_directory, encoding='utf8') as f:
            max_line = 1
            for (line_num, line) in enumerate(f):  # 这里的line_num从0算起
                # if line_num+1 >=
                max_line = max(max_line, line_num + 1)
                line = str(line).strip()
                if line.startswith("<?php"):
                    IS_PHP_CONTENT_FLAG = True

                if not IS_PHP_CONTENT_FLAG:
                    # 非PHP内容，但是可能存在
                    # <html>....<?php ... ?>  ... </html>的情况
                    # 那就直接把<?php ... ?> 删选出来
                    # 目前没有碰到这样的脑残写法
                    # <html> ... <?php
                    # PHP_CONTENT
                    # ?> </HTML>'
                    pattern = re.compile(r'<\?php.*?\?>')
                    s = re.findall(pattern, line)
                    if not s:
                        CH_DICT[line_num + 1] = "\n"
                        continue
                    _l = []
                    for _s in s:
                        __s = _s.replace("<?php", "").replace("?>", "").strip()
                        if not __s.endswith(";"):
                            __s += ";"
                        _l.append(__s)
                    if _l:
                        CH_DICT[line_num + 1] = "".join(_ for _ in _l) + "\n"

                if line.endswith("?>"):
                    IS_PHP_CONTENT_FLAG = False
            if max_line in CH_DICT.keys():
                CH_DICT[max_line].replace("\n", "")
        return CH_DICT
