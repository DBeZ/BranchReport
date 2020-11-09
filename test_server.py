import pandas as pd
import numpy as np
import datetime as dt
import dateutil.rrule as rrule
import dateutil.relativedelta as relativedelta
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, FormatStrFormatter, MultipleLocator
import matplotlib.colors as mcolors
import seaborn as sns
import yagmail

string_test="test test test"

f = open("test_server.txt", "w")
f.write(string_test)
f.close()

