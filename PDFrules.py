def isPDF(file):
    size = len(file)

    expected_last_bytes = b'0a'
    last_bytes = file[size - 2 : size]

    if expected_last_bytes == last_bytes :
        return 1
    
    return 0