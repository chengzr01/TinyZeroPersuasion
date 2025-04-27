import re
import random
import ast
import operator

def compute_score(solution_str, ground_truth, method="strict", format_score=0.1, score=1.):
    """
    The scoring function for persuasion task.
    """
    return score