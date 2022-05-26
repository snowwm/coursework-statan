import re

from code_analyzer import CodeAnalyzer


@CodeAnalyzer.register
def buffer_overflow(source):
    error = list()
    not_safe_functions = ['strcpy', 'strncpy', 'sprintf', 'gets', 'strcat', 'scanf']
    for i in range(len(source)):
        for f in not_safe_functions:
            if f in source[i] and f + '_s' not in source[i]:
                error.append(i)
    return error


@CodeAnalyzer.register
def format_string_error(source):
    functions = [r'printf', r'sprintf', r'syslog', r'fprintf', r'snprintf']
    error = []
    for i in range(len(source)):
        for f in functions:
            if f + '(' in source[i] or f + ' (' in source[i]:
                vskobke = source[i].split("(")[1].split(")")[0].strip()
                if "\"" in vskobke:
                    overtext = vskobke.partition("\"")[2].partition("\"")[2]
                    for format_letter in ['%c', '%d', '%i', '%s', '%e', '%Е', '%f', '%g', '%G', '%o', '%u', '%x',
                                            '%X', '%р', '%n']:
                        if (format_letter in vskobke) and (not overtext):
                            if i not in error:
                                error.append(i)
                            break
                elif vskobke:
                    if i not in error:
                        error.append(i)
                    break
    return error


@CodeAnalyzer.register
def sql_injection(source):
    variables = set()
    dangerous_variables = set()

    for i, line in enumerate(source):
        for d in CodeAnalyzer.var_declarations(line):
            variables.add(d.name)
            
        if "scanf(" in line or "gets(" in line or "cin >>" in line:
            for var in variables:
                if re.search(f"\\b{var}\\b", line):
                    dangerous_variables.add(var)
                    
        elif ".exec(" in line:
            for var in dangerous_variables:
                if re.search(f"\\b{var}\\b", line):
                    yield i
