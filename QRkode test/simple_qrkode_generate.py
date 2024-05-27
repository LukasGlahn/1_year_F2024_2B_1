import qrcode
from PIL import Image

# List of data to be encoded in QR codes (for example purposes, using a simple range)
data_list = [f'QR Code {i+1}' for i in range(99)]

# Function to create a QR code
def create_qr_code(data, fill_color="blue", back_color="white"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    return img

# Create QR code images and store them in a list
qr_images = [create_qr_code(data) for data in data_list]

# Set DPI and calculate A1 paper size in pixels
dpi = 300
a1_width_mm = 841
a1_height_mm = 594
a1_width_px = int(a1_width_mm * dpi / 25.4)
a1_height_px = int(a1_height_mm * dpi / 25.4)

# Determine grid size (10x10 grid will fit 100 QR codes, we only need 99)
cols = 10  # Number of columns of QR codes
rows = 10  # Number of rows of QR codes

# Calculate size for each QR code to fit within A1 dimensions
qr_width_px = a1_width_px // cols
qr_height_px = a1_height_px // rows
qr_size = min(qr_width_px, qr_height_px)

# Resize QR codes to fit the calculated size
# Resize QR codes to fit the calculated size with anti-aliasing
qr_images_resized = [img.resize((qr_size, qr_size), Image.LANCZOS) for img in qr_images]


# Create a blank combined image with A1 dimensions
combined_image = Image.new('RGB', (a1_width_px, a1_height_px), "white")

# Paste each QR code image into the combined image
for row in range(rows):
    for col in range(cols):
        index = row * cols + col
        if index < len(qr_images_resized):
            position = (col * qr_size, row * qr_size)
            combined_image.paste(qr_images_resized[index], position)

# Save the combined image
combined_image.save("combined_qrcodes_a1.png", dpi=(dpi, dpi))

print("All QR codes have been combined and saved as 'combined_qrcodes_a1.png'.")




#Link til custom qr kode hjælp: https://medium.com/@reegan_anne/fully-customizable-qr-codes-in-python-7eb8a7c3b0da