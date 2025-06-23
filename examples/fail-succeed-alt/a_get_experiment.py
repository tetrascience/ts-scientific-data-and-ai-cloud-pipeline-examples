import json

input_file = context.read_file(input['input_file'])["body"].decode("utf-8")
input_json = json.loads(input_file)

label = input_json["experiment_id"]["123"]

output = context.add_labels(input['input_file'],
    labels=[
        {"name": "123", "value": label}
    ]
)
