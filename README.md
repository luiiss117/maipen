# Maipen

 A **Flask-based machine management system** for tracking machines and CTF targets.

 Maipen is also a practical security-focused development project, implementing common web application security controls around authentication, authorization, input validation, and secure session handling.

 ## Development Status

 Maipen is under development. Features, security controls, and application structure may change as the project evolves.

---

 ## Features

 ### Authentication

- User registration, login, and logout
- Argon2 password hashing
- Session-based authentication
- User account deletion

 ### Machine Management

- Add, view, and delete machines
- IPv4 and operating system information
- Machine descriptions
- UUID-based machine identification

 ### Service Management

- Add and remove services
- View network protocols, ports, names, and versions
- Associate services with machines

 ### Deployment

- SQLite database
- Docker and Docker Compose
- HTTPS support

---

 ## Security

- **Argon2** password hashing
- **Parameterized SQLite queries** to mitigate SQL injection
- **Authorization checks** to prevent unauthorized access to user-owned machines
- **UUID-based resource identification** and ownership validation against IDOR
- **CSRF token protection** for state-changing requests
- **Server-side input validation** for machine and service data
- **Session security** for authenticated users
- **User enumeration mitigation** in the login page
- **HTTP 401** responses for unauthenticated access
- **POST-only destructive actions**
- **HTTPS with ML-DSA-87** for experimental post-quantum cryptography

 > ML-DSA-87 support depends on the TLS/certificate configuration and is currently incompatible with Firefox in this setup. Chromium-based browsers are recommended for testing.

 The project is not formally security audited and should not be considered production-hardened.

---

 ## Technology Stack

- Python / Flask
- SQLite
- HTML / CSS
- Docker / Docker Compose
- Argon2
- HTTPS / ML-DSA-87

---

 # Running with Docker

 ### Requirements

 - Git
- Docker
- Docker Compose

 ### Clone

```
git clone https://github.com/luiiss117/maipen.git
cd maipen
```

 ### Configure

 Create `app/.env`:

```
touch app/.env
```

 Generate a secret key:

```
python -c "import secrets; print(secrets.token_hex(32))"
```

 Add it to `.env`:

```
SECRET_KEY=your_generated_key_here
```

 ### Start

```
docker compose up
```

 The application will be available at:

```
http://localhost:5000
```

 Run in the background:

```
docker compose up -d
```

 Stop:

```
docker compose down
```

---

 # Project Structure

```
maipen/
├── app/
│   ├── database/
│   │   ├── __init__.py
│   │   ├── machine.py
│   │   ├── service.py
│   │   └── user.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── machines.py
│   │   └── services.py
│   └── __init__.py
├── app.py
├── CHANGELOG.md
├── Dockerfile
├── docker-compose.yml
├── LICENSE.md
├── README.md
└── requirements.txt
```

---

 # Development

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

 Windows:

```
.venv\Scripts\activate
```

 ## To start HTTPs

Run the `create_certs.sh` script.
```
$ chmod +x create_certs.sh
$ ./create_certs.sh
[+] Created 'certs/' directory
[+] Created private key
[+] Created certificate
-----
[+] Created certificate for service
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names
[alt_names]
DNS.1 = maipen.local
IP.1 = 127.0.0.1
[+] Created v3 ext file
Certificate request self-signature ok
subject=CN=Maipen Web Server, C=AT, ST=Madrid, L=Madrid, O=Maipen Local
[+] Created CA
[+] Done
```

 Uncomment this line in `app.py`:
 ```
#    app.run(host="127.0.0.1",port=5000,debug=False, ssl_context=('certs/web-maipen.crt', 'certs/private/web-maipen.key'))
 ```

 Comment this line instead:

```
 app.run(host="127.0.0.1",port=5000,debug=False)
```
