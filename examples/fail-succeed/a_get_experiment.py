import json

input_file = context.read_file(input['input_file'])["body"].decode("utf-8")
input_json = json.loads(input_file)

output = input_json["experiment_id"]["123"]