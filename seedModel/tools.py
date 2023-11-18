from PIL import Image, ImageEnhance

import logging, socket

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('logger')

HOSTNAME = socket.gethostname()


def get_host_name(relative_path):
    return 'http://' + socket.gethostbyname(HOSTNAME) + ':8001' + relative_path


def make_baw(input_path, baw_path):
    global img

    try:
        img = Image.open(input_path)
    except Exception as e:
        print(str(e))
        return "error"

    contrast = ImageEnhance.Contrast(img)
    r = contrast.enhance(1.5)
    thresh = 200

    def fn(x):
        return 255 if x > thresh else 0

    r = r.convert('1').point(fn, mode='1')

    try:
        r.save(fp=baw_path)
    except Exception as e:
        print(str(e))
        return "error"

    r.close()

    return 'success'


def predict(input_model, img_path, save_dir, data=False):
    logger.info('Started detection ...')
    result = input_model(img_path)
    logger.info('Detection completed')
    text, data = result.process_text(data=data)
    logger.info('Detection text %s', text)
    result.save(save_dir)
    logger.info('Output photo saved')

    return text, data
