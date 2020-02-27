
def split_tweet(str_tweet):
    halves=[]
    l = str_tweet.split()

    s1 = ' '.join(l[:len(l) // 2]) + " [1/2]"
    s2 = "[2/2] " + ' '.join(l[len(l) // 2:])
    halves.append(s1)
    halves.append(s2)
    return halves
