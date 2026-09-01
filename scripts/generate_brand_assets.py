"""Generate HumanTone favicon and social preview assets."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "images"
FONT_REGULAR = Path(r"C:\Windows\Fonts\segoeui.ttf")
FONT_SEMIBOLD = Path(r"C:\Windows\Fonts\seguisb.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\segoeuib.ttf")


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size)


def mix(start: tuple[int, ...], end: tuple[int, ...], amount: float) -> tuple[int, ...]:
    return tuple(round(a + (b - a) * amount) for a, b in zip(start, end))


def gradient(size: tuple[int, int], start: tuple[int, ...], end: tuple[int, ...], horizontal=False) -> Image.Image:
    width, height = size
    image = Image.new("RGBA", size)
    draw = ImageDraw.Draw(image)
    length = width if horizontal else height
    for position in range(length):
        color = mix(start, end, position / max(length - 1, 1))
        if horizontal:
            draw.line((position, 0, position, height), fill=color)
        else:
            draw.line((0, position, width, position), fill=color)
    return image


def add_glow(image: Image.Image, center: tuple[int, int], radius: int, color: tuple[int, int, int, int]) -> None:
    glow = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(glow)
    x, y = center
    draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)
    glow = glow.filter(ImageFilter.GaussianBlur(radius // 2))
    image.alpha_composite(glow)


def create_logo(size: int, inset: int = 0) -> Image.Image:
    canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    icon_size = size - inset * 2
    icon = Image.new("RGBA", (icon_size, icon_size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(icon)
    radius = max(4, round(icon_size * 0.27))
    draw.rounded_rectangle((0, 0, icon_size - 1, icon_size - 1), radius=radius, fill=(11, 18, 32, 255))

    mark = gradient((icon_size, icon_size), (139, 112, 255, 255), (45, 211, 193, 255), horizontal=True)
    mask = Image.new("L", (icon_size, icon_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    stroke = max(2, round(icon_size * 0.13))
    left = round(icon_size * 0.29)
    right = round(icon_size * 0.71)
    top = round(icon_size * 0.25)
    bottom = round(icon_size * 0.75)
    middle = round(icon_size * 0.5)
    mask_draw.rounded_rectangle((left, top, left + stroke, bottom), radius=stroke // 3, fill=255)
    mask_draw.rounded_rectangle((right - stroke, top, right, bottom), radius=stroke // 3, fill=255)
    mask_draw.rounded_rectangle((left, middle - stroke // 2, right, middle + stroke // 2), radius=stroke // 3, fill=255)
    icon.alpha_composite(Image.composite(mark, Image.new("RGBA", mark.size), mask))
    canvas.alpha_composite(icon, (inset, inset))
    return canvas


def save_icons() -> None:
    master = create_logo(512)
    master.resize((16, 16), Image.Resampling.LANCZOS).save(OUTPUT / "favicon-16x16.png")
    master.resize((32, 32), Image.Resampling.LANCZOS).save(OUTPUT / "favicon-32x32.png")

    for size, filename in (
        (180, "apple-touch-icon.png"),
        (192, "android-chrome-192x192.png"),
        (512, "android-chrome-512x512.png"),
    ):
        app_icon = Image.new("RGBA", (size, size), (11, 18, 32, 255))
        safe_logo = create_logo(size, inset=round(size * 0.18))
        app_icon.alpha_composite(safe_logo)
        app_icon.convert("RGB").save(OUTPUT / filename, optimize=True)

    master.save(OUTPUT / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])


def save_social_preview() -> None:
    size = (1200, 630)
    canvas = gradient(size, (8, 13, 23, 255), (7, 18, 26, 255), horizontal=True)
    add_glow(canvas, (100, 90), 260, (118, 84, 255, 75))
    add_glow(canvas, (1120, 545), 310, (35, 205, 187, 62))
    draw = ImageDraw.Draw(canvas)

    for x in range(0, size[0], 56):
        draw.line((x, 0, x, size[1]), fill=(255, 255, 255, 8), width=1)
    for y in range(0, size[1], 56):
        draw.line((0, y, size[0], y), fill=(255, 255, 255, 8), width=1)

    draw.rounded_rectangle((47, 47, 1153, 583), radius=34, fill=(10, 16, 28, 210), outline=(255, 255, 255, 25), width=2)
    logo = create_logo(64)
    canvas.alpha_composite(logo, (86, 82))
    draw.text((169, 92), "HumanTone", font=font(FONT_BOLD, 32), fill=(246, 248, 252, 255))
    draw.text((169, 128), "OPEN-SOURCE WRITING TOOLKIT", font=font(FONT_SEMIBOLD, 14), fill=(75, 211, 197, 255))

    draw.text((86, 218), "Keep your voice.", font=font(FONT_BOLD, 70), fill=(250, 251, 253, 255))
    accent = gradient((650, 82), (163, 142, 255, 255), (70, 218, 203, 255), horizontal=True)
    text_mask = Image.new("L", accent.size, 0)
    ImageDraw.Draw(text_mask).text((0, -7), "Lose the AI tone.", font=font(FONT_BOLD, 70), fill=255)
    canvas.alpha_composite(Image.composite(accent, Image.new("RGBA", accent.size), text_mask), (86, 300))

    draw.text(
        (89, 411),
        "Prompts, guidelines, and examples for AI-assisted writing",
        font=font(FONT_REGULAR, 25),
        fill=(171, 181, 198, 255),
    )
    draw.text(
        (89, 448),
        "that still sounds like you.",
        font=font(FONT_REGULAR, 25),
        fill=(171, 181, 198, 255),
    )

    draw.rounded_rectangle((86, 517, 290, 553), radius=18, fill=(139, 112, 255, 32), outline=(139, 112, 255, 65))
    draw.text((108, 526), "PROMPTS", font=font(FONT_SEMIBOLD, 14), fill=(203, 194, 255, 255))
    draw.rounded_rectangle((307, 517, 521, 553), radius=18, fill=(45, 211, 193, 24), outline=(45, 211, 193, 60))
    draw.text((331, 526), "GUIDELINES", font=font(FONT_SEMIBOLD, 14), fill=(150, 231, 221, 255))
    draw.text((825, 526), "kamrullab.github.io/HumanTone", font=font(FONT_SEMIBOLD, 18), fill=(118, 130, 150, 255))
    canvas.convert("RGB").save(OUTPUT / "og-image.png", quality=95, optimize=True)


if __name__ == "__main__":
    OUTPUT.mkdir(parents=True, exist_ok=True)
    save_icons()
    save_social_preview()
    print("Generated HumanTone brand assets.")
