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

# 4. Draw Clover Hardware vector schematics
def draw_clover_hardware(draw, post_id, x, y, text_color, tag_bg):
    # Base coordinate (x, y) acts as the top-left of our 320x320 hardware canvas
    outline_color = text_color
    fill_color = tag_bg
    
    if post_id == 6:  # Clover Station Duo
        # Draw Merchant Screen Stand
        draw.polygon([(x+80, y+240), (x+140, y+240), (x+120, y+140), (x+100, y+140)], fill=outline_color)
        # Draw Merchant Screen (Big tilted box)
        draw.rounded_rectangle([x+10, y+40, x+190, y+150], radius=10, fill=fill_color, outline=outline_color, width=3)
        draw.rounded_rectangle([x+20, y+50, x+180, y+140], radius=5, fill=None, outline=outline_color, width=1)
        
        # Customer Screen Stand
        draw.polygon([(x+190, y+240), (x+240, y+240), (x+220, y+180), (x+200, y+180)], fill=outline_color)
        # Customer Screen (Smaller tilted box facing user)
        draw.rounded_rectangle([x+170, y+110, x+270, y+180], radius=8, fill=fill_color, outline=outline_color, width=3)
        draw.rounded_rectangle([x+178, y+118, x+262, y+172], radius=4, fill=None, outline=outline_color, width=1)
        # Small circular tap icon representation
        draw.arc([x+210, y+130, x+230, y+150], start=0, end=360, fill=outline_color, width=2)
        
    elif post_id == 7:  # Clover Station Solo
        # Swiveling Stand base
        draw.polygon([(x+100, y+250), (x+200, y+250), (x+160, y+140), (x+140, y+140)], fill=outline_color)
        draw.ellipse([x+135, y+125, x+165, y+155], fill=fill_color, outline=outline_color, width=2)
        # Massive 14-inch Screen
        draw.rounded_rectangle([x+30, y+30, x+270, y+170], radius=15, fill=fill_color, outline=outline_color, width=4)
        draw.rounded_rectangle([x+45, y+45, x+255, y+155], radius=10, fill=None, outline=outline_color, width=2)
        # Menu grid mockup inside the screen
        draw.rectangle([x+60, y+60, x+110, y+90], fill=outline_color)
        draw.rectangle([x+120, y+60, x+240, y+70], fill=outline_color)
        draw.rectangle([x+120, y+80, x+210, y+90], fill=outline_color)
        
    elif post_id == 8:  # Commercial Power Counter Setup
        # Solid Cash Drawer Base
        draw.rounded_rectangle([x+10, y+210, x+290, y+260], radius=5, fill=fill_color, outline=outline_color, width=3)
        draw.line([x+10, y+235, x+290, y+235], fill=outline_color, width=2)
        draw.ellipse([x+145, y+218, x+155, y+228], fill=outline_color)
        
        # Terminal Screen Mount
        draw.polygon([(x+80, y+210), (x+130, y+210), (x+115, y+120), (x+95, y+120)], fill=outline_color)
        # Main Screen
        draw.rounded_rectangle([x+30, y+40, x+180, y+130], radius=10, fill=fill_color, outline=outline_color, width=3)
        
        # Receipts Thermal Printer Next Door
        draw.rounded_rectangle([x+195, y+120, x+280, y+210], radius=8, fill=fill_color, outline=outline_color, width=3)
        draw.rectangle([x+210, y+130, x+265, y+138], fill=outline_color)
        draw.polygon([(x+215, y+138), (x+260, y+138), (x+255, y+185), (x+220, y+185)], fill=outline_color)
        
    elif post_id == 9:  # Always Connected Offline Processing
        # Screen Box
        draw.rounded_rectangle([x+40, y+40, x+260, y+180], radius=12, fill=fill_color, outline=outline_color, width=3)
        # Stand base
        draw.polygon([(x+120, y+240), (x+180, y+240), (x+160, y+180), (x+140, y+180)], fill=outline_color)
        # Draw 4 cellular antenna signal bars inside
        draw.rectangle([x+70, y+140, x+85, y+155], fill=outline_color)
        draw.rectangle([x+95, y+125, x+110, y+155], fill=outline_color)
        draw.rectangle([x+120, y+110, x+135, y+155], fill=outline_color)
        draw.rectangle([x+145, y+95, x+160, y+155], fill=outline_color)
        
        # Giant circular checkmark icon badge (LTE Active)
        draw.ellipse([x+185, y+85, x+235, y+135], fill=outline_color)
        draw.line([x+198, y+112, x+208, y+122], fill=fill_color, width=3)
        draw.line([x+208, y+122, x+225, y+102], fill=fill_color, width=3)
        
    elif post_id == 10:  # Complete Clover POS Unified Ecosystem
        # Main Station terminal screen on left
        draw.rounded_rectangle([x+10, y+60, x+160, y+160], radius=8, fill=fill_color, outline=outline_color, width=3)
        draw.polygon([(x+60, y+230), (x+110, y+230), (x+95, y+160), (x+75, y+160)], fill=outline_color)
        
        # Handheld Clover Flex terminal on right
        draw.rounded_rectangle([x+185, y+70, x+285, y+230], radius=15, fill=fill_color, outline=outline_color, width=3)
        draw.rounded_rectangle([x+195, y+85, x+275, y+175], radius=5, fill=None, outline=outline_color, width=1.5)
        draw.rectangle([x+205, y+190, x+265, y+205], fill=outline_color)
        
        # Sleek connection wifi wave arch linking screens
        draw.arc([x+120, y+70, x+190, y+130], start=210, end=330, fill=outline_color, width=2)


