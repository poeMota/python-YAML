from enum import Enum


class Token:
    def __init__(self, key: any, value: any, indent: int, onList: bool = False) -> None:
        self.key = key
        self.value = value
        self.indent = indent
        self.childrens: list[Token] = []
        self.onList = onList


    def __repr__(self) -> str:
        return f"\nToken: \"{self.key}\", value: {self.value}, indent: {self.indent}, onList: {self.onList}, childrens ({len(self.childrens)}): {self.childrens}\n"


    def add_child(self, child: 'Token'):
        self.childrens.append(child)

