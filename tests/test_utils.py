import jgt_tools.utils


def test_get_pyproject_config():
    config = jgt_tools.utils.get_pyproject_config()
    assert isinstance(config, dict)
    assert config["tool"]["poetry"]["name"] == "jgt_tools"
