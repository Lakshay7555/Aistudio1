import os
import sys
import subprocess

# 1. Programmatically ensure Pillow is installed
try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Pillow not found. Installing programmatically...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow", "--break-system-packages"])
    from PIL import Image, ImageDraw, ImageFont

print("Pillow successfully loaded.")

# 2. Find a suitable TrueType Font on various systems
def get_font(size, bold=False):
    font_paths = [
        # Linux paths
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/liberation/LiberationSans.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if bold else "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
        # macOS paths
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        # Windows paths
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
    ]
    for path in font_paths:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    # Default fallback
    return ImageFont.load_default()

# 3. Text wrapper helper
def draw_multiline_text(draw, text, font, color, max_width, start_x, start_y, line_spacing=1.2):
    words = text.split(' ')
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        line_str = ' '.join(current_line)
        if hasattr(font, 'getbbox'):
            w = font.getbbox(line_str)[2] - font.getbbox(line_str)[0]
        else:
            w = draw.textlength(line_str, font=font)
            
        if w > max_width:
            current_line.pop()
            lines.append(' '.join(current_line))
            current_line = [word]
    if current_line:
        lines.append(' '.join(current_line))
        
    y = start_y
    sample = "Xy"
    if hasattr(font, 'getbbox'):
        line_height = (font.getbbox(sample)[3] - font.getbbox(sample)[1]) * line_spacing
    else:
        line_height = 20 * line_spacing
        
    for line in lines:
        draw.text((start_x, y), line, font=font, fill=color)
        y += line_height
    return y

# 4. Image Generation Configs
posts = [
    {
        "id": 1,
        "bg": "#E07A5F",       # Terracotta Coral
        "text_color": "#F4F1DE", # Cream
        "tag": "PROFIT MAXIMIZER",
        "tag_bg": "#3D5A80",
        "title": "Stop Giving 30% of Your Profits to Delivery Apps",
        "bullets": [
            "Keep 100% of your hard-earned order revenue",
            "Launch your own commission-free online ordering",
            "Fully synced with your in-store Clover POS system"
        ],
        "footer": "Learn Direct Ordering | sevenflow.ca/clover"
    },
    {
        "id": 2,
        "bg": "#2A9D8F",       # Warm Teal/Green
        "text_color": "#FFFFFF",
        "tag": "SMART OPERATIONS",
        "tag_bg": "#264653",
        "title": "Front-of-House meets Back-of-House",
        "bullets": [
            "Orders fire to the kitchen terminal instantly",
            "Perfect modifier accuracy (no lost paper tickets)",
            "Seamless tableside & online flow"
        ],
        "footer": "Unify Your Kitchen | sevenflow.ca/clover"
    },
    {
        "id": 3,
        "bg": "#264653",       # Deep Charcoal Slate
        "text_color": "#E9C46A", # Vibrant Yellow Gold
        "tag": "PATIO POWERHOUSE",
        "tag_bg": "#E76F51",
        "title": "Bring Your Entire POS Direct to the Tableside",
        "bullets": [
            "Accept secure chip & tap payments with Clover Flex",
            "Take orders on-the-go to boost patio speed",
            "Prompt for tips smoothly to delight your staff"
        ],
        "footer": "Get Clover Flex | sevenflow.ca/clover"
    },
    {
        "id": 4,
        "bg": "#F4F1DE",       # Clean Warm Cream
        "text_color": "#264653", # Deep Slate
        "tag": "RESTAURANT ANALYTICS",
        "tag_bg": "#E07A5F",
        "title": "Stop Guessing. Start Growing.",
        "bullets": [
            "Track real-time sales directly from your phone",
            "Automated low-inventory alerts for ingredients",
            "Optimize menus based on top-performing items"
        ],
        "footer": "Download Our Free Tech Guide | sevenflow.ca/clover"
    },
    {
        "id": 5,
        "bg": "#1D3557",       # Premium Royal Blue
        "text_color": "#F1FAEE", # Ice Blue/Cream
        "tag": "LOCAL ADVISORS",
        "tag_bg": "#E63946",
        "title": "Tired of generic tech support on hold?",
        "bullets": [
            "Custom menu, modifiers, and floor plan setup",
            "In-person & virtual training for your entire staff",
            "24/7 Ongoing IT support backed by SevenDesk"
        ],
        "footer": "Based in Edmonton, Serving Canada | sevenflow.ca"
    }
]

# 5. Render loop
os.makedirs("output_images", exist_ok=True)
print("Rendering 5 Instagram posts...")

for post in posts:
    img = Image.new("RGB", (1080, 1080), post["bg"])
    draw = ImageDraw.Draw(img)
    
    font_tag = get_font(24, bold=True)
    font_title = get_font(52, bold=True)
    font_bullets = get_font(32, bold=False)
    font_footer = get_font(28, bold=True)
    
    # Elegant inner border frame
    draw.rectangle([40, 40, 1040, 1040], outline=post["text_color"], width=4)
    
    # Pill Tag
    tag_text = post["tag"]
    if hasattr(font_tag, 'getbbox'):
        tag_w = font_tag.getbbox(tag_text)[2] - font_tag.getbbox(tag_text)[0]
        tag_h = font_tag.getbbox(tag_text)[3] - font_tag.getbbox(tag_text)[1]
    else:
        tag_w = draw.textlength(tag_text, font=font_tag)
        tag_h = 24
        
    pad_x, pad_y = 20, 12
    tag_rect = [100, 100, 100 + tag_w + pad_x*2, 100 + tag_h + pad_y*2]
    draw.rounded_rectangle(tag_rect, radius=15, fill=post["tag_bg"])
    draw.text((100 + pad_x, 100 + pad_y), tag_text, font=font_tag, fill="#FFFFFF" if post["bg"] != "#F4F1DE" else "#F4F1DE")
    
    # Bold Title
    title_y = draw_multiline_text(
        draw, post["title"], font_title, post["text_color"], 
        max_width=880, start_x=100, start_y=180 + tag_h
    )
    
    # Bullet Points
    bullet_y = title_y + 60
    for bullet in post["bullets"]:
        # Custom checkbox bullet shape
        checkbox_rect = [100, bullet_y + 8, 124, bullet_y + 32]
        draw.rectangle(checkbox_rect, fill=post["tag_bg"] if post["bg"] != "#F4F1DE" else post["text_color"])
        
        bullet_y = draw_multiline_text(
            draw, bullet, font_bullets, post["text_color"],
            max_width=780, start_x=150, start_y=bullet_y
        ) + 40
        
    # Footer Button
    footer_text = post["footer"]
    if hasattr(font_footer, 'getbbox'):
        footer_w = font_footer.getbbox(footer_text)[2] - font_footer.getbbox(footer_text)[0]
    else:
        footer_w = draw.textlength(footer_text, font=font_footer)
        
    footer_box = [540 - footer_w//2 - 30, 920, 540 + footer_w//2 + 30, 980]
    draw.rounded_rectangle(footer_box, radius=10, fill=post["tag_bg"] if post["bg"] != "#F4F1DE" else post["text_color"])
    
    footer_text_color = "#FFFFFF" if post["bg"] != "#F4F1DE" else "#F4F1DE"
    draw.text((540 - footer_w//2, 932), footer_text, font=font_footer, fill=footer_text_color)
    
    # Save Image
    filename = f"output_images/post{post['id']}.png"
    img.save(filename, "PNG")
    print(f"Saved: {filename}")

print("All 5 posts successfully generated in 'output_images/'!")