import hashlib
import os
import base64


class DataProvider:
    _CONTENT_DIR = r'../data/content'

    @staticmethod
    def read_base64_encoded_image():
        """
        Read the image from the file system and return it as base64 encoded string.
        """
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), DataProvider._CONTENT_DIR, 'example.png')
        with open(image_path, 'rb') as image_file:
            img_data = image_file.read()
        return base64.b64encode(img_data)

    @staticmethod
    def read_base64_encoded_large_bmp():
        """
        Read the large bmp from the file system and return it as a raw string.
        """
        large_bmp_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), DataProvider._CONTENT_DIR,
                                      'large_bmp.bmp')
        with open(large_bmp_path, 'rb') as large_bmp_file:
            large_bmp_data = large_bmp_file.read()
        return large_bmp_data

    @staticmethod
    def read_base64_encoded_small_shape():
        """
        Read the small shape from the file system and return it as base64 encoded string.
        """
        small_shape_zip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), DataProvider._CONTENT_DIR,
                                            'small_shape.zip')
        with open(small_shape_zip_path, 'rb') as small_shape_zip_file:
            small_shape_zip_data = small_shape_zip_file.read()
        return base64.b64encode(small_shape_zip_data)

    @staticmethod
    def read_base64_encoded_large_shape():
        """
        Read the large shape from the file system and return it as a raw string.
        """
        large_shape_zip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), DataProvider._CONTENT_DIR,
                                            'large_shape.zip')
        with open(large_shape_zip_path, 'rb') as large_shape_zip_file:
            large_shape_zip_data = large_shape_zip_file.read()
        return large_shape_zip_data

    @staticmethod
    def read_base64_encoded_small_task_data():
        """
        Read the small task data from the file system and return it as base64 encoded string.
        """
        small_task_data_zip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), DataProvider._CONTENT_DIR,
                                                'small_taskdata.zip')
        with open(small_task_data_zip_path, 'rb') as small_task_data_zip_file:
            small_task_data_zip_data = small_task_data_zip_file.read()
        return base64.b64encode(small_task_data_zip_data)

    @staticmethod
    def get_hash(_file_content):
        """
        Get the hash of the content / text to compare the content.
        """
        _encoded_text = str(_file_content).encode('utf-8')
        return int(hashlib.sha512(_encoded_text).hexdigest(), 16)
