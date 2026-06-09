# Stage 1: Build the Go backend
FROM golang:alpine AS builder

# Set the current working directory inside the container
WORKDIR /app

# Copy go mod and sum files
COPY go.mod go.sum ./

# Download all dependencies
RUN go mod download

# Copy the source code
COPY backend/ ./backend/

# Build the Go app
RUN CGO_ENABLED=0 GOOS=linux go build -o server ./backend

# Stage 2: Create a minimal image to run the app
FROM alpine:latest

WORKDIR /app

# Install CA certificates for HTTPS requests (e.g. Telegram API) and tzdata for timezones
RUN apk --no-cache add ca-certificates tzdata

# Copy the pre-built binary file from the previous stage
COPY --from=builder /app/server .

# Copy the required static folders
COPY public/ ./public/
COPY data/ ./data/
COPY seo/ ./seo/

# Optional: Add an environment variable for the port
ENV PORT=3030

# Expose port 3030 to the outside world
EXPOSE 3030

# Command to run the executable
CMD ["./server"]
