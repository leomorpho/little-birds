# AI Engine

## Useful commands
Start a development server with hot reloading:
`uvicorn app.main:api --reload --workers 1 --host 0.0.0.0 --port 8000`

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