from PIL import Image, ImageFont, ImageDraw 

my_image = Image.open("images/quote-supergirl.png")

title_text = "\"Teste\""

title_font = ImageFont.truetype('fonts/Roboto-Regular.ttf', 50)

image_editable = ImageDraw.Draw(my_image)

image_editable.text((660,124), title_text, (245, 232, 230), font=title_font)

my_image.save("result.png")