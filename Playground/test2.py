import re


content = """[특징주우우우]"""
regex = "\%s(.*?)\%s" % ('[', ']')
boxContent = re.search(regex, content).group(0)

print(boxContent)
