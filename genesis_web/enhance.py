from PIL import Image, ImageFilter

paths = [
    r"f:\Projects\Python\ZiJin\genesis_web\public\bg-zijin.png",
    r"f:\Projects\Python\ZiJin\genesis_web\public\bg-zaishui.png"
]

def process():
    for p in paths:
        try:
            print("Enhancing", p)
            img = Image.open(p).convert("RGB")
            # 1. 提升分辨率: 2倍 Lanczos 采样，画质最平滑自然
            new_size = (img.width * 2, img.height * 2)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            
            # 2. 增强颗粒感与清晰度：
            # 强化 UnsharpMask 可以将 AI 画作本身隐藏的“宣纸/画布”微小噪点提纯，直接形成极好的真实颗粒感
            img = img.filter(ImageFilter.UnsharpMask(radius=3, percent=200, threshold=1))
            img = img.filter(ImageFilter.UnsharpMask(radius=1, percent=100, threshold=1))
            
            img.save(p, quality=98)
            print("Successfully enhanced:", p)
        except Exception as e:
            print(f"Error on {p}: {e}")

process()
