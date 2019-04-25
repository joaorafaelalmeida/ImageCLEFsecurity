
def isJPG(file):
	score = 0
	size = len(file)

	#weight of each rule
	rules_weight = {}
	rules_weight['file_terminator'] = 0.5
	rules_weight['JFIF'] = 0.5

	#check end of file
	expected_last_bytes = b'ffd9'
	last_bytes = file[size - 4 : size]
	if expected_last_bytes == last_bytes :
		score = score + 1 * rules_weight['file_terminator']
    
	#search for JFIF
	expected_last_bytes = b'4a464946'
	last_bytes = file[12 : 20]
	if expected_last_bytes == last_bytes :
		score = score + 1 * rules_weight['JFIF']

	return score