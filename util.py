def substitute_str_idx(s: str, r: str, i: int) -> str:
    """Substitute char at position

   Arguments:
      s: The str in which to substitute
      r: The char to substitute
      i: index of the substitution

   Returns:
      The string `s` with the i'th char substitute with `r`
   """
    z = ''.join([(lambda: r, lambda: x)[idx != i]() for idx, x in enumerate(s)])
    return z
