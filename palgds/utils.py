""" General-purpose utility functions. """

import gdstk
import numpy as np


def read_raw_ports_from_txt_file(filename):
    """ Reads the parameters of ports from txt file.

        Note:

        Ports in the txt file should be in this format:

        (name, xpos, ypos, orientation, port_type)

        orientation will be converted to the angle in radians (R:0, L:pi, U:pi, D: 3/2pi)
        port_type is either 'op' for optical ports, or 'el' for electrical ports.
        All ports should be in the first line of txt file. example txt file for ports:

        (in,-10,0,L,op) (out1,10,2.5,R,op) (el_in,5,5,U,el)

    :param filename: path and file name.
    :return: dict of raw ports.
    """
    try:
        with open(filename) as txt_file:
            lines = txt_file.read().splitlines()
    except FileNotFoundError:
        print("Error: No file exist with name ", filename, " for reading raw_ports.", sep="'")
        raise FileNotFoundError from None

    orientation_dict = {"R": 0, "L": np.pi, "U": np.pi/2, "D": 3/2*np.pi}
    raw_ports = {}
    s = lines[0]
    s = s.replace(' ', '') #remove all whitespaces
    while len(s) > 0:
        k = s.find('(')
        l = s.find(')')
        if k == -1 or l == -1:
            break
        p = s[k + 1:l]
        try:
            name, x, y, orientation, port_type= p.split(',')
            angle = orientation_dict[orientation]
            raw_ports.update({name: (float(x), float(y), angle, port_type)})
        except:
            print('Error in splitting coordinates of raw ports! filename:', filename)
            raise ValueError

        s = s[l + 1:]

    return raw_ports


def calculate_path_between_two_ports(_port0, _port1, bend_radius):
    """Calculates the points of path between two port depending on angles of ports and bend radius.

    :param _port0: (x, y, angle)
    :param _port1: (x, y, angle)
    :param bend_radius:
    :return: list of points
    """
    s_p = _port0[0:2] # start point
    e_p = _port1[0:2] # end point
    s_ang = round(_port0[2] * 180 / np.pi, 2) # start angle in degrees
    e_ang = round(_port1[2] * 180 / np.pi, 2) # end angle in degrees
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


def apply_transformation(_port, translation=(0, 0), rotation=0, x_reflection=False):
    """ Transforms a port in this order: reflection, rotation and finally translation.

    :param _port: (x, y, angle)
    :param translation: (x, y)
    :param rotation: in radians
    :param x_reflection: boolean
    :return: transformed raw port
    """

    p_x = _port[0]
    p_y = _port[1]
    p_angle = _port[2] % (np.pi * 2)

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
