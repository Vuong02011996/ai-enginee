# from app.core.config import settings
import os

from minio import Minio
import logging

from app.core.config import settings

LOGGER = logging.getLogger("minio_logger")


class MinioServices:
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(MinioServices, cls).__new__(cls)
            cls.instance._init()
        return cls.instance

    def _init(self):
        self.minio_url = settings.MINIO_SERVER
        self.minio_access_key = settings.MINIO_ACCESS_KEY
        self.minio_secret_key = settings.MINIO_SECRET_KEY
        self.bucket = settings.BUCKET

        # self.minio_url = "s3.oryza.vn"
        # self.minio_access_key = "admin"
        # self.minio_secret_key = "Oryza@2024"
        # self.bucket = "oryza-ai"
        self.client = Minio(
            self.minio_url,
            access_key=self.minio_access_key,
            secret_key=self.minio_secret_key,
            secure=True,
        )

    def upload_file(self, source_file: str, destionation_file: str, bucket=None):
        LOGGER.info("Source file to upload: %s", source_file)
        # print("destionation_file", destionation_file)
        if bucket is None:
            bucket = self.bucket
        try:
            self.client.fput_object(bucket, destionation_file, source_file)
            return f"https://{self.minio_url}/{bucket}/{destionation_file}"
        except Exception as e:
            LOGGER.debug(e)
            print("Error upload_file: ", e)
            return False

    def upload_file_form(self, name, contents, bucket=None, forder=None):
        if bucket is None:
            bucket = self.bucket
        path = ""
        try:
            path = os.path.join("./temp", name + ".jpg")
            if not os.path.exists("./temp"):
                os.makedirs("./temp")
            with open(path, "wb") as f:
                f.write(contents)
            if forder is None:
                self.client.fput_object(bucket, f"{name}.jpg", path)
            else:
                self.client.fput_object(bucket, f"{forder}/{name}.jpg", path)
            data = self.client.presigned_get_object(bucket, path)

            if path and os.path.exists(path):
                os.remove(path)
            if forder is None:
                return f"https://{self.minio_url}/{bucket}/{name}.jpg"
            return f"https://{self.minio_url}/{bucket}/{forder}/{name}.jpg"
        except Exception as e:
            if path and os.path.exists(path):
                os.remove(path)
            print("Error upload_file: ", e)
            return False

    def delete_file(self, file_name: str, bucket=None):
        if bucket is None:
            bucket = self.bucket
        try:
            self.client.remove_object(bucket, file_name)
            return True
        except Exception as e:
            LOGGER.debug(e)
            return False


upload_services = MinioServices()


minio_services = MinioServices()


if __name__ == "__main__":
    import requests

    minio = MinioServices()
    # url = "http://192.168.111.11:9000/camera-ai-user/6645c0e97184492d11c8288b_20240516151641902066.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=admin%2F20240516%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240516T081642Z&X-Amz-Expires=604800&X-Amz-SignedHeaders=host&X-Amz-Signature=1d8fe239b675ab3c2a4e28e9b34b663b2c55b9b56594dee12e7874cd6800c4fb"
    # response = requests.get(url)
    # image_bytes = response.content
    # # save image to file
    # with open("demoyy.jpg", "wb") as file:
    #     file.write(image_bytes)

    # print(minio.upload_file("demoyy.jpg", "demo.jpg"))
    print(minio.delete_file("setting_uniforms_company/2024-06-20-16-59-3396778a9e0cf04693bb88945b95cd082e.jpg"))
    print("Done")
