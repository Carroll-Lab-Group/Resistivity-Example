# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 23:26:55 2022

@author: ammar
"""

from resipy import R2
import random
import itertools
import csv
import numpy as np
import os
import time

no_of_model_runs = 1000
tic = time.time()

def rand_shapes():
    x = list(range(1, 80))
    z = list(range(-35, -1))
    x_backup = x
    x1 = random.choice(x)
    x_backup.remove(x1)

    x2 = random.choice(x_backup)
    z_backup = z
    z1 = random.choice(z)
    z_backup.remove(z1)
    z2 = random.choice(z_backup)
    coordinates = [[x1, x2, x2, x1], [z1, z1, z2, z2]]
    return coordinates

def overlap_check(rect_1, rect_2):
    x_min_rect1 = min(rect_1[0])
    x_max_rect1 = max(rect_1[0])
    y_min_rect1 = min(rect_1[1])
    y_max_rect1 = max(rect_1[1])

    x_min_rect2 = min(rect_2[0])
    x_max_rect2 = max(rect_2[0])
    y_min_rect2 = min(rect_2[1])
    y_max_rect2 = max(rect_2[1])

    # since last argument is non-inclusive therefore x2+1
    a = list(range(x_min_rect1, x_max_rect1+1))
    b = list(range(y_min_rect1, y_max_rect1+1))

    comb = list(itertools.product(a, b))

    # since last argument is non-inclusive therefore x2+1
    c = list(range(x_min_rect2, x_max_rect2+1))
    d = list(range(y_min_rect2, y_max_rect2+1))
    comb2 = list(itertools.product(c, d))

    check = any(item in comb for item in comb2)
    return check

def rand_rect_gen(shapes):
    non_ovl_rect = []
    size = 0
    
    first = rand_shapes()
    print('first default value: ', first)
    non_ovl_rect.append(first)
    size += 1
    print('-------')
    
    shapes_no = shapes
    
    while size < shapes_no:
        new_coord = rand_shapes()
        print('-------')
        print('..START..')
        print('-------')
        
        print('to add: ', new_coord)
        print('-------')
        
        print('currently available values in non_ovl_rect')
        for l in range(len(non_ovl_rect)):
            print(l+1, non_ovl_rect[l])
        
        print('-------')
        for l in range(len(non_ovl_rect)):
            print('Overlapping is: ', overlap_check(new_coord, non_ovl_rect[l]))
        print('-------')
        
        for l in range(len(non_ovl_rect)):
            if overlap_check(new_coord, non_ovl_rect[l]):
                print(new_coord, 'overlapping, not going to append!')
                ov_flag = True
                break
            else:
                ov_flag = False
        if ov_flag == False:
            non_ovl_rect.append(new_coord)
            size += 1
            print('-------')
        print('final values:')
        for index in range(len(non_ovl_rect)):
            print('s. no. : ',index+1, non_ovl_rect[index])
        print('end of iteration!', size-1)
        print('-------')
    print('-------')
    print(size)
    
    return(non_ovl_rect)


def geo_model(coordinates_rect, num, num_shapes):
    print("Coordinate pairs =", coordinates_rect)
    # print("Centroids = ", coord_centroids)
    # print("Length, width = ", length_width)
    print("No. of total rectangle coordinates = ", len(coordinates_rect))
    print(coordinates_rect)
    fil_name = 'IP-coords.csv'
    file = open(fil_name, 'a+', newline='')
    with file:
        write = csv.writer(file)
        write.writerow(coordinates_rect)

    cwd = os.getcwd()

    pth = cwd + '//target_' + str(num_shapes) +'_'+ str(num+1)

    k = R2(dirname=pth, typ='cR2')
    # defining electrode array
    elec = np.zeros((25, 3))
    elec[:, 0] = np.arange(0, 25*5.0, 5.0)  # with 25 electrodes at 5 m spacing
    k.setElec(elec)
    print(k.elec)

    if num_shapes == 1:
        geom_input = {
            'polygon1': coordinates_rect[0]}
    elif num_shapes == 2:
        geom_input = {
            'polygon1': coordinates_rect[0],
            'polygon2': coordinates_rect[1]}
    elif num_shapes == 3:
        geom_input = {
            'polygon1': coordinates_rect[0],
            'polygon2': coordinates_rect[1],
            'polygon3': coordinates_rect[2]}
    elif num_shapes == 4:
        geom_input = {
            'polygon1': coordinates_rect[0],
            'polygon2': coordinates_rect[1],
            'polygon3': coordinates_rect[2],
            'polygon4': coordinates_rect[3]}
    elif num_shapes == 6:
        geom_input = {
            'polygon1': coordinates_rect[0],
            'polygon2': coordinates_rect[1],
            'polygon3': coordinates_rect[2],
            'polygon4': coordinates_rect[3],
            'polygon5': coordinates_rect[4],
            'polygon6': coordinates_rect[5]}
    elif num_shapes == 9:
        geom_input = {
            'polygon1': coordinates_rect[0],
            'polygon2': coordinates_rect[1],
            'polygon3': coordinates_rect[2],
            'polygon4': coordinates_rect[3],
            'polygon5': coordinates_rect[4],
            'polygon6': coordinates_rect[5],
            'polygon7': coordinates_rect[6],
            'polygon8': coordinates_rect[7],
            'polygon9': coordinates_rect[8]
            }
    # let's create the mesh based on these electrodes position
    k.createMesh(typ='trian', res0=1000, geom_input=geom_input)
    k.showMesh(xlim=[0, 120], zlim=[-40, 0], color_map='viridis')

    # this assign a resistivity value (ohm.m) for each region defined.

    # 2 regions (1 target body)
    # k.setStartingRes(regionValues={1:1000, 2:10}, ipValues={1:0, 2:-5})

    # regionValues_1 = {1: 1000, 2: 10}
    # regionValues_2 = {1: 1000, 2: 10, 3: 100}
    # regionValues_3 = {1: 1000, 2: 10, 3: 100, 4: 200}
    # regionValues_4 = {1: 1000, 2: 10, 3: 100, 4: 200, 5: 300}
    # regionValues_6 = {1: 1000, 2: 10, 3: 100, 4: 200, 5: 300, 6: 400, 7: 500}
    # regionValues_9 = {1: 1000, 2: 10, 3: 100, 4: 200,
    #                   5: 300, 6: 400, 7: 500, 8: 600, 9: 700, 10: 800}

    my_regionValues = [{1: 1000, 2: 10},
                       {1: 1000, 2: 10, 3: 100},
                       {1: 1000, 2: 10, 3: 100, 4: 200},
                       {1: 1000, 2: 10, 3: 100, 4: 200, 5: 300},
                       {},
                       {1: 1000, 2: 10, 3: 100, 4: 200, 5: 300, 6: 400, 7: 500},
                       {},
                       {},
                       {1: 1000, 2: 10, 3: 100, 4: 200, 5: 300, 6: 400, 7: 500, 8: 600, 9: 630, 10: 700}]



    # ipValues_1 = {1: 0, 2: -5}
    # ipValues_2 = {1: 0, 2: -5, 3: -10}
    # ipValues_3 = {1: 0, 2: -5, 3: -10, 4: -15}
    # ipValues_4 = {1: 0, 2: -5, 3: -10, 4: -15, 5: -20}
    # ipValues_6 = {1: 0, 2: -5, 3: -10, 4: -15, 5: -20, 6: -25, 7: -30}
    # ipValues_9 = {1: 0, 2: -5, 3: -10, 4: -15, 5: -20, 6: -25, 7: -30, 8: -35, 9: -40, 10: -45}

    my_ipValues = [{1: 0, 2: -5},
                   {1: 0, 2: -5, 3: -10},
                   {1: 0, 2: -5, 3: -10, 4: -15},
                   {1: 0, 2: -5, 3: -10, 4: -15, 5: -20},
                   {},
                   {1: 0, 2: -5, 3: -10, 4: -15, 5: -20, 6: -25, 7: -30},
                   {},
                   {},
                   {1: 0, 2: -5, 3: -10, 4: -15, 5: -20, 6: -25, 7: -30, 8: -35, 9: -40, 10: -45}]
    
    # this assign a resistivity value (ohm.m) for each region defined.
    
    k.setStartingRes(regionValues = my_regionValues[num_shapes-1],
                     ipValues = my_ipValues[num_shapes-1])
    
    
    # k.setStartingRes(regionValues={1: 1000, 2: 10, 3: 100}, ipValues={
                     # 1: 0, 2: -5, 3: -10})

    k.showMesh(attr='res0', color_map='jet')



    # create a dipole dipole sequence of diple spacing of 5 (=skip 0) with 10 levels
    k.createSequence([('dpdp1', 1, 10)])
    print(k.sequence)  # the sequence is stored inside the R2 object

    # forward modelling with 5 % noise added to the output
    k.forward(noise=0.05, noiseIP=2, iplot=False)
    k.showPseudo()
    k.showPseudoIP()

    # we are now informing R2 that the relative error is 0.05 for inversion
    k.param['b_wgt'] = 0.05
    # the offset error is zero, to be consistent with the error added to the forward model
    k.param['a_wgt'] = 0.02

    k.invert()
    k.showResults(index=0)  # initial model
    k.showResults(index=1, sens=False)  # recovered
    k.showResults(index=1, sens=False, attr='Phase(mrad)',
                  color_map='jet', contour=True)
    k.showResults(index=1, sens=False, attr='Magnitude(ohm.m)',
                  color_map='jet', contour=True)
    k.showResults(index=1, sens=False, attr='Sensitivity(log10)',
                  color_map='jet', contour=True)
    k.showResults(index=1, sens=False, attr='Conductivity(mS/m)',
                  color_map='jet', contour=True)
    k.showResults(index=1, sens=False, attr='Magnitude(log10)',
                  color_map='jet', contour=True)
    k.showResults(index=1, sens=False, attr='Sigma_imag(log10)',
                  color_map='jet', contour=True)


sh_list = [1, 2, 3, 4, 6, 9]


for sh in sh_list:
    for i in range(no_of_model_runs):
        geo_model(rand_rect_gen(sh), i, sh)

toc = time.time()

print('elapsed time: ', toc-tic)