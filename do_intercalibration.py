from inter_calibration import InterCalibrator
csv = 'AVA_MR_2251-178_lco.csv'
filters = ['u', 'B', 'g', 'V', 'r', 'i', 'z']
objName = 'MR_2251'

cal = InterCalibrator(csv, objName)
priors = [[0.01, 10.0], [0.0, 2.0]]
Nsamples=15000
Nburnin=10000
f = filters[5]
cal.calibrate(f, priors=priors, Nsamples=Nsamples, Nburnin=Nburnin)
