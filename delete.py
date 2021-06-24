try:
    raise ValueError
except (IndexError, ValueError )as e:
    print('oh no')