import re

class SyntaxRule:
  def __init__(self, candidate_rule):
    def string_repl_table_convert(repl_table, modif_string):
      for k, v in repl_table:
        modif_string = re.sub(k, v, modif_string, 0, re.IGNORECASE)
      return modif_string
    match_str = '\s*\((.*)\)\s*AND\s*!\s*\((.*)\)\s*'
#    from_plain_text_repl_tbl = [('\(', 'U+0028'), ('\)', 'U+0029'), ('"', 'U+0022'), ("'", 'U+0027'), ('!', 'U+0021')]
    to_plain_text_repl_tbl = [('U\+0028', '('), ('U\+0029', ')'), ('U\+0022', '"'), ('U\+0027', "'"), ('U\+0021', '!')]
    part_piece_repl_tbl = [('\s+', ' '), ('"', ''), ('^\s', ''), ('\s$', '')]
    if re.match(match_str, candidate_rule, re.IGNORECASE) is not None:
      positive_pieces = []
      negative_pieces = []
      parts = re.findall(match_str, candidate_rule, re.IGNORECASE)
      positive_parts = re.split('"\s*OR\s*"', parts[0][0], 0, re.IGNORECASE)
      negative_parts = re.split('"\s*OR\s*"', parts[0][1], 0, re.IGNORECASE)
      for i in range(len(positive_parts)):
        candidate_string = string_repl_table_convert(part_piece_repl_tbl, positive_parts[i])
        candidate_string = string_repl_table_convert(to_plain_text_repl_tbl, candidate_string)
        if len(candidate_string) > 0:
          positive_pieces.append(candidate_string.lower())
      for i in range(len(negative_parts)):
        candidate_string = string_repl_table_convert(part_piece_repl_tbl, negative_parts[i])
        candidate_string = string_repl_table_convert(to_plain_text_repl_tbl, candidate_string)
        if len(candidate_string) > 0:
          negative_pieces.append(candidate_string.lower())
      self.positive = positive_pieces
      self.negative = negative_pieces
      self.status = 'valid'
    else:
      self.positive = []
      self.negative = []
      self.status = 'invalid'

# ----------------------------------
  def found_occurrences(self, text):
    test_result = None
    if (self.status == 'valid' and len(text) > 0):
      for current_piece in self.negative:
        pattern_words = re.split('\s', current_piece)
        occurrences = 0
        for i in pattern_words:
          if re.search(i, text, re.IGNORECASE) is not None:
            occurrences = occurrences + 1
        if occurrences == len(pattern_words):
          test_result = False
          break
      if test_result is None:
        test_result = True
        if len(self.positive) > 0:
          test_result = False
          for current_piece in self.positive:
            pattern_words = re.split('\s', current_piece)
            occurrences = 0
            for i in pattern_words:
              if re.search(i, text, re.IGNORECASE) is not None:
                occurrences = occurrences + 1
            if occurrences == len(pattern_words):
              test_result = True
              break
    return test_result
