import gdstk
import numpy as np

def break_library_into_components(filename, path_for_components):
    """# break_library_into_components('cornerstone_pdk/gds/CORNERSTONE MPW Run 28 GDSII Template.gds', 'cornerstone_pdk/gds/')"""
    library = gdstk.read_gds(filename)
    top_cells = library.top_level()

    for i in top_cells:
        print(i.name)
        temp_lib = gdstk.Library()
        temp_lib.add(i)
        filename = path_for_components + i.name +'.gds'
        temp_lib.write_gds(filename)

def read_ports_from_txt_file(filename):
    """Important note: The angle value in the file should be in the unit of degrees. It is converted to radians here."""
    try:
        with open(filename) as txt_file:
            lines = txt_file.read().splitlines()
    except FileNotFoundError:
        print("Error: No file exist with name ", filename, " for reading ports.", sep="'")
        raise FileNotFoundError from None

    ports = []
    s = lines[0]
    s = s.replace(' ', '') #remove all whitespaces
    while len(s) > 0:
        k = s.find('(')
        l = s.find(')')
        if k == -1 or l == -1:
            break
        p = s[k + 1:l]
        try:
            x, y, angle= p.split(',')
            ports.append((float(x), float(y), float(angle)/180*np.pi))
        except:
            print('Error in splitting coordinates of ports! filename:', filename)
            raise ValueError

        s = s[l + 1:]

    return ports

