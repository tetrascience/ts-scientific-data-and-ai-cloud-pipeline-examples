from ts_sdk.task.__task_script_runner import Context
import json
import datetime
import os

def print_hello_world(input: dict, context: Context):
    print("Hello World!")
    
def decorate_input_file(input: dict, context: Context) -> dict:
    print("Start 'decorate_input_file' function...")
    
    input_file_pointer = input["input_file_pointer"]
    # file_name = context.get_file_name(input_file_pointer)
    labels_json = input["labels_json"]
    
    # added_labels = 
    context.add_labels(file=input_file_pointer,labels=labels_json)
    
    print("'decorate_input_file' completed")
    return input_file_pointer

def harmonize_input_file(input: dict, context: Context) -> dict:
    print("Start 'harmonize_input_file' function...")

    input_file_pointer = input["input_file_pointer"]

    # Open the file and import json
    f = context.read_file(input_file_pointer, form='file_obj')
    raw_data = f['file_obj'].read().decode("utf-8")
    raw_json = json.loads(raw_data)

    # Information from raw file json
    # ASSUMPTION: there is only one reading and one json entry
    """
    {
    "analysisResult": "DAILY_CHECKS TestBatch-2 R24_A02 Probe1A Glucose 12/11/2020 10:50 AM 23.08 52.9 mmol/L 1 mmol/L 1",
    "timestamp": 1607701875000
    }
    """

    # Pull out the relevant fields from json
    analysisResult = raw_json["analysisResult"]
    timestamp = raw_json["timestamp"]

    # Order of fields analysisResult from biochemistry-analyzer IDS Details
    # ASSUMPTION: concentration units are always mmol/L
    """
    <Experiment Name> <Batch Name> <Analyte Source Id> <Probe Id> <Chemistry> <Machine Date> <Machine Time> <Temperature in Celsius> <Concentration value> <Concentration units> <Analysis Error Code>
    """

    analysisResult_items = analysisResult.split(" ")
    experiment_name = analysisResult_items[0]
    batch_name = analysisResult_items[1]
    analyte_source_id = analysisResult_items[2]
    probe_id = analysisResult_items[3]
    chemistry = analysisResult_items[4]
    machine_datetime = datetime.datetime.strptime(" ".join(analysisResult_items[5:8]), '%m/%d/%Y %H:%M %p').isoformat()
    temp_in_c = analysisResult_items[8]
    concentration_value = analysisResult_items[9]
    analysis_error_code = analysisResult_items[13]

    time_export = datetime.datetime.fromtimestamp(raw_json['timestamp']/1000).isoformat()

    # Create IDS dictionary
    """
    To get the structure, look at the expected.json file in the biochemistry-analyzer IDS Details
    """
    ids_dict = {}

    # Generic Info
    ids_dict["@idsNamespace"] = "common"
    ids_dict["@idsType"] = "biochemistry-analyzer"
    ids_dict["@idsVersion"] = "v1.0.0"

    # Export Time
    ids_dict["time"] = {"export": time_export}

    # Sample
    ids_dict["sample"] = {"batch": batch_name}

    # Results
    ids_results_item = {}
    ids_results_item["time"] = {"measurement": machine_datetime}
    ids_results_item["probe"] = probe_id
    ids_results_item["temperature"] = {"value": temp_in_c, "unit": "DegreesCelsius"}
    ids_results_item["chemical_concentration"] = {"name": chemistry, "value": concentration_value, "unit": "MillimolePerLiter"}
    ids_dict["results"] = [ids_results_item]


    # Save the file to S3 and save pointer to return
    saved_ids = context.write_file(
        content=json.dumps(ids_dict),
        file_name="ids_demo.json",
        file_category="IDS",
        ids="common/biochemistry-analyzer:v1.0.0"
    )
    
    print("'harmonize_input_file' completed")
    return saved_ids

