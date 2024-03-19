from sentence_transformers import SentenceTransformer

def get_embedding(model_name, search_keyword):


    model = SentenceTransformer(model_name)

    input_texts = [
        f'query: {search_keyword}'
    ]

    vectors = model.encode(input_texts, normalize_embeddings=True)

    return vectors[0]