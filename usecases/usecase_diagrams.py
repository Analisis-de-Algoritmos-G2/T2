from wordcloud import WordCloud, STOPWORDS
import plotly.graph_objects as go
from utils import transforms, files
import matplotlib.pyplot as plt
import plotly.io as pio
import networkx as nx
import itertools
import os


def create_cloud_words(file, stopwords, video_id):

    stopwords.update(transforms.create_set(files.read_file(os.getenv("STOPWORDS_FILE"))))
    with open(file, 'r', encoding='utf-8') as file:
        texto = file.read()

    wordcloud = WordCloud(stopwords=stopwords,
                          background_color='white',
                          width=800,
                          height=800,
                          max_words=200,
                          colormap='viridis').generate(texto)

    plt.figure(figsize=(10, 10))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')

    output_path = os.path.join(os.getenv('DIAGRAM_FOLDER'), f'{video_id}_wordcloud.png')

    # Guarda la imagen en la carpeta especificada
    plt.savefig(output_path, bbox_inches='tight')

    # Muestra la imagen en la ventana gráfica (opcional)
    plt.show()


def create_network(texto, video_id):

    palabras = texto.split()

    grafo = nx.Graph()
    ventana = 1

    for i in range(len(palabras) - ventana):

        ventana_palabras = palabras[i:i + ventana]

        for pair in itertools.combinations(ventana_palabras, 2):
            if grafo.has_edge(pair[0], pair[1]):
                grafo[pair[0]][pair[1]]['weight'] += 1
            else:
                grafo.add_edge(pair[0], pair[1], weight=1)

    pos = nx.spring_layout(grafo)
    node_x = [pos[node][0] for node in grafo.nodes()]
    node_y = [pos[node][1] for node in grafo.nodes()]

    edge_x = []
    edge_y = []

    for edge in grafo.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        text=list(grafo.nodes()),  # Asignamos las palabras/nodos al hovertext
        marker=dict(showscale=True, colorscale='YlGnBu', size=10)
    )

    layout = go.Layout(showlegend=False, hovermode='closest')
    fig = go.Figure(data=[edge_trace, node_trace], layout=layout)

    # Guardar la figura en un archivo de imagen
    pio.write_image(fig, os.getenv('DIAGRAM_FOLDER') + f"{video_id}_network.png")