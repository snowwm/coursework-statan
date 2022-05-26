from collections import defaultdict
import random

import test_lib


class TestGenerator:
    @staticmethod
    def gen_test(vuln_codes=None):
        blocks = defaultdict(list)  # functions/classes + global code
        blocks["global"].append(test_lib.preamble)
        prog = ""
        
        if vuln_codes is None:
            all_vuln_codes = test_lib.vuln_dict.keys()
            vuln_codes = random.sample(all_vuln_codes, random.randint(3, 12))
        
        # take one fragment for each vuln + some number of correct fragments
        fragments = [random.choice(test_lib.vuln_tests[vc]) for vc in vuln_codes]
        fragments += random.sample(test_lib.correct_fragments, random.randint(3, 10))
        
        # populate blocks with their fragments
        for f in fragments:
            # wrap simple fragments that consist of only one block
            if isinstance(f, str):
                f = {"int main()": f}
                
            for block_name, code in f.items():
                blocks[block_name].append(code)
                
        # make main() the last thing
        t = blocks.pop("int main()")
        blocks["int main()"] = t

        # add vulnerability headers      
        for vc in vuln_codes:
            prog += f"// !test {vc}\n"
        prog += "\n"
        
        # add global code
        glob = blocks.pop("global")
        prog += "".join(glob)
        
        for block_name, fragments in blocks.items():
            random.shuffle(fragments)
            # add indentation and strip extra newlines
            fragments = ["  " + f.strip().replace("\n", "\n  ") for f in fragments]

            prog += "\n" + block_name + " {\n"
            prog += "\n\n".join(fragments)
            prog += "\n}\n"
            
        return prog
