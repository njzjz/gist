# -*- coding:utf-8 -*-
import random

 # 以下比较函数，用于给生物的“环境适应性”排序


def compare(x, y):
    accu = 0
    # 逐个衡量与拟合点的差距，选出较优解
    for points in fitPoints:
        outputX = 0
        for k in range(len(x)):
            outputX += x[k]*points**k
        outputY = 0
        for k in range(len(y)):
            outputY += y[k]*points**k
        if abs(outputX - fitPoints[points]) < abs(outputY - fitPoints[points]):
            accu += 1
        else:
            accu -= 1
    if accu > 0:
        return -1
    else:
        return 1

 # 使生物体的参数发生随机波动


def muta(x):
    inta = random.uniform(-1, 1)
    if inta > 0:
        return round(x+random.randrange(2)*(1/inta - 1), 1)  # 定义精度可以有效加快收敛速度
    else:
        return round(x+random.randrange(2)*(1/inta + 1), 1)

 # 变异函数，使下一代种群发生变异


def envo(x):
    points = map(muta, x)
    envv = random.randrange(3)
    if envv == 0 and len(points) > 1:
        points.pop()
    elif envv == 1 and points[-1] != 0:
        points.append(0)
    return points

 # 主程序开始

 # 拟合点
fitPoints = {-10: 853231.0, -9: 559842.8, -8: 349541.6, -7: 204926.2, -6: 110642.6, -5: 53384.0, -4: 21890.8, -3: 6950.6, -2: 1398.2, -
    1: 115.6, 0: 32.0, 1: 123.8, 2: 1414.6, 3: 6975.2, 4: 21923.6, 5: 53425.0, 6: 110691.8, 7: 204983.6, 8: 349607.2, 9: 559916.6, }

 # 初始种群
population = [[0, ] for x in xrange(100)]

 x = 0
while x < 1000:
    population = sorted(population, compare)
    if x % 50 == 0:
        print '第%s代：%s' % (x, population[0])
    nextGen1 = map(envo, population[:20])
    nextGen2 = map(envo, population[:30])
    nextGen3 = map(envo, population[:40])
    population = population[:10]+nextGen1+nextGen2+nextGen3
    x += 1

 print 'end'

 raw_input() 
