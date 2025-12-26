import yaml

def load_config(path="config.yaml"):
    """Load configuration from a YAML file.
    Args:
        path (str): Path to the YAML configuration file.
        """
    with open(path, "r") as file:
        config = yaml.safe_load(file)
    return config

# test config loading or not

# if __name__ == "__main__":
#     config = load_config("config.yaml")
#     print(config)