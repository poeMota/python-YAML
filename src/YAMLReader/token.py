from enum import Enum


class TokenStates(Enum):
    Value = 1
    ListOpener = 2
    DictOpener = 3
    ListMember = 4
    DictMember = 5
    ListStart = 6
    DictStart = 7
    Ender = 8


class Token:
    def __init__(self, indent: int, key: any) -> None:
        self.indent = indent
        self.key = key
        self.childrens: list[Token] = []
        self.listStarter = False
        self.statuses: list[TokenStates] = []


    def __repr__(self) -> str:
        return f"\n{'\t'*self.indent}Token: \"{self.key}\", indent: {self.indent}, statuses: {self.statuses}, childrens: {self.childrens}\n"