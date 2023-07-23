# Globally unique identifiers: URIs provide a way to create globally 
# unique identifiers for resources, ensuring that there are no conflicts 
# or ambiguities between different datasets or systems.
# Eg: https://example.org/floors/1547809435
#
# Below example generates GUIDs for all the entities in a Building ontology
#
# Author: Sreejith.Naarakathil@gmail.com

import json
import hashlib

def create_uid(entity, domain="http://example.org/building-ontology/"):
    return f"{domain}{entity}"

def generate_unique_number(uri):
    hash_object = hashlib.sha256(uri.encode('utf-8'))
    return int.from_bytes(hash_object.digest()[:4], byteorder='big')

def main():
    with open("building-ontology.jsonld", "r") as file:
        ontology_data = json.load(file)

    # Get entities from the ontology
    entities = ontology_data["@graph"]

    # Generate UIDs and unique numbers for all entities
    for entity in entities:
        # Skip if the entity is an RDF property
        if entity["@type"] == "rdf:Property":
            continue

        uid = create_uid(entity["@id"])
        unique_number = generate_unique_number(uid)
        print(f"{entity['rdfs:label']}: {uid}, Unique Number: {unique_number}")

if __name__ == "__main__":
    main()
