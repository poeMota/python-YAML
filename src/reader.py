from .token import Token
import json


def read(path):
    with open(path, "r", encoding="utf8") as file:
        root = Token(None, None, -1, True)
        indent_stack = {-1: root}  # {indent_level: token}

        for line in file:
            token = TokenParse(line)
            if not token:
                continue

            indent_stack[token.indent] = token
            indent_stack[token.indent - 1].add_child(token)

        return TokensTreeConvert(root)


def TokenParse(token_str: str):
    onList = False
    if "- " in token_str:
        onList = True

    key = token_str.replace("- ", "").replace(' ', '').replace('\n', '')#.replace('"', '').replace("'", '')
    value = None
    other_token = None
    if not key:
        return
    #if '#' in key:
    #    key = key.split('#')[0]
    if ':' in key:
        keys = key.split(':')
        if len(keys) > 2:
            key = keys[0]
            other_token = TokenParse(':'.join(keys[1::]))
        else:
            key, value = keys
            if not value: value = None

    token = Token(
        TryParseKey(key),
        TryParseKey(value),
        GetIndent(token_str),
        onList
    )
    if other_token:
        other_token.indent = token.indent + 1
        token.add_child(other_token)
    return token


def TokensTreeConvert(token: Token):
    key = token.key if type(token.key) is not list else str(token.key).replace('[', '').replace(']', '')
    if not token.childrens:
        if token.value is not None:
            return {key: token.value}
        else: return key
    lastItem = None
    childrens_dict = {}
    if token.childrens[0].onList:
        childrens_dict = []
    if token.key == "nodes": print(childrens_dict, token)

    for child in token.childrens:
        ckey = child.key if type(child.key) is not list else str(child.key).replace('[', '').replace(']', '')
        # Dict start in list
        if (child.value is not None or child.childrens) and child.onList:
            if lastItem: Merge(childrens_dict, lastItem)
            lastItem = {ckey: child.value}
        # List item
        if not child.value is not None and child.onList and not child.childrens:
            if lastItem is None:
                lastItem = child.key
            elif type(lastItem) is not list:
                Merge(childrens_dict, lastItem)
                lastItem = child.key
            else:
                Merge(lastItem, child.key)
        # dict member (key: value)
        if child.value is not None and not child.onList and not child.childrens:
            if lastItem is None:
                lastItem = {ckey: child.value}
            elif type(lastItem) is not dict:
                Merge(childrens_dict, lastItem)
                lastItem = {ckey: child.value}
            else:
                Merge(lastItem, {ckey: child.value})
        # Dict or list opener (key: dict/list)
        if not child.value is not None and child.childrens:
            if lastItem is None:
                lastItem = {ckey: TokensTreeConvert(child)}
            elif type(lastItem) is not dict:
                Merge(childrens_dict, lastItem)
                lastItem = {ckey: TokensTreeConvert(child)}
            else:
                Merge(lastItem, {ckey: TokensTreeConvert(child)})

    if lastItem: Merge(childrens_dict, lastItem)
    return childrens_dict


def Merge(l: list | dict, l2):
    if l is None: return l2

    if type(l) is list:
        l.append(l2)
    elif type(l) is dict and type(l2) is dict:
        for i in l2:
            if i not in l:
                l[i] = l2[i]
            else:
                l[i] = Merge(l[i], l2[i])
    return l


def TryParseKey(token: str):
    if token is None:
        return token
    try:
        return json.loads(token)
    except: pass
    # Split into list
    if ',' in token:
        return [TryParseKey(t) for t in token.split(',')]
    # Try parse float
    elif '.' in token:
        try:
            return float(token.removesuffix("rad"))
        except: return token
    # Try parse bool
    elif token.lower() == "true":
        return True
    elif token.lower() == "false":
        return False
    else:
        # Try parse int
        try: return int(token.removesuffix("rad"))
        # Else string
        except: return token


def GetIndent(string: str):
    indent = 0
    for ch in string:
        if ch == " ": indent += 1
        else:
            if indent % 2 == 0: return indent // 2 + ('- ' in string * 2)
            else: raise ValueError("Incorrect indentation level")

