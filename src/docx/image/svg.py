import xml.etree.ElementTree as ET

from .constants import MIME_TYPE
from .image import BaseImageHeader


class Svg(BaseImageHeader):
    """
    Image header parser for SVG images.
    """

    @classmethod
    def from_stream(cls, stream):
        """
        Return |Svg| instance having header properties parsed from SVG image
        in *stream*.
        """
        px_width, px_height = cls._dimensions_from_stream(stream)
        return cls(px_width, px_height, 72, 72)

    @property
    def content_type(self):
        """
        MIME content type for this image, unconditionally `image/svg+xml` for
        SVG images.
        """
        return MIME_TYPE.SVG

    @property
    def default_ext(self):
        """
        Default filename extension, always 'svg' for SVG images.
        """
        return "svg"

    @classmethod
    def _parse_svg_dims(cls, value):
        svg_dims_dict = {
            'px': 1,
            'cm': 37.7952755906,
            'pt': 1 / 0.75,
            'in': 96,
            'mm': 3.77952755906,
        }
        try:
            return int(value)
        except ValueError:
            for unit, factor in svg_dims_dict.items():
                if value.endswith(unit):
                    return int(float(value[:-len(unit)]) * factor)
            
    @classmethod
    def _dimensions_from_stream(cls, stream):
        stream.seek(0)
        data = stream.read()
        root = ET.fromstring(data)
        # FIXME: The width could be expressed as '4cm'
        # See https://www.w3.org/TR/SVG11/struct.html#NewDocument
        width = cls._parse_svg_dims(root.attrib["width"])
        height = cls._parse_svg_dims(root.attrib["height"])
        return width, height
