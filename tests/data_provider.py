import os
import base64


class DataProvider:
    _CONTENT_DIR = r'service\content'

    @staticmethod
    def read_base64_encoded_image():
        image_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), DataProvider._CONTENT_DIR, 'example.png')
        with open(image_path, 'rb') as image_file:
            img_data = image_file.read()
        return base64.b64encode(img_data)

    @staticmethod
    def read_base64_encoded_large_bmp():
        large_bmp_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), DataProvider._CONTENT_DIR,
                                      'large_bmp.bmp')
        with open(large_bmp_path, 'rb') as large_bmp_file:
            large_bmp_data = large_bmp_file.read()
        return base64.b64encode(large_bmp_data)

    @staticmethod
    def read_large_bmp():
        large_bmp_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), DataProvider._CONTENT_DIR,
                                      'large_bmp.bmp')
        with open(large_bmp_path, 'rb') as large_bmp_file:
            large_bmp_data = large_bmp_file.read()
        return large_bmp_data

    @staticmethod
    def read_base64_encoded_small_shape():
        small_shape_zip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), DataProvider._CONTENT_DIR,
                                            'small_shape.zip')
        with open(small_shape_zip_path, 'rb') as small_shape_zip_file:
            small_shape_zip_data = small_shape_zip_file.read()
        return base64.b64encode(small_shape_zip_data)

    @staticmethod
    def read_base64_encoded_large_shape():
        large_shape_zip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), DataProvider._CONTENT_DIR,
                                            'large_shape.zip')
        with open(large_shape_zip_path, 'rb') as large_shape_zip_file:
            large_shape_zip_data = large_shape_zip_file.read()
        return base64.b64encode(large_shape_zip_data)

    @staticmethod
    def read_base64_encoded_small_task_data():
        small_task_data_zip_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), DataProvider._CONTENT_DIR,
                                                'small_taskdata.zip')
        with open(small_task_data_zip_path, 'rb') as small_task_data_zip_file:
            small_task_data_zip_data = small_task_data_zip_file.read()
        return base64.b64encode(small_task_data_zip_data)
