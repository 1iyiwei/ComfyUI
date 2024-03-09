# run comfyui workflow from command line
# based on https://web.archive.org/web/20231012081212/https://medium.com/@yushantripleseven/comfyui-using-the-api-261293aa055a

from urllib.parse import urljoin
import json
import urllib.request
import urllib.parse
import argparse
import uuid
import websocket
from PIL import Image
import io
import sys

def queue_prompt(server_url, client_id, prompt_workflow):
    p = {"prompt": prompt_workflow, "client_id": client_id}
    data = json.dumps(p).encode('utf-8')
    request_url = urljoin(server_url, "prompt")
    req = urllib.request.Request(request_url, data=data)
    return json.loads(urllib.request.urlopen(req).read())
    # response = urllib.request.urlopen(req)
    # return response.read().decode('utf-8')

def get_image(server_url, filename, subfolder, folder_type):
    data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
    url_values = urllib.parse.urlencode(data)
    with urllib.request.urlopen("{}/view?{}".format(server_url, url_values)) as response:
        return response.read()

def get_history(server_url, prompt_id):
    with urllib.request.urlopen("{}/history/{}".format(server_url, prompt_id)) as response:
        return json.loads(response.read())

def get_images(server_url, client_id, ws, prompt):
    prompt_id = queue_prompt(server_url, client_id, prompt)['prompt_id']
    output_images = {}
    while True:
        out = ws.recv()
        if isinstance(out, str):
            message = json.loads(out)
            if message['type'] == 'executing':
                data = message['data']
                if data['node'] is None and data['prompt_id'] == prompt_id:
                    break #Execution is done
        else:
            sys.stdout.write('.')
            sys.stdout.flush()
            continue #previews are binary data

    history = get_history(server_url, prompt_id)[prompt_id]
    for o in history['outputs']:
        for node_id in history['outputs']:
            node_output = history['outputs'][node_id]
            if 'images' in node_output:
                images_output = []
                for image in node_output['images']:
                    image_data = get_image(server_url, image['filename'], image['subfolder'], image['type'])
                    images_output.append(image_data)
            output_images[node_id] = images_output

    return output_images

def main_prompt(server_url, client_id, input_file):
    prompt_workflow = json.load(open(input_file, 'r', encoding='utf-8'))
    response = queue_prompt(server_url, client_id, prompt_workflow)
    print(response)

def main_image(server_url, client_id, input_file):
    prompt_workflow = json.load(open(input_file, 'r', encoding='utf-8'))
    server_address = server_url.split('//')[1]
    ws = websocket.WebSocket()
    ws_address = "ws://{}/ws?clientId={}".format(server_address, client_id)
    # print(ws_address)
    ws.connect(ws_address)
    images = get_images(server_url, client_id, ws, prompt_workflow)

    for node_id in images:
        for image_data in images[node_id]:
            image = Image.open(io.BytesIO(image_data))
            image.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--server_url", help="server url")
    parser.add_argument("--input_file", help="input json file")
    args = parser.parse_args()

    client_id = str(uuid.uuid4())
    main_prompt(args.server_url, client_id, args.input_file)
    # main_image(args.server_url, client_id, args.input_file)
