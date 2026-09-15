# -*- coding: utf-8 -*-
"""紹介ページ用のアイコンを生成する。

深緑の下地に、GPXのルート線（クリーム色の折れ線）を斜めに通し、
その上におにぎりを置く。ルートの先端には赤いピン（見つけたスポット）。
外部の画像素材は使わず、ここで描く。

    py make_icon.py      → assets/icon.png, assets/favicon.ico
"""
import os

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, 'assets')
S = 1024

GREEN = (30, 122, 76)        # 下地
GREEN_DEEP = (22, 96, 60)    # 下地の縁（わずかな陰）
ROUTE = (242, 232, 200)      # ルート線（クリーム）
RICE = (251, 250, 245)       # おにぎりの米
RICE_EDGE = (214, 210, 196)  # 米の縁（白を浮かせる）
NORI = (27, 42, 34)          # 海苔
PIN = (224, 72, 58)          # スポットのピン
WHITE = (255, 255, 255)


def draw(img):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, S, S), radius=int(S * 0.22), fill=GREEN)

    # ---- ルート線：左下から右上へ、曲がり角のある折れ線 ----
    route = [(-40, 890), (150, 780), (200, 540), (380, 225), (700, 190), (870, 170)]
    d.line(route, fill=GREEN_DEEP, width=88, joint='curve')      # 線の下の陰
    d.line(route, fill=ROUTE, width=64, joint='curve')

    # ---- おにぎり：角の丸い三角形 ----
    cx, cy = 540, 600
    h = 540           # 高さ
    w = 330           # 底辺の半分
    r = 80            # 角の丸み
    tri = [(cx, cy - h * 0.62), (cx - w, cy + h * 0.38), (cx + w, cy + h * 0.38)]
    # 縁：太い線を joint='curve' で回すと角が丸くなる
    d.line(tri + [tri[0], tri[1]], fill=RICE_EDGE, width=2 * r + 14, joint='curve')
    d.polygon(tri, fill=RICE_EDGE)
    d.line(tri + [tri[0], tri[1]], fill=RICE, width=2 * r, joint='curve')
    d.polygon(tri, fill=RICE)

    # 海苔：底辺に沿った帯（三角形からはみ出さないよう、少し内側に）
    ny0 = cy + h * 0.06
    ny1 = cy + h * 0.38 + r * 0.5
    # 三角形の左右の辺に沿って台形にする
    def edge_x(y, sign):
        t = (y - tri[0][1]) / (tri[1][1] - tri[0][1])
        return cx + sign * (w * t)
    nori = [(edge_x(ny0, -1) + 12, ny0), (edge_x(ny0, 1) - 12, ny0),
            (cx + w * 0.72, ny1), (cx - w * 0.72, ny1)]
    d.polygon(nori, fill=NORI)

    # ---- ピン：ルートの先端に赤い丸（白縁） ----
    px, py = 870, 170
    d.ellipse((px - 96, py - 96, px + 96, py + 96), fill=WHITE)
    d.ellipse((px - 76, py - 76, px + 76, py + 76), fill=PIN)


def main():
    os.makedirs(ASSETS, exist_ok=True)
    img = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    draw(img)
    img.save(os.path.join(ASSETS, 'icon.png'))
    ico = img.convert('RGBA')
    ico.save(os.path.join(ASSETS, 'favicon.ico'), sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print('wrote', os.path.join(ASSETS, 'icon.png'))

    # 小さいサイズでの見え方を画素の割合で確認する（画像は目で見ないため）
    for sz in (16, 32, 64):
        small = img.resize((sz, sz), Image.LANCZOS)
        px = small.load()
        rice = pin = route = 0
        for y in range(sz):
            for x in range(sz):
                r, g, b, a = px[x, y]
                if a < 128:
                    continue
                if r > 225 and g > 225 and b > 215:
                    rice += 1
                elif r > 190 and g < 110:
                    pin += 1
                elif r > 200 and g > 190 and b < 215 and b > 150:
                    route += 1
        n = sz * sz
        print(f'{sz}px: 米 {100*rice/n:.1f}%  ピン {100*pin/n:.1f}%  ルート {100*route/n:.1f}%')


if __name__ == '__main__':
    main()
