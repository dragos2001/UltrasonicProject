import matplotlib.pyplot as plt
import pandas as pd
def plot_signal (timestamps,values,title="plot",color='blue'):
        fig = plt.figure(figsize=(10,8), layout="constrained")
        fig.suptitle(title)
        ax = fig.add_subplot()
        ax.plot(timestamps, values, color = color)
        #plt.show()
        return ax

