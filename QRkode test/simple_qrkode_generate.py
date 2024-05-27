import qrcode

for i in range(1, 11):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(f'bagage/{i}')
    qr.make(fit=True)  

    img = qr.make_image(fill_color="rgb(211, 187, 123)", back_color="rgb(0, 29, 19)")

    img.save(f"qrcode_{i}.png")
