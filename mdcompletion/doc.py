from dataclasses import dataclass


@dataclass
class Document:
    uri: str
    text: str

    def __str__(self) -> str:
        return f'{self.uri}: {self.text[:50]}'

    @property 
    def lines(self) -> list[str]:
        return self.text.splitlines()

    def text_at(self, line: int, start_col: int, end_col: int) -> str:
        return self.lines[line][start_col:end_col]
