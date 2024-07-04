import svgwrite
import os
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import unary_union

# Define custom colors for masks (RGB)
def rgb(r, g, b):
    return "rgb({}, {}, {})".format(r, g, b)


# Function to create SVG content
def create_svg_content(polygons, img_str, transparency_svg, current_img, mask_color, image_path):
    height, width, _ = current_img.shape
    dwg = svgwrite.Drawing(profile='tiny', size=(width, height))
    
    # Add background image
    image_element = dwg.image(href='data:image/jpeg;base64,' + img_str, insert=(0, 0), size=(width, height))
    dwg.add(image_element)
    
    # Extract image name without extension
    image_name = os.path.splitext(os.path.basename(image_path))[0]

    # Add segmentation masks
    if polygons != None:
        for i, polygon in enumerate(polygons):
            points = [(int(point[0]), int(point[1])) for point in polygon.exterior.coords]
            color = rgb(mask_color[0], mask_color[1] , mask_color[2])
            dwg.add(dwg.polygon(
                points, 
                fill=color, 
                fill_opacity=transparency_svg, 
                stroke=color, 
                stroke_opacity= transparency_svg,
                id = f'{image_name}.{i+1}'
                ))
    
    return dwg.tostring()

def point_in_polygon(x, y, polygon):
        # Ray-Casting algorithm to check if a point is inside a polygon
        n = len(polygon.exterior.coords)
        inside = False
        p1x, p1y = polygon.exterior.coords[0]
        for i in range(n + 1):
            p2x, p2y = polygon.exterior.coords[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

def mask2polygon(results):
    # Collect all polygons
    polygons = []
    masks = results[0].masks.xy
    if results[0].masks is not None:
        for i in range(len(masks)):
            points = [(int(point[0]), int(point[1])) for point in masks[i]]
            polygons.append(Polygon(points))
    else:
        polygons = None
    
    return polygons

def merge_polygons(polygons):    
    # Merge overlapping polygons
    merged_polygons = unary_union(polygons)
        
    # Check if the result is MultiPolygon
    if isinstance(merged_polygons, MultiPolygon):
        merged_polygons = list(merged_polygons.geoms)  # Convert MultiPolygon to list of Polygons
    else:
        merged_polygons = [merged_polygons]  # Convert single Polygon to a list

    return merged_polygons