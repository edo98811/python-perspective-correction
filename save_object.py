import json
import os

class ObjectLocations:
    def __init__(self):
        self.objects: dict = {}
        self.self.associated_image: str = ""

    def add_object(self, name: str, coordinates: tuple):
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not (isinstance(coordinates, tuple) and len(coordinates) == 2 and all(isinstance(coord, (int, float)) for coord in coordinates)):
            raise TypeError("coordinates must be a tuple of two numbers")
        
        self.objects[name] = coordinates

    def save_to_json(self, file_path: str):

        if not isinstance(file_path, str):
            raise TypeError("file_path must be a string")
        
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                existing_data = json.load(file)
            
            image_found = False
            for image in existing_data:
                if image['image_name'] == self.associated_image:
                    image['objects'].update(self.objects)
                    image_found = True
                    break
            
            if not image_found:
                existing_data.append({'image_name': self.associated_image, 'objects': self.objects})
            
            data_to_save = existing_data
        else:
            data_to_save = [{'image_name': self.associated_image, 'objects': self.objects}]
        
        with open(file_path, 'w') as file:
            json.dump(data_to_save, file, indent=4)

        with open(file_path, 'w') as file:
            json.dump(data_to_save, file, indent=4)

# Example usage:
# obj_loc = ObjectLocations()
# obj_loc.add_object("object1", (10, 20))
# obj_loc.save_to_json("/path/to/your/file.json")