from xg_deltaGen import deltaGen

coilCount_list = [.5, 1, 3, 5, 8, 13]
coilRadius_list = [.2, .5, 1, 2, 3]

noisFreq_list = [.1, .5, 1, 3, 5, 8, 13]
noisMag_list = [1, 2, 3, 5, 8, 13]

ar_cutlength = [5, 10, 15, 20, 25, 30]
gScale_list = [0.6, 1.0, 1.3, 1.6, 2]
namelist = ['AliceRivera',
    'AmandaMoore',
    'CamilaMazurek',
    'ChrisHemsworth',
    'JasonMomoa',
    'JenniferMendez',
    'KamilaTen',
    'KarenBennet',
    'LouisPrice',
    'LucyMae',
    'LynneLerner',
    'ManuelTucker',
    'MonstaXJooheon',
    'PaulSamatar',
    'PhilipAn',
    'RonaldNelson',
    'ScottPerry',
    'SimonYuen',
    'VeronicaYoung',
    'WandaEdwards']

groomName = 'AliceRivera'
deltaGen(groomName, ['pony_coll'], 'dh_coil', count=coilCount_list, radius=coilRadius_list)
deltaGen(groomName, ['pony_coll'], 'dh_cutClamp', cut_length=ar_cutlength)
deltaGen(groomName, ['pony_coll'], 'dh_exp_gScale', gScale=gScale_list)
deltaGen(groomName, ['head_coll', 'pony_coll'], 'dh_noise', frequency=noisFreq_list, magnitude=noisMag_list)

