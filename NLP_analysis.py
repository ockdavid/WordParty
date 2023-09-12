import spacy


def NLP_analysis_english(chat):
    from spacy.lang.en.stop_words import STOP_WORDS
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
    nlp.max_length = 2000000

    doc_1 = nlp(chat_str)

    # Definir una lista de palabras para agregar al conjunto (set)
    add_stop_words = ['medium', 'omit','media', 'message', 'deleted', \
        'multimedia', 'omitido', 'Multimedia', 'q']

    # Agregar las palabras de la lista al conjunto (set) usando el método update()
    STOP_WORDS.update(add_stop_words)

    filtrado = []

    for token in doc_1:
        if (token.is_alpha) and not(token.lemma_.lower() in STOP_WORDS):
            filtrado.append(token.text.lower())

    words_as_string = ' '.join(filtrado)
    return words_as_string


def NLP_analysis_spanish(chat):
    from spacy.lang.es.stop_words import STOP_WORDS
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
    nlp = spacy.load("es_core_news_sm")
    nlp.max_length = 2000000

    doc_1 = nlp(chat_str)

    # Definir una lista de palabras para agregar al conjunto (set)
    add_stop_words = ['medium', 'omit','media', 'message', 'deleted', \
        'multimedia', 'omitido', 'Multimedia', 'q']

    # Agregar las palabras de la lista al conjunto (set) usando el método update()
    STOP_WORDS.update(add_stop_words)

    filtrado = []

    for token in doc_1:
        if (token.is_alpha) and not(token.lemma_.lower() in STOP_WORDS):
            filtrado.append(token.text.lower())

    words_as_string = ' '.join(filtrado)
    return words_as_string