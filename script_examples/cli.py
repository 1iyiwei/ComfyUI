# run comfyui workflow from command line
# based on https://web.archive.org/web/20231012081212/https://medium.com/@yushantripleseven/comfyui-using-the-api-261293aa055a

from urllib.parse import urljoin
import json
from urllib import request, parse
import argparse

def queue_prompt(server_url, prompt_workflow):
    p = {"prompt": prompt_workflow}
    data = json.dumps(p).encode('utf-8')
    request_url = urljoin(server_url, "prompt")
    req = request.Request(request_url, data=data)
    response = request.urlopen(req)
    print(response.read().decode('utf-8'))

def main(server_url, input_file):
    prompt_workflow = json.load(open(input_file, 'r', encoding='utf-8'))
    queue_prompt(server_url, prompt_workflow)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--server_url", help="server url")
    parser.add_argument("--input_file", help="input json file")
    args = parser.parse_args()

    main(args.server_url, args.input_file)