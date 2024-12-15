from flask import Flask, render_template, request, redirect, url_for
from py2neo import Graph
from pymongo import MongoClient
from flask_pymongo import PyMongo

# Initialize Flask app
app = Flask(__name__)

# Connect to MongoDB (ensure it's running on localhost)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Protein_Database"  # Change this if needed
mongo = PyMongo(app)

# Connect to Neo4j (ensure it's running on localhost)
graph = Graph("bolt://localhost:7687", auth=("neo4j", "#Samsom1"))  # Replace with your credentials

# Homepage Route
@app.route('/')
def index():
    return render_template('index.html')  # Ensure you have index.html in the templates folder

# Protein Search Route
@app.route('/search', methods=['POST'])
def search_protein():
    protein_entry = request.form.get('protein_entry')
    
    # Search MongoDB for protein details
    protein = mongo.db.Domain_in_One.find_one({"Entry": protein_entry})
    
    if protein:
        protein_details = {
            "Name": protein['Entry Name'],
            "Gene Names": protein['Gene Names'],
            "Organism": protein['Organism'],
        }
    else:
        protein_details = "Protein not found in MongoDB."
    
    # Search Neo4j for protein relationships
    query = f"MATCH (p:Protein {{entry: '{protein_entry}'}})-[:SIMILAR_TO]-(neighbor) RETURN p, neighbor LIMIT 5"
    results = graph.run(query)
    relationships = []
    for record in results:
        relationships.append(f"{record['p']['entry']} <-> {record['neighbor']['entry']}")
    
    return render_template('index.html', protein_details=protein_details, relationships=relationships)

# Statistics Route
@app.route('/statistics')
def show_statistics():
    # Query MongoDB for labeled and unlabeled proteins
    labeled_count = mongo.db.Domain_in_One.count_documents({"EC number": {"$ne": None}})
    unlabeled_count = mongo.db.Domain_in_One.count_documents({"EC number": None})

    # Query Neo4j for isolated proteins
    query = "MATCH (p:Protein) WHERE NOT (p)-[:SIMILAR_TO]-() RETURN COUNT(p) AS isolated_count"
    isolated_count = graph.run(query).data()[0]['isolated_count']

    stats = {
        "Labeled Proteins": labeled_count,
        "Unlabeled Proteins": unlabeled_count,
        "Isolated Proteins": isolated_count,
    }

    return render_template('statistics.html', stats=stats)

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5001)