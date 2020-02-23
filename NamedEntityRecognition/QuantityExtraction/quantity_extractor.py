from quantulum3 import parser


class QuantityExtractor:
    def __init__(self, text):
        self.text = text

    def extract_most_informative(self):
        quants = parser.parse(self.text)
        # print(quants)
        return quants

    def get_all_numbers(self):
        raise NotImplementedError


def test_quantity_extraction():
    test_txt = """
I spent 20 pounds on this!
The LHC smashes proton beams at 12.8–13.0 TeV
Sound travels at 0.34 km/s
"""
    return QuantityExtractor(test_txt).extract_most_informative()


if __name__ == "__main__":
    q = test_quantity_extraction()
    print(q)
