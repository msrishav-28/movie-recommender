"""
Aesthetic Query Parser - Production Grade
Parses natural language queries for visual aesthetics into structured filters.
Extracts colors, weather, time-of-day, emotions, etc.
"""

from typing import Dict, List, Any, Optional
import re
import logging

logger = logging.getLogger(__name__)


class AestheticQueryParser:
    """
    Parse aesthetic queries into structured filters.
    
    Examples:
    - "rain with pink skies" -> {weather: ['rain'], colors: ['pink'], scene_type: 'outdoor'}
    - "neon lights at night" -> {time_of_day: 'night', visual_elements: ['neon_lights']}
    - "warm autumn colors" -> {colors: ['warm'], season: 'autumn'}
    """
    
    def __init__(self):
        """Initialize query parser with pattern dictionaries."""
        
        # Color patterns
        self.color_patterns = {
            'pink': ['pink', 'rose', 'magenta'],
            'blue': ['blue', 'azure', 'cyan', 'navy'],
            'red': ['red', 'crimson', 'scarlet'],
            'green': ['green', 'emerald', 'lime'],
            'yellow': ['yellow', 'gold', 'golden'],
            'orange': ['orange', 'amber'],
            'purple': ['purple', 'violet', 'lavender'],
            'black': ['black', 'dark'],
            'white': ['white', 'pale'],
            'brown': ['brown', 'sepia'],
            'gray': ['gray', 'grey', 'silver'],
            'warm': ['warm', 'cozy', 'hot'],
            'cool': ['cool', 'cold', 'icy'],
            'vibrant': ['vibrant', 'bright', 'vivid'],
            'muted': ['muted', 'desaturated', 'faded'],
            'pastel': ['pastel', 'soft'],
            'neon': ['neon', 'fluorescent']
        }
        
        # Weather patterns
        self.weather_patterns = {
            'rain': ['rain', 'rainy', 'raining', 'pouring', 'drizzle'],
            'snow': ['snow', 'snowy', 'snowing', 'blizzard'],
            'fog': ['fog', 'foggy', 'mist', 'misty', 'haze'],
            'sunny': ['sunny', 'sunshine', 'bright sun'],
            'cloudy': ['cloudy', 'overcast'],
            'storm': ['storm', 'stormy', 'thunder', 'lightning']
        }
        
        # Time of day patterns
        self.time_patterns = {
            'night': ['night', 'nighttime', 'midnight', 'evening'],
            'day': ['day', 'daytime', 'noon', 'afternoon'],
            'dawn': ['dawn', 'sunrise', 'morning'],
            'dusk': ['dusk', 'sunset', 'twilight', 'golden hour']
        }
        
        # Season patterns
        self.season_patterns = {
            'spring': ['spring', 'bloom', 'blossom'],
            'summer': ['summer'],
            'autumn': ['autumn', 'fall', 'leaves falling'],
            'winter': ['winter', 'snow']
        }
        
        # Location/setting patterns
        self.location_patterns = {
            'urban': ['city', 'urban', 'street', 'downtown', 'cityscape'],
            'rural': ['rural', 'countryside', 'farm', 'field'],
            'indoor': ['indoor', 'inside', 'interior', 'room'],
            'outdoor': ['outdoor', 'outside', 'exterior'],
            'beach': ['beach', 'ocean', 'seaside', 'shore'],
            'forest': ['forest', 'woods', 'trees'],
            'mountain': ['mountain', 'peak', 'summit'],
            'desert': ['desert', 'sand', 'dunes']
        }
        
        # Visual element patterns
        self.visual_element_patterns = {
            'neon_lights': ['neon', 'neon lights', 'neon sign'],
            'reflections': ['reflection', 'reflected', 'mirror'],
            'silhouette': ['silhouette', 'shadow', 'shadows'],
            'symmetry': ['symmetrical', 'symmetric', 'centered'],
            'wide_shot': ['wide shot', 'landscape', 'panoramic', 'vast'],
            'close_up': ['close up', 'closeup', 'tight shot'],
            'bokeh': ['bokeh', 'blur', 'blurred background'],
            'lens_flare': ['lens flare', 'flare', 'sun flare']
        }
        
        # Mood/emotion patterns
        self.mood_patterns = {
            'melancholic': ['melancholic', 'melancholy', 'sad', 'lonely', 'isolated'],
            'happy': ['happy', 'joyful', 'cheerful', 'upbeat'],
            'tense': ['tense', 'tension', 'suspenseful', 'intense'],
            'calm': ['calm', 'peaceful', 'serene', 'tranquil'],
            'romantic': ['romantic', 'love', 'intimate'],
            'mysterious': ['mysterious', 'enigmatic', 'cryptic'],
            'dreamy': ['dreamy', 'ethereal', 'surreal', 'fantasy'],
            'gritty': ['gritty', 'harsh', 'raw', 'rough']
        }
        
        logger.info("AestheticQueryParser initialized")
    
    def parse_query(self, query: str) -> Dict[str, Any]:
        """
        Parse natural language query into structured filters.
        
        Args:
            query: Natural language query (e.g., "rain with pink skies at night")
        
        Returns:
            Dictionary of extracted filters
        """
        query_lower = query.lower()
        filters = {}
        
        # Extract colors
        colors = self._extract_patterns(query_lower, self.color_patterns)
        if colors:
            filters['colors'] = colors
        
        # Extract weather
        weather = self._extract_patterns(query_lower, self.weather_patterns)
        if weather:
            filters['weather'] = weather
        
        # Extract time of day
        time_of_day = self._extract_patterns(query_lower, self.time_patterns)
        if time_of_day:
            filters['time_of_day'] = time_of_day
        
        # Extract seasons
        seasons = self._extract_patterns(query_lower, self.season_patterns)
        if seasons:
            filters['seasons'] = seasons
        
        # Extract locations
        locations = self._extract_patterns(query_lower, self.location_patterns)
        if locations:
            filters['locations'] = locations
        
        # Extract visual elements
        visual_elements = self._extract_patterns(query_lower, self.visual_element_patterns)
        if visual_elements:
            filters['visual_elements'] = visual_elements
        
        # Extract moods
        moods = self._extract_patterns(query_lower, self.mood_patterns)
        if moods:
            filters['moods'] = moods
        
        logger.info(f"Parsed query: '{query}' -> {filters}")
        return filters
    
    def _extract_patterns(
        self,
        query: str,
        pattern_dict: Dict[str, List[str]]
    ) -> List[str]:
        """
        Extract patterns from query text.
        
        Args:
            query: Query text
            pattern_dict: Dictionary of pattern categories and keywords
        
        Returns:
            List of matched pattern categories
        """
        matched = []
        
        for category, keywords in pattern_dict.items():
            for keyword in keywords:
                # Use word boundaries for better matching
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, query, re.IGNORECASE):
                    if category not in matched:
                        matched.append(category)
                    break
        
        return matched
    
    def expand_query(self, query: str) -> List[str]:
        """
        Expand query with synonyms and related terms.
        
        Args:
            query: Original query
        
        Returns:
            List of expanded queries
        """
        expanded = [query]
        
        # Parse query to get structured filters
        filters = self.parse_query(query)
        
        # Generate variations
        if 'colors' in filters:
            for color in filters['colors']:
                # Add specific color names
                if color == 'warm':
                    expanded.append(query.replace('warm', 'orange and red'))
                elif color == 'cool':
                    expanded.append(query.replace('cool', 'blue and cyan'))
        
        if 'time_of_day' in filters:
            for time in filters['time_of_day']:
                if time == 'dusk':
                    expanded.append(query + ' with golden hour lighting')
                elif time == 'night':
                    expanded.append(query + ' with dark atmosphere')
        
        return expanded[:5]  # Limit to 5 variations
    
    def enhance_with_metadata(
        self,
        filters: Dict[str, Any],
        metadata_suggestions: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Enhance parsed filters with additional metadata.
        
        Args:
            filters: Parsed filters
            metadata_suggestions: Additional metadata to merge
        
        Returns:
            Enhanced filters
        """
        enhanced = filters.copy()
        
        # Infer additional attributes
        if 'weather' in filters:
            if 'rain' in filters['weather']:
                # Rain implies outdoor, possibly urban
                if 'locations' not in enhanced:
                    enhanced['locations'] = []
                if 'outdoor' not in enhanced['locations']:
                    enhanced['locations'].append('outdoor')
        
        if 'time_of_day' in filters:
            if 'night' in filters['time_of_day']:
                # Night scenes often have certain colors
                if 'colors' not in enhanced:
                    enhanced['colors'] = []
                if 'dark' not in enhanced['colors']:
                    enhanced['colors'].append('dark')
        
        # Merge with metadata suggestions
        if metadata_suggestions:
            for key, value in metadata_suggestions.items():
                if key in enhanced:
                    # Merge lists
                    if isinstance(enhanced[key], list) and isinstance(value, list):
                        enhanced[key] = list(set(enhanced[key] + value))
                else:
                    enhanced[key] = value
        
        return enhanced
    
    def to_pinecone_filter(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert parsed filters to Pinecone metadata filter format.
        
        Args:
            filters: Parsed filters
        
        Returns:
            Pinecone-compatible filter dictionary
        """
        pinecone_filter = {}
        
        # Colors
        if 'colors' in filters and filters['colors']:
            pinecone_filter['dominant_colors'] = {
                '$in': filters['colors']
            }
        
        # Weather
        if 'weather' in filters and filters['weather']:
            pinecone_filter['weather_conditions'] = {
                '$in': filters['weather']
            }
        
        # Time of day
        if 'time_of_day' in filters and filters['time_of_day']:
            pinecone_filter['time_of_day'] = {
                '$in': filters['time_of_day']
            }
        
        # Visual elements
        if 'visual_elements' in filters and filters['visual_elements']:
            pinecone_filter['visual_tags'] = {
                '$in': filters['visual_elements']
            }
        
        # Moods
        if 'moods' in filters and filters['moods']:
            pinecone_filter['mood_tags'] = {
                '$in': filters['moods']
            }
        
        return pinecone_filter
    
    def suggest_similar_queries(self, query: str) -> List[str]:
        """
        Suggest similar queries based on parsed elements.
        
        Args:
            query: Original query
        
        Returns:
            List of similar query suggestions
        """
        filters = self.parse_query(query)
        suggestions = []
        
        # Generate variations
        if 'colors' in filters and 'weather' in filters:
            colors = filters['colors']
            weather = filters['weather']
            for color in colors:
                for w in weather:
                    suggestions.append(f"{w} with {color} atmosphere")
        
        if 'time_of_day' in filters and 'locations' in filters:
            times = filters['time_of_day']
            locations = filters['locations']
            for time in times:
                for loc in locations:
                    suggestions.append(f"{loc} scenes at {time}")
        
        return suggestions[:5]
