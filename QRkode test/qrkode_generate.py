import qrcode
img = qrcode.make('Google.com')
type(img) 
img.save("qrcode1.png")

#Link til kodehjælp: https://medium.com/@reegan_anne/fully-customizable-qr-codes-in-python-7eb8a7c3b0da