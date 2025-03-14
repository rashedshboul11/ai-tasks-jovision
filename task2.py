from PIL import Image

img = Image.open('./test.jpg')
w ,h = img.size

gray_img = Image.new("RGB", (w, h))

for x in range(w):
    for y in range(h):
        r, g, b = img.getpixel((x, y))
        gray = int(0.299 * r + 0.587 * g + 0.114 * b)
        gray_img.putpixel((x,y), (gray, gray, gray))
    
gray_img.save('test_gray.jpg')
gray_img.show()


