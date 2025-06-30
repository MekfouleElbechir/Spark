"""
Projet Amis Communs avec PySpark
Objectif : Identifier les amis communs entre utilisateurs dans un réseau social
Auteur : Mekfoula El Bechir
"""

import os
import subprocess
from pyspark import SparkContext

def installer_spark():
    # Installer Java
    os.system("apt-get install openjdk-11-jdk-headless -qq > /dev/null")

    # Essayer plusieurs sources pour télécharger Spark
    urls = [
        "https://archive.apache.org/dist/spark/spark-3.4.1/spark-3.4.1-bin-hadoop3.tgz",
        "https://dlcdn.apache.org/spark/spark-3.4.1/spark-3.4.1-bin-hadoop3.tgz",
        "https://downloads.apache.org/spark/spark-3.4.1/spark-3.4.1-bin-hadoop3.tgz"
    ]

    for url in urls:
        print(f"Tentative de téléchargement depuis : {url}")
        result = subprocess.run(["wget", "-q", url], capture_output=True)
        if result.returncode == 0 and os.path.exists("spark-3.4.1-bin-hadoop3.tgz"):
            print("Téléchargement réussi !")
            os.system("tar xf spark-3.4.1-bin-hadoop3.tgz")
            print("Extraction réussie !")
            return True
        else:
            print(f"Échec du téléchargement depuis {url}")

    print("Échec du téléchargement, installation via pip...")
    os.system("pip install -q pyspark==3.4.1")
    return False

def configurer_environnement():
    os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-11-openjdk-amd64"
    if os.path.exists("/content/spark-3.4.1-bin-hadoop3"):
        os.environ["SPARK_HOME"] = "/content/spark-3.4.1-bin-hadoop3"
        import findspark
        findspark.init()
        print("Utilisation de Spark installé manuellement")
    else:
        print("Utilisation de PySpark installé via pip")

def parser_ligne(ligne):
    parties = ligne.strip().split()
    user_id = int(parties[0])
    nom = parties[1]
    amis = list(map(int, parties[2].split(','))) if len(parties) > 2 else []
    return (user_id, nom, amis)

def creer_paires(user_data):
    user_id, nom, amis = user_data
    paires = []
    for ami_id in amis:
        paire = (min(user_id, ami_id), max(user_id, ami_id))
        amis_utilisateur = set(amis) - {ami_id}
        paires.append((paire, amis_utilisateur))
    return paires

def main():
    installer_spark()
    configurer_environnement()

    sc = SparkContext(appName="AmisCommuns")

    donnees = [
        "1 Sidi 2,3,4",
        "2 Mohamed 1,3,5",
        "3 Amine 1,2,5",
        "4 Sara 1",
        "5 Salma 2,3"
    ]

    lignes = sc.parallelize(donnees)
    users_data = lignes.map(parser_ligne)
    noms = users_data.map(lambda x: (x[0], x[1])).collectAsMap()

    paires = users_data.flatMap(creer_paires)
    amis_communs = paires.reduceByKey(lambda a, b: a & b)

    print("Toutes les paires ayant des amis communs :")
    resultats = amis_communs.filter(lambda x: len(x[1]) > 0).collect()
    for ((id1, id2), amis) in resultats:
        print(f"{id1} {noms[id1]} {id2} {noms[id2]} {sorted(amis)}")

    print("\n" + "="*50)

    cible = amis_communs.filter(lambda x: x[0] == (1, 2)).collect()
    print("Résultat pour la paire (1, 2) :")
    for ((id1, id2), amis) in cible:
        print(f"{id1}<{noms[id1]}>{id2}<{noms[id2]}>{sorted(amis)}")

    sc.stop()

if __name__ == "__main__":
    main()
