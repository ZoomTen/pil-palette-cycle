#!/usr/bin/python3

import re
import sys
from PIL import Image

from argparse import ArgumentParser as ap

base_palette = []
cycle_palette = []
palette_direction = ''
palette_len = 0

VALID_DIRECTIONS = ['left', 'right']
VALID_DIR_RE_STRING = '^('
for i in VALID_DIRECTIONS:
	VALID_DIR_RE_STRING += i
	if i != VALID_DIRECTIONS[len(VALID_DIRECTIONS)-1]:
		VALID_DIR_RE_STRING += '|'
VALID_DIR_RE_STRING += ')$'


parser = ap(description='Generate separate, palette cycling images given base colors, cycle colors, and direction.')
parser.add_argument('image', metavar='base_image', help='A base image to start out from. This should be a png with alpha channel.')
parser.add_argument('listfile', metavar='list_file', help='A text file containing information about the palette mapping. The file itself should be in the format of "base <hex> <hex> ... \\n dir <left|right> \\n cycle <hex> <hex> ...", where \\n denotes a new line.')
parser.add_argument('output', metavar='output_prefix', help='Will output to png\'s in the form of <Prefix>_0.png, <Prefix>_1.png, ... This is where you\'ll set <Prefix>.')

args = parser.parse_args()

with open(args.listfile, "r") as n:
	current_line = n.readline()
	
	color_commands = re.compile(r'(base\s+|cycle\s+|[0-9a-f]{3,6})')
	other_commands = re.compile(r'(\w+)\s*')
	
	while current_line:
		color_match = color_commands.findall(current_line)
		other_match = other_commands.findall(current_line)
		if color_match:
			command = color_match.pop(0)
			if command.lower().startswith('base'):
				while color_match:
					base_palette.append(color_match.pop(0))
				print('- base palette: {}'.format(base_palette))
			if command.lower().startswith('cycle'):
				color_index = 0
				while color_match:
					cycle_palette.append(color_match.pop(0))
				print('- cycle palette: {}'.format(cycle_palette))
		if other_match:
			command = other_match.pop(0)
			if command.lower().startswith('dir'):
				palette_direction = other_match.pop(0)
		current_line = n.readline()

if (len(base_palette)==0):
	print("! Error: Base palette must be supplied by: base <hex> <hex> ...")
	sys.exit(1)

if (len(cycle_palette)==0):
	print("! Error: Cycle palette must be supplied by: cycle <hex> <hex> ...")
	sys.exit(1)

if (palette_direction==''):
	print("! Error: Cycle direction must be supplied by: dir <left|right>")
	sys.exit(1)
elif (re.match(VALID_DIR_RE_STRING, palette_direction)) is None:
	print("! Error: Direction must be one of {}".format(VALID_DIRECTIONS))
	sys.exit(1)
else:
	print("- cycle direction: {}".format(palette_direction))

if (len(base_palette) != len(cycle_palette)):
	print("! Error: colors in cycle palette must be the same as base palette!")
	sys.exit(1)
else:
	palette_len = len(cycle_palette)

try:
	base_image_fn = args.image
	base_image = Image.open(base_image_fn)
except IOError:
	print("! Error: can't load image {}".format(base_image_fn))
	sys.exit(1)

# rgb hex -> rgb, rgba tuple
#to_color = lambda x:tuple(int((x+'ff')[i:i+2], 16) for i in (0, 2, 4))
to_color_rgba = lambda x:tuple(int((x+'ff')[i:i+2], 16) for i in (0, 2, 4, 6))

# image -> pixel array
base_image_pixels = base_image.load()
print("- Loading base image")
image_width, image_height = base_image.size

# apply palette 0
for c in range(palette_len):
	print("- Processing cycle {}".format(c))
	current_image = Image.new('RGB', base_image.size)
	current_image_pixels = current_image.load()
	for h in range(image_width):
		for w in range(image_height):
			current_color = base_image_pixels[h,w]
			for j in range(palette_len):
				if current_color == to_color_rgba(base_palette[j]):
					current_color = to_color_rgba(cycle_palette[j])
			current_image_pixels[h,w] = current_color
	if palette_direction == 'left':
		cycle_palette.append(cycle_palette.pop(0))
	else:
		cycle_palette.insert(0, cycle_palette.pop())
	cycle_filename = '{}_{}.png'.format(args.output,c)
	current_image.save(cycle_filename)
	print("! Saved: {}".format(cycle_filename))
print("! All done!")
