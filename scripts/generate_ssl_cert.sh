#!/bin/bash

echo "🔐 Generating SSL certificates for local development..."

mkdir -p ../ssl

echo "Generating private key..."
openssl genrsa -out ../ssl/localhost.key 2048

echo "Generating certificate signing request..."
openssl req -new -key ../ssl/localhost.key -out ../ssl/localhost.csr \
  -subj "/C=US/ST=California/L=San Francisco/O=Development/CN=localhost"

echo "Generating self-signed certificate..."
openssl x509 -req -days 365 -in ../ssl/localhost.csr \
  -signkey ../ssl/localhost.key -out ../ssl/localhost.crt

chmod 600 ../ssl/localhost.key
rm ../ssl/localhost.csr

echo ""
echo "✅ SSL certificates generated successfully!"
echo "📁 Location: ssl/ directory"
echo "🔑 Private Key: ssl/localhost.key"
echo "📄 Certificate: ssl/localhost.crt"
