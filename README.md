# Palette Cycling with PIL/Pillow

A simple and terrible hack to make palette cycling effects using Python's PIL / Pillow. Python 3.

## Prerequisites
Install PIL and ArgParse:
```
pip install pillow argparse
```

## Files
**Base image** (`base_image.png`):

![Base image](base_image.png)

Use easily-distinguishable colors. The colors on the top left of the sample base image are only as a guide.

Make sure to save it as **PNG with alpha channel**!

**Palette definitions** (`colors.txt`):
```
base  ff0000 ff0086 ec00ff 7700ff 0047ff 00c7ff 00f4ff 00ff7f 0e6f09 51cb00 b3cb00 cb9b00 cb5d00
dir   left
cycle eefaff d8f5ff c0efff a4e8ff 8ee2ff 8de1ff 55d2ff 88e0ff 9fe6ff b6ecff d2f3ff e8f9ff ffffff
```
* The `base` command specifies which colors to use for the base palette, sequentially.
* `dir` tells the direction which the palette should cycle through
* `cycle` command specifies which colors to map to each entry specified in `base`. The amount of colors here **must** match the `base` colors!

## Generating the animation
Explanation of `palette_cycle.sh` follows...

Make a folder to dump the generated images:
```
mkdir palette_anim
```

Generate the images:
```
python cycle_colors.py base_image.png colors.txt palette_anim/_palette_anim
```
After this command is run, you should see a bunch of images in the `palette_anim` folder.

Create the animation (avi, gif):
```
ffmpeg -framerate 6 -i palette_anim/_palette_anim_%01d.png -c:v huffyuv -y -an _palette_anim.avi
ffmpeg -i _palette_anim.avi -vf "palettegen=reserve_transparent=0" -y _palette_anim_palette.png
ffmpeg -i _palette_anim.avi -i _palette_anim_palette.png -lavfi paletteuse -r 6 -y _palette_anim.gif
```
This first creates the avi, then makes a gif from the avi.

Remove the avi:
```
rm _palette_anim.avi
```

Remove the palette:
```
rm _palette_anim_palette.png
```

Remove the image directory:
```
rm -r palette_anim
```

## Result
![Palette cycle](_palette_anim.gif)
