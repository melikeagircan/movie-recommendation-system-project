from app.db.session import SessionLocal
from app.services.recommender_service import RecommenderService
import matplotlib.pyplot as plt
import sys

def test_cluster_analysis():
    print("Starting cluster analysis...")
    db = SessionLocal()
    try:
        print("Creating recommender service...")
        recommender = RecommenderService(db)
        
        print("Preparing features...")
        recommender.prepare_features(db)
        print(f"Number of movies: {len(recommender.movie_ids)}")
        
        print("Plotting cluster analysis...")
        # Grafikleri interaktif modda göster
        plt.ion()  # Interaktif modu aç
        
        # Küme analizini çalıştır ve grafikleri göster
        optimal_k = recommender.plot_cluster_analysis()
        print(f"Optimal number of clusters: {optimal_k}")
        
        # Grafikleri ekranda tut
        plt.show(block=True)
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()
        print("Database connection closed.")

if __name__ == "__main__":
    # Matplotlib backend kontrolü
    print(f"Matplotlib backend: {plt.get_backend()}")
    
    # Alternatif backend denemesi
    try:
        plt.switch_backend('TkAgg')  # veya 'Qt5Agg'
        test_cluster_analysis()
    except Exception as e:
        print(f"Error with TkAgg backend: {str(e)}")
        try:
            plt.switch_backend('Qt5Agg')
            test_cluster_analysis()
        except Exception as e:
            print(f"Error with Qt5Agg backend: {str(e)}")
            print("Trying default backend...")
            test_cluster_analysis() 