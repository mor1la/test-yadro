import argparse
import logging
import random

import requests


DEFAULT_BASE_URL = "https://tools-httpstatus.pickup-services.com"
REQUESTS_COUNT = 5

STATUS_CODES = [
    100, 101, 102, 103,
    200, 201, 202, 203, 204, 205, 206, 207, 208, 226,
    300, 301, 302, 303, 304, 305, 306, 307, 308,
    400, 401, 402, 403, 404, 405, 406, 407, 408, 409,
    410, 411, 412, 413, 414, 415, 416, 417, 418, 421,
    422, 423, 424, 425, 426, 428, 429, 431, 451,
    500, 501, 502, 503, 504, 505, 506, 507, 508, 510, 511,
]


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--url",
        default=DEFAULT_BASE_URL,
        help="Base URL for requests",
    )

    parser.add_argument(
        "--codes",
        nargs="+",
        type=int,
        choices=STATUS_CODES,
        help="HTTP status codes to request",
    )

    return parser.parse_args()


def make_request(base_url: str, expected_status: int) -> None:
    url = f"{base_url.rstrip('/')}/{expected_status}"

    logging.info("Making request: GET %s", url)

    try:
        response = requests.get(
            url,
            timeout=10,
            allow_redirects=False,
        )
    except requests.RequestException as error:
        logging.critical(
            "Got error while requesting. Message: %s",
            error,
        )
        return

    status_code = response.status_code
    body = response.text.strip()

    if 100 <= status_code <= 399:
        logging.info(
            "Successfully handled request. Status code: %s, Body: %s",
            status_code,
            body,
        )

    elif 400 <= status_code <= 599:
        raise Exception(
            f"HTTP exception. URL: {url}, Status code: {status_code}, Body: {body}"
        )

    else:
        logging.error(
            "Got unexpected HTTP code: %s. Body: %s",
            status_code,
            body,
        )


def main() -> None:
    args = parse_args()

    if args.codes:
        status_codes = args.codes
    else:
        status_codes = random.choices(STATUS_CODES, k=REQUESTS_COUNT)

    logging.info("Selected status codes: %s", status_codes)

    for status_code in status_codes:
        try:
            make_request(args.url, status_code)
        except Exception as error:
            logging.error(error)

    logging.info("Script finished")


if __name__ == "__main__":
    main()