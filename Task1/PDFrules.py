def isPDF(file): 
    size = len(file)
    score = 0

    #weight of each rule
    rules_weight = {}
    rules_weight['EOF'] = 1

    #search for EOL
    expected_last_bytes = b'454f46'
    last_bytes = file[size - 20 : size]
    if last_bytes.find(expected_last_bytes) > -1 :
        score = score + 1 * rules_weight['EOF']
    
    return score