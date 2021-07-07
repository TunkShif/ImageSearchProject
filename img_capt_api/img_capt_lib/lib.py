# 若你的显存超过16G，注释第4行以使用GPU运算
import os

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

from multiprocessing import Process, Queue
import tensorflow as tf

input = Queue(1)
output = Queue(1)

p = None


class ModelNotInitialized(Exception):
    pass


def _initialized(f):
    def g(*args, **kwargs):
        global p
        if p == None or not p.is_alive():
            raise ModelNotInitialized
        res = f(*args, **kwargs)
        return res

    g.__doc__ = f.__doc__
    g.__name__ = f.__name__

    return g


def _uninitialized(f):
    def g(*args, **kwargs):
        global p
        if p != None and p.is_alive():
            raise Exception("Model already initialized.")
        res = f(*args, **kwargs)
        return res

    g.__doc__ = f.__doc__
    g.__name__ = f.__name__

    return g


def _load_image(img_path):
    img = tf.io.read_file(img_path)
    img = tf.image.decode_jpeg(img, channels=3)
    img = tf.image.resize(img, (299, 299))
    img = tf.keras.applications.inception_v3.preprocess_input(img)
    img = tf.expand_dims(img, 0)
    return img


def _convert_to_sentence(tokenizer, sequences):
    result = []
    for i, seq in enumerate(sequences):
        result.append("")
        for index in seq[1:]:
            if tokenizer.index_word[index.numpy()] == "<end>":
                break
            else:
                result[i] += " " + tokenizer.index_word[index.numpy()]
    return result


def _predict(input, output, debug):
    if debug:
        print("Loading Models...")

    feature_extract = tf.keras.applications.InceptionV3(include_top=False)
    image_caption = tf.keras.models.load_model("img_capt_lib/ImageCaptionModel")

    with open("img_capt_lib/tokenizer_config.json", "r") as f:
        tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(f.read())

    output.put([])

    if debug:
        print("Model loaded.")

    while True:
        try:
            fp = input.get()

            if debug:
                print(f"Get img: {fp}")

            if fp == "":
                if debug:
                    print("Release Model.")
                break

            img = _load_image(fp)
            features = feature_extract(img)
            results = image_caption(features)
            if debug:
                results = _convert_to_sentence(tokenizer, results)[0]
            output.put(results)
        except Exception as e:
            output.put("E:" + str(e))


@_uninitialized
def initialize(debug=False):
    """
    加载模型。
    必须在预测和释放操作之前执行。

    Parameters
    ----------
    debug: bool, default False
        debug 模式下将提供阶段性输出来提示模型的加载和预测情况并将预测结果转换成句子。

    """

    global p, input, output
    p = Process(target=_predict, args=[input, output, debug])
    p.start()

    output.get()


@_initialized
def release():
    """
    释放模型。
    只能在加载模型之后执行。
    """

    global input, output
    input.put("")
    while not output.empty():
        output.get()


@_initialized
def predict(img):
    """
    预测图片内容。
    只能在加载模型后且未释放模型时执行

    Parameters
    ----------
    img: str
        图片的绝对路径。

    Returns
    -------
    list or str
        返回形状为 (1, length) 的列表，列表元素为单词的索引值。
        debug 模式下，返回预测句子字符串。
        若产生异常，返回以 E: 开头的异常字符串。
    """

    global input
    input.put(img)
    res = output.get()
    return res
