import requests
import zipfile
import tempfile
import os
import json
import time

class PresentationToVideoAPI:
    def __init__(self, api_key, api_url='https://api.narakeet.com', polling_interval=5, extension='pptx'):
        self.api_key = api_key
        self.api_url = api_url
        self.polling_interval = polling_interval
        self.extension = extension

    def request_upload_token(self):
        url = f'{self.api_url}/presentation/{self.extension}/upload-request'
        headers = {'x-api-key': self.api_key}
        response = requests.get(url, headers=headers)
        return response.json()

    def zip_directory_into_tempfile(self, directory):
        temp = tempfile.NamedTemporaryFile(delete=False)
        zip_file = zipfile.ZipFile(temp, 'w')
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, arcname=file)
        zip_file.close()
        temp.close()
        return temp.name

    def upload_file(self, upload_token, local_file):
        url = upload_token['url']
        headers = {'Content-Type': upload_token.get('contentType', 'application/binary')}
        with open(local_file, 'rb') as f:
            response = requests.put(url, headers=headers, data=f)
            response.raise_for_status()

    def request_conversion(self, upload_token):
        url = f'{self.api_url}/presentation/{self.extension}/{upload_token["uploadId"]}/import'
        headers = {'Content-Type': 'application/json', 'x-api-key': self.api_key}
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def request_build_task(self, upload_token, conversion_task, build_config):
        url = f'{self.api_url}/presentation/{self.extension}/{upload_token["uploadId"]}/{conversion_task["conversionId"]}/build'
        headers = {'Content-Type': 'application/json', 'x-api-key': self.api_key}
        response = requests.post(url, headers=headers, json=build_config)
        response.raise_for_status()
        return response.json()

    def poll_until_finished(self, task_url, progress_callback=None):
        while True:
            response = requests.get(task_url)
            response.raise_for_status()
            data = response.json()
            if data['finished']:
                break

            if progress_callback:
                progress_callback(data)

            time.sleep(self.polling_interval)

        return data

    def download_to_temp_file(self, url):
        temp_file = tempfile.NamedTemporaryFile(prefix='video', suffix='.mp4', delete=False)
        response = requests.get(url)
        response.raise_for_status()
        temp_file.write(response.content)
        temp_file.close()
        return temp_file.name

