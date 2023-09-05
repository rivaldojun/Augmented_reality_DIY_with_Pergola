import itertools
from typing import List, Tuple


class Panel:
    def __init__(self, panel_id: int, width: int, height: int):
        self.id = panel_id
        self.width = width
        self.height = height

class Item:
    def __init__(self, item_id: int, width: int, height: int, can_rotate: bool,name:str):
        self.id = item_id
        self.width = width
        self.height = height
        self.can_rotate = can_rotate
        self.name = name

class Unused:
    def __init__(self, panel: Panel, width: int, height: int, x: int, y: int):
        self.panel = panel
        self.width = width
        self.height = height
        self.x = x
        self.y = y

class Used:
    def __init__(self, panel: Panel, item: Item, x: int, y: int, rotate: bool):
        self.panel = panel
        self.item = item
        self.x = x
        self.y = y
        self.rotate = rotate

class Params:
    def __init__(self, panels: List[Panel], items: List[Item], cut_width: int,min_initial_usage:bool):
        self.panels = panels
        self.items = items
        self.cut_width = cut_width
        self.min_initial_usage = min_initial_usage

class Result:
    def __init__(self, params: Params, used: List[Used], unused: List[Unused]):
        self.params = params
        self.used = used
        self.unused = unused
_fitness_K = 0.03

panel1 = Panel(1, 20, 2000)
    # panel2 = Panel(2, 20, 30)
    # panel3 = Panel(3, 15, 25)
    # panel4 = Panel(4, 30, 40)

item1 = Item(1, 10, 10, True,"3 entre")
item2 = Item(2, 10, 10, True,"4 entre")
item3 = Item(3, 10, 10, True,"5 entre")
item4 = Item(4, 10, 10, True,"3 entre")
item5 = Item(5, 10, 10, True,"2 entre")
item6 = Item(6, 30, 20, True,"1 entre")
# item6 = Item(4, 10, 10, True)

# unused1 = Unused(panel1, 3, 6, 1, 2)
# # unused2 = Unused(panel2, 4, 7, 2, 4)
# # unused3 = Unused(panel3, 5, 8, 3, 6)
# # unused4 = Unused(panel4, 6, 9, 4, 8)

# # used1 = Used(panel1, item1, 2, 3, True)
# # used2 = Used(panel2, item2, 5, 6, False)
# # used3 = Used(panel3, item3, 8, 9, True)
# # used4 = Used(panel4, item4, 10, 12, False)

params = Params([panel1], [item1, item2, item3, item4,item5,item6], 0.3, False)

