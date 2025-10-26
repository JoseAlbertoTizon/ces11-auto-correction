import re

def convert_special_caracters(string):
    # Replace common special/accented characters with ASCII equivalents.
    replacements = {
        'ç': 'c',
        'Ç': 'C',
        'ã': 'a',
        'Ã': 'A',
        'á': 'a',
        'Á': 'A',
        'à': 'a',
        'À': 'A',
        'â': 'a',
        'Â': 'A',
        'é': 'e',
        'É': 'E',
        'ê': 'e',
        'Ê': 'E',
        'í': 'i',
        'Í': 'I',
        'ó': 'o',
        'Ó': 'O',
        'õ': 'o',
        'Õ': 'O',
        'ô': 'o',
        'Ô': 'O',
        'ú': 'u',
        'Ú': 'U',
        'ü': 'u',
        'Ü': 'U',
    }
    
    for orig, repl in replacements.items():
        string = string.replace(orig, repl)
    return string

def make_regex_to_match_string(string):
    return re.escape(string)

def get_lines_that_matches_any_regex(text_as_str_list, pattern_list, ignorecase=True, return_first_match_only=True):
    ignorecase_flag = re.IGNORECASE if ignorecase else 0
    matches = []
    for line in text_as_str_list:
        for regex in pattern_list:
            match = re.search(regex, line, ignorecase_flag)
            if match:
                if return_first_match_only:
                    return line
                matches.append(line)
    if not matches:
        return None if return_first_match_only else []
    return matches

def get_substrings_that_matches_any_regex(string, pattern_list, ignorecase=True, return_first_match_only=True):
    ignorecase_flag = re.IGNORECASE if ignorecase else 0
    matches = []
    for regex in pattern_list:
        match = re.search(regex, string, ignorecase_flag)
        if match:
            if return_first_match_only:
                return match.group()
            matches.append(match.group())
    if not matches:
        return None if return_first_match_only else []
    return matches

def get_first_match_in_first_matching_line(lines, line_pattern_list, value_pattern_list):
    line = get_lines_that_matches_any_regex(lines, line_pattern_list, ignorecase=True, return_first_match_only=True)
    if not line:
        return None
    value = get_substrings_that_matches_any_regex(line, value_pattern_list, ignorecase=True, return_first_match_only=True)
    return value

def get_first_matches_in_many_matching_lines(lines, line_pattern_list, value_pattern_list):
    lines = get_lines_that_matches_any_regex(lines, line_pattern_list, ignorecase=True, return_first_match_only=False)
    if not lines:
        return []
    values = []
    for line in lines:  
        match = get_substrings_that_matches_any_regex(line, value_pattern_list, ignorecase=True, return_first_match_only=True)
        # If student skips lines, there will be None values
        if match is not None:
            values.append(match)

    return values

def read_file_lines(path):
    try:
        with open(path, encoding='utf-8') as f:
            return [convert_special_caracters(line) for line in f.readlines()]
    except UnicodeDecodeError:
        with open(path, encoding='latin1') as f:
            return [convert_special_caracters(line) for line in f.readlines()]