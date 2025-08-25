from PIL import Image, ImageChops, ImageStat

def image_diff_score(img1_path: str, img2_path: str):
    im1 = Image.open(img1_path).convert("RGB")
    im2 = Image.open(img2_path).convert("RGB")
    # Resize to smallest common to avoid size mismatch
    w = min(im1.width, im2.width)
    h = min(im1.height, im2.height)
    im1 = im1.crop((0,0,w,h))
    im2 = im2.crop((0,0,w,h))
    diff = ImageChops.difference(im1, im2)
    stat = ImageStat.Stat(diff)
    mean = sum(stat.mean) / len(stat.mean)
    return mean, diff  # mean intensity as a simple score, and diff image object