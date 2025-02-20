import traceback
from datetime import datetime

from minio import Minio
import io
from io import BytesIO
from PIL import Image
import cv2
import requests
import numpy as np
import time

from sentry_sdk import capture_message

from app.app_utils.file_io_untils import ip_run_service_ai

# https://github.com/Vuong02011996/ai-engineer/blob/master/Database/Minio/minio_python.py

bucket = "face"
host = 's3.oryza.vn'  # Endpoint in file readme
# host = '192.168.111.11:42415'  # Endpoint in file readme
# host = 'http://s3.oryza.vn'  # Endpoint in file readme
minio_access_key = 'hoang'
minio_secret_key = '12345678'
minio_client = Minio(host, access_key=minio_access_key, secret_key='minio_secret_key', secure=False)


def upload_array_image_to_minio(image, bucket="face", folder_name="group", image_name="test", mode_rgb="BRG"):
    """Upload image into MinIO Server. Parse the path of image and upload to

    server.

    Args:
        image (np.array): 1_numpy array image
        folder_name(str): Folder Name on MinIO server

    Returns:
        url
    """
    # img_name = "{}/{}.jpg".format(folder_name, generate_rand_string(30))
    # img_name = "{}/{}.jpg".format(folder_name, image_name)
    img_name = "{}/{}.jpg".format(folder_name, image_name)

    # Make  bucket if not exist.
    found = minio_client.bucket_exists(bucket)
    if not found:
        minio_client.make_bucket(bucket)
    else:
        print("Bucket already exists")

    try:
        if mode_rgb == "BRG":
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)

        out_img = io.BytesIO()

        image.save(out_img, quality=100, format='JPEG')
        out_img.seek(0)
        start_time = time.time()
        minio_client.put_object(
            bucket, img_name, out_img, length=out_img.getbuffer().nbytes, content_type="image/jpeg",
        )
        print("Upload file to minio cost: ", time.time() - start_time)

    except Exception as error:
        print(error)
        return
    url = "https://{}/{}/{}".format(host, bucket, img_name)

    # url = minio_client.presigned_get_object(bucket, img_name)

    return url


def read_stream_img(url, timeout=0.6):
    """
    :param url: url in minio
    :param timeout:
    :return: 1_numpy array
    """
    i = 0
    response = None
    while i < 5:
        try:
            i += 1
            response = requests.get(url, timeout=timeout)
        except Exception as e:
            print(e)
            print("Error read_stream_img")
            capture_message(f"[FACE][{ip_run_service_ai}][{datetime.today().strftime('%d-%m-%Y %H:%M:%S')}][Error] {str(e).upper()} : {traceback.format_exc()}")

        if response is not None:
            break

    if response is None:
        return response

    return np.array(Image.open(io.BytesIO(response.content)))


def read_url_img_minio_to_array(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    # if the image mode is not RGB, convert it
    if img.mode != "RGB":
        img = img.convert("RGB")
    img_array = np.array(img)
    # cv2.imwrite("/home/vuong/Desktop/Project/MyGitHub/ai-engineer/Database/Minio/test2.png", img_array)
    return img_array


def get_image_array_from_object_name(bucket="clover", object_name="/group/test1.jpg"):
    data = minio_client.get_object(bucket_name=bucket, object_name=object_name)
    img = Image.open(BytesIO(data.data))
    # if the image mode is not RGB, convert it
    if img.mode != "RGB":
        img = img.convert("RGB")
    img_array = np.array(img)
    # cv2.imwrite("/home/vuong/Desktop/Project/MyGitHub/ai-engineer/Database/Minio/test.png", img_array)
    return img_array


if __name__ == '__main__':
    img = cv2.imread('/home/oryza/Pictures/Face/Truc.jpg')
    url_image = upload_array_image_to_minio(img)
    # url_image = "http://172.24.0.2:9000/clover/group/test.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=WMAFIW9185E29TJ9U2BY%2F20210902%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20210902T093245Z&X-Amz-Expires=604800&X-Amz-Security-Token=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3NLZXkiOiJXTUFGSVc5MTg1RTI5VEo5VTJCWSIsImV4cCI6MzYwMDAwMDAwMDAwMCwicG9saWN5IjoiY29uc29sZUFkbWluIn0.sGMe_540hPf5VHwACzwNGRzUoeJOKy0PKBjdhFokW43VL-WeanCd8e4VpBIdizVdxiLm_ePy6jZzmi_XPot_BQ&X-Amz-SignedHeaders=host&versionId=null&X-Amz-Signature=746534484ebdc28e8194220b635e96ccb5c18ba7e10bd49c70c234c2f4fa9e87"
    # url can not read
    # convert to "http://172.24.0.2:11039/object-browser/clover/group/test_upload_get_url.jpg"

    print("url_image", url_image)
    # data = read_stream_img(url_image)
    # url_image = upload_image(data, image_name="test_upload_get_url")
    # url_image = "http://s3.oryza.vn/face/group/test.jpg"
    # img_array = read_url_img_minio_to_array(url_image)
    # image_path = '/home/oryza/Pictures/Face/Truc1.jpg'
    # # Save the image using OpenCV
    # cv2.imwrite(image_path, img_array)
    # print(img_array)
