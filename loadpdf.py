from pprint import pprint

from langchain_community.document_loaders import PyPDFLoader

path = "./eq.pdf"

def load_pdf(path: str) -> str:
    loader = PyPDFLoader(path, mode="page")
    documents = loader.load()
    content = "\n".join([doc.page_content for doc in documents])
    return documents, content

if __name__ == "__main__":
    documents, pdf_content = load_pdf(path)
    # print(pdf_content)
    # pprint(documents[0].metadata)

    # show all content at page n
    for i, doc in enumerate(documents):
        print(f"--- Page {i+1} ---")
        print(doc.page_content)
        print("\n")

    # print("—"*10)