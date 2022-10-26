import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


xs = []
ys = []
av_freq = 0
quant_step = 0

with open("settings.txt", "r") as f:
    av_freq, quant_step = tuple(float(item) for item in f.readlines())

ys = np.loadtxt("data.txt", dtype = int) * quant_step
xs = np.arange(0, len(ys)) / av_freq
tmax = np.argmax(ys) / av_freq
tmin = len(ys) / av_freq - tmax
fig, ax = plt.subplots(figsize=(8,5), dpi=100)
ax.plot(xs, ys, '-bo', markevery=300, color='r',linewidth=1)
ax.set_title("Процесс зарядки и разрядки конденсатора", loc="center")

ax.set_xlim(0, 80)
ax.set_ylim(0, 3.5)

ax.set_xlabel("Время, с")
ax.set_ylabel("Напряжение, В")
ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.1))
ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
ax.grid(which='major')
ax.grid(which="minor", ls='--', linewidth=0.3)
ax.legend(["V(t)"])
plt.text(55, 2, 'Время заряда = ' + '{:.2f}'.format(tmax) + ' c')
plt.text(55, 1.5, 'Время разряда = ' + '{:.2f}'.format(tmin) + ' c')

plt.savefig("RC_graph.svg")
plt.show()