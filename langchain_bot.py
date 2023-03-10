from langchain.llms import OpenAI
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.docstore.document import Document
import requests
import pickle

from decouple import config

OPENAI_API_KEY = config('OPENAI_API_KEY')

## Get Sample Data from Wikipedia
def get_wiki_data(title, first_paragraph_only):
    url = f"https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&explaintext=1&titles={title}"
    if first_paragraph_only:
        url += "&exintro=1"
    data = requests.get(url).json()
    return Document(
        page_content=list(data["query"]["pages"].values())[0]["extract"],
        metadata={"source": f"https://en.wikipedia.org/wiki/{title}"},
    )

## Set some sample sources to consult
sources = [
    get_wiki_data("Unix", True),
    get_wiki_data("Microsoft_Windows", True),
    get_wiki_data("Linux", True),
    get_wiki_data("Seinfeld", True),
]

## Load Lang Chain
chain = load_qa_with_sources_chain(OpenAI(temperature=0))

## Print Answer
def print_answer(question):
    with open("sources.pickle", "wb") as file:
        for source in sources:
            pickle.dump(source, file)
    print(
        chain(
            {
                "input_documents": sources,
                "question": question,
            },
            return_only_outputs=True,
        )["output_text"]
    )
    