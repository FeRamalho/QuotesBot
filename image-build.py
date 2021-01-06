from PIL import Image, ImageFont, ImageDraw 
import textwrap

def main():
    my_image = Image.open("images/quote-supergirl04.png")

    test = "\"aqui está um texto com vários caracteres, queria dizer que isso é muito estranho, imagino que não seja tanto assim, thunder, ele repete muito essa palavra, não gosto de músicas que\""
    test = "\"I love woooo\""
    #test = "\"iraaaa isso é muuuito estranho, imagino que não\""

    margin = 611
    offset = 14

    if len(test) <= 100:
        offset = 212

    title_font = ImageFont.truetype('fonts/Roboto-Regular.ttf', 50)
    italic_font = ImageFont.truetype('fonts/Roboto-Italic.ttf', 50)

    image_editable = ImageDraw.Draw(my_image)

    text = "\n".join(textwrap.wrap(test, width=23))

    image_editable.text((margin, offset), text, (241, 19, 38), font=title_font)

    offset += (title_font.getsize(text)[1] * len(textwrap.wrap(test, width=23)))

    character = "-Supergirl"
    image_editable.text((margin, offset), character, (178, 30, 42), font=italic_font)

    my_image.save("result.png")

if __name__ == "__main__":
    main()




#250 caracteres
#183 caracteres sem precisar mudar a fonte
#212 -> -100caracteres
#cortar a frase se tiver mais de 183 chars
#cor -> (245, 232, 230)