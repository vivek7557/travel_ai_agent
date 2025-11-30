import pinecone
from sentence_transformers import SentenceTransformer

class AgentMemory:
    
    def __init__(self):
        # Initialize vector database for semantic search
        pinecone.init(
            api_key=os.environ.get("PINECONE_API_KEY"),
            environment="us-west1-gcp"
        )
        self.index = pinecone.Index("customer-memory")
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
    
    def remember_customer(self, customer_id: str, info: Dict):
        """
        Store customer preferences and history
        """
        # Create embedding of customer info
        text = f"{info['preferences']} {info['past_trips']}"
        embedding = self.encoder.encode(text).tolist()
        
        # Store in vector database
        self.index.upsert([(
            customer_id,
            embedding,
            {
                "preferences": info['preferences'],
                "past_trips": info['past_trips'],
                "budget_range": info['budget_range'],
                "travel_style": info['travel_style']
            }
        )])
    
    def recall_customer(self, customer_id: str) -> Dict:
        """
        Retrieve everything we know about this customer
        """
        results = self.index.fetch([customer_id])
        if customer_id in results['vectors']:
            return results['vectors'][customer_id]['metadata']
        return {}
    
    def find_similar_customers(self, preferences: str, top_k=5):
        """
        Find customers with similar preferences for recommendations
        """
        embedding = self.encoder.encode(preferences).tolist()
        results = self.index.query(embedding, top_k=top_k)
        return results
