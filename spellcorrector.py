#53% correct

import re, math, random

def words(text): return re.findall(r'\w+', text.lower())

from collections import Counter

#read all the words in words.txt and count their occurrences
#WORDS maps a word to their number of occurrences in words.txt
WORDS = Counter(words(open('words.txt').read()))

def probability_of_word_given_candidate(word, candidate, candidate_edit_dist):
    ########### ADD YOUR CODE TO THIS METHOD ###########
    #c: candidate
    #w: word  (possibly misspelled)
    # You want to return an estimate of P(c|w) in this method.
    # By Bayes' rule, P(c|w) = P(w|c) P(c) / P(w)
    # When comparing multiple candidates for each word, P(w)
    # remains the same for every candidate, hence we can ignore
    # it. For example in
    # P(c|w)  = P(w|c) P(c) / P(w) and
    # P(c'|w) = P(w|c') P(c') / P(w),
    # we only need to consider the P(w|c)P(c) and P(w|c')P(c') terms
    # on the right hand side to decide which of P(c|w) and P(c'|w)
    # is larger. (The comparison will be done by the correction() method.)

    # The candidate_edit_dist parameter is a distance measure between
    # word and candidate. The larger the distance, the greater the difference
    # between word and candidate. In fact, it has been noted 
    # that the distance follows an exponential distribution with the mean of 10.
    # You may wish to use it to compute P(w|c)

    # Think about how to compute P(w|c) and P(c). You may use some or all of the
    # parameters of this method.

    # Write code to compute P(w|c) P(c) and return it.R

    #get number of potential candidates
    num_of_instances_of_word = WORDS[candidate]
    dist_to_candidates_map = candidates(word)
    number_of_candidates_occurance = 0
    c = 0

    if 1 not in dist_to_candidates_map:
        if 2 not in dist_to_candidates_map:
            pass
        else:
            list = dist_to_candidates_map[2]
            for word in list:
                number_of_candidates_occurance += WORDS[word]
    else:
        list = dist_to_candidates_map[1]
        for word in list:
            number_of_candidates_occurance += WORDS[word]

    if number_of_candidates_occurance == 0:
        pass
    else:
        c = num_of_instances_of_word / number_of_candidates_occurance
    return c

def correction(word):
    '''Most probable spelling correction for word.'''
    dist_to_candidates_map = candidates(word) #takes a word and returns a dictionary of lists of words that are potentially that word
    maxProb = 0
    maxCandidate = ''
    for candidate_edit_dist, cands in dist_to_candidates_map.items():
        for cand in cands:
            p = probability_of_word_given_candidate(word, cand, candidate_edit_dist)
            #get the probability of the candidate word being the actual word
            if p > maxProb:
                maxProb = p
                maxCandidate = cand
    return maxCandidate


def candidates(word): 
    '''Generate possible spelling corrections for word.'''
    # known words that are edit distance 1 and 2 from given word
    dist_to_candidates_map = {}

    e1_words    = edits1(word)
    e2_words = set(e for w in e1_words for e in edits1(w))
    #e3_words = set(e for w in e2_words for e in edits1(w))

    dist1_words = known( e1_words )
    dist2_words = known( e2_words )
    #dist3_words = known( e3_words )

    dist2_words = dist2_words - (dist1_words & dist2_words)
    #dist3_words = dist3_words - (dist1_words & dist3_words)
    #dist3_words = dist3_words - (dist2_words & dist3_words)

    if len(dist1_words) != 0: dist_to_candidates_map[1] = dist1_words
    if len(dist2_words) != 0: dist_to_candidates_map[2] = dist2_words
    #if len(dist2_words) != 0: dist_to_candidates_map[3] = dist3_words
    if len(dist_to_candidates_map) == 0: dist_to_candidates_map[0] = {word}

    return dist_to_candidates_map


def known(words): 
    '''The subset of `words` that appear in the dictionary of WORDS.'''
    return set(w for w in words if w in WORDS)

def edits1(word):
    '''All edits that are one edit away from `word`.'''
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def test(tests, verbose=False):
    '''Run correction(wrong) on all (right, wrong) pairs; report results.'''
    import time
    start = time.process_time() #time.clock()
    good, unknown = 0, 0
    n = len(tests)
    for right, wrong in tests:
        w = correction(wrong)
        #take the wrong word and return the most probable word
        good += (w == right)
        if w != right:
            unknown += (right not in WORDS)
            if verbose:
                print('WRONG correction({}) => {} ({}); expected {} ({})'
                      .format(wrong, w, WORDS[w], right, WORDS[right]))
        else:
            if verbose:
                print('RIGHT correction({}) => {} ({})'
                      .format(wrong, w, WORDS[w]))
    dt = time.process_time() - start #time.clock() - start
    print('{:.0%} of {} correct ({:.0%} unknown) at {:.0f} words per second '
          .format(good / n, n, unknown / n, n / dt))
    
def testset(lines):
    '''Parse 'right: wrong1 wrong2' lines into [('right', 'wrong1'), ('right', 'wrong2')] pairs.'''
    return [(right, wrong)
            for (right, wrongs) in (line.split(':') for line in lines)
            for wrong in wrongs.split()]

'''reads the testwords.txt file'''
if __name__ == '__main__':
    test(testset(open('testwords.txt')), True)