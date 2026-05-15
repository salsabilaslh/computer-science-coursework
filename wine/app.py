import gradio as gr
from model import model

# prediction function
def predict_wine(alcohol, malic_acid, ash):

    data = [[alcohol, malic_acid, ash]]

    prediction = model.predict(data)[0]

    probabilities = model.predict_proba(data)[0]

    confidence = max(probabilities) * 100

    wine_info = {
        0: {
            "name": "🍷 Premium Red Wine",
            "description": "Rich flavor with balanced aroma."
        },

        1: {
            "name": "🍇 Classic Wine",
            "description": "Smooth texture with medium acidity."
        },

        2: {
            "name": "🥂 Sparkling White Wine",
            "description": "Fresh and light sparkling taste."
        }
    }

    result = wine_info[prediction]

    bar0 = "🟩" * int(probabilities[0] * 10)
    bar1 = "🟩" * int(probabilities[1] * 10)
    bar2 = "🟩" * int(probabilities[2] * 10)

    return f"""
# 🍷 Wine Analysis

## Prediction
### {result['name']}

## Confidence Score
### {confidence:.2f}%

## Wine Characteristics
{result['description']}

# 📊 AI Probability Analysis

### 🍷 Premium Red Wine
{probabilities[0]*100:.2f}%

{bar0}

### 🍇 Classic Wine
{probabilities[1]*100:.2f}%

{bar1}

### 🥂 Sparkling White Wine
{probabilities[2]*100:.2f}%

{bar2}
"""


# custom theme
theme = gr.themes.Soft(
    primary_hue="orange",
    secondary_hue="gray"
)

# UI
with gr.Blocks(theme=theme) as demo:

    gr.Markdown("""
# 🍷 Wine Prediction AI Service

Advanced Machine Learning prediction system using
Scikit-learn `load_wine()` dataset.

### Selected Features
- Alcohol
- Malic Acid
- Ash
""")

    with gr.Row():

        # left column
        with gr.Column(scale=1):

            alcohol = gr.Slider(
                10,
                15,
                value=11,
                step=0.1,
                label="Alcohol"
            )

            malic_acid = gr.Slider(
                0,
                6,
                value=1.8,
                step=0.1,
                label="Malic Acid"
            )

            ash = gr.Slider(
                1,
                4,
                value=2.4,
                step=0.1,
                label="Ash"
            )

            predict_btn = gr.Button(
                "Analyze Wine",
                variant="primary"
            )

        # right column
        with gr.Column(scale=1):

            output = gr.Markdown("""
## 🍷 AI Analysis Result

Waiting for prediction...
""")

    # button click
    predict_btn.click(
        fn=predict_wine,
        inputs=[alcohol, malic_acid, ash],
        outputs=output
    )

# launch
demo.launch(share=True)
