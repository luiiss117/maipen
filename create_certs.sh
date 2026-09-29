CANAME=Maipen-RootCA

mkdir -p certs/private
echo "[+] Created 'certs/' directory"

# generate aes encrypted private key
openssl genpkey -algorithm ML-DSA-87 -out certs/private/$CANAME.key
echo "[+] Created private key"

# create certificate authority
openssl req -x509 -new -nodes -key certs/private/$CANAME.key -days 365 -out certs/$CANAME.crt -subj '/CN=Maipen Root CA/C=AT/ST=Madrid/L=Madrid/O=MyOrganisation'
echo "[+] Created certificate"

# create certificate for service
MYCERT="web-maipen"
openssl req -new -nodes -out certs/$MYCERT.csr -newkey ML-DSA-87 -keyout certs/private/$MYCERT.key -subj '/CN=Maipen Web Server/C=AT/ST=Madrid/L=Madrid/O=Maipen Local'
echo "[+] Created certificate for service"

# create a v3 ext file for SAN properties
tee certs/$MYCERT.v3.ext <<EOF
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names
[alt_names]
DNS.1 = maipen.local
IP.1 = 127.0.0.1
EOF
echo "[+] Created v3 ext file"

openssl x509 -req -in certs/$MYCERT.csr -CA certs/$CANAME.crt -CAkey certs/private/$CANAME.key -CAcreateserial -out certs/$MYCERT.crt -days 365 -extfile certs/$MYCERT.v3.ext
echo "[+] Created CA"
echo "[+] Done"
