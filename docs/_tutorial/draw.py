def draw(pcell, path, scaling=10, name=None):
    """ svg export function from gdstk library."""
    
    if name is not None:
        name = path + name + ".svg"
    else:
        name = path + pcell.name + ".svg"

    pcell.write_svg(
        name,
        scaling=scaling,
        background="none",
        shape_style={(0, 0): {"fill": "darkorange", "stroke": "chocolate"}},
        label_style={(3, 2): {"stroke": "red", "fill": "none", "font-size": "32px"}},
        pad="5%",
    )