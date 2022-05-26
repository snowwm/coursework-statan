from collections import defaultdict
import re

from code_analyzer import CodeAnalyzer

FUNC_START_RE = re.compile(r"[a-zA-Z_][a-zA-Z_0-9]* ([a-zA-Z_][a-zA-Z_0-9]*)\s*\(.*\) {")
THREAD_CREATE_RE = re.compile(r"(?:pthread_create|CreateThread)\([^,]+, [^,]+, &?([a-zA-Z_][a-zA-Z_0-9]*)")
MUTEX_LOCK_RE = re.compile(r"pthread_mutex_lock\(|WaitForSingleObject\(")


@CodeAnalyzer.register
def race_condition(source):
    cur_func = None
    cur_indent = None
    has_mutex = False
    threads = set()
    threads.add("main")
    global_vars = set()
    local_vars = set()
    var_usage = defaultdict(set)
    
    for ln, line in enumerate(source):
        line = line.partition("//")[0]
        indent = len(line) - len(line.lstrip())
        line = line.strip()
        
        if m := FUNC_START_RE.fullmatch(line):
            cur_func = m[1]
            cur_indent = indent
            local_vars = set()
        elif line == "}" and indent == cur_indent:
            # func end
            cur_func = cur_indent = None
            has_mutex = False
        elif MUTEX_LOCK_RE.search(line):
            has_mutex = True
        elif m := THREAD_CREATE_RE.search(line):
            threads.add(m[1])
        elif cur_func is None:
            for d in CodeAnalyzer.var_declarations(line):
                global_vars.add(d.name)
        else:
            for d in CodeAnalyzer.var_declarations(line):
                local_vars.add(d.name)

            for var in global_vars:
                if var not in local_vars:
                    if CodeAnalyzer.var_usage_mode(var, line) and not has_mutex:
                        var_usage[var].add((ln, cur_func))
            
    var_threads = defaultdict(set)
    for var, usages in var_usage.items():
        for ln, func in usages:
            if func in threads:
                var_threads[var].add(func)

    for var, usages in var_usage.items():
        if len(var_threads[var]) > 1:
            for ln, func in usages:
                if func in threads:
                    yield ln


@CodeAnalyzer.register
def incorr_rw_sync(source):
    cur_func = None
    cur_indent = None
    has_mutex = False
    threads = set()
    fstreams = set()
    maybe_errors = list()
    
    for ln, line in enumerate(source):
        line = line.partition("//")[0]
        indent = len(line) - len(line.lstrip())
        line = line.strip()
        
        if m := FUNC_START_RE.fullmatch(line):
            cur_func = m[1]
            cur_indent = indent
        elif line == "}" and indent == cur_indent:
            # func end
            cur_func = cur_indent = None
            has_mutex = False
        elif MUTEX_LOCK_RE.search(line):
            has_mutex = True
        elif m := THREAD_CREATE_RE.search(line):
            threads.add(m[1])
        else:
            for d in CodeAnalyzer.var_declarations(line):
                if d.type in ("ifstream", "ofstream"):
                    fstreams.add(d.name)

            for s in fstreams:
                if "s" in CodeAnalyzer.var_usage_mode(s, line):
                    if not has_mutex:
                        maybe_errors.append((ln, cur_func))
            
    for ln, func in maybe_errors:
        if func in threads:
            yield ln


@CodeAnalyzer.register
def uninit_var(source):
    uninit_vars = set()
    
    for ln, line in enumerate(source):
        decls = list(CodeAnalyzer.var_declarations(line))
        if decls:
            for d in decls:
                if not d.value and not d.arr:
                    uninit_vars.add(d.name)
                else:
                    uninit_vars.discard(d.name)
        else:
            for var in list(uninit_vars):
                usage = CodeAnalyzer.var_usage_mode(var, line)
                if "r" in usage:
                    yield ln
                if "w" in usage:
                    uninit_vars.remove(var)
