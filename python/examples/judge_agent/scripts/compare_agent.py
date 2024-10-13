'''
Author: Gege-Wang 2891067867@qq.com
Date: 2024-10-13 17:59:33
LastEditors: Gege-Wang 2891067867@qq.com
LastEditTime: 2024-10-13 20:25:33
FilePath: /python/examples/judge_agent/scripts/compare_agent.py
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
    def __init__(self):
        self.answer_resolve = None
        self.answer_base = None
        self.task = None
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            if dora_event["id"] == "task":
                self.answer_resolve = dora_event["value"][1].as_py()
                print('Received Answer resolve:', self.answer_resolve)
                self.task = dora_event["value"][0].as_py()
                print('Received Task:', self.task) 
            elif dora_event["id"] == "base":
                self.answer_base = dora_event["value"][0].as_py()
                print('Received Answer base:', self.answer_base)

            if self.answer_resolve and self.answer_base and self.task:
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='compare_agent.yml')
                inputs = load_agent_config(yaml_file_path)
                inputs['input_fields'] = {'answer_resolve': self.answer_resolve,'answer_base':self.answer_base,'task':self.task}
                agent_result = run_dspy_or_crewai_agent(agent_config=inputs)
                record_agent_result_log(agent_config=inputs,
                                        agent_result={
                                            "1, "+ inputs.get('log_step_name', "Step_one"): {self.task:agent_result}})
                send_output("compare_results", pa.array([create_agent_output(step_name='keyword_results', output_data=agent_result,dataflow_status=os.getenv('IS_DATAFLOW_END',True))]),dora_event['metadata'])
                print('Received Answer Resolved:', self.answer_resolve)
                print('Received Answer Base:', self.answer_base)
                print('Compare Result:', agent_result)

                self.answer_resolve = None
                self.answer_base = None
                self.task = None


        return DoraStatus.CONTINUE