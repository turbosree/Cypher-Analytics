
// In windows environment setup openssl using https://github.com/Microsoft/vcpkg

use openssl::pkey::Private;
use openssl::x509::X509;
use std::fs::File;
use std::io::{BufReader, Read};
use openssl::pkey::PKey;
use hex;

fn main() {
    // Open the X509 certificate file
    let file = File::open("../test-ca/ecdsa/end-cert.pem").unwrap();
    let reader = BufReader::new(file);

    // Parse the X509 certificate
    let cert = X509::from_pem(&mut reader.buffer()).unwrap();

    // Extract the public key from the X509 certificate
    let public_key = cert.public_key().unwrap();

    // Extract the private key from the X509 certificate
    // let private_key = cert.private_key().unwrap().to_owned().private_key_pem().unwrap();
    let private_key_file = File::open("../test-ca/ecdsa/end.pem").unwrap();
    let private_key_reader = BufReader::new(private_key_file);
    let private_key = PKey::private_key_from_pem(&private_key_reader.buffer()).unwrap();

    println!("Private key: {:?}", private_key);
    println!("Public key: {:?}", public_key);
}
