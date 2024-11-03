import yaml

def get_mongo():
    """
    Reads MongoDB connection string from configuration file `config.yaml`.
    
    Returns
    -------
    str
        MongoDB connection string.
    """
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
        return config.get("MONGO_DETAILS")


def get_token():
    """
    Загружает токен GitHub из файла конфигурации `config.yaml`.
    
    Returns
    -------
    str
        GitHub токен для API-запросов.
    """
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)
        return config.get("github_token")
