"""
TEMP: DEVELOP LINE OF SIGHT DISCOVERY ALGORITHM
test change for GIT by Hans 4-Feb-2020 13:47
hahaha
"""
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

nr_tiles_x = 20
nr_tiles_y = 30
map_matrix = np.random.rand(nr_tiles_y, nr_tiles_x) * 4
map_matrix = map_matrix.astype("uint8")
map_matrix = np.where(map_matrix > 2, 1, 0)


viewing_dist = 5
p_x = 10
p_y = 12

dist_matrix = np.zeros((nr_tiles_y, nr_tiles_x))
angle_matrix = np.zeros((nr_tiles_y, nr_tiles_x))
view_matrix = np.zeros((nr_tiles_y, nr_tiles_x))

x_list = []
y_list = []
dist_list = []
view_angle_list = []
min_block_angle_list = []
max_block_angle_list = []
# block_list = []

for x in range(nr_tiles_x):
    for y in range(nr_tiles_y):

        if x == p_x and y == p_y:
            print("Own tile")
            continue

        dist_x = p_x - x
        dist_y = p_y - y
        dist = np.sqrt(np.power(dist_x, 2) + np.power(dist_y, 2))
        dist_matrix[y][x] = dist
        angle = np.arctan2(dist_y, dist_x)
        angle_matrix[y][x] = angle

        if dist <= viewing_dist:
            # consider tile to be in line of sight
            x_list.append(x)
            y_list.append(y)
            dist_list.append(dist)

            view_angle = np.arctan2(dist_y, dist_x)
            view_angle_list.append(view_angle)

            # block_list.append(map_matrix[y][x])

            if map_matrix[y][x] == 1:
                block_angle1 = np.arctan2(dist_y+0.5, dist_x+0.5)
                block_angle2 = np.arctan2(dist_y+0.5, dist_x-0.5)
                block_angle3 = np.arctan2(dist_y-0.5, dist_x+0.5)
                block_angle4 = np.arctan2(dist_y-0.5, dist_x-0.5)
                min_block_angle = np.min([block_angle1, block_angle2, block_angle3, block_angle4])
                max_block_angle = np.max([block_angle1, block_angle2, block_angle3, block_angle4])
                min_block_angle_list.append(min_block_angle)
                max_block_angle_list.append(max_block_angle)
            else:
                min_block_angle_list.append(0)
                max_block_angle_list.append(0)

df = pd.DataFrame({"x": x_list, "y": y_list, "dist": dist_list, "view_angle": view_angle_list,
                   "min_block_angle": min_block_angle_list, "max_block_angle":
                       max_block_angle_list})#, "block": block_list})

nr_in_range = []

for index, row in df.iterrows():

    df_in_range = df[df["dist"] < row.dist]

    # df_in_range = df_in_range[df_in_range.index != index]
    nr_in_range.append(df_in_range.shape[0])

    x = int(row.x)
    y = int(row.y)

    min_block_angles = df_in_range["min_block_angle"].values
    max_block_angles = df_in_range["max_block_angle"].values
    view_angle = row.view_angle

    view_matrix[y][x] = 1

    for min_angle, max_angle in zip(min_block_angles, max_block_angles):#, blocks):

        if min_angle == 0 and max_angle == 0:
            continue

        if min_angle < 0 < max_angle:
            if max_angle > 0.5*np.pi:
                if view_angle > max_angle:
                    view_matrix[y][x] = 0
                    print(f"1: VA: {view_angle}, MIA: {min_angle}, MAA: {max_angle}")
                    break
                elif view_angle < min_angle:
                    view_matrix[y][x] = 0
                    print(f"2: VA: {view_angle}, MIA: {min_angle}, MAA: {max_angle}")
                    break
            if max_angle < 0.5*np.pi:
                if 0 <= view_angle < max_angle:
                    view_matrix[y][x] = 0
                    print(f"3: VA: {view_angle}, MIA: {min_angle}, MAA: {max_angle}")
                    break
                if 0 > view_angle > min_angle:
                    view_matrix[y][x] = 0
                    print(f"4: VA: {view_angle}, MIA: {min_angle}, MAA: {max_angle}")
                    break
        elif min_angle < view_angle < max_angle:
            view_matrix[y][x] = 0
            print(f"5: VA: {view_angle}, MIA: {min_angle}, MAA: {max_angle}")
            break


df["nr_in_range"] = nr_in_range

view_matrix[p_y][p_x] = 2
map_matrix[p_y][p_x] = 2

plt.subplot(1, 2, 1)
plt.imshow(view_matrix)
plt.subplot(1, 2, 2)
plt.imshow(map_matrix)