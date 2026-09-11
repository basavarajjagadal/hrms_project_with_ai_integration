from .vector_store import load_vector_store


def get_retriever(k=3):
    """
    Returns a retriever for schema search
    k = number of results to return
    """

    vectordb = load_vector_store()

    retriever = vectordb.as_retriever(
        search_kwargs={"k": k}
    )

    return retriever


def retrieve_schema(question, k=3):
    """
    Retrieve relevant schema documents for a question
    """

    retriever = get_retriever(k=k)

    docs = retriever.invoke(question)

    # Combine all retrieved docs into one string
    schema_context = "\n\n".join(
        doc.page_content for doc in docs
    )

    return schema_context, docs