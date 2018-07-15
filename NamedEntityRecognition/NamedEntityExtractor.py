from typing import List

# FIXME 인풋으로 리스트가 아닌 raw 텍스트 받을것.
def FetchEntityNames() -> List[str]:
    raise NotImplementedError


class NamedEntityExtractor:
    def __init__(self, txtArr:List[str]):
        pass

    def ExtractEntityNames(self):
        raise NotImplementedError
