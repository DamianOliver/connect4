import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt

def find_angles(num_angles):
    angle_list = []
    for i in range(num_angles):
        angle_list.append((i + 1) * (2*3.14 / num_angles))

    return angle_list

def find_points(angle_list, radius, center):
    point_list = []
    for angle in angle_list:
        point_x = np.cos(angle) * radius + center[0]
        point_y = np.sin(angle) * radius + center[1]
        point_list.append([point_x, point_y])

    return np.array(point_list)

radius = 5

def draw(center, points, skip, num_points, figure, axes, circle_color, line_color):
    Drawing_colored_circle = plt.Circle((center[0], center[1]), radius, fill = False, color = circle_color)
    axes.set_aspect(1)
    axes.add_artist(Drawing_colored_circle)
    stargon_title = "Stargon " + str(num_points) + " " + str(skip)
    plt.title(stargon_title)

    for i in range(len(points)):
        x1_index = points[i][0]
        x2_index = points[(i + skip) % num_points][0]
        y1_index = points[i][1]
        y2_index = points[(i + skip) % num_points][1]
        plt.plot([x1_index, x2_index], [y1_index, y2_index], color = line_color)


def graph_graph(a, b, start_a, start_b):
    figure, axes = plt.subplots()
    plt.xlim([-100, 900])
    plt.ylim([-100, 900])
    for y in range(start_a, a):
        for x in range(start_b, b):
            center = [x * 11, y * 11]
            angles = find_angles(x)
            points = find_points(angles, radius, center)
            skip = y
            if skip > x:
                points = []
            color_change = 1 / a
            circle_color = (0.0, 1 - color_change * y, 1 - color_change * y)
            color_change = 1 / b
            line_color = (0.0, 1 - (color_change * x * 0.75), 1 - (color_change * x * 0.75))
            circle_color = (1, 1, 1)

            if x - skip > skip:
                color_index = skip
            else:
                color_index = x - skip
                
            if color_index != 0:
                if x % color_index == 0:
                    line_color = color_picker(x / color_index * 50)

            draw(center, points, skip, x, figure, axes, circle_color, line_color)

    plt.show()

def input_draw():
    while True:
        num_points = int(input("Enter Num Points: "))
        radius = 5
        angles = find_angles(num_points)
        points = find_points(angles, radius, [0,0])
        skip = int(input("Enter Skip Number: "))

        figure, axes = plt.subplots()
        Drawing_colored_circle = plt.Circle(( 0 , 0 ), radius, fill = False)
        axes.set_aspect( 1 )
        axes.add_artist( Drawing_colored_circle )
        stargon_title = "Stargon " + str(num_points) + " " + str(skip)
        plt.title( stargon_title )

        for i in range(len(points)):
            x1_index = points[i][0]
            x2_index = points[(i + skip) % num_points][0]
            y1_index = points[i][1]
            y2_index = points[(i + skip) % num_points][1]
            plt.plot([x1_index, x2_index], [y1_index, y2_index], color = 'c')

        plt.xlim([-5.5, 5.5])
        plt.ylim([-5.5, 5.5])
        plt.show()

def color_picker(index):
    if index > 765:
        return (0, 1, 1)

    color = [255, 0, 0]
    new_color = color[1] + index
    if new_color > 255:
        new_color = 255
    index -= (255 - color[1])
    color[1] = new_color

    if index <= 0:
        return color_convert(color)
    
    new_color = color[0] - index
    if new_color < 0:
        new_color = 0
    index -= color[0]
    color[0] = new_color
    if index <= 0:
        return color_convert(color)

    new_color = color[2] + index
    if new_color > 255:
        new_color = 255
    index -= (255 - color[2])
    color[2] = new_color

    return color_convert(color)

def color_convert(input_color):
    output_color = []
    for num in input_color:
        if num == 0:
            output_color.append(0)
        else:
            output_color.append(num / 255)
    return output_color

def omnistargon():
    for r in range(20):
        num_points = r
        radius = 5
        angles = find_angles(num_points)
        points = find_points(angles, radius, [0,0])
        figure, axes = plt.subplots()
        Drawing_colored_circle = plt.Circle(( 0 , 0 ), radius, fill = False)
        axes.set_aspect( 1 )
        axes.add_artist( Drawing_colored_circle )
        stargon_title = "OmniStargon " + str(num_points)
        plt.title( stargon_title )

        for k in range(1, len(points)):
            for i in range(len(points)):
                x1_index = points[i][0]
                x2_index = points[(i + k) % num_points][0]
                y1_index = points[i][1]
                y2_index = points[(i + k) % num_points][1]
                plt.plot([x1_index, x2_index], [y1_index, y2_index])

        plt.xlim([-5.5, 5.5])
        plt.ylim([-5.5, 5.5])
        plt.show()




graph_graph(40, 40, 1, 3)
# input_draw()
# omnistargon()

