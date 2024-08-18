def write(path: str, content: dict | list, indent: int = 2):
    with open(path, 'w', encoding="utf-8") as f:
        f.write(ConvertToYaml(content, -1, indent).removeprefix('\n'))


def ConvertToYaml(content: dict | list, nesting: int, indent: int):
    nest = nesting + 1
    ret = ""

    # Dont read this, please
    if type(content) is list:
        if not content:
            return "[]"
        for i in content:
            if type(i) is dict:
                _ret = ''
                for key in i:
                    if not _ret:
                        _ret = f"\n{(nest - 1) * indent * ' '}- {key}:{' ' if '!' not in str(key) else ''}{ConvertToYaml(i[key], nest, indent)}"
                    else:
                        _ret = f"{_ret}\n{nest * indent * ' '}{key}:{' ' if '!' not in str(key) else ''}{ConvertToYaml(i[key], nest, indent)}"
                ret = f"{ret}{_ret}"
            elif type(i) is list:
                [ret := f"{ret}\n{(nest - 1) * indent * ' '}- {ConvertToYaml(i[key], nest, indent)}" for j in i]
            else:
                ret = f"{ret}\n{(nest - 1) * indent * ' '}- {ConvertToYaml(i, nest, indent)}"
    elif type(content) is dict:
        if not content:
            return "{}"
        for key in content:
            ret += f"\n{nest * indent * ' '}{key}:{' ' if '!' not in str(key) else ''}{ConvertToYaml(content[key], nest, indent)}"
    else:
        if content == None:
            return "null"

        return str(content)
    return ret

