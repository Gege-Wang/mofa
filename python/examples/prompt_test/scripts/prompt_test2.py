'''
Author: Gege-Wang 2891067867@qq.com
Date: 2024-10-13 18:15:46
LastEditors: Gege-Wang 2891067867@qq.com
LastEditTime: 2024-10-13 19:24:36
FilePath: /judge_agent/scripts/base_agent.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import json
import os
from dora import Node, DoraStatus
import pyarrow as pa
from mofa.kernel.utils.util import load_agent_config, load_dora_inputs_and_task, create_agent_output
from mofa.run.run_agent import run_dspy_agent, run_crewai_agent, run_dspy_or_crewai_agent
from mofa.utils.files.dir import get_relative_path
from mofa.utils.log.agent import record_agent_result_log


class Operator:
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            agent_inputs = ['data','task']
            if dora_event["id"] in agent_inputs:
                task = dora_event["value"][0].as_py()
                # print('task:', task)
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='prompt.yml')
                inputs = load_agent_config(yaml_file_path)
                inputs["task"] = task
                agent_result = run_dspy_or_crewai_agent(agent_config=inputs)
                record_agent_result_log(agent_config=inputs,
                                        agent_result={
                                            "1, "+ inputs.get('log_step_name', "Step_one"): {task:agent_result}})
                send_output("base_results", pa.array([create_agent_output(step_name='keyword_results', output_data=agent_result,dataflow_status=os.getenv('IS_DATAFLOW_END',False))]),dora_event['metadata'])
                print('base_results:', agent_result)

        return DoraStatus.Continue