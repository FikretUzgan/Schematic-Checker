"""
Create application icon for Auto_Altium Rating Verification Tool
Generates a professional icon with circuit board theme and checkmark
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Create a 256x256 icon with circuit board and checkmark design"""
    
    # Create image with transparent background
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw rounded square background (PCB green)
    margin = 20
    pcb_green = (34, 139, 34, 255)  # Forest green for PCB
    draw.rounded_rectangle(
        [(margin, margin), (size-margin, size-margin)],
        radius=30,
        fill=pcb_green,
        outline=(20, 80, 20, 255),
        width=4
    )
    
    # Draw circuit traces (copper color)
    copper = (184, 115, 51, 255)
    trace_width = 6
    
    # Horizontal traces
    for y in [60, 100, 140, 180, 220]:
        draw.line([(40, y), (size-40, y)], fill=copper, width=trace_width)
    
    # Vertical traces
    for x in [60, 120, 180]:
        draw.line([(x, 50), (x, size-50)], fill=copper, width=trace_width)
    
    # Draw component pads (solder mask)
    pad_color = (220, 220, 220, 255)
    pad_size = 12
    for x in [60, 120, 180]:
        for y in [60, 100, 140, 180]:
            draw.ellipse(
                [(x-pad_size, y-pad_size), (x+pad_size, y+pad_size)],
                fill=pad_color,
                outline=copper,
                width=2
            )
    
    # Draw large checkmark overlay (white with shadow)
    check_color = (255, 255, 255, 255)
    check_shadow = (0, 0, 0, 128)
    check_width = 20
    
    # Shadow
    check_points = [
        (80, 150),
        (110, 180),
        (190, 90)
    ]
    for i in range(len(check_points)-1):
        draw.line([check_points[i], check_points[i+1]], fill=check_shadow, width=check_width+4)
    
    # Main checkmark
    check_points = [
        (75, 145),
        (105, 175),
        (185, 85)
    ]
    for i in range(len(check_points)-1):
        draw.line([check_points[i], check_points[i+1]], fill=check_color, width=check_width)
    
    # Draw "R C L" text in corner (component types)
    try:
        # Try to use a system font
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        # Fallback to default font
        font = ImageFont.load_default()
    
    text_color = (255, 255, 255, 200)
    draw.text((35, size-50), "R C L", fill=text_color, font=font)
    
    # Save as PNG first
    png_path = os.path.join(os.path.dirname(__file__), 'resources', 'app_icon.png')
    os.makedirs(os.path.dirname(png_path), exist_ok=True)
    img.save(png_path, 'PNG')
    print(f"Created PNG icon: {png_path}")
    
    # Create multiple sizes for .ico file
    icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    icons = []
    
    for icon_size in icon_sizes:
        resized = img.resize(icon_size, Image.Resampling.LANCZOS)
        icons.append(resized)
    
    # Save as .ico file
    ico_path = os.path.join(os.path.dirname(__file__), 'resources', 'app_icon.ico')
    icons[0].save(ico_path, format='ICO', sizes=icon_sizes)
    print(f"Created ICO icon: {ico_path}")
    
    return ico_path, png_path

if __name__ == "__main__":
    print("Generating application icon...")
    ico_path, png_path = create_icon()
    print("\n✅ Icon creation complete!")
    print(f"   ICO: {os.path.abspath(ico_path)}")
    print(f"   PNG: {os.path.abspath(png_path)}")
