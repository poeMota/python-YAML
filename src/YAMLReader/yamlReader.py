from .token import Token, TokenStates
import pprint

def read_yaml(path):
    with open(path, "r", encoding="utf8") as file:
        ret = []
        tokens: list[Token] = []
        root = Token(-1, None)
        root.statuses.append(TokenStates.ListOpener)
        parents = {
            -1: root
        }
        for line in file:
            indent = GetIndent(line)
            listStarter = False
            if "- " in line:
                indent += 1
                listStarter = True 
            _tokens = line.replace("- ", "").replace(' ', '').replace('\n', '').split(':')
            _prev = None
            for i in range(len(_tokens)):
                # Remove comments
                if '#' in _tokens[i]: _tokens[i] = _tokens[i].split('#')[0]
                
                if _tokens[i] != '': 
                    token = Token(
                        indent,
                        TryParseKey(token=_tokens[i])
                        )
                    token.listStarter = listStarter
                    listStarter = False
                    if _prev is not None:
                        _prev.childrens.append(token)
                        token.indent = _prev.indent
                    else:
                        parents[token.indent - 1].childrens.append(token)
                        parents[token.indent] = token
                    _prev = token
                    tokens.append(token)
        
        # Mark token statuses
        SetTokenStatuses(tokens)
        print(root)

        return TokensConvert(root)[None]


def SetTokenStatuses(tokens: list[Token]) -> None:
    for token in tokens:
        if token.key == "...":
            token.statuses.append(TokenStates.Ender)
            continue
    
        if token.listStarter:
            if len(token.childrens) == 1:
                token.statuses.append(TokenStates.DictStart)
            elif not token.childrens:
                token.statuses.append(TokenStates.ListMember)
        else:
            if len(token.childrens) == 1:
                token.statuses.append(TokenStates.DictMember)
            elif not token.childrens:
                token.statuses.append(TokenStates.Value)
                continue
        
        if token.childrens and token.childrens[0].childrens and not token.childrens[0].listStarter:
            if TokenStates.DictMember in token.statuses: token.statuses.remove(TokenStates.DictMember)
            token.statuses.append(TokenStates.DictOpener)
        elif len(token.childrens) > 1:
            token.statuses.append(TokenStates.ListOpener)

        if token.indent != -1 and not token.statuses:
            raise ValueError(f"None root token has none statuses: {token}")
        if len(token.statuses) > 1:
            raise ValueError(f"Token have more than one status: f{token}")


def TokensConvert(root: Token, ret={}):
    if TokenStates.Value in root.statuses: return root.key
    if TokenStates.ListMember in root.statuses: return root.key
    key = root.key if type(root.key) is not list else str(root.key)
    lastItem=None

    for token in root.childrens:
        if TokenStates.ListStart in root.statuses:
            ret = Append(ret, lastItem)
            lastItem = TokensConvert(token, [])
        elif TokenStates.DictStart in root.statuses: # FIXME
            ret = Append(ret, lastItem)
            lastItem = {token.key: TokensConvert(token)}
        elif TokenStates.ListMember in root.statuses:
            if type(lastItem) is not list and lastItem is not None:
                ret = Append(ret, lastItem)
                lastItem = TokensConvert(token, [])
            else:
                lastItem = Append(lastItem, TokensConvert(token, []))
        elif TokenStates.DictMember in root.statuses:
            if type(lastItem) is not dict and lastItem is not None:
                ret = Append(ret, lastItem)
                lastItem = {key: TokensConvert(token)}
            else:
                lastItem = Append(lastItem, {key: TokensConvert(token)})
        elif TokenStates.ListOpener in root.statuses:
            if type(lastItem) is not dict and lastItem is not None:
                ret = Append(ret, lastItem)
                lastItem = {key: TokensConvert(token, [])}
            else:
                lastItem = Append(lastItem, {key: TokensConvert(token, [])})
        elif TokenStates.DictOpener in root.statuses:
            if type(lastItem) is not dict and lastItem is not None:
                ret = Append(ret, lastItem)
                lastItem = {key: TokensConvert(token, {})}
            else:
                lastItem = Append(lastItem, {key: TokensConvert(token, {})})

    if lastItem is not None: ret = Append(ret, lastItem)
    if type(ret) is list and len(ret) == 1 and type(ret[0]) is dict and lastItem is not None: ret = ret[0]
    return ret


def Append(l: list | dict, l2):
    if l is None: return l2

    if type(l) is list: 
        l.append(l2)
    elif type(l) is dict and type(l2) is dict:
        for i in l2:
            if i not in l:
                l[i] = l2[i]
            else:
                l[i] = Append(l[i], l2[i])
    #else: raise ValueError(f"Given not list or dict")

    return l


def TryParseKey(token: str):
    # Split into list
    if ',' in token:
        return [TryParseKey(t) for t in token.split(',')]
    # Try parse float
    elif '.' in token:
        try: return float(token)
        except: return token
    # Try parse bool
    elif token == "true":
        return True
    elif token == "false":
        return False
    else:
        # Try parse int
        try: return int(token)
        # Else string 
        except: return token


def GetIndent(string: str):
    indent = 0
    for ch in string:
        if ch == " ": indent += 1
        else:
            if indent % 2 == 0: return indent // 2
            else: raise(ValueError("Incorrect indentation level"))