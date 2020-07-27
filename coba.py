# -*- coding: utf-8 -*-
"""
Created on Fri Jul 17 11:28:42 2020

@author: RVM18
"""

import pandas as pd

presidents = ["Washington", "Adams", "Jefferson", "Madison", "Monroe", "Adams", "Jackson"]
for i in range(len(presidents)):
    print("President {}: {}".format(i + 1, presidents[i]))

presidents = ["Washington", "Adams", "Jefferson", "Madison", "Monroe", "Adams", "Jackson"]
for num, name in enumerate(presidents, start=1):
    print("President {}: {}".format(num, name))


t = 20190530
pd.to_datetime(str(t), format='%Y%m%d')
print(t)