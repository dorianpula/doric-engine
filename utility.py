def convert_hex_code_into_floats(color, alpha=1.0):
    _color = color
    if not (len(_color) == 7 and _color.startswith('#')):
        raise ValueError('Value of color has the wrong format: e.g. #001234')
    _color = _color[1:]

    def _convert_to_hex_to_int(cmp_1, cmp_2):
        return int('0x{}{}'.format(cmp_1, cmp_2), base=16)

    color_components = [_convert_to_hex_to_int(_color[x], _color[x + 1]) for x in xrange(0, len(_color), 2)]
    float_color_components = [round(float_component / 255.0, 2) for float_component in color_components]

    return float_color_components[0], float_color_components[1], float_color_components[2], alpha
