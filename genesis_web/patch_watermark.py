from PIL import Image

in_path = r"C:\Users\Gurid\.gemini\antigravity\brain\346939a0-d2b7-4b8b-b71b-05b4eb7be419\ink_painting_hero_1777228812383.png"
out_path = r"f:\Projects\Python\ZiJin\genesis_web\public\bg-zaishui.png"

try:
    img = Image.open(in_path)
    
    # 提取水印右侧天空区域的色块 (200,0) 到 (400,200)
    # 因为AI生成的水印通常在左上角 (0, 0) ~ (150, 150)
    box_source = (180, 0, 380, 200)
    patch = img.crop(box_source)
    
    # 水平翻转以制造自然的云雾过渡
    patch = patch.transpose(Image.FLIP_LEFT_RIGHT)
    
    # 将色块覆盖在左上角的水印区域
    img.paste(patch, (0, 0))
    
    # 向下可能还有小印章，用下方背景覆盖
    box_source_2 = (0, 250, 150, 350)
    patch_2 = img.crop(box_source_2)
    patch_2 = patch_2.transpose(Image.FLIP_TOP_BOTTOM)
    img.paste(patch_2, (0, 150))
    
    img.save(out_path)
    print("成功覆盖左上角水印！")
except Exception as e:
    print(f"Error: {e}")
