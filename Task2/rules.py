
def hasMessage(file) :
    size = len(file)
    score = 0

    #weight of each rule
    rules_weight = {}
    rules_weight['sequence_1'] = 0.5
    rules_weight['sequence_2'] = 0.5

    #sequence 1
    expected_last_bytes = b'3435363738393a434445464748494a535455565758595a636465666768696a737475767778797a'
    last_bytes = file[0 : 1260]
    if last_bytes.find(expected_last_bytes) > -1  :
        score = score + 1 * rules_weight['sequence_1']

    #sequence 2
    expected_last_bytes = b'35363738393a434445464748494a535455565758595a636465666768696a737475767778797a'
    last_bytes = file[0 : 1260]
    if last_bytes.find(expected_last_bytes) > -1  :
        score = score + 1 * rules_weight['sequence_2']

    print (score)
    
    return score