# 5. Image Generation Configs (Now extended to 10 Posts)
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
    },
    # ------------------ NEW CLOVER STATION HARDWARE POSTS (6 - 10) ------------------
    {
        "id": 6,
        "bg": "#264653",       # Dark Charcoal Slate
        "text_color": "#F1FAEE", # Ice White
        "tag": "CLOVER STATION DUO",
        "tag_bg": "#F4A261",    # Warm Orange Accent
        "title": "Dual-Screen Speed. Zero Checkout Friction.",
        "bullets": [
            "Double screens: One for servers, one for guests",
            "Customer-facing screen for fast tap, tips, & receipts",
            "Instantly captures loyal guests on order confirmation"
        ],
        "footer": "Upgrade Your Counter | sevenflow.ca/clover"
    },
    {
        "id": 7,
        "bg": "#1D3557",       # Royal Navy Blue
        "text_color": "#FFFFFF",
        "tag": "CLOVER STATION SOLO",
        "tag_bg": "#E9C46A",    # Gold Accent
        "title": "The Ultimate Full-Service Command Center.",
        "bullets": [
            "Massive 14\" high-definition swiveling touchscreen",
            "Visual table mapping, courses, & bar tab pacing",
            "Custom system menu build by local tech advisors"
        ],
        "footer": "Power Your Restaurant | sevenflow.ca/clover"
    },
    {
        "id": 8,
        "bg": "#E07A5F",       # Warm Terracotta
        "text_color": "#F4F1DE", # Cream text
        "tag": "COMMERCIAL STRENGTH",
        "tag_bg": "#2D3142",    # Dark Slate
        "title": "Clover Station Hardware vs. Flimsy iPads.",
        "bullets": [
            "Heavy-duty metal construction built for hot kitchens",
            "High-speed thermal printer & secure cash drawer",
            "Ditch loose terminal wires and messy charging stands"
        ],
        "footer": "Built for Food Service | sevenflow.ca/clover"
    },
    {
        "id": 9,
        "bg": "#2A9D8F",       # Warm Emerald Teal
        "text_color": "#FFFFFF",
        "tag": "FAIL-SAFE OFFLINE",
        "tag_bg": "#E76F51",    # Burnt Coral
        "title": "No Wi-Fi? No Problem. Keep Taking Payments.",
        "bullets": [
            "Built-in offline mode processes card payments safely",
            "Automatic fallback to LTE backup network if Wi-Fi drops",
            "Never turn away diners or lose revenue during a storm"
        ],
        "footer": "Never Lose a Sale | sevenflow.ca/clover"
    },
    {
        "id": 10,
        "bg": "#3D5A80",       # Slate Blue
        "text_color": "#F1FAEE", # Off-White
        "tag": "CLOVER ECOSYSTEM",
        "tag_bg": "#EE6C4D",    # Bright Orange
        "title": "One Unified Ecosystem. Desk to Patio.",
        "bullets": [
            "Station Duo for front counters, Clover Flex for tableside",
            "Full real-time syncing of menus, seats, and pricing",
            "Local 24/7 technical support backed by SevenDesk"
        ],
        "footer": "Unify Your Tech | sevenflow.ca/clover"
    }
]

# 6. Render loop
os.makedirs("output_images", exist_ok=True)
print("Rendering 10 Instagram posts with customized layouts...")

for post in posts:
    img = Image.new("RGB", (1080, 1080), post["bg"])
    draw = ImageDraw.Draw(img)
    
    # Fetch fonts
    font_tag = get_font(24, bold=True)
    font_title = get_font(50, bold=True)
    font_bullets = get_font(32, bold=False)
    font_footer = get_font(28, bold=True)
    
    # Draw elegant inner border
    draw.rectangle([40, 40, 1040, 1040], outline=post["text_color"], width=4)
    
    # Draw Pill Tag
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
    
    # Text color inside the Pill Tag
    tag_text_color = "#FFFFFF" if post["bg"] != "#F4F1DE" else "#F4F1DE"
    draw.text((100 + pad_x, 100 + pad_y), tag_text, font=font_tag, fill=tag_text_color)
    
    # Draw Bold Title
    title_y = draw_multiline_text(
        draw, post["title"], font_title, post["text_color"], 
        max_width=880, start_x=100, start_y=180 + tag_h
    )
    
    # Determine Layout: For Posts 6 to 10, use split-panel layout to draw Clover Hardware
    is_hardware_post = post["id"] >= 6
    bullet_max_width = 460 if is_hardware_post else 780
    
    # Draw Bullet Points
    bullet_y = title_y + 60
    for bullet in post["bullets"]:
        # Draw sleek bullet checkbox/accent
        checkbox_rect = [100, bullet_y + 8, 124, bullet_y + 32]
        draw.rectangle(checkbox_rect, fill=post["tag_bg"] if post["bg"] != "#F4F1DE" else post["text_color"])
        
        # Draw text beside checkbox
        bullet_y = draw_multiline_text(
            draw, bullet, font_bullets, post["text_color"],
            max_width=bullet_max_width, start_x=150, start_y=bullet_y
        ) + 40
        
    # If this is a hardware post (6-10), draw the custom vector schematic on the right panel
    if is_hardware_post:
        draw_clover_hardware(draw, post["id"], x=640, y=420, text_color=post["text_color"], tag_bg=post["tag_bg"])
        
    # Draw Footer CTA Button/Box
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

print("All 10 posts successfully generated in 'output_images/'!")
