# Preprocessing Helper

This utily creates an object of the following form from an html blob:
```json=
{
    "id": "UUID",
    "text": "The full text of the html node",
    "concise_text": "text passed through NLP preprocessor. Tentative."
    "meta_words_of_interest": "A list of extracted word from the html meta.",
    "meta": "The full html meta, just to have the original",
    "annotation_approver": "Related to annotation of full_text",
    "labels": ["List of labels"],
    "html": "Raw html for reference"
}
```
Currently, concise_text is not needed to build a corpora. I think the exact preprocessing pipeline can be defined depending on my chosen ML pipeline. For now, compile examples and annotate them on Doccano. The annotations use index FROM and TO. Annotated bits can be extracted using this index and passed through the NLP preprocessing pipeline. These annotated bits can then be glued to form one html element.