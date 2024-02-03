from langchain_community.embeddings.spacy_embeddings import SpacyEmbeddings


if __name__ == "__main__":
    spacy_lm = SpacyEmbeddings(model_name="en_core_web_sm")

    text = "This is an example sentence for SpaCy and LangChain integration."
    processed_text = spacy_lm.embed_query(text)

    entities = processed_text
    print(entities)