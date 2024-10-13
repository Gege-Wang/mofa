'''
Author: Gege-Wang 2891067867@qq.com
Date: 2024-10-13 18:54:27
LastEditors: Gege-Wang 2891067867@qq.com
LastEditTime: 2024-10-13 18:56:10
FilePath: /judge_agent/test.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import json
import os
from mofa.utils.files.dir import get_relative_path
json_file_path = get_relative_path(current_file=__file__, sibling_directory_name='data', target_file_name='agent_response.json')
with open(json_file_path, 'r') as json_file:
    json_data = json.load(json_file)
task = json_data.get('task', '')
print('task:', task)
agent_response = json_data.get('agent_response', '')
print('agent_response:', agent_response)