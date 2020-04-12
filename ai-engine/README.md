# AI Engine

## Useful commands
Start a development server with hot reloading:
`uvicorn app.main:api --reload --workers 1 --host 0.0.0.0 --port 8000`

## Preprocessing
The text of html is extracted bu not cleaned for useless words. I keep that operation for later as I want to minimize the information loss since I am not yet sure of what I want to do with it. However, the extracted metadata from the html tags are cleaned to only retrieve useful words and info (like datetime, categories, important semantic words).

## Parse Webpage - Structural Components
How to parse a normalized web page into structural components.
* card
* table
* list
* article
* figcaption
* form

## Component types and semantics
* job posting
* for sale

### Parse sub-components
Since sub-components appear in a context, the sequence contains information.
Different category are mutually exclusive and may be part of different models, called once the context is discovered: job posting, for sale...
* title
* subtitle
* price
* datetime
* shipping
* category (explicit)
* location
* employment load
* salary
* employer
* seller

## Clean data
Strip text from html while appending useful information extracted from the html elements (classes, url, etc)

### Pipeline
1. Extract text from html
2. Remove extra whitespace
3. (Expand contractions)
4. (Remove special characters?)
5. Convert numbers to numeric form
6. Remove stopwords

Ideas: train a message encode to extract useful features (encoder)

**Example of training dataset:**
```
{
    "originalHtmlString": "The html string cleaned out of any script or comments",
    "parsedString": "Only words. (Metadata may extracted from html may have been appended, such as datetime)."
}
```

# TODO
* Write tests!
* Metawords don't need to keep track of what counts towards the count, since the pipeline can be re-run on all saved data to normalize count