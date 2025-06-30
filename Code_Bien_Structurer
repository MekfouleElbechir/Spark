"""
Projet Amis Communs avec PySpark
Objectif: Identifier les amis communs entre utilisateurs dans un réseau social
Auteur: Mekfoula El Bechir
"""

from pyspark import SparkContext, SparkConf
import sys
from typing import List, Tuple, Set, Dict

class MutualFriendsAnalyzer:
    """Analyseur d'amis communs utilisant PySpark"""
    
    def __init__(self, app_name: str = "MutualFriends"):
        """Initialise l'analyseur avec la configuration Spark"""
        self.conf = SparkConf().setAppName(app_name).setMaster("local[*]")
        self.sc = SparkContext(conf=self.conf)
        
    def parse_user_data(self, line: str) -> Tuple[int, str, List[int]]:
        """
        Parse une ligne de données utilisateur
        
        Args:
            line: Ligne au format "user_id nom friend_id1,friend_id2,..."
            
        Returns:
            Tuple (user_id, nom, liste_amis)
        """
        parts = line.strip().split()
        user_id = int(parts[0])
        name = parts[1]
        
        # Gestion des utilisateurs sans amis
        if len(parts) > 2:
            friends = [int(fid) for fid in parts[2].split(',') if fid.strip()]
        else:
            friends = []
            
        return (user_id, name, friends)
    
    def create_friend_pairs(self, user_data: Tuple[int, str, List[int]]) -> List[Tuple[Tuple[int, int], Set[int]]]:
        """
        Crée des paires d'amis avec leurs amis potentiellement communs
        
        Args:
            user_data: Tuple (user_id, nom, liste_amis)
            
        Returns:
            Liste de tuples ((id1, id2), ensemble_amis_potentiels)
        """
        user_id, name, friends = user_data
        pairs = []
        
        for friend_id in friends:
            # Créer une paire ordonnée (plus petit ID en premier)
            pair = (min(user_id, friend_id), max(user_id, friend_id))
            # Amis potentiellement communs = tous les amis sauf celui de la paire
            potential_common = set(friends) - {friend_id}
            pairs.append((pair, potential_common))
            
        return pairs
    
    def find_mutual_friends(self, data: List[str]) -> Dict[Tuple[int, int], Set[int]]:
        """
        Trouve tous les amis communs dans le réseau
        
        Args:
            data: Liste des lignes de données
            
        Returns:
            Dictionnaire {(id1, id2): ensemble_amis_communs}
        """
        # Convertir en RDD
        lines_rdd = self.sc.parallelize(data)
        
        # Parser les données
        users_data = lines_rdd.map(self.parse_user_data)
        
        # Créer le mapping ID -> Nom
        self.names_map = users_data.map(lambda x: (x[0], x[1])).collectAsMap()
        
        # Créer les paires d'amis
        pairs_rdd = users_data.flatMap(self.create_friend_pairs)
        
        # Calculer les amis communs par intersection
        mutual_friends = pairs_rdd.reduceByKey(lambda a, b: a & b)
        
        # Retourner seulement les paires avec des amis communs
        return mutual_friends.filter(lambda x: len(x[1]) > 0).collectAsMap()
    
    def display_results(self, mutual_friends: Dict[Tuple[int, int], Set[int]], 
                       target_pair: Tuple[int, int] = (1, 2)):
        """
        Affiche les résultats de l'analyse
        
        Args:
            mutual_friends: Dictionnaire des amis communs
            target_pair: Paire cible à mettre en évidence
        """
        print("=" * 50)
        print(" ANALYSE DES AMIS COMMUNS")
        print("=" * 50)
        
        # Afficher tous les amis communs
        print("\n Tous les amis communs trouvés:")
        for (id1, id2), common in sorted(mutual_friends.items()):
            name1 = self.names_map.get(id1, f"User{id1}")
            name2 = self.names_map.get(id2, f"User{id2}")
            common_names = [self.names_map.get(fid, f"User{fid}") for fid in sorted(common)]
            print(f"  {id1}({name1}) et {id2}({name2}): {common_names}")
        
        # Résultat spécifique pour la paire cible
        print(f"\n RÉSULTAT SPÉCIFIQUE - Paire {target_pair}:")
        print("-" * 30)
        
        if target_pair in mutual_friends:
            id1, id2 = target_pair
            common = mutual_friends[target_pair]
            name1 = self.names_map.get(id1, f"User{id1}")
            name2 = self.names_map.get(id2, f"User{id2}")
            
            # Format demandé
            result = f"{id1}<{name1}>{id2}<{name2}>{sorted(common)}"
            print(f" {result}")
            
            # Explication
            common_names = [self.names_map.get(fid, f"User{fid}") for fid in sorted(common)]
            print(f"Explication: {' et '.join(common_names)} {'est' if len(common) == 1 else 'sont'} "
                  f"{'l\'ami commun' if len(common) == 1 else 'les amis communs'} "
                  f"entre {name1} et {name2}")
        else:
            print(f" Aucun ami commun trouvé entre les utilisateurs {target_pair}")
    
    def display_statistics(self, data: List[str], mutual_friends: Dict[Tuple[int, int], Set[int]]):
        """Affiche les statistiques de l'analyse"""
        print(f"\nSTATISTIQUES:")
        print(f"   Nombre total d'utilisateurs: {len(self.names_map)}")
        print(f"   Nombre de paires avec amis communs: {len(mutual_friends)}")
        
        # Statistiques détaillées
        total_common_friends = sum(len(friends) for friends in mutual_friends.values())
        print(f"   Nombre total d'amis communs: {total_common_friends}")
        
        if mutual_friends:
            avg_common = total_common_friends / len(mutual_friends)
            print(f"   Moyenne d'amis communs par paire: {avg_common:.2f}")
    
    def stop(self):
        """Arrête le contexte Spark"""
        self.sc.stop()

def main():
    """Fonction principale"""
    print(" Démarrage de l'analyse des amis communs...")
    
    # Données d'exemple
    data = [
        "1 Sidi 2,3,4",
        "2 Mohamed 1,3,5", 
        "3 Amine 1,2,5",
        "4 Sara 1",
        "5 Salma 2,3"
    ]
    
    print("\n Données d'entrée:")
    for i, line in enumerate(data, 1):
        print(f"  {i}. {line}")
    
    # Analyse
    analyzer = MutualFriendsAnalyzer()
    
    try:
        # Trouver les amis communs
        mutual_friends = analyzer.find_mutual_friends(data)
        
        # Afficher les résultats
        analyzer.display_results(mutual_friends)
        
        # Afficher les statistiques
        analyzer.display_statistics(data, mutual_friends)
        
    except Exception as e:
        print(f" Erreur lors de l'analyse: {e}")
        return 1
    
    finally:
        analyzer.stop()
    
    print("\n Analyse terminée avec succès!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
