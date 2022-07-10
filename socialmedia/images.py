# In this module we can create images from text and those kind of things

from PIL import Image, ImageDraw, ImageFont

# create an image object
#imgObject = Image.new("RGB", (500, 500), (255, 255, 255))

text = """📚 What do you think is the right answer?

I've been revising all day long and I'm pretty confident I know the subject _____ out.

💡 Options:
- within
- in
- inside

#English #EnglishQuizzes
"""
font_size = 30
text_color = (1, 68, 33)

def get_wrapped_text(text: str, font: ImageFont.ImageFont, line_length: int):
        lines = ['']
        for word in text.split(' '):
            line = f'{lines[-1]} {word}'.strip()
            if font.getlength(line) <= line_length:
                lines[-1] = line
            else:
                lines.append(word)
        return '\n'.join(lines)


if __name__ == '__main__':

    font_object = ImageFont.truetype("fonts\\OpenSansEmoji.ttf", font_size)
    imgObject = Image.open('templates\\frame2.jpeg')
    width, height = imgObject.size
    height_offset = height*0.2
    width_offset = width*0.2

    for line_text in text.split("\n"):
        wrapped_line_text = get_wrapped_text(line_text, font_object, line_length=width-2*width_offset)
        number_of_produced_lines = len(wrapped_line_text.split("\n"))
        add_break_line = 0

        # add additional line if the line text is empty
        if line_text=="":
            add_break_line = font_size

        # draw on image
        drawing_object = ImageDraw.Draw(imgObject)
        drawing_object.multiline_text((width_offset, height_offset), wrapped_line_text, font=font_object, fill=text_color)
        # height_offset += font_object.getsize(wrapped_line_text)[1]*number_of_produced_lines + add_break_line
        height_offset += font_size*number_of_produced_lines + add_break_line

    if height_offset > height:
        print("height_offset > height")
        print("Maybe inform programmer and do not create image")
    imgObject.save('images\\new_image.jpeg')