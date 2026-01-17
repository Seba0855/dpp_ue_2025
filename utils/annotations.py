from xml.etree import ElementTree
import dataclasses
import pathlib


@dataclasses.dataclass
class Annotation:
    """ Parsed annotation object. """
    img_id: int 
    img_path: pathlib.Path
    img_size: tuple[int, int]
    plate_num: str
    bounding_box: tuple[float, float, float, float]
    rotation: float


def parse_annotations(annotations_file_path: str, images_dir: str) -> list[Annotation]:
    """ Parses a given annotations.xml file into a list of Annotation objects. """
    annotations: list[Annotation] = []
    
    root = ElementTree.parse(annotations_file_path).getroot()
    for image_tag in root.findall("image"):
        prop = lambda attr: str(image_tag.get(attr))
        
        img_id = int(prop("id"))
        img_path = (pathlib.Path(images_dir) / prop("name")).resolve()
        img_size = (int(prop("width")), int(prop("height"))) 
        
        box_tag = image_tag.find("box")
        if box_tag is None: raise KeyError("Unsupported annotation file schema")
        prop = lambda attr: str(box_tag.get(attr)) # type: ignore
        
        bounding_box = (float(prop("xtl")), float(prop("ytl")), float(prop("xbr")), float(prop("ybr")))
        rotation = box_tag.get("rotation")
        rotation = float(rotation) if rotation is not None else 0.0
        
        attribute_tag = box_tag.find("attribute")
        if attribute_tag is None: raise KeyError("Unsupported annotation file schema")
        
        plate_num = str(attribute_tag.text)
        
        annotation = Annotation(img_id, img_path, img_size, plate_num, bounding_box, rotation)
        annotations.append(annotation)
    
    return annotations
