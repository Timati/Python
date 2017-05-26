
import pywt
import numpy as np
import scipy.io.wavfile as wavfile
import matplotlib.pyplot as plt
import sys
import csv

rate,signal = wavfile.read(sys.argv[1])
time = [x /rate for x in range(0, len(signal))]
tree = pywt.wavedec(data=signal, wavelet='db2', level=5, mode='symmetric')
newTree = [tree[0], tree[1], tree[2], tree[3]*0, tree[4]*0, tree[5]*0]
recSignal = pywt.waverec(newTree, 'db2')

fig, ax = plt.subplots(2, 1)
ax[0].plot(time[0:1000], signal[0:1000])
ax[0].set_xlabel('Czas [s]')
ax[0].set_ylabel('Amplituda')

ax[1].plot(time[0:1000], recSignal[0:1000])
ax[1].set_xlabel('Czas [s]')
ax[1].set_ylabel('Amplituda')
plt.show()

peaks = []
peaks_2 = []
step = 0.27*rate
#n = len(recSignal)
for i in range(1,len(signal)-2):
    if recSignal[i] > recSignal[i+1] and recSignal[i] > recSignal[i - 1]:
        if len(peaks) == 0 or (i - peaks[-1]) > step:
            peaks.append(i)
            peaks_2.append(i/rate)
        elif recSignal[i] > recSignal[peaks[-1]]:
            peaks[-1] = i
            peaks_2[-1] = i/rate

print(peaks)
print(peaks_2)

# for i, element in enumerate(peaks_s, 1):
#   print('{} {}'.format(i, element))

for i, element in enumerate(peaks_2[::2], 1):
    print('{} {}'.format(i, element))
#Wyznaczanie tonów
peaks1 = []
peaks_ton1 = []
peaks_ton2 = []
iterator =0
for i in range(0,len(peaks)):
    if (i%2 == 1):
        iterator = iterator+1
        peaks_ton1.append(peaks_2[i])
        peaks1.append(peaks_2[i])
    else:
        peaks_ton2.append(peaks_2[i])

bpm = []
for i in range(1,len(peaks_ton1)):
        bpm.append(round(60 / (peaks_ton1[i] - peaks_ton1[i -1]),2))
print(bpm)

print(sum(bpm)/43)
for j, element in enumerate(bpm, 1):
    print('{} {}'.format(j,element))

    peaks_new = []
    if len(peaks_ton1)>len(bpm):
        max_len=len(bpm)
    else:
        max_len=len(peaks_ton1)
    for i in range(1,max_len):
        try:
            peaks_new.append((i, bpm[i-1]))
        except IndexError:
            break
name_file = sys.argv[2]
with open(name_file, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', lineterminator='\n')
        for line in peaks_new:
            spamwriter.writerow(line)