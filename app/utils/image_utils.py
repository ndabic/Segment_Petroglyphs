import svgwrite

# Define custom colors for masks (RGB)
def rgb(r, g, b):
    return "rgb({}, {}, {})".format(r, g, b)


# Function to create SVG content
def create_svg_content(results, img_str, transparency_svg, current_img, mask_color):
    height, width, _ = current_img.shape
    dwg = svgwrite.Drawing(profile='tiny', size=(width, height))
    
    # Add background image
    image_element = dwg.image(href='data:image/jpeg;base64,' + img_str, insert=(0, 0), size=(width, height))
    dwg.add(image_element)
    
    # Add segmentation masks
    if results[0].masks != None:
        for mask in results[0].masks.xy:
            points = [(int(point[0]), int(point[1])) for point in mask]
            color = rgb(mask_color[0], mask_color[1] , mask_color[2])
            dwg.add(dwg.polygon(points, fill=color, fill_opacity=transparency_svg, stroke=color, stroke_opacity= transparency_svg))
    
    return dwg.tostring()

