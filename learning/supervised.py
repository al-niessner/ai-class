"""Implements some learning algorithms
"""

"""Definition of a bag:
     'all'        : count of all unique words in all bags
     'count'      : number of message in this bag
     'sum'        : total number of words that have passed through this bag
     'vocabulary' : words in this bag
"""
from collections import namedtuple
Bag = namedtuple('Bag','all count sum vocabulary')

def naiveBayes (message, bags, smoothing=1):
    """A simple bag of words with a naive bayes network to select between bags.

    The algorithm is a very simple naive-bayes network to learn how to
    catergorize messages between several options. Given a collection of bags
    of words, compute the probability that the given message belongs into any
    of the given bags in the collection.

    message   : a string of characters representing the unknown message
    bags      : a collection of bags-of-words
    smoothing : the Laplacian smoother and when 0 the computation becomes
                maximum likelihood

    return P(A|message) where A is every name in the bag
    """
    k = float(smoothing)
    P = {}
    total = 0.0
    for bag in bags.values(): total += bag.count
    for w in message.lower().split():
        if 0 < len (w):
            for name,bag in bags.iteritems():
                p = (bag.vocabulary.get (w, 0) + k) / (bag.sum + k * bag.all)
                P[name] = P.get (name, bag.count/total) * p
                pass
            pass
        pass
    total = 0.0
    for p in P.values(): total += p
    for name in P.keys(): P[name] = P[name]/total
    return P

def updateBags (bags, name, message):
    """Training algorithm for the naive bayes network.

    Given a collection of bags, a bag name, and a message, then learn.

    bags    : a collection of bags-of-words
    name    : the name of the bag that the given message belongs to
    message : a string of characters
    """
    # create a collection of bags if it does not yet exist
    if bags is None: bags = {}
    
    # make sure the collection is consistent
    all = 0
    if 0 < len (bags):
        all = bags[bags.keys()[0]].all
        for bag in bags.values():
            if all != bag.all: raise ValueError("Bags is inconsistent. Not all of the 'all' values are the same!")
            pass
        pass

    # modify the bag that we care about
    count = 0
    thisbag = Bag(all,0,0,{}) if name not in bags else bags[name]
    for w in message.lower().split():
        count += 1
        unknown = True
        for bag in bags.values(): unknown &= w not in bag.vocabulary

        if unknown: all += 1

        if w in thisbag.vocabulary: thisbag.vocabulary[w] += 1
        else: thisbag.vocabulary[w] = 1
        pass

    # adjust all of the items in the bag if new words have been learned
    if 0 < len (bags):
        if all != bags[bags.keys()[0]]:
            for key in bags.keys(): bags[key] = Bag(all,
                                                    bags[key].count,
                                                    bags[key].sum,
                                                    bags[key].vocabulary)
            pass
        pass

    # insert the new bag
    bags[name] = Bag(all,
                     thisbag.count+1,
                     thisbag.sum+count,
                     thisbag.vocabulary)
    return bags
