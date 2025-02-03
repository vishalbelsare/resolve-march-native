# Copyright (C) 2015 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

def flags_sort_key(text):
    if text.startswith('-march='):
        return (0, text)  # March goes first
    if text.startswith('-mcpu='):
        return (0.1, text)
    if text.startswith('-mtune='):
        return (0.5, text)
    elif text.startswith('--param'):
        return (2, text)
    elif text.startswith('-O'):
        return (3, text)
    elif text == '-pipe':
        return (4, text)
    else:
        return (1, text)
