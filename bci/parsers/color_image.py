from PIL import Image


class ColorImageParser:

    field = 'color_image'

    def parse(self, context, snapshot):
        path = context.path(f'color_image.jpg')
        size = snapshot.color_image.width, snapshot.color_image.height
        image = Image.frombytes('RGB', size, snapshot.color_image.data)
        image.save(path)
