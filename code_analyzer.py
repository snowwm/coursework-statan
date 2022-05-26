from collections import defaultdict
import re

# Typical dark magic. May be dangerous for your brain.
# The percent sign is to be substituted for the variable's name.
VAR_WRITE_RE = r"((&|>>\s*)%\b|\b%\s*=[^=])"
VAR_READ_RE = r"[^&]\b%\b(?!\s*=[^=])"
VAR_RW_RE = r"((\+\+|--)%\b|\b%(\+\+|--|\s*[-+*/|&^]=))"
VAR_STREAM_RE = r"\b%\s*(<<|>>)"

VAR_DECL_RE = re.compile(r"([a-zA-Z_][a-zA-Z_0-9<*&]*) (.*);")
VAR_DECL_PART_RE = re.compile(r"([*&]*)([a-zA-Z_][a-zA-Z_0-9]*)(\[*)[= ]*(.*?)(, |$)")

BRACKET_PAIRS = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}


class CodeAnalyzer:
    detectors = dict()

    @staticmethod
    def register(detector):
        CodeAnalyzer.detectors[detector.__name__] = detector

    @staticmethod
    def find_vulns(source, vuln_code):
        errors = CodeAnalyzer.detectors[vuln_code](source)
        return sorted(set(errors))
    
    @staticmethod
    def var_usage_mode(var, code):
        res = set()
        if re.search(VAR_RW_RE.replace("%", var), code):
            res.add("r")
            res.add("w")
        if re.search(VAR_READ_RE.replace("%", var), code):
            res.add("r")
        if re.search(VAR_WRITE_RE.replace("%", var), code):
            res.add("w")
        if re.search(VAR_STREAM_RE.replace("%", var), code):
            res.add("s")
        return res
    
    @staticmethod
    def var_declarations(line):
        l, s = CodeAnalyzer.preprocess_line(line)
        m = VAR_DECL_RE.fullmatch(s)
        
        if not m or m[1] in ("return", "using", "new", "delete"):
            return
        
        common_type = m[1]
        s = m[2]
        start, end = m.span(2)
        l = l[start:end]
        pos = 0

        while pos < len(s):
            m = VAR_DECL_PART_RE.match(s, pos)
            if not m:
                return
            pos = m.end()
            d = VarDecl()
            
            start, end = m.span(1)
            d.type = common_type + l[start:end]
            
            start, end = m.span(2)
            d.name = l[start:end]
            
            start, end = m.span(3)
            d.arr = l[start:end]
            
            start, end = m.span(4)
            d.value = l[start:end]
            
            yield d
             
    @staticmethod       
    def preprocess_line(line):
        line = line.strip()
        l = ""  # line with whitespace collapsed and comments removed
        s = ""  # high-level structure of the line
        brs = ["a"]  # bracket stack
        prevc = "a"
        
        for c in line:
            mode = "take"
            br = brs[-1]
            brpop = None
            
            if br == "*":
                if prevc + c == "*/":
                    brs.pop()
                mode = "throw"
            
            elif br in "\"\'":
                if c == br and prevc != "\\":
                    brpop = brs.pop()
                elif c == "\\" and prevc == "\\":
                    c = "a"  # escaped slash is not a slash
                
            elif prevc + c in ("//", "/*"):
                mode = "throw2"
                brs.append("*")
                
            elif c in "([{\"\'" or (c == "<" and prevc.isalnum()):
                brs.append(c)
                
            elif c == BRACKET_PAIRS.get(br):
                brpop = brs.pop()
                
            elif c.isspace():
                mode = "space"
                
            if mode == "throw":
                pass
            elif mode == "throw2":
                l = l[:-1]
                s = s[:-1]
                if c == "/":
                    break
            elif mode == "space" and s and s[-1] == " ":
                pass
            else:
                l += c
                s += brs[1] if len(brs) > 1 else (brpop or c)
                
            prevc = c
            
        # if line:
            # print(line)
            # print(l)
            # print(s)
            # print()
            
        return l.strip(), s.strip()


class VarDecl:                                                      
    type: str = None
    name: str = None
    arr: str = None
    value: str = None
    
    def is_pointer(self):
        # type ends with * or *&
        return re.search(r"\*&?$", self.type) is not None
