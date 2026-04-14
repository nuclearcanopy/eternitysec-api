import string
import math

def strength(password: string):
    if password == '':
        return {
            "entropy": 0,
            "crack_time": "less than a second"
        }


    guesses_per_second = 1000000000000 # 1 trillion guesses per second, arbitrary worst-case guess. this would only be realistic if a literal nation-state was targeting you, with multiple 5090s or such
    pool = 0

    if any(c in string.ascii_lowercase for c in password):
        pool += 26
    if any(c in string.ascii_uppercase for c in password):
        pool += 26
    if any(c in string.digits for c in password):
        pool += 10
    if any(c in string.punctuation for c in password):
        pool += 32

    entropy = len(password) * math.log2(pool)
    log2_crack_time = entropy - 1 - math.log2(guesses_per_second)

    if log2_crack_time >= 57:
        return {
            "entropy": entropy,
            "crack_time": "longer than the Sun's remaining lifespan"
        }
    

    crack_time = 2**log2_crack_time
    crack_time_human = 0
    # this could be simplified mathematically, i opted not to for clarity
    # / 2 because average crack time is at 1/2 of the way there. 

    times = [1, 60, 3600, 86400, 31536000, 315360000, 3153600000, 31536000000]    
    units = ["seconds", "minutes", "hours", "days", "years", "decades", "centuries", "millenniums"]

    for i in range (7, -1, -1):
        n = math.floor(crack_time/times[i])

        suffix = units[i]
 
        if n == 1 and i != 6:
            suffix = suffix[:-1]
        elif n == 1 and i == 6:
            suffix = "century"

        if n > 0:
            crack_time_human = str(n) + " " + suffix   
            break


    if crack_time_human == 0 or crack_time_human == "0 seconds":
        crack_time_human = "less than a second"

    return {
        "entropy": entropy,
        "crack_time": crack_time_human
    }
