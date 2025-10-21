from task_script import parse


def test_parse_contents():
    """Test that the parse_file function maps the input to the expected output field."""
    # Arrange
    contents = b"123"

    # Act
    actual = parse.parse_file(contents)

    # Assert
    assert actual.file == "123"
