import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def build_recommendations(products):
    """
    Build TF-IDF matrix and cosine similarity for all products
    """
    # Adjust field names according to your Product model
    df = pd.DataFrame(list(products.values(
        'id', 'name', 'desc', 'category__title', 'brands__title'
    )))
    
    # Combine fields into a single text feature
    df['features'] = (
        df['name'] + ' ' +
        df['desc'].fillna('') + ' ' +
        df['category__title'].fillna('') + ' ' +
        df['brands__title'].fillna('')
    )
    
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['features'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    return df, cosine_sim

def get_recommendations(product_id, df, cosine_sim, top_n=6):
    """
    Return a list of recommended product IDs
    """
    indices = pd.Series(df.index, index=df['id'])
    idx = indices[product_id]
    
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Exclude the product itself
    sim_scores = [s for s in sim_scores if s[0] != idx]
    
    top_indices = [i[0] for i in sim_scores[:top_n]]
    return df['id'].iloc[top_indices].tolist()
