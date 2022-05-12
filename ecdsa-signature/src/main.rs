// Signature test vectors generated with ECDSA/ECC NIST P-256
// NIST P-256 ECDSA as specified in FIPS 186-4: Digital Signature Standard
// Author: sreejith.naarakathil@gmail.com

use p256::ecdsa::{signature::Signer, SigningKey};
use rand_core::OsRng;
use hex::FromHex;

fn main() {
    let custom_data1 = "001122334466778899";
    println!("custom_data1 {}\n", custom_data1);
    let custom_data2 = "99887766554433221100";
    println!("custom_data2 {}\n", custom_data2);
    let custom_data3 = "0A0B0C0D0E0F";
    println!("custom_data3 {}\n", custom_data3);
    let data = format!("{}{}{}", custom_data1, custom_data2, custom_data3);
    println!("Message {}\n", data);
    let message: Vec<u8> = Vec::from_hex(data).expect("Invalid Hex String");
    
    // Signing the message
    let signing_key = SigningKey::random(&mut OsRng);
    println!("Signing Key {:02X?}\n\n", signing_key.to_bytes());
    let signature = signing_key.sign(&message);
    println!("{:02X?}\n", signature.to_asn1());

    // Verification of the signature
    use p256::ecdsa::{signature::Verifier, VerifyingKey};
    let verifying_key = VerifyingKey::from(&signing_key);
    assert!(verifying_key.verify(&message, &signature).is_ok());
}
