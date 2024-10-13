from dora import Node, DoraStatus
import pyarrow as pa
import json
from mofa.utils.files.dir import get_relative_path


class Operator:
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            # log_file_path = get_relative_path(current_file=__file__, sibling_directory_name='logs', target_file_name='log.md')

            # with open(log_file_path, 'r') as log_file:
            #     log_data = log_file.read()

            # send_output("log_results", pa.array([log_data]), dora_event['metadata'])
            # print('log_results:', log_data)

            json_file_path = get_relative_path(current_file=__file__, sibling_directory_name='data', target_file_name='agent_response.json')
            with open(json_file_path, 'r') as json_file:
                json_data = json.load(json_file)
                task = json_data.get('task', '')
                print('task:', task)
                agent_response = json_data.get('agent_response', '')
                print('agent_response:', agent_response)

            print('task:', task)
            print('agent_response:', agent_response)
            send_output("resolve_result", pa.array([task, agent_response]), dora_event['metadata'])

        return DoraStatus.CONTINUE
