import json
import requests
from pyzbar.pyzbar import decode
from pdf2image import convert_from_bytes
from requests.exceptions import RequestException


def lambda_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(body)
    }


def handler(event, _):

    if 'body' not in event:
        return lambda_response(400, {'error': 'Body has to been provided', 'code': 'BODY_MISSING'})

    request = json.loads(event['body'])

    if 'url' not in request:
        return lambda_response(400, {'error': 'You must provide an url parameter', 'code': 'URL_MISSING'})

    try:
        r = requests.get(request['url'], stream=True)
        r.raise_for_status()
        r.raw.decode_content = True
    except RequestException:
        return lambda_response(500, {'error': 'Request Failed', 'code': 'REQUEST_FAILED'})

    images = convert_from_bytes(r.raw.read(), dpi=150)

    decoded = []

    for img_page in images:
        decoded_image = decode(img_page)
        for barcode in decoded_image:
            decoded.append({
                'data': barcode.data.decode(),
                'type': barcode.type,
                'position': barcode.rect,
                'polygon': barcode.polygon
            })
    return lambda_response(200, decoded)
