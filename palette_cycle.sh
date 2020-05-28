#!/bin/sh

mkdir palette_anim
python cycle_colors.py base_image.png colors.txt palette_anim/_palette_anim
ffmpeg -framerate 6 -i palette_anim/_palette_anim_%01d.png -c:v huffyuv -y -an _palette_anim.avi
ffmpeg -i _palette_anim.avi -vf "palettegen=reserve_transparent=0" -y _palette_anim_palette.png
ffmpeg -i _palette_anim.avi -i _palette_anim_palette.png -lavfi paletteuse -r 6 -y _palette_anim.gif
rm _palette_anim.avi
rm _palette_anim_palette.png
rm -r palette_anim