def enrich_input_file(input: dict, context: Context) -> dict:

    # Perform elasticsearch query
    # This query could also be in a configuration element and be passed to task-script
    # Here it's hardcoded and there is only one file on the test platform that it finds.

    elasticsearch_query =  {
                            "query": {
                                "bool": {
                                    "must": [
                                                {
                                                    "term": { "category": "RAW" }
                                                },
                                                {
                                                    "nested": {
                                                        "path": "labels",
                                                        "query": {
                                                            "bool": {
                                                                "must": [
                                                                        {
                                                                        "term": {
                                                                            "labels.name": "enrichment-file"
                                                                        }
                                                                        },
                                                                        {
                                                                        "term": {
                                                                            "labels.value": "enrichment-file"
                                                                        }
                                                                    }
                                                                ]
                                                            }
                                                        }
                                                    }
                                                }
                                            ]
                                        }
                                    }
                            }

    # Take contents of file and add a label
    print("Using Elasticsearch")
    eql_file_pointers = context.search_eql(payload=elasticsearch_query, returns="filePointers")

    # Open the file and import json
    print("Getting extra file contents")
    f = context.read_file(eql_file_pointers[0], form='file_obj')
    enrichfile_data = f['file_obj'].read().decode("utf-8")

    # This file has some labels and then some other data
    # ASSUMPTION: This extra file has a specific format and can be parsed to add data to IDS
    print("Get Labels and Data")
    labels, data = enrichfile_data.split('\n\ndata')

    labels_to_add = [{"name": x.split(", ")[0], "value": x.split(", ")[1]} for x in labels.split('\n')]
    data_to_add = [[int(y) for y in x.split(',')] for x in data.split('\n')[1:-1]]

    # Get IDS input file and add to the json
    print("Get IDS File info")
    input_file_pointer = input["input_file_pointer"]
    g = context.read_file(input_file_pointer, form='file_obj')
    ids_data = g['file_obj'].read().decode("utf-8")
    ids_json = json.loads(ids_data)
    ids_json["extra_data"] = data_to_add

    # Save this file to S3 as PROCESSED and save pointer to return
    print("Saving PROCESSED file")
    saved_processed = context.write_file(
        content=json.dumps(ids_json),
        file_name="processed_demo.json",
        file_category="PROCESSED",
    )

    # Add labels to processed file
    print("Adding labels")
    # added_labels = 
    context.add_labels(file=saved_processed, labels=labels_to_add)

    print("'enrich_input_file' completed")
    return saved_processed
    
def push_data(input: dict, context: Context) -> dict:

    print("Starting push to 3rd party")

    # Pull out the arguments to the function
    input_file_pointer = input["input_file_pointer"]
    kaggle_username = input["kaggle_username"]
    kaggle_api_key_secret = input["kaggle_api_key"]
    kaggle_api_key = context.resolve_secret(kaggle_api_key_secret)

    print("Get Processed file data")
    # Open the file and import json
    f = context.read_file(input_file_pointer, form='file_obj')
    processed_data = f['file_obj'].read().decode("utf-8")
    processed_json = json.loads(processed_data)

    print("Start Kaggle content")
    # Kaggle Specific
    # Add username and API Key to OS environment
    os.environ['KAGGLE_USERNAME'] = kaggle_username
    os.environ['KAGGLE_KEY'] = kaggle_api_key

    # Kaggle Specific
    # Pull out the data from the PROCESSED file and save as a temporary file
    data = {}
    data["data"] = processed_json["extra_data"]

    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

    # Kaggle Specific
    # Create dataset metadata and save as a temporary file
    dataset_name = "exampledataset"
    dataset_metadata = {
                        "title": dataset_name,
                        "id": kaggle_username+"/"+dataset_name,
                        "licenses": [
                                {
                                "name": "CC0-1.0"
                                }
                            ]
                        }
    with open('dataset-metadata.json', 'w') as outfile:
        json.dump(dataset_metadata, outfile)


    # Kaggle Specific
    # Upload data to Kaggle. Uses OS environment variables
    os.system("kaggle datasets create -p .")