def optimize(params):
    state=""

    def _get_next_results(result):
        selected_item = None
        used_items = {used.item.id for used in result.used}
        for item in result.params.items:
            if item.id in used_items:
                continue
            if (not selected_item or
                    max(item.width, item.height) >
                    max(selected_item.width, selected_item.height)):
                selected_item = item
        if not selected_item:
            raise Exception
        return _get_next_results_for_item(result, selected_item)


    def _get_next_results_for_item(result, item):
        ret = []
        loop_iter = ((False, i, unused) for i, unused in enumerate(result.unused))
        if item.can_rotate:
            loop_iter = itertools.chain(
                loop_iter,
                ((True, i, unused) for i, unused in enumerate(result.unused)))
        for rotate, i, unused in loop_iter:
            for vertical in [True, False]:
                new_used, new_unused = _cut_item_from_unused(
                    unused, item, rotate, result.params.cut_width, vertical)
                if not new_used:
                    continue
                new_result = Result(params=result.params, used=result.used + [new_used], unused=result.unused[:i] + new_unused + result.unused[i+1:])
                ret.append(new_result)
        return ret


    def _cut_item_from_unused(unused, item, rotate, cut_width, vertical):
        item_width = item.width if not rotate else item.height
        item_height = item.height if not rotate else item.width
        if unused.height < item_height or unused.width < item_width:
            return None, []
        used = Used(panel=unused.panel,
                        item=item,
                        x=unused.x,
                        y=unused.y,
                        rotate=rotate)
        new_unused = []
        width = unused.width - item_width - cut_width
        height = unused.height if vertical else item_height
        if width > 0:
            new_unused.append(Unused(panel=unused.panel,
                                            width=width,
                                            height=height,
                                            x=unused.x + item_width + cut_width,
                                            y=unused.y))
        width = item_width if vertical else unused.width
        height = unused.height - item_height - cut_width
        if height > 0:
            new_unused.append(Unused(panel=unused.panel,
                                            width=width,
                                            height=height,
                                            x=unused.x,
                                            y=unused.y + item_height + cut_width))
        return used, new_unused


    def _is_done(result):
        return len(result.params.items) == len(result.used)


    def _fitness(result):
        total_area = sum(panel.width * panel.height
                        for panel in result.params.panels)
        fitness = 0
        for panel in result.params.panels:
            used_areas = [used.item.width * used.item.height
                        for used in result.used
                        if used.panel == panel]
            unused_areas = [unused.width * unused.height
                            for unused in result.unused
                            if unused.panel == panel]
            fitness += (panel.width * panel.height - sum(used_areas)) / total_area
            fitness -= (_fitness_K *
                        min(used_areas, default=0) * max(unused_areas, default=0) /
                        (total_area * total_area))

        if not result.params.min_initial_usage:
            return fitness

        unused_initial_count = sum(1 for unused in result.unused
                                if _is_unused_initial(unused))
        return (-unused_initial_count, fitness)


    def _is_unused_initial(unused):
        return (unused.x == 0 and
                unused.y == 0 and
                unused.width == unused.panel.width and
                unused.height == unused.panel.height)



    def _create_initial_result(params):
        return Result(params=params,
                            used=[],
                            unused=[Unused(panel=panel,
                                                width=panel.width,
                                                height=panel.height,
                                                x=0,
                                                y=0)
                                    for panel in params.panels])


    def _calculate_greedy(result):
        while not _is_done(result):
            new_result = None
            new_fitness = None
            for next_result in _get_next_results(result):
                next_result_fitness = _fitness(next_result)
                
                if new_fitness is None or next_result_fitness < new_fitness:
                    new_result = next_result
                    new_fitness = next_result_fitness
            if not new_result:
                state="pas possible"
                return state
            result = new_result
        return result

    def calculate(method,
                params: Params
                ) -> Result:
        """Calculate cutting stock problem"""

        if method == "GREEDY":
            return _calculate_greedy(_create_initial_result(params))
        

    

    # result = Result(params, [used1, used2, used3, used4], [unused1, unused2, unused3, unused4])

    result=calculate("GREEDY",params)
    if result=="pas possible":
        return "pas possible"

    import enum
    import importlib.resources
    import typing
    mm: float = 72 / 25.4


    class OutputSettings(typing.NamedTuple):
        pagesize: typing.Tuple[float, float] = (210 * mm, 297 * mm)
        margin_top: float = 10 * mm
        margin_bottom: float = 20 * mm
        margin_left: float = 10 * mm
        margin_right: float = 10 * mm

    # Exemple d'instanciation de OutputSettings
    settings = OutputSettings(pagesize=(150 * mm, 150 * mm))



    class OutputFormat(enum.Enum):
        PDF = 'pdf'
        SVG = 'svg'

    # Exemple d'instanciation de OutputFormat
    format = OutputFormat.PDF


    import io
    import typing

    import cairo
    
    



    def generate(result:Result,
                output_format:OutputFormat,
                panel_id: typing.Optional[str] = None,
                settings:OutputSettings =OutputSettings()
                ) -> bytes:
        """Generate output"""
        ret = io.BytesIO()

        if output_format ==OutputFormat.PDF:
            surface_cls = cairo.PDFSurface

        elif output_format ==OutputFormat.SVG:
            surface_cls = cairo.SVGSurface

        else:
            raise ValueError('unsupported output type')

        with surface_cls(ret,
                        settings.pagesize[0],
                        settings.pagesize[1]) as surface:
            for panel in result.params.panels:
                if panel_id and panel.id != panel_id:
                    continue

                _write_panel(surface, settings, result, panel)
                surface.show_page()
        pdf_bytes=ret.getvalue()
        with open('static/output.pdf', 'wb') as f:
            f.write(pdf_bytes)

        return ret.getvalue()


    def _write_panel(surface, settings, result, panel):
        scale = _calculate_scale(settings, panel)
        width = panel.width * scale
        height = panel.height * scale
        x0 = ((settings.pagesize[0] - width) * settings.margin_left /
            (settings.margin_left + settings.margin_right))
        y0 = ((settings.pagesize[1] - height) * settings.margin_top /
            (settings.margin_top + settings.margin_bottom))

        ctx = cairo.Context(surface)
        ctx.set_line_width(0)
        ctx.set_source_rgb(0.5, 0.5, 0.5)
        ctx.rectangle(x0, y0, width, height)
        ctx.fill()

        for used in result.used:
            if used.panel != panel:
                continue
            _write_used(surface, scale, x0, y0, used)

        for unused in result.unused:
            if unused.panel != panel:
                continue
            _write_unused(surface, scale, x0, y0, unused)

        _write_centered_text(surface, settings.pagesize[0] / 2,
                            settings.pagesize[1] - settings.margin_bottom / 2,
                            panel.id)


    def _write_used(surface, scale, x0, y0, used):
        width = used.item.width * scale
        height = used.item.height * scale
        if used.rotate:
            width, height = height, width
        x = x0 + used.x * scale
        y = y0 + used.y * scale

        ctx = cairo.Context(surface)
        ctx.set_line_width(0)
        if used.item.name=="Joint a 3 entres":
         ctx.set_source_rgb(0, 0.5, 0)
        if used.item.name=="Joint a 4 entres":
         ctx.set_source_rgb(0, 0, 1)
        if used.item.name=="Joint a 5 entres":
         ctx.set_source_rgb(1, 0, 0)
        if used.item.name=="Joint de fixation":
         ctx.set_source_rgb(1, 1, 1)

        ctx.rectangle(x, y, width, height)
        ctx.fill()
        


        _write_centered_text(surface, x + width / 2, y + height / 2,
                            str(used.item.name) + (' (r)' if used.rotate else ''))
        _write_centered_text(surface, x + width / 2, y + height /1.5,
                            str(used.item.width)+' mm ' +'x '+ str(used.item.height)+' mm ')


    def _write_unused(surface, scale, x0, y0, unused):
        width = unused.width * scale
        height = unused.height * scale
        x = x0 + unused.x * scale
        y = y0 + unused.y * scale

        ctx = cairo.Context(surface)
        ctx.set_line_width(0)
        ctx.set_source_rgb(0.7, 0.7, 0.7)
        ctx.rectangle(x, y, width, height)
        ctx.fill()


    def _write_centered_text(surface, x, y, text):
        ctx = cairo.Context(surface)
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_font_size(2)

        text_ext = ctx.text_extents(str(text))
        ctx.move_to(x - text_ext.width / 2,
                    y + text_ext.height / 2)
        ctx.show_text(str(text))


    def _calculate_scale(settings, panel):
        page_width = (settings.pagesize[0] - settings.margin_left -
                    settings.margin_right)
        page_height = (settings.pagesize[1] - settings.margin_top -
                    settings.margin_bottom)
        page_ratio = page_width / page_height
        panel_ratio = panel.width / panel.height
        return (page_width / panel.width if panel_ratio > page_ratio
                else page_height / panel.height)
    pdf_bytes=generate(result,
             format,
              None,
             settings
             )

    return state

optimize(params)
