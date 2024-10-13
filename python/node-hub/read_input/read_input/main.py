'''
Author: Gege-Wang 2891067867@qq.com
Date: 2024-10-13 20:04:08
LastEditors: Gege-Wang 2891067867@qq.com
LastEditTime: 2024-10-13 20:33:11
FilePath: /python/node-hub/read_input/read_input/main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

import os
import json
import numpy as np
import pyarrow as pa
from dora import Node
from mofa.utils.files.dir import get_relative_path

RUNNER_CI = True if os.getenv("CI") == "true" else False

def main():

# 初始化 Node
    node = Node()
# 遍历 data 目录中的所有 JSON 文件
    data_dir = "data"
    for json_filename in os.listdir(data_dir):
        if json_filename.endswith(".json"):
            json_file_path = get_relative_path(current_file=__file__, sibling_directory_name='data', target_file_name=json_filename)
        # 从 JSON 文件中加载数据
            with open(json_file_path, 'r') as json_file:
                json_data = json.load(json_file)
                task = json_data.get('task', '')
                print('task:', task)
                agent_response = json_data.get('agent_response', '')
                print('agent_response:', agent_response)
                node.send_output("resolve_result", pa.array([task]))

        else:
            print(f"Unexpected data format in {json_file_path}")

if __name__ == "__main__":
    main()
