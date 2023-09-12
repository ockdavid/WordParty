# Importar las librerías necesarias
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import streamlit as st
from io import StringIO
import time
import io

st.set_page_config(
    page_title="Word Party 📃",
    page_icon="📃",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.linkedin.com/in/david-landeo/',
        'Report a bug': "https://www.linkedin.com/in/david-landeo/",
        'About': "This app allows you to get a wordcloud of your WhatsApp chat"
    }
)

hide_menu_style = """
                <style>
                footer {visibility: hidden; }
                </style>
                """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# if "visibility" not in st.session_state:
#     st.session_state.visibility = "hidden"

st.session_state.image = False

def show_image():
    st.session_state.image = True

st.write(st.session_state.image)

# def language_chosen():
#     if st.session_state.language: 
#         st.sessi


st.title('Word Party 📃')
st.markdown("Export any WhatsApp chat you desire and upload it below to visualize the most common words in a generated word cloud.")

# Upload the file to analyze
uploaded_file = st.file_uploader("Upload file to analyze", type=['txt'])

# Verificar si se cargó un archivo
if uploaded_file is not None:
    # Leer el contenido del archivo
    chat = uploaded_file.read().decode('utf-8')

    new_chat = []
    a = 0
    b = 0

    #The string variable is split at each carriage return and separates the messages into a list.
    while chat.find('\n', a+1) != -1:
        a = chat.find('\n',b)
        b = chat.find('\n',a+1)
        new_chat.append(chat[a+1:b])

    # new list that will not include the time and date
    cleaned_chat = []

    for i in range(len(new_chat)):
        # Messages has at least 2 colons, that's why I'm filtering if there is only one and has a date with 2 '/'
        if (new_chat[i].count(':') == 1 and new_chat[i].count('/')==2) :
            a=0
        else:
            # Findind the positions of the colons, slash, and the hyphen
            first_colon = new_chat[i].find(':')
            second_colon = new_chat[i].find(':',first_colon+1)
            slash = new_chat[i].find('/')
            comment = new_chat[i][second_colon+2:]
            # With the amount of slash we can know if there is a link in the message
            if (comment.count('/')<3):
                cleaned_chat.append(comment)

    chat_str = ' '.join(cleaned_chat)
    nlp = spacy.load("en_core_web_sm")
    doc_1 = nlp(chat_str)

    # Definir una lista de palabras para agregar al conjunto (set)
    add_stop_words = ['medium', 'omit','media', 'message', 'deleted', 'multimedia', 'omitido', 'Multimedia']

    # Agregar las palabras de la lista al conjunto (set) usando el método update()
    STOP_WORDS.update(add_stop_words)

    filtrado = []

    for token in doc_1:
        if (token.is_alpha) and not(token.lemma_.lower() in STOP_WORDS):
            filtrado.append(token.text.lower())

    words_as_string = ' '.join(filtrado)

    # Get the number of words for the word cloud
    number = st.number_input('How many words do you want to show?',step=int, format='%.0f')
    max_words_inserted = int(number)
    st.write('Words: ', max_words_inserted)
    
    if max_words_inserted>0:
        # Crear el objeto WordCloud con las opciones deseadas
        try:
            wordcloud = WordCloud(width=800, height=800, background_color='white', min_font_size=10, max_words=max_words_inserted).generate(words_as_string)
        except IndexError:
            pass
        
        if st.button('Show World Cloud', on_click = show_image) or st.session_state.image:
                st.write(st.session_state.image)
                fig, ax = plt.subplots(figsize=(5,5))

                # Visualizar el WordCloud generado en la subtrama
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis("off")

                st.pyplot(fig)
                plt.savefig('wordcloud.png')
                buffer = io.BytesIO()
                plt.savefig(buffer, format='png')
                buffer.seek(0)  # Vuelve al principio del buffer

                imagen_en_variable = buffer.read()

                # Cierra el buffer
                buffer.close()
                
                st.download_button(
                    label="Download image",
                    data=imagen_en_variable,
                    file_name='wordcloud.png',
                    mime='image/png',
                )