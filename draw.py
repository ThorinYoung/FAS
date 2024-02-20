import matplotlib.pyplot as plt

plt.style.use('fivethirtyeight')

with open('d:/whitebox/checkpoint/FaceForensics++/logs.txt')as f:
    lines = f.readlines()
p = []
v = []
j = []
x = [i for i in range(1,101)]
for i in range(100):
    line = lines[i]
    a = line.strip().split(' | ')
    # print(a)
    p.append(eval(a[-3].split(': ')[-1]))
    v.append(eval(a[-2].split(': ')[-1]))
    j.append(eval(a[-1].split(': ')[-1][:-3]))

plt.subplot(131)
plt.plot(x, p, color='red', linestyle='solid', linewidth=1.5)
plt.title('Perceptual Loss', y=-0.2)
plt.subplots_adjust(bottom=0.2)
plt.subplot(132)
plt.plot(x, v, color='red', linestyle='solid', linewidth=1.5)
plt.title('Equivariance Loss', y=-0.2)
plt.subplots_adjust(bottom=0.2)

plt.subplot(133)
plt.plot(x, j, color='red', linestyle='solid', linewidth=1.5)
plt.title('Equivariance Jacobian', y=-0.2)
plt.subplots_adjust(bottom=0.2)

plt.show()
