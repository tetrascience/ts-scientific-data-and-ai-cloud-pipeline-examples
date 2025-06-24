import json
from ts_sdk.task.__task_script_runner import Context

def safe_pipeline_config(pipeline_config: dict):
    secrets = [
        k.split(":")[1]
        for k in pipeline_config
        if k.startswith("_resolved_")
    ]

    return {
        k: "********" if (k in secrets or k.startswith("_resolved_"))
        else v
        for k, v in pipeline_config.items()
    }

def use_context_api_actual(input: dict, context: Context):

    SECRET_KEY = "password"
    # Getting inputs passed to Task Script from Protocol/Pipeline
    input_file_pointer = input["input_file_pointer"]
    password = input[SECRET_KEY]


    print("========== Testing Context API Properties ==========")

    print(f"Pipeline ID: {context.pipeline_id}")
    print(f"Workflow ID: {context.workflow_id}")
    print(f"Master Script Namespace: {context.master_script_namespace}")
    print(f"Master Script Slug: {context.master_script_slug}")
    print(f"Master Script Version: {context.master_script_version}")
    print(f"Protocol Slug: {context.protocol_slug}")
    print(f"Protocol Version: {context.protocol_version}")
    print(f"Pipeline Config: {safe_pipeline_config(context.pipeline_config)}")
    print(f"Input File: {context.input_file}")
    print(f"Created At: {context.created_at}")
    print(f"Task ID: {context.task_id}")
    print(f"Task Created At: {context.task_created_at}")
    print(f"Platform URL: {context.platform_url}")
    print(f"Platform Version: {context.platform_version}")
    print(f"Tmp Directory: {context.tmp_dir}")


    print("========== Testing Context API Functions ==========")

    print("Get Logger")
    logger = context.get_logger()
    logger.log({
        "message": "Using the logger",
        "level": "info"
    })

    logger.log("Read File")
    read_file_output = context.read_file(context.input_file, form="body")
    read_file_contents = json.loads(read_file_output["body"])
    # print(read_file_contents)

    logger.log("Add Labels")
    add_labels_output = context.add_labels(input_file_pointer,[{"name": "label-name", "value": "label-value"}])
    print(add_labels_output)
    label_to_remove_later = add_labels_output[0]["id"]

    logger.log("Get Labels")
    file_labels_output = context.get_labels(input_file_pointer)
    print(file_labels_output)

    logger.log("Get File Name")
    get_file_name_output = context.get_file_name(input_file_pointer)
    print(get_file_name_output)

    logger.log("Get File ID")
    file_id_output = context.get_file_id(input_file_pointer)
    print(file_id_output)

    logger.log("Get IDS Schema")
    get_ids_output = context.get_ids(namespace = "common", slug = "plate-reader-perkinelmer-envision", version = "v6.0.1")
    print(get_ids_output)

    logger.log("Search EQL")
    search_eql_output = context.search_eql(payload = {"query": {"term": {"source.type": "context-api"}}},
                                            returns = "filePointers")
    print(search_eql_output)

    logger.log("Get Presigned URL")
    get_presigned_url_output = context.get_presigned_url(input_file_pointer, 900)
    print(get_presigned_url_output)

    logger.log("Get Secret Config Value from Config")
    get_secret_config_value_output = context.get_secret_config_value("password")
    print("********")

    logger.log(f"Unresolved Secret: {password}")

    logger.log("Resolve Secret")
    resolve_secret_output = context.resolve_secret(password)
    print("********")

    logger.log("Write File")
    write_file_output = context.write_file(content = json.dumps(read_file_contents),
                                            file_name = "ids.json",
                                            file_category="IDS",
                                            ids="common/plate-reader-perkinelmer-envision:v6.0.1")
    print(write_file_output)

    logger.log("Write IDS")
    write_ids_output = context.write_ids(content_obj = read_file_contents,
                                            file_suffix = "demo",
                                            file_category = "IDS",
                                            ids = "common/plate-reader-perkinelmer-envision:v6.0.1")
    print(write_ids_output)

    logger.log("Update Metadata Tags")
    update_metadata_tags_output = context.update_metadata_tags(input_file_pointer,
                                                                custom_meta = {'meta-key1': 'meta-value1'},
                                                                custom_tags = ['tag1', 'tag2'])
    print(update_metadata_tags_output)

    logger.log("Add Attributes")
    add_attributes_output = context.add_attributes(input_file_pointer,
                                                    custom_meta = {'meta-key2': 'meta-value2'},
                                                    custom_tags = ['tag3', 'tag4'],
                                                    labels = [{"name": "label-name2", "value": "label-value2"}])
    print(add_attributes_output)

    logger.log("Delete Labels")
    delete_labels_output = context.delete_labels(input_file_pointer, label_ids = [str(label_to_remove_later)])
    print(delete_labels_output)

    logger.log("Validate IDS")
    validate_ids_output = context.validate_ids(data = read_file_contents,
                                                namespace = "common",
                                                slug = "plate-reader-perkinelmer-envision",
                                                version = "v6.0.1")
    print(validate_ids_output)

    # logger.log("Run Command")
    # run_command_output = context.run_command()
    # print(run_command_output)
