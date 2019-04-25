def isPNG(file):
    size = len(file)

    expected_last_bytes = b'49454e44ae426082'
    last_bytes = file[size - 16 : size]

    if expected_last_bytes == last_bytes :
        return 1
    
    return 0