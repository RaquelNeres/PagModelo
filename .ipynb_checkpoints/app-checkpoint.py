from flask import Flask, request, render_template, url_for
import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2
from io import BytesIO
from PIL import Image
import base64
import os

app = Flask(__name__)

MODEL_PATH = "/mnt/d/modelos baixados/best_model_custom.keras"
IMG_SIZE = (224, 224)  # entrada do modelo
LAST_CONV_LAYER_NAME = "separable_conv2d_13"

# Carregar modelo
model = keras.models.load_model(MODEL_PATH)

# Classes do dataset
CLASS_NAMES = ['CNV', 'DME', 'DRUSEN', 'NORMAL']
class_names = {i: name for i, name in enumerate(CLASS_NAMES)}


def crop_and_equalize(img_rgb):
    """Remove margens/legendas e aplica equalização adaptativa de contraste."""
    h, w, _ = img_rgb.shape
    y0, y1 = int(0.08*h), int(0.92*h)
    x0, x1 = int(0.04*w), int(0.96*w)
    img = img_rgb[y0:y1, x0:x1]

    lab = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    l2 = clahe.apply(l)
    img = cv2.cvtColor(cv2.merge((l2, a, b)), cv2.COLOR_LAB2RGB)
    return img


def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    grad_model = keras.models.Model(
        model.inputs, [model.get_layer(last_conv_layer_name).output, model.output]
    )
    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array, training=False)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    grads = tape.gradient(class_channel, last_conv_layer_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)
    heatmap = tf.maximum(heatmap, 0) / (tf.math.reduce_max(heatmap) + 1e-8)
    return heatmap.numpy()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files["image"]

        if file.filename == "":
            return render_template("index.html", error="Nenhum arquivo selecionado.")

        # Verifica tipo do arquivo
        if not file.mimetype.startswith("image/"):
            return render_template("index.html", error="O arquivo enviado não é uma imagem válida.")

        # Verifica tamanho (5MB)
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        if file_size > 5 * 1024 * 1024:
            return render_template("index.html", error="O arquivo é muito grande. Máximo permitido: 5MB.")

        # Lê os bytes
        file_bytes = np.frombuffer(file.read(), np.uint8)
        img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if img is None:
            return render_template("index.html", error="Formato não suportado (ex: AVIF).")

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Pré-processamento
        img = crop_and_equalize(img)
        orig_array = img.copy()
        img_resized = cv2.resize(img, IMG_SIZE)
        img_array = tf.expand_dims(img_resized, 0)

        # Predição
        predictions = model.predict(img_array)
        probabilities = tf.nn.softmax(predictions[0]).numpy()
        predicted_class_index = np.argmax(probabilities)
        predicted_class_name = class_names[predicted_class_index]
        confidence = probabilities[predicted_class_index]

        # Grad-CAM
        heatmap = make_gradcam_heatmap(img_array, model, LAST_CONV_LAYER_NAME, predicted_class_index)
        heatmap = np.array(heatmap).astype(np.float32)
        if heatmap.max() > 0:
            heatmap /= heatmap.max()

        heatmap_resized = cv2.resize(heatmap, (orig_array.shape[1], orig_array.shape[0]))
        heatmap_colored = cv2.applyColorMap(np.uint8(255 * heatmap_resized), cv2.COLORMAP_JET)
        superimposed_img = cv2.addWeighted(orig_array, 0.6, heatmap_colored, 0.4, 0)

        # Converte original e Grad-CAM para Base64
        def to_base64(arr):
            pil_img = Image.fromarray(arr)
            buf = BytesIO()
            pil_img.save(buf, format="PNG")
            return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("utf-8")

        orig_b64 = to_base64(orig_array)
        gradcam_b64 = to_base64(superimposed_img)

        return render_template("result.html",
                               predicted_class_name=predicted_class_name,
                               confidence=confidence,
                               probs=[(class_names[i], p) for i, p in enumerate(probabilities)],
                               orig_img=orig_b64,
                               gradcam_img=gradcam_b64)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
