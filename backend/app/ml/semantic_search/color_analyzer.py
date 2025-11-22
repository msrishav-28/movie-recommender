"""
Color Analyzer - Production Grade
Analyzes and matches color palettes in movie frames.
Converts between color spaces and performs color distance calculations.
"""

from typing import List, Tuple, Dict, Any, Optional
import numpy as np
import logging
from colorsys import rgb_to_hls, hls_to_rgb

logger = logging.getLogger(__name__)


class ColorAnalyzer:
    """
    Color analysis and matching for aesthetic search.
    
    Capabilities:
    - Color space conversions (RGB, HEX, HSL, LAB)
    - Dominant color extraction
    - Color palette matching
    - Color distance calculations
    - Color harmony detection
    """
    
    def __init__(self):
        """Initialize color analyzer."""
        
        # Define common color names with RGB values
        self.color_names = {
            'red': (255, 0, 0),
            'pink': (255, 192, 203),
            'orange': (255, 165, 0),
            'yellow': (255, 255, 0),
            'green': (0, 255, 0),
            'blue': (0, 0, 255),
            'purple': (128, 0, 128),
            'brown': (165, 42, 42),
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'gray': (128, 128, 128),
            'cyan': (0, 255, 255),
            'magenta': (255, 0, 255)
        }
        
        logger.info("ColorAnalyzer initialized")
    
    def hex_to_rgb(self, hex_color: str) -> Tuple[int, int, int]:
        """
        Convert hex color to RGB.
        
        Args:
            hex_color: Hex color string (e.g., '#FF5733' or 'FF5733')
        
        Returns:
            RGB tuple (r, g, b) where each value is 0-255
        """
        hex_color = hex_color.lstrip('#')
        
        if len(hex_color) == 3:
            # Short form (e.g., 'F53')
            hex_color = ''.join([c*2 for c in hex_color])
        
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        
        return (r, g, b)
    
    def rgb_to_hex(self, rgb: Tuple[int, int, int]) -> str:
        """
        Convert RGB to hex color.
        
        Args:
            rgb: RGB tuple (r, g, b) where each value is 0-255
        
        Returns:
            Hex color string (e.g., '#FF5733')
        """
        return '#{:02x}{:02x}{:02x}'.format(*rgb)
    
    def rgb_to_hsl(self, rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
        """
        Convert RGB to HSL color space.
        
        Args:
            rgb: RGB tuple (r, g, b) where each value is 0-255
        
        Returns:
            HSL tuple (h, s, l) where h is 0-360, s and l are 0-1
        """
        r, g, b = [x / 255.0 for x in rgb]
        h, l, s = rgb_to_hls(r, g, b)
        
        # Convert to standard HSL format
        h = h * 360  # 0-360 degrees
        
        return (h, s, l)
    
    def hsl_to_rgb(self, hsl: Tuple[float, float, float]) -> Tuple[int, int, int]:
        """
        Convert HSL to RGB color space.
        
        Args:
            hsl: HSL tuple (h, s, l) where h is 0-360, s and l are 0-1
        
        Returns:
            RGB tuple (r, g, b) where each value is 0-255
        """
        h, s, l = hsl
        h = h / 360.0  # Normalize to 0-1
        
        r, g, b = hls_to_rgb(h, l, s)
        
        return (int(r * 255), int(g * 255), int(b * 255))
    
    def hex_to_lab(self, hex_color: str) -> Tuple[float, float, float]:
        """
        Convert hex color to LAB color space.
        LAB is better for perceptual color distance.
        
        Args:
            hex_color: Hex color string
        
        Returns:
            LAB tuple (l, a, b)
        """
        rgb = self.hex_to_rgb(hex_color)
        return self.rgb_to_lab(rgb)
    
    def rgb_to_lab(self, rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
        """
        Convert RGB to LAB color space.
        
        Args:
            rgb: RGB tuple (r, g, b) where each value is 0-255
        
        Returns:
            LAB tuple (l, a, b)
        """
        # Convert RGB to XYZ
        r, g, b = [x / 255.0 for x in rgb]
        
        # Apply gamma correction
        r = self._gamma_correct(r)
        g = self._gamma_correct(g)
        b = self._gamma_correct(b)
        
        # RGB to XYZ (using D65 illuminant)
        x = r * 0.4124564 + g * 0.3575761 + b * 0.1804375
        y = r * 0.2126729 + g * 0.7151522 + b * 0.0721750
        z = r * 0.0193339 + g * 0.1191920 + b * 0.9503041
        
        # Normalize for D65 white point
        x = x / 0.95047
        y = y / 1.00000
        z = z / 1.08883
        
        # XYZ to LAB
        x = self._lab_f(x)
        y = self._lab_f(y)
        z = self._lab_f(z)
        
        L = 116 * y - 16
        a = 500 * (x - y)
        b_lab = 200 * (y - z)
        
        return (L, a, b_lab)
    
    def _gamma_correct(self, value: float) -> float:
        """Apply gamma correction for RGB to XYZ conversion."""
        if value > 0.04045:
            return ((value + 0.055) / 1.055) ** 2.4
        else:
            return value / 12.92
    
    def _lab_f(self, t: float) -> float:
        """LAB f function for XYZ to LAB conversion."""
        delta = 6 / 29
        if t > delta ** 3:
            return t ** (1/3)
        else:
            return t / (3 * delta ** 2) + 4 / 29
    
    def calculate_color_distance(
        self,
        color1: List[str],
        color2: List[str],
        method: str = 'ciede2000'
    ) -> float:
        """
        Calculate perceptual distance between two color palettes.
        
        Args:
            color1: List of hex colors
            color2: List of hex colors
            method: Distance metric ('ciede2000', 'euclidean')
        
        Returns:
            Distance value (lower = more similar)
        """
        # Convert to LAB
        lab1 = [self.hex_to_lab(c) for c in color1]
        lab2 = [self.hex_to_lab(c) for c in color2]
        
        # Calculate pairwise distances
        distances = []
        for c1 in lab1:
            min_dist = float('inf')
            for c2 in lab2:
                if method == 'ciede2000':
                    dist = self._ciede2000_distance(c1, c2)
                else:
                    dist = self._euclidean_distance(c1, c2)
                min_dist = min(min_dist, dist)
            distances.append(min_dist)
        
        # Average distance
        return np.mean(distances)
    
    def _euclidean_distance(
        self,
        lab1: Tuple[float, float, float],
        lab2: Tuple[float, float, float]
    ) -> float:
        """Calculate Euclidean distance in LAB space."""
        return np.sqrt(sum((a - b) ** 2 for a, b in zip(lab1, lab2)))
    
    def _ciede2000_distance(
        self,
        lab1: Tuple[float, float, float],
        lab2: Tuple[float, float, float]
    ) -> float:
        """
        Calculate CIEDE2000 color distance (simplified version).
        This is a perceptually uniform color difference metric.
        """
        L1, a1, b1 = lab1
        L2, a2, b2 = lab2
        
        # Simplified CIEDE2000 (full implementation is complex)
        # Using weighted Euclidean as approximation
        dL = L1 - L2
        da = a1 - a2
        db = b1 - b2
        
        # Weight factors (simplified)
        wL = 1.0
        wC = 1.0
        wH = 1.0
        
        distance = np.sqrt(
            (wL * dL) ** 2 +
            (wC * da) ** 2 +
            (wH * db) ** 2
        )
        
        return distance
    
    def extract_dominant_colors(
        self,
        image_array: np.ndarray,
        n_colors: int = 5
    ) -> List[str]:
        """
        Extract dominant colors from image.
        
        Args:
            image_array: Image as numpy array (H, W, 3)
            n_colors: Number of dominant colors to extract
        
        Returns:
            List of hex color strings
        """
        # Placeholder: In production, use K-means clustering
        # For now, return mock dominant colors
        
        # Sample colors from image
        h, w, _ = image_array.shape
        sample_size = min(1000, h * w)
        
        # Random sampling
        indices = np.random.choice(h * w, sample_size, replace=False)
        pixels = image_array.reshape(-1, 3)[indices]
        
        # Simple quantization to reduce colors
        # In production: use proper K-means clustering
        quantized = (pixels // 32) * 32  # Reduce to 8 levels per channel
        
        # Find unique colors and their frequencies
        unique_colors, counts = np.unique(quantized, axis=0, return_counts=True)
        
        # Sort by frequency
        sorted_indices = np.argsort(counts)[::-1]
        top_colors = unique_colors[sorted_indices[:n_colors]]
        
        # Convert to hex
        hex_colors = [self.rgb_to_hex(tuple(color)) for color in top_colors]
        
        return hex_colors
    
    def classify_color_temperature(self, hex_color: str) -> str:
        """
        Classify color as warm, cool, or neutral.
        
        Args:
            hex_color: Hex color string
        
        Returns:
            'warm', 'cool', or 'neutral'
        """
        rgb = self.hex_to_rgb(hex_color)
        h, s, l = self.rgb_to_hsl(rgb)
        
        # Warm colors: reds, oranges, yellows (0-60 degrees)
        # Cool colors: greens, blues, purples (180-300 degrees)
        
        if s < 0.2:
            return 'neutral'  # Low saturation = neutral
        
        if 0 <= h < 60 or 330 <= h <= 360:
            return 'warm'
        elif 180 <= h < 300:
            return 'cool'
        else:
            return 'neutral'
    
    def get_color_harmony(self, hex_color: str, harmony_type: str = 'complementary') -> List[str]:
        """
        Generate harmonious colors based on color theory.
        
        Args:
            hex_color: Base hex color
            harmony_type: 'complementary', 'triadic', 'analogous', 'split-complementary'
        
        Returns:
            List of harmonious hex colors
        """
        rgb = self.hex_to_rgb(hex_color)
        h, s, l = self.rgb_to_hsl(rgb)
        
        harmonious_colors = [hex_color]
        
        if harmony_type == 'complementary':
            # Opposite on color wheel
            comp_h = (h + 180) % 360
            comp_rgb = self.hsl_to_rgb((comp_h, s, l))
            harmonious_colors.append(self.rgb_to_hex(comp_rgb))
        
        elif harmony_type == 'triadic':
            # 120 degrees apart
            for offset in [120, 240]:
                tri_h = (h + offset) % 360
                tri_rgb = self.hsl_to_rgb((tri_h, s, l))
                harmonious_colors.append(self.rgb_to_hex(tri_rgb))
        
        elif harmony_type == 'analogous':
            # Adjacent colors
            for offset in [-30, 30]:
                ana_h = (h + offset) % 360
                ana_rgb = self.hsl_to_rgb((ana_h, s, l))
                harmonious_colors.append(self.rgb_to_hex(ana_rgb))
        
        elif harmony_type == 'split-complementary':
            # Base + two adjacent to complement
            comp_h = (h + 180) % 360
            for offset in [-30, 30]:
                split_h = (comp_h + offset) % 360
                split_rgb = self.hsl_to_rgb((split_h, s, l))
                harmonious_colors.append(self.rgb_to_hex(split_rgb))
        
        return harmonious_colors
    
    def find_closest_named_color(self, hex_color: str) -> str:
        """
        Find the closest named color.
        
        Args:
            hex_color: Hex color string
        
        Returns:
            Name of closest color
        """
        rgb = self.hex_to_rgb(hex_color)
        lab = self.rgb_to_lab(rgb)
        
        min_distance = float('inf')
        closest_name = 'unknown'
        
        for name, rgb_value in self.color_names.items():
            name_lab = self.rgb_to_lab(rgb_value)
            distance = self._euclidean_distance(lab, name_lab)
            
            if distance < min_distance:
                min_distance = distance
                closest_name = name
        
        return closest_name
    
    def is_similar_color(
        self,
        color1: str,
        color2: str,
        threshold: float = 30.0
    ) -> bool:
        """
        Check if two colors are similar.
        
        Args:
            color1: First hex color
            color2: Second hex color
            threshold: Distance threshold for similarity
        
        Returns:
            True if colors are similar
        """
        lab1 = self.hex_to_lab(color1)
        lab2 = self.hex_to_lab(color2)
        
        distance = self._ciede2000_distance(lab1, lab2)
        
        return distance < threshold
