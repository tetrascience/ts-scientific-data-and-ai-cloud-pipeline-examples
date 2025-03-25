import re
import ts_dataweave as dw

DEFAULT_TIMEOUT = 300

class DataWeaveError(Exception):
    """Wrapper for DataWeave errors which removes ANSI control codes from message."""

    def __init__(self, parent: dw.Error):
        # regular expression to catch ANSI control codes
        ansi_regex = re.compile(r"(\x9B|\x1B\[)[0-9:;<=>?]*[ -\/]*[@-~]")

        # Using a lot of `strip()` here to eliminate extra newlines.
        # Generally we only expect to see output in stderr, but we don't want
        # to lose anything from stdout either.
        error_str = "\n".join([parent.stdout.strip(), parent.stderr.strip()]).strip()

        super().__init__(ansi_regex.sub("", error_str))


def prepare_dataweave_transform_inputs(input_dict, context):
    """
    This function takes an `input` object and a `context` object as parameters.
    The `context` object contains metadata info of the current task and some helper functions.
    The `input` object is a dictionary containing the following key-value pairs.
    """

    # Get Input File Pointer and category
    input_file_pointer = input_dict["input_file_pointer"]

    # Build a dataweave input object:
    #  There will be 2 inputs to the DW transform
    #  payload = Input File Contents
    #  payloadMetadata = Input File Metadata
    dataweave_input = {
        "payload": {},
        "payloadMetadata": {}
    }

    file_obj = context.read_file(input_file_pointer)
    dataweave_input["payload"] = file_obj["body"]

    # add the metadata, tags, and labels
    dataweave_input["payloadMetadata"] = {
        "metadata": file_obj["custom_metadata"],
        "tags": file_obj["custom_tags"],
        "labels": context.get_labels(input_file_pointer),
    }

    # add all the rest of the metadata headers in the input file
    for key in file_obj.get("metadata", {}).keys():
        if key not in dataweave_input["payloadMetadata"]:
            dataweave_input["payloadMetadata"][key] = file_obj["metadata"][key]

    dataweave_input["payloadMetadata"]["ts_file_bucket"] = input_file_pointer["bucket"]
    dataweave_input["payloadMetadata"]["ts_file_key"] = input_file_pointer["fileKey"]
    dataweave_input["payloadMetadata"]["ts_file_version"] = input_file_pointer[
        "version"
    ]

    return dataweave_input, file_obj


def dataweave_exec(input_dict, context):
    """
    This function takes an `input` object and a `context` object as parameters.
    The `context` object contains metadata info of the current task and some helper functions.
    The `input_dict` object is a dictionary containing the following key-value pairs.
    
    `input_file_pointer` - dict - the input file pointer
    `dw_mapping_script` - string - the actual DataWeave mapping script

    """

    # prepare the dataweave inputs
    dataweave_input, input_file_obj = prepare_dataweave_transform_inputs(input_dict, context)

    # get the dataweave mapping
    map_file = input_dict["dw_mapping_script"]

    # Execute the DW transform on the content itself
    if map_file:
        try:
            raw_output = dw.run(
                payload={key: dw.Payload(value) for key, value in dataweave_input.items()},
                script=map_file,
                timeout=DEFAULT_TIMEOUT
        )
        except dw.Error as error:
            raise DataWeaveError(error) from error

    print(raw_output)
    return raw_output
