from loguru import logger


class DictStrTranscoder:
    """
    Transcodes between a string and a single layered dictionary of string pairs
    """

    @staticmethod
    def encode(dict: dict[str, str]):
        dict_string = ""

        for key, value in dict:
            if dict_string == "":
                dict_string += f"╳{key}◆{value}"

            else:
                dict_string += f"▶{key}◆{value}"

        return dict_string

    @staticmethod
    def decode(string: str):
        string_dict: dict[str, str] = {}

        if not string.startswith("╳"):
            logger.error(
                "Decoding failure. Input string did not start with unicode character #02573 '╳'. Invalid string."
            )
            return
        else:
            clean_string = string.replace("╳", "")

        for kv_pair in clean_string.split("▶"):
            key, value = kv_pair.split("◆")
            string_dict[key] = value

        return string_dict
