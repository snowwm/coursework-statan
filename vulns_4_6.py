from collections import defaultdict
import re

from code_analyzer import CodeAnalyzer


@CodeAnalyzer.register
def command_intrusion(source):
    vulnlist = []
    charmas = []
    danger = ['system', 'popen', 'execlp', 'execvp', '_wsystem']
    for i in range(len(source)):
        line = source[i]
        if 'char ' in line:
            if '[' and ']' in line:
                newchar = line.split('char')[1].split('[')[0].strip()
                charmas.append(newchar)
    for i in range(len(source)):
        line = source[i]
        for d in danger:
            if d in line and (line.find(d) < line.find('(') < line.find(')')):
                templine = line.split('(')[1].split(')')[0].strip()
                command = line.split('(')[0].strip()
                for char in charmas:
                    if templine.find(char) != -1 and command.find(d) != -1:
                        if i not in vulnlist:
                            vulnlist.append(i)
    return vulnlist


@CodeAnalyzer.register
def unsafe_data_storage(source):
    words = ['pass', 'password', 'pwd', 'adminpassword', 'passwd', 'secret', 'passphrase', 'crypt', 'cipher',
                'cypher']
    vulnerabilitylines = []
    for i in range(len(source)):
        for word in words:
            line = source[i]
            if word in line or word in line.lower():
                if ('=' in line) or ('==' in line and 'if' in line):
                    tmp = line.split('=')[1].strip()
                    if ('\"' in tmp) or ('\'' in tmp) or ('&' in tmp):
                        if not i in vulnerabilitylines:
                            vulnerabilitylines.append(i)
    return vulnerabilitylines


@CodeAnalyzer.register
def memory_leak(source):
    variables = set()
    dangerous_variables = defaultdict(set)

    for i, line in enumerate(source):
        for d in CodeAnalyzer.var_declarations(line):
            variables.add(d.name)
            
        if "new" in line or "malloc" in line:
            for var in variables:
                if re.search(f"\\b{var}\\b", line):
                    dangerous_variables[var].add(i)
                    
        if "delete" in line or "free" in line:
            for var in list(dangerous_variables):
                if re.search(f"\\b{var}\\b", line):
                    dangerous_variables.pop(var)
                    
    for var_set in dangerous_variables.values():
        yield from var_set
