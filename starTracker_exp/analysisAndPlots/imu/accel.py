import pylab as pl 
p1 = [3.83,
3.79,
3.6,
3.47,
3.29,
3.18,
3.07,
2.99,
2.89,
2.8,
2.74,
2.66,
2.62,
2.55,
2.5,
2.45,
2.38,
2.29,
2.22,
2.14,
2.12,
2.14,
2.1,
2.08,
2.02,
2.02,
1.96,
1.96,
1.95,
1.96,
1.97,
1.96,
1.95,
1.92,
1.88,
1.88,
1.89,
1.87,
1.88,
1.81,
1.77,
1.73,
1.73,
1.76,
1.76,
1.76,
1.72,
1.71,
1.66,
1.67,
1.66,
1.64,
1.64,
1.67,
1.66,
1.65,
1.67,
1.71,
1.72,
1.69]

pl.plot(p1)
pl.xlabel('sample number')
pl.ylabel('Pitch Angle (deg)')
pl.title('Startup Change in Pitch Angle')
pl.show()
