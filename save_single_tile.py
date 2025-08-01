"""
Script to understand how to load WSIs using the OpenSlide library and extract tiles.
"""

import openslide

# Load the slide
slide_path = "path/to/slide.mrxs"  # Path to the .mrxs file

try:
    slide = openslide.OpenSlide(slide_path)
    print("Slide loaded successfully!")
except Exception as e:
    print(f"Failed to load slide: {e}")
    exit()

# Get thumbnail to explore image
thumbnail = slide.get_thumbnail((1000,1000))
thumbnail = thumbnail.convert("RGB")
thumbnail.save('thumbnail_example.png')

# Print metadata related to the bounds of the tissue
bounds_x = slide.properties.get("openslide.bounds-x", 0)
bounds_y = slide.properties.get("openslide.bounds-y", 0)
bounds_width = slide.properties.get("openslide.bounds-width", slide.level_dimensions[0][0])
bounds_height = slide.properties.get("openslide.bounds-height", slide.level_dimensions[0][1])

print("Bounds X:", bounds_x)
print("Bounds Y:", bounds_y)
print("Bounds Width:", bounds_width)
print("Bounds Height:", bounds_height)


# Extract a tile from the slide
try:
    tile = slide.read_region(
    location=(int(bounds_x), int(bounds_y)),
    level=0,
    size=(512, 512))
    print("Successfully read a region!")
except Exception as e:
    print(f"Failed to read region: {e}")

# Convert tile to RGB if necessary
tile = tile.convert("RGB")

# Save the tile
tile.save('tile_example.png')
