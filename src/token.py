class Token:
    def __init__(self, key: any, value: any, indent: int, onList: bool = False) -> None:
        self.key = key
        self.value = value
        self.indent = indent
        self.childrens: list[Token] = []
        self.onList = onList


    def add_child(self, child: 'Token'):
        self.childrens.append(child)

