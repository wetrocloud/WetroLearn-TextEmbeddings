# Understanding Embedding Space  

This Streamlit app visualizes the embedding space of text inputs using cosine similarity. It helps users compare how similar different texts are to a reference text by mapping them in a visual space.

## Features  
- Enter a **Reference Text**, **Text-A**, and **Text-B**  
- Compute **cosine similarity** between the reference and the other texts  
- Visualize the distance in embedding space using **Plotly**  
- Uses **MiniLM-L3-v2**, a lightweight sentence transformer model  

## How It Works  
1. Enter a **Reference Text** in the input box.  
2. Enter **Text-A** and **Text-B** in their respective input boxes.  
3. Click **Analyze Texts** to compute embeddings and visualize distances.  
4. The graph will show how far **Text-A** and **Text-B** are from the reference text in embedding space.  

## System Snapshot
<img src="https://github.com/user-attachments/assets/f07c30a1-fcd4-46c9-a411-fa7a4694f2fa" width="900"/>

## Try It Out  
🚀 **[Run the App](https://wetrolearn-embeddings.streamlit.app/)**   

## Learn More  
This project is part of **[Wetroclouds](https://wetrocloud.com/) Wetrolearn**, an initiative to educate the public on AI.  
   
📕📖 **[Read the Article](#)**  

## Installation  
To run the project locally, follow these steps:  
```bash
git clone https://github.com/your-repo/embedding-space-visualizer.git  
cd WetroLearn-TextEmbeddings  
```

Then
```bash
pip install -r requirements.txt  
streamlit run app.py
```

## Give Us a Star  
⭐ If you enjoyed learning about embeddings, please consider giving the repo a star on GitHub!  
