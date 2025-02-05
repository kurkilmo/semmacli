import re

tab_lines = open("semmatabs.txt").readlines()

pattern = r"costNumber=\d+"
numbers = []
for line in tab_lines:
    match = re.findall(pattern, line)
    number = match[0].split("=")[1]
    numbers.append(number)

print(f"[{",\n".join(numbers)}]")