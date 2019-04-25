def isPDF(file):
    size = len(file)

    expected_last_bytes = b'2525454f460a'
    last_bytes = file[size - 12 : size]

    if expected_last_bytes == last_bytes :
        return 1
    
    return 0