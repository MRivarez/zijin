from PIL import Image
import os

path_zaishui = r"C:\Users\Gurid\.gemini\antigravity\brain\346939a0-d2b7-4b8b-b71b-05b4eb7be419\ink_painting_hero_1777228812383.png"
path_zijin = r"C:\Users\Gurid\.gemini\antigravity\brain\346939a0-d2b7-4b8b-b71b-05b4eb7be419\qingqingzijin_hero_1777229103479.png"
out_zaishui = r"f:\Projects\Python\ZiJin\genesis_web\public\bg-zaishui.png"
out_zijin = r"f:\Projects\Python\ZiJin\genesis_web\public\bg-zijin.png"

def process_image(in_path, out_path, crop_profile):
    if not os.path.exists(in_path):
        print(f"File not found: {in_path}")
        return
    img = Image.open(in_path)
    w, h = img.size
    print(f"Original size: {img.size} for {in_path}")
    
    # Target is 16:9 aspect ratio
    target_ratio = 16 / 9
    
    # We will crop height to w / target_ratio
    new_h = int(w / target_ratio) # For 1024x1024, new_h = 576. Crop = 448
    
    if crop_profile == 'zaishui':
        # Crop more from the top to remove the "在墨画" watermark (top left)
        # e.g., cut 300px from top, 148px from bottom
        top = int(h * 0.3)
        bottom = top + new_h
        # safety check
        if bottom > h:
            bottom = h
            top = h - new_h
    elif crop_profile == 'zijin':
        # Center crop conceptually
        top = (h - new_h) // 2
        bottom = top + new_h
    else:
        top = (h - new_h) // 2
        bottom = top + new_h
        
    img_cropped = img.crop((0, top, w, bottom))
    img_resized = img_cropped.resize((1920, 1080), Image.Resampling.LANCZOS)
    img_resized.save(out_path)
    print(f"Saved {out_path} with size {img_resized.size}")

process_image(path_zaishui, out_zaishui, 'zaishui')
process_image(path_zijin, out_zijin, 'zijin')
