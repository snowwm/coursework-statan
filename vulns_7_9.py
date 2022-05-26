import re

from code_analyzer import CodeAnalyzer


@CodeAnalyzer.register
def bad_file_access(source):
    error = []
    safe_functions = ['access']
    files = []
    for i in range(len(source)):
        if ('fopen' in source[i]) or ('.open' in source[i]):
            char_name = source[i].split('(')[1]
            char_name = char_name.split(')')[0]
            char_name = char_name.split(',')[0]
            if char_name != "":
                files.append(char_name)
            for num in range(i - 10, i):
                if num in range(len(source)):
                    for func in safe_functions:
                        if source[num].find(func) != -1 and source[num].find(char_name) != -1:
                            if char_name in files:
                                files.remove(char_name)
    for file in files:
        for j in range(len(source)):
            if file in source[j] and ('fopen(' in source[j] or '.open(' in source[j]):
                error.append(j)
    return error


@CodeAnalyzer.register
def null_pointer_derefence(source):
    pointers = set()
    safe_pointers = set()

    for i, line in enumerate(source):
        decls = list(CodeAnalyzer.var_declarations(line))
        if decls:
            for d in decls:
                if d.is_pointer():
                    pointers.add(d.name)
        else:
            if "if (" in line:
                for ptr in pointers:
                    if re.search(f"\\b{ptr}\\b", line):
                        safe_pointers.add(ptr)
            else:
                for ptr in pointers:
                    if re.search(f"\\*{ptr}\\b|\\b{ptr}->", line):
                        yield i


@CodeAnalyzer.register
def number_overflow(source):
    def toInt(num, numbermas, numvalmas):
        if num in numbermas:
            out = numvalmas[numbermas.index(num)]
        else:
            try:
                out = int(num)
            except Exception:
                out = -1
        return out

    def scissors(line, numbermas, numvalmas):
        tmp = toInt(line, numbermas, numvalmas)
        if tmp != -1:
            return tmp
        else:
            if ' + ' in line:
                f = scissors(line.split("+", 1)[0].strip(), numbermas, numvalmas)
                s = scissors(line.split("+", 1)[1].strip(), numbermas, numvalmas)
                return f + s
            elif ' - ' in line:
                f = scissors(line.split("-", 1)[0].strip(), numbermas, numvalmas)
                s = scissors(line.split("-", 1)[1].strip(), numbermas, numvalmas)
                return f - s
            elif ' * ' in line:
                f = scissors(line.split("*", 1)[0].strip(), numbermas, numvalmas)
                s = scissors(line.split("*", 1)[1].strip(), numbermas, numvalmas)
                return f * s
            elif ' / ' in line:
                f = scissors(line.split("/", 1)[0].strip(), numbermas, numvalmas)
                s = scissors(line.split("/", 1)[1].strip(), numbermas, numvalmas)
                return f // s
            else:
                return -1

    error = []
    # warnings = []
    numbers = []
    numervalues = []
    numberplaces = []
    int_max_val = 2147483647
    source = source[:]
    for i in range(len(source)):
        if 'int ' in source[i]:
            if 'main' not in source[i] and 'for' not in source[i] and ' ' in source[i]:
                newint = 'error!'
                startval = -1
                if '=' not in source[i]:
                    newint = source[i].replace('int ', '', 1).split(';')[0].strip()
                    startval = 0
                else:
                    newint = source[i].replace('int ', '', 1).split('=')[0].strip()
                    startval = scissors(source[i].split("=")[1].split(";")[0].strip(), numbers, numervalues)
                    source[i] = source[i].replace('=', '', 1)
                numbers.append(newint)
                numberplaces.append(i)
                numervalues.append(startval)
            elif 'for ' in source[i]:
                znak = source[i].split(";")[1]
                if ('>' in znak) and ('++' or '+=' in source[i]):
                    if '*=' in source[i]:
                        a = toInt(source[i].split(";")[0].split('=')[1].strip(), numbers, numervalues)
                        b = toInt(source[i].split(";")[1].split('>')[1].strip(), numbers, numervalues)
                        mnozh = source[i].split(";")[2].split('*=')[1].split(')')[0].strip()
                        mnozh2 = toInt(mnozh, numbers, numervalues)
                        if mnozh2 == -1:
                            mnozh = float(mnozh)
                        else:
                            mnozh = mnozh2
                        if a > b and mnozh > 1:
                            error.append(i)
                    elif '+=':
                        a = toInt(source[i].split(";")[0].split('=')[1].strip(), numbers, numervalues)
                        b = toInt(source[i].split(";")[1].split('>')[1].strip(), numbers, numervalues)
                        if a > b:
                            error.append(i)
                elif '<' in znak:
                    a = toInt(source[i].split(";")[0].split('=')[1].strip(), numbers, numervalues)
                    b = toInt(source[i].split(";")[1].split('<')[1].strip(), numbers, numervalues)
                    if a < b and '--' in source[i]:
                        error.append(i)
    for i in range(len(source)):
        for inta in numbers:
            if (inta + ' ' in source[i]) and (source[i].find(inta) < source[i].find('=')):
                if ' += ' in source[i]:
                    addval = scissors(source[i].split("=")[1].split(";")[0].strip(), numbers, numervalues)
                    numervalues[numbers.index(inta)] += addval
                elif ' -= ' in source[i]:
                    addval = scissors(source[i].split("=")[1].split(";")[0].strip(), numbers, numervalues)
                    numervalues[numbers.index(inta)] -= addval
                elif ' = ' in source[i]:
                    numervalues[numbers.index(inta)] = scissors(source[i].split("=")[1].split(";")[0].strip(),
                                                                numbers, numervalues)
                elif ' *= ' in source[i]:
                    addval = scissors(source[i].split("=")[1].split(";")[0].strip(), numbers, numervalues)
                    numervalues[numbers.index(inta)] *= addval
                elif ' /= ' in source[i]:
                    addval = scissors(source[i].split("=")[1].split(";")[0].strip(), numbers, numervalues)
                    numervalues[numbers.index(inta)] /= addval
    for i in range(len(numbers)):
        if abs(numervalues[i]) > int_max_val:
            error.append(numberplaces[i])
    return error
