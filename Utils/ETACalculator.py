from datetime import datetime

import sys


def LogETA(processName:str, startTime:datetime, totalProcess:int, currentProcess:int)->str:
    try:
        percentage = currentProcess / totalProcess * 100
    except ZeroDivisionError:
        percentage = 0

    prettyPercentage = round(percentage, 1)

    now = datetime.now()
    elapsed = now - startTime

    try:
        eta = elapsed.seconds * 100/percentage
    except ZeroDivisionError:
        eta = 0
    prettyETA = datetime.fromtimestamp(eta).strftime('%H:%M:%S')

    message = "PROCESS: %s %f %% ETA: %s" % (processName, prettyPercentage, prettyETA)



    if percentage >= 100:
        message = "STATUS :: COMPLETE"
    return message
    #
    # sys.stdout.write(message)
    # sys.stdout.flush()
