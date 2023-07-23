// Attestation test vectors generated with ECDSA/ECC NIST P-256 key 
// extracted from a x509 certificate.
// Attestation is the process by which an entity produces evidence about itself 
// that another party can use to evaluate the trustworthiness of that entity.
// NIST P-256 ECDSA as specified in FIPS 186-4: Digital Signature Standard
// Author: sreejith.naarakathil@gmail.com

use p256::{ecdsa::{signature::Signer, SigningKey, Signature, signature::Verifier, VerifyingKey}};
use rand_core::OsRng;
use hex::FromHex;
use pkcs8::*;
use pkcs8::der::Decodable;

extern crate pem;
use pem::parse;
use der_parser::parse_der;
use der_parser::der::*;

use pkcs8::PrivateKeyInfo;
//use pkcs8::FromPrivateKey;
//use pkcs8::der::Decodable;
//use generic_array::GenericArray;
//use generic_array::typenum::U16;

use x509_parser::prelude::*;

fn main() {
    let custom_data1 = "001122334466778899";
    println!("custom_data1 {}\n", custom_data1);
    let custom_data2 = "99887766554433221100";
    println!("custom_data2 {}\n", custom_data2);
    let custom_data3 = "0A0B0C0D0E0F";
    println!("custom_data3 {}\n", custom_data3);
    let data = format!("{}{}{}", custom_data1, custom_data2, custom_data3);
    println!("Data to be attested: {}\n", data);
    let message: Vec<u8> = Vec::from_hex(data).expect("Invalid Hex String");

    // 1. Test CA used for generating attestation certificate
    static CA_DER: &[u8] = include_bytes!("../../test-ca/ecdsa/ca.der");
    static INTER_DER: &[u8] = include_bytes!("../../test-ca/ecdsa/inter.der");
    static INTER_KEY: &[u8] = include_bytes!("../../test-ca/ecdsa/inter.key");

    // 2. Check attestation certificate
    let res = X509Certificate::from_der(CA_DER);
    match res {
        Ok((rem, cert)) => {
            assert!(rem.is_empty());
            // cert is Root CA certificate
            assert_eq!(cert.version(), X509Version::V3);
            println!("Cert.subject {}\n", cert.subject());
            println!("Cert.is_ca {}\n", cert.is_ca());
            let issuer_public_key = cert.public_key();
            println!("Cert.verify_signature {}\n", cert.verify_signature(Some(issuer_public_key)).is_ok());

            let res = X509Certificate::from_der(INTER_DER);
            match res {
                Ok((rem, cert)) => {
                    assert!(rem.is_empty());
                    // cert is Intermediate CA certificate
                    assert_eq!(cert.version(), X509Version::V3);
                    println!("Cert.subject {}\n", cert.subject());
                    println!("Cert.is_ca {}\n", cert.is_ca());
                    println!("Cert.verify_signature {}\n", cert.verify_signature(Some(issuer_public_key)).is_ok());
                },
                _ => panic!("x509 parsing failed: {:?}", res),
            }
        },
        _ => panic!("x509 parsing failed: {:?}", res),
    }

    // 3. Setup attestation key (Private key of the Intermediate CA)
    let mut INTER_PUB_KEY:&[u8] = &[0];
    let mut INTER_PRI_KEY:&[u8] = &[0];
    let priv_key = parse(INTER_KEY).unwrap().contents;
    // println!("priv_key: {:02X?}", priv_key);
    let (_, parsed_der_priv) = parse_der(&priv_key).unwrap();
    // println!("parsed_der_priv: {:02X?}", parsed_der_priv);
    // PrivateKeyInfo ::= SEQUENCE {
    //     version                   Version,
    //     privateKeyAlgorithm       PrivateKeyAlgorithmIdentifier,
    //     privateKey                PrivateKey,
    //     attributes           [0]  IMPLICIT Attributes OPTIONAL }
    //   Version ::= INTEGER
    //   PrivateKeyAlgorithmIdentifier ::= AlgorithmIdentifier
    //   PrivateKey ::= OCTET STRING
    //   Attributes ::= SET OF Attribute
    //
    // AlgorithmIdentifier ::= SEQUENCE {
    //     algorithm       OBJECT IDENTIFIER,
    //     parameters      ANY DEFINED BY algorithm OPTIONAL
    //   }
    let (rem, seq) = parse_der_sequence_defined(|content| {
        let (rem, obj1) = parse_der_integer(content)?;
        let (rem, obj2) = parse_der_sequence(rem)?;
        let (rem, obj3) = parse_der_octetstring(rem)?;
        // println!("obj3: {:02X?}\n", obj3.as_slice().unwrap());
        let ECPrivateKeyDer = obj3.as_slice().unwrap();
        // ECPrivateKey ::= SEQUENCE {
        //     version INTEGER { ecPrivkeyVer1(1) } (ecPrivkeyVer1),
        //     privateKey OCTET STRING,
        //     parameters [0] ECDomainParameters {{ SECGCurveNames }} OPTIONAL,
        //     publicKey [1] BIT STRING OPTIONAL
        //   }
        let (rem, seq) = parse_der_sequence_defined(|content| {
            let (rem, obj1) = parse_der_integer(content)?;
            let (rem, obj2) = parse_der_octetstring(rem)?;
            INTER_PRI_KEY = obj2.as_slice().unwrap();
            println!("Attestation Key (Private Key of Intermediate CA) {:02X?}\n", INTER_PRI_KEY);                                    
            Ok((rem, vec![obj1, obj2]))                                
        })(&ECPrivateKeyDer)
        .expect("parsing failed");

        Ok((rem, vec![obj1, obj2, obj3]))                                
    })(&priv_key)
    .expect("parsing failed");

    // 4. Create attestation of the message 
    let res = X509Certificate::from_der(INTER_DER);
    match res {
        Ok((rem, cert)) => {
            assert!(rem.is_empty());
            // cert is Intermediate CA certificate
            let public_key_der = cert.public_key().raw;
            //SubjectPublicKeyInfo  ::=  SEQUENCE  {
            //    algorithm            AlgorithmIdentifier,
            //    subjectPublicKey     BIT STRING  }
            //
            // AlgorithmIdentifier ::= SEQUENCE {
            //     algorithm       OBJECT IDENTIFIER,
            //     parameters      ANY DEFINED BY algorithm OPTIONAL
            //   }
            let (rem, seq) = parse_der_sequence_defined(|content| {
                let (rem, obj1) = parse_der_sequence(content)?;
                let (rem, obj2) = parse_der_bitstring(rem)?;
                INTER_PUB_KEY = obj2.as_slice().unwrap();
                println!("Public Key of Intermediate CA {:02X?}\n", INTER_PUB_KEY);  

                // Create an ecdsa signature using the private key
                let signing_key = SigningKey::from_bytes(INTER_PRI_KEY).unwrap();
                // println!("Signing Key {:02X?}\n\n", signing_key.to_bytes());
                let signature = signing_key.sign(&message);
                // Verify signature using the public key
                let verifying_key = VerifyingKey::from_sec1_bytes(INTER_PUB_KEY).unwrap();
                // println!("Verifying Key {:02X?}\n\n", verifying_key.to_encoded_point(false).as_bytes());  
                assert!(verifying_key.verify(&message, &signature).is_ok());

                Ok((rem, vec![obj1, obj2]))                                
            })(&public_key_der)
            .expect("parsing failed");
        },
        _ => panic!("x509 parsing failed: {:?}", res),
    }    

    // 5. Test attestation of the message 
    let signing_key = SigningKey::from_bytes(INTER_PRI_KEY).unwrap();
    // println!("Signing Key {:02X?}\n\n", signing_key.to_bytes());
    let signature = signing_key.sign(&message);
    println!("Attestation of the message {:02X?}\n", signature.to_asn1());
    // Test attestation using the public key derived from the private key of the Intermediate CA
    let verifying_key = VerifyingKey::from(&signing_key);
    // println!("Public Key of Intermediate CA (derived) {:02X?}\n", verifying_key.to_encoded_point(false).as_bytes());  
    assert!(verifying_key.verify(&message, &signature).is_ok());
}