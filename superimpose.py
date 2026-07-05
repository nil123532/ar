import fitz  # PyMuPDF
from PIL import Image
import io

interaction_3D = "AR/3D_images/compound_a_b/enm_sup_b.png"
interaction_2D = "AR/2D_images/compound_a_b/compound_b.pdf"

# 1. Open the large PNG canvas
base = Image.open(interaction_3D).convert("RGBA")

# 2. Open and render the PDF overlay
pdf = fitz.open(interaction_2D)
page = pdf[0]  # first page of the PDF

# Render at higher resolution for clarity
pix = page.get_pixmap(matrix=fitz.Matrix(4, 4), alpha=True)

# Convert PDF page into a Pillow image
overlay = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGBA")

# 3. Resize the PDF overlay
# Example: make it 28% of the main PNG width
overlay_width = int(base.width * 0.28)
overlay_height = int(overlay.height * overlay_width / overlay.width)

overlay = overlay.resize(
    (overlay_width, overlay_height),
    Image.Resampling.LANCZOS
)

# 4. Place it at the bottom-right
margin = 150
x = base.width - overlay.width - margin
y = base.height - overlay.height - margin

base.alpha_composite(overlay, (x, y))

# 5. Save final image
base.convert("RGB").save(f"AR/combined/{interaction_3D.split('/')[-1]}", quality=95)