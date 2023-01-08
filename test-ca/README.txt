Introduction
------------
A test Root CA based on https://github.com/rustls/rustls/tree/main/test-ca
CAUTION: Private keys are committed in this folder. Do not use this CA for any kind of production environments! 


Test output
-----------

$ sh build-a-pki.sh
+ rm -rf rsa/ ecdsa/ eddsa/
+ mkdir -p rsa/ ecdsa/ eddsa/
+ openssl req -nodes -x509 -days 3650 -newkey rsa:4096 -keyout rsa/ca.key -out rsa/ca.cert -sha256 -batch -subj '/CN=ponytown RSA CA'
Generating a RSA private key
.....................................................................................................................................................................++++
.....................................++++
writing new private key to 'rsa/ca.key'
-----
+ openssl req -nodes -newkey rsa:3072 -keyout rsa/inter.key -out rsa/inter.req -sha256 -batch -subj '/CN=ponytown RSA level 2 intermediate'
Generating a RSA private key
.......................................................................................................................................................................++++
................................................................................................................................++++
writing new private key to 'rsa/inter.key'
-----
+ openssl req -nodes -newkey rsa:2048 -keyout rsa/end.key -out rsa/end.req -sha256 -batch -subj /CN=testserver.com
Generating a RSA private key
.................................................+++++
...................+++++
writing new private key to 'rsa/end.key'
-----
+ openssl rsa -in rsa/end.key -out rsa/end.rsa
writing RSA key
+ openssl req -nodes -newkey rsa:2048 -keyout rsa/client.key -out rsa/client.req -sha256 -batch -subj '/CN=ponytown client'
Generating a RSA private key
..............+++++
.......................................................................+++++
writing new private key to 'rsa/client.key'
-----
+ openssl rsa -in rsa/client.key -out rsa/client.rsa
writing RSA key
+ openssl ecparam -name prime256v1 -out ecdsa/nistp256.pem
+ openssl ecparam -name secp384r1 -out ecdsa/nistp384.pem
+ openssl req -nodes -x509 -newkey ec:ecdsa/nistp384.pem -keyout ecdsa/ca.key -out ecdsa/ca.cert -sha256 -batch -days 3650 -subj '/CN=ponytown ECDSA CA'
Generating an EC private key
writing new private key to 'ecdsa/ca.key'
-----
+ openssl req -nodes -newkey ec:ecdsa/nistp256.pem -keyout ecdsa/inter.key -out ecdsa/inter.req -sha256 -batch -days 3000 -subj '/CN=ponytown ECDSA level 2 intermediate'
Ignoring -days; not generating a certificate
Generating an EC private key
writing new private key to 'ecdsa/inter.key'
-----
+ openssl req -nodes -newkey ec:ecdsa/nistp256.pem -keyout ecdsa/end.key -out ecdsa/end.req -sha256 -batch -days 2000 -subj /CN=testserver.com
Ignoring -days; not generating a certificate
Generating an EC private key
writing new private key to 'ecdsa/end.key'
-----
+ openssl req -nodes -newkey ec:ecdsa/nistp384.pem -keyout ecdsa/client.key -out ecdsa/client.req -sha256 -batch -days 2000 -subj '/CN=ponytown client'
Ignoring -days; not generating a certificate
Generating an EC private key
writing new private key to 'ecdsa/client.key'
-----
+ openssl genpkey -algorithm Ed25519 -out eddsa/ca.key
+ openssl req -nodes -x509 -key eddsa/ca.key -out eddsa/ca.cert -sha256 -batch -days 3650 -subj '/CN=ponytown EdDSA CA'
+ openssl genpkey -algorithm Ed25519 -out eddsa/inter.key
+ openssl req -nodes -new -key eddsa/inter.key -out eddsa/inter.req -sha256 -batch -subj '/CN=ponytown EdDSA level 2 intermediate'
+ openssl genpkey -algorithm Ed25519 -out eddsa/end.key
+ openssl req -nodes -new -key eddsa/end.key -out eddsa/end.req -sha256 -batch -subj /CN=testserver.com
+ openssl genpkey -algorithm Ed25519 -out eddsa/client.key
+ openssl req -nodes -new -key eddsa/client.key -out eddsa/client.req -sha256 -batch -subj '/CN=ponytown client'
+ for kt in rsa ecdsa eddsa
+ openssl x509 -req -in rsa/inter.req -out rsa/inter.cert -CA rsa/ca.cert -CAkey rsa/ca.key -sha256 -days 3650 -set_serial 123 -extensions v3_inter -extfile openssl.cnf
Signature ok
subject=CN = ponytown RSA level 2 intermediate
Getting CA Private Key
+ openssl x509 -req -in rsa/end.req -out rsa/end.cert -CA rsa/inter.cert -CAkey rsa/inter.key -sha256 -days 2000 -set_serial 456 -extensions v3_end -extfile openssl.cnf
Signature ok
subject=CN = testserver.com
Getting CA Private Key
+ openssl x509 -req -in rsa/client.req -out rsa/client.cert -CA rsa/inter.cert -CAkey rsa/inter.key -sha256 -days 2000 -set_serial 789 -extensions v3_client -extfile openssl.cnf
Signature ok
subject=CN = ponytown client
Getting CA Private Key
+ cat rsa/inter.cert rsa/ca.cert
+ cat rsa/end.cert rsa/inter.cert rsa/ca.cert
+ cat rsa/inter.cert rsa/ca.cert
+ cat rsa/client.cert rsa/inter.cert rsa/ca.cert
+ openssl asn1parse -in rsa/ca.cert -out rsa/ca.der
+ for kt in rsa ecdsa eddsa
+ openssl x509 -req -in ecdsa/inter.req -out ecdsa/inter.cert -CA ecdsa/ca.cert -CAkey ecdsa/ca.key -sha256 -days 3650 -set_serial 123 -extensions v3_inter -extfile openssl.cnf
Signature ok
subject=CN = ponytown ECDSA level 2 intermediate
Getting CA Private Key
+ openssl x509 -req -in ecdsa/end.req -out ecdsa/end.cert -CA ecdsa/inter.cert -CAkey ecdsa/inter.key -sha256 -days 2000 -set_serial 456 -extensions v3_end -extfile openssl.cnf
Signature ok
subject=CN = testserver.com
Getting CA Private Key
+ openssl x509 -req -in ecdsa/client.req -out ecdsa/client.cert -CA ecdsa/inter.cert -CAkey ecdsa/inter.key -sha256 -days 2000 -set_serial 789 -extensions v3_client -extfile openssl.cnf
Signature ok
subject=CN = ponytown client
Getting CA Private Key
+ cat ecdsa/inter.cert ecdsa/ca.cert
+ cat ecdsa/end.cert ecdsa/inter.cert ecdsa/ca.cert
+ cat ecdsa/inter.cert ecdsa/ca.cert
+ cat ecdsa/client.cert ecdsa/inter.cert ecdsa/ca.cert
+ openssl asn1parse -in ecdsa/ca.cert -out ecdsa/ca.der
+ for kt in rsa ecdsa eddsa
+ openssl x509 -req -in eddsa/inter.req -out eddsa/inter.cert -CA eddsa/ca.cert -CAkey eddsa/ca.key -sha256 -days 3650 -set_serial 123 -extensions v3_inter -extfile openssl.cnf
Signature ok
subject=CN = ponytown EdDSA level 2 intermediate
Getting CA Private Key
+ openssl x509 -req -in eddsa/end.req -out eddsa/end.cert -CA eddsa/inter.cert -CAkey eddsa/inter.key -sha256 -days 2000 -set_serial 456 -extensions v3_end -extfile openssl.cnf
Signature ok
subject=CN = testserver.com
Getting CA Private Key
+ openssl x509 -req -in eddsa/client.req -out eddsa/client.cert -CA eddsa/inter.cert -CAkey eddsa/inter.key -sha256 -days 2000 -set_serial 789 -extensions v3_client -extfile openssl.cnf
Signature ok
subject=CN = ponytown client
Getting CA Private Key
+ cat eddsa/inter.cert eddsa/ca.cert
+ cat eddsa/end.cert eddsa/inter.cert eddsa/ca.cert
+ cat eddsa/inter.cert eddsa/ca.cert
+ cat eddsa/client.cert eddsa/inter.cert eddsa/ca.cert
+ openssl asn1parse -in eddsa/ca.cert -out eddsa/ca.der

