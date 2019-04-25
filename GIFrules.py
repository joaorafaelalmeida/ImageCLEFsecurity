def isGIF(file):
    size = len(file)
    score = 0

    #weight of each rule
    rules_weight = {}
    rules_weight['file_terminator'] = 1

    #terminator
    expected_last_bytes = b'3b'
    last_bytes = file[size - 2 : size]
    if expected_last_bytes == last_bytes :
        score = score + 1 * rules_weight['file_terminator']
    
    return score