import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)

class WhiskyRecommender:
    def __init__(self, whisky_data):
        """Initialize the recommender with whisky dataset"""
        self.whisky_data = whisky_data
        self.preprocess_data()
        logger.debug(f"Initialized recommender with {len(whisky_data)} bottles")
    
    def preprocess_data(self):
        """Prepare whisky data for recommendations"""
        # Ensure essential columns exist
        essential_columns = ['name', 'brand', 'spirit', 'price', 'proof', 'region']
        for col in essential_columns:
            if col not in self.whisky_data.columns:
                logger.warning(f"Missing column: {col}, adding it with default values")
                self.whisky_data[col] = 'Unknown' if col not in ['price', 'proof', 'age'] else 0
                
        # Add age column if not present
        if 'age' not in self.whisky_data.columns:
            logger.warning("Missing column: age, adding it with default values")
            self.whisky_data['age'] = 0
                
        # Ensure numeric columns are properly formatted
        self.whisky_data['price'] = pd.to_numeric(self.whisky_data['price'], errors='coerce')
        self.whisky_data['proof'] = pd.to_numeric(self.whisky_data['proof'], errors='coerce')
        self.whisky_data['age'] = pd.to_numeric(self.whisky_data['age'], errors='coerce')
        
        # Fill missing values
        self.whisky_data['price'] = self.whisky_data['price'].fillna(self.whisky_data['price'].median() if not self.whisky_data['price'].empty else 0)
        self.whisky_data['proof'] = self.whisky_data['proof'].fillna(self.whisky_data['proof'].median() if not self.whisky_data['proof'].empty else 0)
        self.whisky_data['age'] = self.whisky_data['age'].fillna(0)  # 0 for NAS (No Age Statement)
        
        # Extract features for similarity calculation
        self.feature_columns = ['price', 'proof', 'age']
        
        # Create vectorized features
        self.spirit_dummies = pd.get_dummies(self.whisky_data['spirit'], prefix='spirit')
        self.region_dummies = pd.get_dummies(self.whisky_data['region'], prefix='region')
        self.brand_dummies = pd.get_dummies(self.whisky_data['brand'], prefix='brand')
        
        # Combine features
        self.features_df = pd.concat([
            self.whisky_data[self.feature_columns],
            self.spirit_dummies,
            self.region_dummies,
            self.brand_dummies
        ], axis=1)
        
        # Normalize features
        self.scaler = StandardScaler()
        self.normalized_features = self.scaler.fit_transform(self.features_df)
        
        logger.debug("Data preprocessing complete")
    
    def get_recommendations(self, bar_data, num_recommendations=5):
        """
        Generate whisky recommendations based on user bar
        
        Parameters:
        - bar_data: List of user's bottles from BAXUS API
        - num_recommendations: Number of recommendations to generate
        
        Returns:
        - user_profile: Dict of user preferences
        - similar_recs: List of similar bottles to user's collection
        - complementary_recs: List of bottles that diversify collection
        - bar_stats: Statistics about user's collection
        """
        try:
            # Extract bottle info from bar data
            user_bottles = []
            for item in bar_data:
                if 'product' in item and item['product']:
                    bottle = item['product']
                    user_bottles.append({
                        'id': bottle.get('id'),
                        'name': bottle.get('name', 'Unknown'),
                        'brand': bottle.get('brand', 'Unknown'),
                        'spirit': bottle.get('spirit', 'Unknown'),
                        'price': bottle.get('price'),
                        'proof': bottle.get('proof'),
                        'region': bottle.get('region', 'Unknown'),
                        'age': bottle.get('age'),
                        'image_url': bottle.get('image_url')
                    })
            
            if not user_bottles:
                logger.warning("No valid bottles found in user bar data")
                return {}, [], [], {}
            
            # Create DataFrame of user bottles
            user_df = pd.DataFrame(user_bottles)
            
            # Analyze user preferences
            user_profile = self.analyze_user_preferences(user_df)
            
            # Find similar bottles (based on user preferences)
            similar_recs = self.find_similar_bottles(user_df, num_recommendations)
            
            # Find complementary bottles (to diversify collection)
            complementary_recs = self.find_complementary_bottles(user_df, user_profile, num_recommendations)
            
            # Get collection statistics
            bar_stats = self.calculate_bar_stats(user_df)
            
            return user_profile, similar_recs, complementary_recs, bar_stats
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}", exc_info=True)
            return {}, [], [], {}
    
    def analyze_user_preferences(self, user_df):
        """Extract user preferences from their bottle collection"""
        user_profile = {}
        
        # Price preferences
        if 'price' in user_df.columns and not user_df['price'].empty:
            price_stats = user_df['price'].describe()
            user_profile['avg_price'] = price_stats.get('mean', 0)
            user_profile['min_price'] = price_stats.get('min', 0)
            user_profile['max_price'] = price_stats.get('max', 0)
        else:
            user_profile['avg_price'] = 0
            user_profile['min_price'] = 0
            user_profile['max_price'] = 0
        
        # Preferred spirits
        if 'spirit' in user_df.columns:
            spirit_counts = user_df['spirit'].value_counts()
            user_profile['top_spirits'] = spirit_counts.head(3).to_dict()
        
        # Preferred regions
        if 'region' in user_df.columns:
            region_counts = user_df['region'].value_counts()
            user_profile['top_regions'] = region_counts.head(3).to_dict()
        
        # Preferred brands
        if 'brand' in user_df.columns:
            brand_counts = user_df['brand'].value_counts()
            user_profile['top_brands'] = brand_counts.head(3).to_dict()
        
        # Age preferences
        if 'age' in user_df.columns and not user_df['age'].empty:
            age_stats = user_df['age'].describe()
            user_profile['avg_age'] = age_stats.get('mean', 0)
        else:
            user_profile['avg_age'] = 0
        
        # Proof preferences
        if 'proof' in user_df.columns and not user_df['proof'].empty:
            proof_stats = user_df['proof'].describe()
            user_profile['avg_proof'] = proof_stats.get('mean', 0)
        else:
            user_profile['avg_proof'] = 0
        
        return user_profile
    
    def find_similar_bottles(self, user_df, num_recommendations=5):
        """Find bottles similar to user's collection"""
        # Get IDs of bottles in user's collection
        user_bottle_ids = set(user_df['id'].astype(str).tolist())
        
        # Create feature vectors for user bottles
        user_feature_vectors = []
        for _, bottle in user_df.iterrows():
            # Get similar features as in the whisky dataset
            features = {}
            
            # Numeric features
            for col in self.feature_columns:
                if col in bottle and not pd.isna(bottle[col]):
                    features[col] = bottle[col]
                else:
                    features[col] = 0
            
            # One-hot encoded features
            if 'spirit' in bottle and not pd.isna(bottle['spirit']):
                spirit_key = f"spirit_{bottle['spirit']}"
                if spirit_key in self.spirit_dummies.columns:
                    features[spirit_key] = 1
            
            if 'region' in bottle and not pd.isna(bottle['region']):
                region_key = f"region_{bottle['region']}"
                if region_key in self.region_dummies.columns:
                    features[region_key] = 1
            
            if 'brand' in bottle and not pd.isna(bottle['brand']):
                brand_key = f"brand_{bottle['brand']}"
                if brand_key in self.brand_dummies.columns:
                    features[brand_key] = 1
            
            # Create a DataFrame with the features
            bottle_features_df = pd.DataFrame([features])
            
            # Fill in missing columns from the full feature set
            for col in self.features_df.columns:
                if col not in bottle_features_df.columns:
                    bottle_features_df[col] = 0
            
            # Reorder columns to match the full feature set
            bottle_features_df = bottle_features_df[self.features_df.columns]
            
            # Scale features
            bottle_features_scaled = self.scaler.transform(bottle_features_df)
            user_feature_vectors.append(bottle_features_scaled[0])
        
        # Calculate average user profile vector
        if user_feature_vectors:
            user_profile_vector = np.mean(user_feature_vectors, axis=0).reshape(1, -1)
            
            # Calculate similarity between user profile and all whisky bottles
            similarity_scores = cosine_similarity(user_profile_vector, self.normalized_features)[0]
            
            # Get indices of most similar bottles, excluding user's existing bottles
            similar_indices = []
            for idx in np.argsort(similarity_scores)[::-1]:
                bottle_id = str(self.whisky_data.iloc[idx]['id'])
                if bottle_id not in user_bottle_ids:
                    similar_indices.append(idx)
                if len(similar_indices) >= num_recommendations:
                    break
            
            # Get recommended bottle details
            similar_bottles = []
            for idx in similar_indices:
                bottle = self.whisky_data.iloc[idx]
                
                # Extract reasoning based on similarity to user's collection
                reasoning = self.generate_similarity_reasoning(bottle, user_df)
                
                similar_bottles.append({
                    'id': bottle['id'],
                    'name': bottle['name'],
                    'brand': bottle['brand'],
                    'spirit': bottle['spirit'],
                    'region': bottle.get('region', 'Unknown'),
                    'age': bottle.get('age', 'NAS'),
                    'price': bottle['price'],
                    'proof': bottle['proof'],
                    'image_url': bottle.get('image_url', ''),
                    'similarity_score': similarity_scores[idx],
                    'reasoning': reasoning
                })
            
            return similar_bottles
        
        return []
    
    def find_complementary_bottles(self, user_df, user_profile, num_recommendations=5):
        """Find bottles that complement and diversify user's collection"""
        # Get IDs of bottles in user's collection
        user_bottle_ids = set(user_df['id'].astype(str).tolist())
        
        # Extract user's preferences
        user_spirits = set(user_df['spirit'].unique())
        user_regions = set(user_df['region'].unique())
        
        # Find underrepresented categories in user's collection
        all_spirits = set(self.whisky_data['spirit'].unique())
        all_regions = set(self.whisky_data['region'].unique())
        
        missing_spirits = all_spirits - user_spirits
        missing_regions = all_regions - user_regions
        
        # Prioritize bottles with characteristics not in user's collection
        complementary_score = []
        
        for idx, bottle in self.whisky_data.iterrows():
            score = 0
            bottle_id = str(bottle['id'])
            
            # Skip bottles already in user's collection
            if bottle_id in user_bottle_ids:
                continue
            
            # Boost score for spirits not in user's collection
            if bottle['spirit'] in missing_spirits:
                score += 3
            
            # Boost score for regions not in user's collection
            if bottle.get('region') in missing_regions:
                score += 2
            
            # Consider price range similar to user's collection
            avg_price = user_profile.get('avg_price', 0)
            if abs(bottle['price'] - avg_price) < (avg_price * 0.3):  # Within 30% of average price
                score += 1
            
            complementary_score.append((idx, score))
        
        # Sort by complementary score (descending)
        complementary_score.sort(key=lambda x: x[1], reverse=True)
        
        # Get top N complementary bottles
        complementary_bottles = []
        for idx, score in complementary_score[:num_recommendations]:
            bottle = self.whisky_data.iloc[idx]
            
            # Generate reasoning for why this bottle complements their collection
            reasoning = self.generate_complementary_reasoning(bottle, user_df, user_profile)
            
            complementary_bottles.append({
                'id': bottle['id'],
                'name': bottle['name'],
                'brand': bottle['brand'],
                'spirit': bottle['spirit'],
                'region': bottle.get('region', 'Unknown'),
                'age': bottle.get('age', 'NAS'),
                'price': bottle['price'],
                'proof': bottle['proof'],
                'image_url': bottle.get('image_url', ''),
                'complementary_score': score,
                'reasoning': reasoning
            })
        
        return complementary_bottles
    
    def generate_similarity_reasoning(self, rec_bottle, user_df):
        """Generate reasoning for why a bottle is similar to user's collection"""
        reasons = []
        
        # Check if brand matches any in user collection
        if rec_bottle['brand'] in user_df['brand'].values:
            reasons.append(f"You have other {rec_bottle['brand']} bottles in your collection")
        
        # Check if spirit type matches
        if rec_bottle['spirit'] in user_df['spirit'].values:
            reasons.append(f"Matches your preference for {rec_bottle['spirit']}")
        
        # Check if region matches
        if 'region' in rec_bottle and rec_bottle['region'] in user_df['region'].values:
            reasons.append(f"From {rec_bottle['region']}, a region you enjoy")
        
        # Check price point similarity
        avg_price = user_df['price'].mean()
        if abs(rec_bottle['price'] - avg_price) < (avg_price * 0.2):
            reasons.append(f"Similar price point to your collection (${rec_bottle['price']})")
        
        # If we couldn't find specific reasons, add a generic one
        if not reasons:
            reasons.append("Has similar characteristics to bottles in your collection")
        
        return reasons
    
    def generate_complementary_reasoning(self, rec_bottle, user_df, user_profile):
        """Generate reasoning for why a bottle complements user's collection"""
        reasons = []
        
        # Check if this is a new spirit type
        if rec_bottle['spirit'] not in user_df['spirit'].values:
            reasons.append(f"Adds a new spirit type ({rec_bottle['spirit']}) to your collection")
        
        # Check if this is a new region
        if 'region' in rec_bottle and rec_bottle['region'] not in user_df['region'].values:
            reasons.append(f"Expands your collection with a bottle from {rec_bottle['region']}")
        
        # Check if this is a new brand
        if rec_bottle['brand'] not in user_df['brand'].values:
            reasons.append(f"Introduces you to {rec_bottle['brand']}")
        
        # Check if this has a different age profile
        avg_age = user_profile.get('avg_age', 0)
        if 'age' in rec_bottle and rec_bottle['age'] > avg_age + 3:
            reasons.append(f"Offers an older expression ({rec_bottle['age']} years) than your average")
        
        # Check if this has a different proof profile
        avg_proof = user_profile.get('avg_proof', 0)
        if rec_bottle['proof'] > avg_proof + 10:
            reasons.append(f"Higher proof ({rec_bottle['proof']}) than your current collection")
        elif rec_bottle['proof'] < avg_proof - 10:
            reasons.append(f"Lower proof option ({rec_bottle['proof']}) to diversify your collection")
        
        # If we couldn't find specific reasons, add a generic one
        if not reasons:
            reasons.append("Brings diversity to your whisky collection")
        
        return reasons
    
    def calculate_bar_stats(self, user_df):
        """Calculate statistics about user's bar collection for visualization"""
        stats = {}
        
        # Count bottles by spirit type
        if 'spirit' in user_df.columns:
            stats['spirits_count'] = user_df['spirit'].value_counts().to_dict()
        
        # Count bottles by region
        if 'region' in user_df.columns:
            stats['regions_count'] = user_df['region'].value_counts().to_dict()
        
        # Count bottles by brand
        if 'brand' in user_df.columns:
            stats['brands_count'] = user_df['brand'].value_counts().to_dict()
        
        # Price distribution
        if 'price' in user_df.columns and not user_df['price'].empty:
            price_bins = [0, 50, 100, 200, 500, 1000, float('inf')]
            price_labels = ['<$50', '$50-100', '$100-200', '$200-500', '$500-1000', '$1000+']
            price_counts = pd.cut(user_df['price'], bins=price_bins, labels=price_labels).value_counts().to_dict()
            stats['price_distribution'] = price_counts
        
        # Age distribution
        if 'age' in user_df.columns and not user_df['age'].empty:
            age_bins = [0, 5, 10, 15, 20, 25, float('inf')]
            age_labels = ['NAS/≤5', '6-10', '11-15', '16-20', '21-25', '25+']
            age_counts = pd.cut(user_df['age'], bins=age_bins, labels=age_labels).value_counts().to_dict()
            stats['age_distribution'] = age_counts
        
        # Proof distribution
        if 'proof' in user_df.columns and not user_df['proof'].empty:
            proof_bins = [0, 80, 90, 100, 110, 120, float('inf')]
            proof_labels = ['≤80', '80-90', '90-100', '100-110', '110-120', '120+']
            proof_counts = pd.cut(user_df['proof'], bins=proof_bins, labels=proof_labels).value_counts().to_dict()
            stats['proof_distribution'] = proof_counts
        
        return stats
