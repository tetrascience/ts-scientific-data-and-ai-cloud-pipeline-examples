from src.use_context_api_actual import use_context_api_actual
import pytest
import os

# Create the Logger class, to be used in Context
class Logger:
    def __init__(self):
        return
    def log(self, msg):
        print(msg)

# Create the context class, including the properties and methods
# TODO: Make more nuanced handling of issues with methods
class Context:
    def __init__(self,
                    pipeline_id = None,
                    workflow_id = None,
                    master_script_namespace = None,
                    master_script_slug = None,
                    master_script_version = None,
                    protocol_slug = None,
                    protocol_version = None,
                    pipeline_config = None,
                    input_file = None,
                    created_at = None,
                    task_id = None,
                    task_created_at = None,
                    platform_url = None,
                    platform_version = None,
                    tmp_dir = None,
                    file_name = None,
                    file_id = None,
                    body = None,
                    ids_info = None,
                    eql_info = None,
                    presigned_url = None,
                    password = None
                    ):

        # Parameters
        self.pipeline_id = pipeline_id
        self.workflow_id = workflow_id
        self.master_script_namespace = master_script_namespace
        self.master_script_slug = master_script_slug
        self.master_script_version = master_script_version
        self.protocol_slug = protocol_slug
        self.protocol_version = protocol_version
        self.pipeline_config = pipeline_config
        self.input_file = input_file
        self.created_at = created_at
        self.task_id = task_id
        self.task_created_at = task_created_at
        self.platform_url = platform_url
        self.platform_version = platform_version
        self.tmp_dir = tmp_dir

        # Info for functions
        self.file_name = file_name
        self.file_id = file_id
        self.body = body
        self.ids_info = ids_info
        self.eql_info = eql_info
        self.presigned_url = presigned_url
        self.password = password
        self.file_pointer = eql_info

    # Methods
    
    def get_logger(self):
        self.logger = Logger()
        return self.logger
    
    def read_file(self, input_file, form):
        if form=="body":
            return input_file

    def add_labels(self, input_file, labels):
        self.labels = labels
        for i,label in enumerate(self.labels):
            self.labels[i]["id"] = i
        return self.labels
    
    def get_labels(self, input_file):
        return self.labels
    
    def get_file_name(self, input_file):
        return self.file_name
    
    def get_file_id(self, input_file):
        return self.file_id
    
    def get_ids(self, namespace, slug, version):
        return self.ids_info
    
    def search_eql(self, payload, returns):
        return self.eql_info
    
    def get_presigned_url(self, input_file, duration):
        return self.presigned_url
    
    def get_secret_config_value(self, config_item):
        return self.password
    
    def resolve_secret(self, password):
        return self.password
    
    def write_file(self, content, file_name, file_category, ids=None):
        return self.file_pointer
    
    def write_ids(self, content_obj, file_suffix, file_category, ids):
        return self.file_pointer
    
    def update_metadata_tags(self, input_file, custom_meta, custom_tags):
        return self.file_pointer
    
    def add_attributes(self, input_file, custom_meta, custom_tags, labels):
        return self.file_pointer
    
    def delete_labels(self, input_file, label_ids):
        print("Labels successfully deleted")
        return []
    
    def validate_ids(self, data, namespace, slug, version):
        print("downloading ids, ids-info")
        return None
    
    # def run_command(self):
    #     return {"command": "command info"}


#========== TEST SCENARIO 1 ==========#

# Use a specific test file
test_file_name = "raw_envision.json"

# Create a specific context object
@pytest.fixture
def context_a():

    # Get the file contents of the file
    current_dir = os.path.dirname(__file__)
    data_path = os.path.join(current_dir, '..', 'data', test_file_name)
    with open(data_path) as f:
        file_contents = f.read()
        file_contents_body = {"body": file_contents}

    # Create the context object
    # TODO: Replace with more detailed scenario data
    return Context(pipeline_id = "00000000-0000-0000-0000-000000000001",
                    workflow_id = "00000000-0000-0000-0000-000000000002",
                    master_script_namespace = "private-ORG",
                    master_script_slug = "testing-protocol",
                    master_script_version = "v0.1.0",
                    protocol_slug = "testing-protocol",
                    protocol_version = "v0.1.0",
                    input_file = file_contents_body,
                    created_at = "2025-01-01T00:00:00.000Z",
                    task_id = "00000000-0000-0000-0000-000000000004",
                    task_created_at = "2025-01-01T00:00:10.000+00:00",
                    platform_url = "https://www.tetrascience.com",
                    platform_version = "v4.2",
                    tmp_dir = "/tmp/tmp",
                    file_name=test_file_name,
                    file_id="00000000-0000-0000-0000-000000000001",
                    body=file_contents_body,
                    ids_info = {'$schema': 'http://json-schema.org/draft-07/schema', '$id': 'http://ids.tetrascience.com/common/plate-reader-perkinelmer-envision/v6.0.1/schema.json', 'type': 'object'},
                    eql_info = {"filename": test_file_name},
                    presigned_url="http://www.presigned-url.com/",
                    password = "password"
                    )

# Create placeholder for inputs to task script
# TODO: Modify with realistic scenario data
test_input = {"input_file_pointer": "file_pointer",
                "password": "password"}

# Create test for getting properties and methods
def test_context_fixture(context_a):
    assert context_a.file_name == test_file_name
    assert context_a.get_file_name(test_input["input_file_pointer"]) == test_file_name

# Create a test for the full task script functionality
def test_use_context_api_actual(context_a):
    output = use_context_api_actual(input=test_input, context=context_a)
