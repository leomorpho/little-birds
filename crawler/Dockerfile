FROM golang:1.13

WORKDIR /go/src/app
COPY . .

RUN go get -d -v ./...
RUN go build ./cmd/main/main.go

CMD ["./main"]
