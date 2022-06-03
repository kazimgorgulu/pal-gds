def draw(pcell, path, scale=300):
    """ svg export function from gdstk library."""
    bb = pcell.bounding_box()
    scaling = scale / (1.1 * (bb[1][0] - bb[0][0]))
    name = path + pcell.name + ".svg"
    pcell.write_svg(
        name,
        scaling=scaling,
        background="none",
        shape_style={(0, 0): {"fill": "darkorange", "stroke": "chocolate"}},
        label_style={(3, 2): {"stroke": "red", "fill": "none", "font-size": "32px"}},
        pad="5%",
    )