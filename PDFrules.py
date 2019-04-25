def isPDF(file): 
    size = len(file)
    score = 0

    #weight of each rule
    rules_weight = {}
    rules_weight['file_terminator'] = 0.5
    rules_weight['EOL'] = 0.5

    #search for EOL
    expected_last_bytes = b'454f46'
    last_bytes = file[size - 10 : size]
    if last_bytes.find(expected_last_bytes) > -1 :
        score = score + 1 * rules_weight['EOL']

    #file terminator
    expected_last_bytes = b'0a'
    last_bytes = file[size - 12 : size]
    if expected_last_bytes == last_bytes :
        score = score + 1 * rules_weight['file_terminator']
    

    return score