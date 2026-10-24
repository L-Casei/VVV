"""Render the example GUI's coordinates and DDSs for offline art/layout review.

This is not a CK3 renderer: native window/button skins and fonts are approximated.
All positions, labels, visibility predicates, strengths and custom textures come
from the actual mod source. Requires Pillow. Output is never shipped in the mod.
"""
import argparse
import json
from pathlib import Path
import re

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]


def parse(text):
    tokens = re.findall(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}=]|[^\s{}=]+', text.lstrip('\ufeff'))
    tokens = [token for token in tokens if not token.startswith('#')]
    index = 0

    def block():
        nonlocal index
        result = []
        while index < len(tokens) and tokens[index] != '}':
            key = tokens[index]
            index += 1
            if index < len(tokens) and tokens[index] == '=':
                index += 1
                value = tokens[index]
                index += 1
                if value == '{':
                    value = block()
                    index += 1
                elif value.startswith('"'):
                    value = json.loads(value)
                result.append((key, value))
            else:
                result.append(key)
        return result
    return block()


def get(node, name, default=None):
    return next((item[1] for item in node if isinstance(item, tuple) and item[0] == name), default)


def initial_state():
    effects = parse((ROOT / 'common/scripted_effects/vvv_effects.txt').read_text())
    state = {}
    for key, value in get(effects, 'vvv_initialize_drill_effect'):
        if key == 'set_variable':
            if isinstance(value, str):
                state[value] = 1
            else:
                state[get(value, 'name')] = int(get(value, 'value'))
    return state


def visible(node, state):
    expression = get(node, 'visible', '')
    match = re.search(r"GetScriptedGui\('([^']+)'\)", expression)
    if not match:
        return expression != 'no'
    name = match[1]
    troops = ('archers', 'levies', 'light_infantry')
    for index, troop in enumerate(troops):
        if name == f'vvv_gui_selected_{troop}':
            return state['vvv_selected_unit'] == index
        for lane in range(3):
            if name == f'vvv_gui_{troop}_{lane}':
                return state[f'vvv_{troop}_lane'] == lane
    raise ValueError(f'Unknown visibility predicate: {name}')


def render(language='english', destination=None):
    tree = parse((ROOT / 'gui/vvv_battlefield.gui').read_text())
    window = get(tree, 'window')
    width, height = map(int, get(window, 'size'))
    canvas = Image.new('RGBA', (width, height), '#252622')
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, width - 1, height - 1), outline='#97805b', width=2)
    locale = (ROOT / f'localization/{language}/vvv_l_{language}.yml').read_text(encoding='utf-8-sig')
    labels = dict(re.findall(r'^\s+(\S+):0 "(.*)"$', locale, re.M))
    state = initial_state()

    def font(size, title=False):
        name = 'DejaVuSerif-Bold.ttf' if title else 'DejaVuSans.ttf'
        return ImageFont.truetype(name, size)

    def paint(kind, node, origin):
        if not visible(node, state):
            return
        x, y = origin
        dx, dy = map(int, get(node, 'position', ['0', '0']))
        x, y = x + dx, y + dy
        w, h = map(int, get(node, 'size', ['0', '0']))
        if kind == 'icon':
            texture = get(node, 'texture', '')
            if texture.startswith('gfx/interface/vvv/'):
                tile = Image.open(ROOT / texture).convert('RGBA').resize((w, h), Image.Resampling.LANCZOS)
                canvas.alpha_composite(tile, (x, y))
            elif texture.endswith('/gold.dds'):
                draw.rectangle((x, y, x + w - 1, y + h - 1), fill='#ddbd72')
        if kind == 'button_standard':
            draw.rectangle((x, y, x + w - 1, y + h - 1), fill='#30312b', outline='#90794e')
            text = labels[get(node, 'text')]
            draw.text((x + w / 2, y + h / 2), text, font=font(15), anchor='mm', fill='#e0d4b7')
        if kind == 'text_single':
            value = get(node, 'text', '')
            match = re.search(r"Var\('([^']+)'\)", value)
            text = str(state[match[1]]) if match else labels.get(value, value)
            size = int(get(node, 'fontsize', '16'))
            centered = get(node, 'align', '').startswith('center')
            draw.text((x + w / 2 if centered else x, y + h / 2), text,
                      font=font(size, get(node, 'font') == 'TitleFont'),
                      anchor='mm' if centered else 'lm', fill='#f0e3bf')
        for item in node:
            if isinstance(item, tuple) and isinstance(item[1], list):
                if item[0] in ('widget', 'icon', 'button', 'button_standard', 'text_single'):
                    paint(item[0], item[1], (x, y))

    paint('window', window, (0, 0))
    destination = destination or ROOT / 'docs/tactics-preview.png'
    canvas.convert('RGB').save(destination)
    print(destination)
    return destination


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--language', choices=('english', 'spanish'), default='english')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    render(args.language, args.output)