def calculate_path_between_two_ports(port0, port1, bend_radius):
    s_p = port0[:2]  # start point
    e_p = port1[:2]  # end point
    s_ang = round(port0[2] * 180/np.pi, 2) # start angle in degrees
    e_ang = round(port1[2] * 180/np.pi, 2) # end angle in degrees
    r = bend_radius

    if s_ang == 0:
        if e_ang == 0:
            if s_p[0] < e_p[0]:
                points = [s_p, (e_p[0] + r, s_p[1]), (e_p[0] + r, e_p[1]), e_p]
            else:
                points = [s_p, (s_p[0] + r, s_p[1]), (s_p[0] + r, e_p[1]), e_p]

        elif e_ang == 90:
            if s_p[1] > e_p[1] and s_p[0] < e_p[0]:
                points = [s_p, (e_p[0], s_p[1]), e_p]
            else:
                points = [s_p, (s_p[0] + r, s_p[1]), (s_p[0] + r, e_p[1] + r), (e_p[0], e_p[1] + r), e_p]

        elif e_ang == 180:
            if s_p[0] < e_p[0]:
                if s_p[1] == e_p[1]:
                    points = [s_p, e_p]
                else:
                    points = [s_p, (e_p[0] - r, s_p[1]), (e_p[0] - r, e_p[1]), e_p]
            else:
                points = [s_p, (s_p[0] + r, s_p[1]), (s_p[0] + r, s_p[1] / 2 + e_p[1] / 2),
                          (e_p[0] - r, s_p[1] / 2 + e_p[1] / 2), (e_p[0] - r, e_p[1]), e_p]

        elif e_ang == 270:
            if s_p[1] < e_p[1] and s_p[0] < e_p[0]:
                points = [s_p, (e_p[0], s_p[1]), e_p]
            else:
                points = [s_p, (s_p[0] + r, s_p[1]), (s_p[0] + r, e_p[1] - r), (e_p[0], e_p[1] - r), e_p]

        else:
            raise ValueError("Angle should be an integer multiple of 90 deg, but got: " + str(e_ang))

    elif s_ang == 90:

        if e_ang == 0:
            if s_p[1] < e_p[1] and s_p[0] > e_p[0]:
                points = [s_p, (s_p[0], e_p[1]), e_p]
            else:
                points = [s_p, (s_p[0], s_p[1] + r), (e_p[0] + r, s_p[1] + r), (e_p[0] + r, e_p[1]), e_p]

        elif e_ang == 90:
            if s_p[1] < e_p[1]:
                points = [s_p, (s_p[0], e_p[1] + r), (e_p[0], e_p[1] + r), e_p]
            else:
                points = [s_p, (s_p[0], s_p[1] + r), (e_p[0], s_p[1] + r), e_p]

        elif e_ang == 180:
            if s_p[0] < e_p[0] and s_p[1] < e_p[1]:
                points = [s_p, (s_p[0], e_p[1]), e_p]
            else:
                points = [s_p, (s_p[0], s_p[1] + r), (e_p[0] - r, s_p[1] + r), (e_p[0] - r, e_p[1]), e_p]

        elif e_ang == 270:
            if s_p[1] < e_p[1]:
                if s_p[0] == e_p[0]:
                    points = [s_p, e_p]
                else:
                    points = [s_p, (s_p[0], e_p[1] - r), (e_p[0], e_p[1] - r), e_p]
            else:
                points = [s_p, (s_p[0], s_p[1] + r), (s_p[0] / 2 + e_p[0] / 2, s_p[1] + r),
                          (s_p[0] / 2 + e_p[0] / 2, e_p[1] - r), (e_p[0], e_p[1] - r), e_p]

        else:
            raise ValueError("Angle should be an integer multiple of 90 deg, but got: " + str(e_ang))

    elif s_ang == 180:
        if e_ang == 0:
            if s_p[0] > e_p[0]:
                if s_p[1] == e_p[1]:
                    points = [s_p, e_p]
                else:
                    points = [s_p, (e_p[0] + r, s_p[1]), (e_p[0] + r, e_p[1]), e_p]
            else:
                points = [s_p, (s_p[0] - r, s_p[1]), (s_p[0] - r, s_p[1] / 2 + e_p[1] / 2),
                          (e_p[0] + r, s_p[1] / 2 + e_p[1] / 2), (e_p[0] + r, e_p[1]), e_p]

        elif e_ang == 90:
            if s_p[0] > e_p[0] and s_p[1] > e_p[1]:
                points = [s_p, (e_p[0], s_p[1]), e_p]
            else:
                points = [s_p, (s_p[0] - r, s_p[1]), (s_p[0] - r, e_p[1] + r), (e_p[0], e_p[1] + r), e_p]

        elif e_ang == 180:
            if s_p[0] > e_p[0]:
                points = [s_p, (e_p[0] - r, s_p[1]), (e_p[0] - r, e_p[1]), e_p]
            else:
                points = [s_p, (s_p[0] - r, s_p[1]), (s_p[0] - r, e_p[1]), e_p]

        elif e_ang == 270:
            if s_p[1] < e_p[1] and s_p[0] > e_p[0]:
                points = [s_p, (e_p[0], s_p[1]), e_p]
            else:
                points = [s_p, (s_p[0] - r, s_p[1]), (s_p[0] - r, e_p[1] - r), (e_p[0], e_p[1] - r), e_p]

        else:
            raise ValueError("Angle should be an integer multiple of 90 deg, but got: " + str(e_ang))

    elif s_ang == 270:
        if e_ang == 0:
            if s_p[1] > e_p[1] and s_p[0] > e_p[0]:
                points = [s_p, (s_p[0], e_p[1]), e_p]
            else:
                points = [s_p, (s_p[0], s_p[1] - r), (e_p[0] + r, s_p[1] - r), (e_p[0] + r, e_p[1]), e_p]

        elif e_ang == 90:
            if s_p[1] > e_p[1]:
                if s_p[0] == e_p[0]:
                    points = [s_p, e_p]
                else:
                    points = [s_p, (s_p[0], e_p[1] + r), (e_p[0], e_p[1] + r), e_p]
            else:
                points = [s_p, (s_p[0], s_p[1] - r), (s_p[0] / 2 + e_p[0] / 2, s_p[1] - r),
                          (s_p[0] / 2 + e_p[0] / 2, e_p[1] + r), (e_p[0], e_p[1] + r), e_p]

        elif e_ang == 180:
            if s_p[1] > e_p[1] and s_p[0] < e_p[0]:
                points = [s_p, (s_p[0], e_p[1]), e_p]
            else:
                points = [s_p, (s_p[0], s_p[1] - r), (e_p[0] - r, s_p[1] - r), (e_p[0] - r, e_p[1]), e_p]

        elif e_ang == 270:
            if s_p[1] < e_p[1]:
                points = [s_p, (s_p[0], s_p[1] - r), (e_p[0], s_p[1] - r), e_p]
            else:
                points = [s_p, (s_p[0], e_p[1] - r), (e_p[0], e_p[1] - r), e_p]

        else:
            raise ValueError("Angle should be an integer multiple of 90 deg, but got: " + str(e_ang))

    else:
        raise ValueError("Angle should be an integer multiple of 90 degree, but got: " + str(s_ang))

    return points

def apply_transformation(port, translation=(0, 0), rotation=0, x_reflection=False):
    """Note: reflection is applied before rotation."""

    p_x = port[0]
    p_y = port[1]
    p_angle = port[2] % (np.pi * 2)

    # apply x-reflection
    if x_reflection:
        p_y = - p_y
        p_angle = (np.pi * 2 - p_angle) % (np.pi * 2)

    # apply rotation
    p_x, p_y  = p_x * np.cos(rotation) - p_y * np.sin(rotation), p_x * np.sin(rotation) + p_y * np.cos(rotation)
    p_angle = (p_angle + rotation) % (np.pi * 2)

    # apply translation
    p_x = p_x + translation[0]
    p_y = p_y + translation[1]

    return p_x, p_y, p_angle
