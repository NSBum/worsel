import re
from util import substitute_str_idx


def compare_wordle(trial: str, target: str) -> (list, list):
    out_chars = [x for x in trial]
    out_colours = []
    done = False
    outcol = "*****"
    idx = 0
    while not done:
        # find greens
        for c in trial:
            if c == target[idx]:
                # positional match
                outcol = substitute_str_idx(outcol, 'g', idx)
                trial = substitute_str_idx(trial, '*', idx)
                target = substitute_str_idx(target, '*', idx)
            idx += 1
        idx = 0
        for c in trial:
            if c == '*':
                idx += 1
                continue
            if re.search(rf'{c}', target):
                # char is present still be incorrectly positioned
                outcol = substitute_str_idx(outcol, 'y', idx)
                trial = substitute_str_idx(trial, '*', idx)
                # find the first one in the target that it matched with
                target_idx = 0
                for ct in target:
                    if c == ct:
                        target = substitute_str_idx(target, '*', target_idx)
                        break
                    target_idx += 1
            else:
                outcol = substitute_str_idx(outcol, 'x', idx)
                trial = substitute_str_idx(trial, '*', idx)
            idx += 1
        if trial == '*****':
            done = True
    out_colours = [x for x in outcol]
    return out_chars, out_colours


class Trial(object):
    def __init__(self, t_id: int, word: str):
        self.gid = t_id
        self.word = word
