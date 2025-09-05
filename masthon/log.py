from logger import Logger, str_config

config = """
{
    "name": "Masthon Logger",
    "targets": {
        "_STDOUT": {
            "filter":{
                "levels": "*",
                "kwblacklist": ["__dnsos__", "do not show on stdout"],
                "kwwhitelist": null,
                "custom_filter": null,
                "custom_allower": null
            },
            "log_type": "FORMATED"
        },
        "DEBUG.json": {
            "filter":{
                "levels": ["DEBUG", "INFO"],
                "kwblacklist": [],
                "kwwhitelist": ["debug"],
                "custom_filter": null,
                "custom_allower": null
            },
            "log_type": "JSON"
        },
        "logs.log":{
            "filter":{
                "levels": "*",
                "kwblacklist": [],
                "kwwhitelist": null,
                "custom_filter": null,
                "custom_allower": null
            },
            "log_type": "CLEAN"
        }
    }
}
"""


logger = Logger(str_config(config))
logger.debug("Logger created")