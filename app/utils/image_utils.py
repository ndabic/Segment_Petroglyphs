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
            exterior_coords = [(int(point[0]), int(point[1])) for point in polygon.exterior.coords]
            color = rgb(mask_color[0], mask_color[1], mask_color[2])
            path_data = f'M {exterior_coords[0][0]},{exterior_coords[0][1]} ' + ' '.join([f'L {x},{y}' for x, y in exterior_coords[1:]]) + ' Z'
            

            for interior in polygon.interiors:
                interior_coords = [(int(point[0]), int(point[1])) for point in interior.coords]
                path_data += f' M {interior_coords[0][0]},{interior_coords[0][1]} ' + ' '.join([f'L {x},{y}' for x, y in interior_coords[1:]]) + ' Z'
        
            dwg.add(dwg.path(
                d=path_data,
                fill=color,
                fill_opacity=transparency_svg,
                stroke=color,
                stroke_opacity=transparency_svg,
                id=f'{image_name}.{i}'  # Naming the polygon with image name and index
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
    if results[0].masks is not None:
        masks = results[0].masks.xy
        
        for i in range(len(masks)):
            points = [(int(point[0]), int(point[1])) for point in masks[i]]
            polygons.append(Polygon(points))
    else:
        polygons = None
    
    return polygons

def merge_polygons(polygons):    
    valid_polygons = []
    if polygons is not None:
        for polygon in polygons:
            if not polygon.is_valid:
                polygon = polygon.buffer(0)
            valid_polygons.append(polygon)

        merged_polygons = unary_union(valid_polygons)

        if isinstance(merged_polygons, MultiPolygon):
            return list(merged_polygons.geoms)
        else:
            return [merged_polygons]
    else:
        return None