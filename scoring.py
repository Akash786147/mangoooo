"""
Scoring system for the game based on time and diamonds collected.
"""


class ScoreCalculator:
    """Calculate and manage game scores."""
    
    def __init__(self):
        """Initialize the score calculator."""
        self.grade_thresholds = {
            'A': {'max_time': 30, 'min_diamonds_percent': 90},
            'B': {'max_time': 60, 'min_diamonds_percent': 70},
            'C': {'max_time': 90, 'min_diamonds_percent': 50},
            'D': {'max_time': 999, 'min_diamonds_percent': 0}
        }
    
    def calculate_grade(self, time_seconds, diamonds_collected, total_diamonds):
        """
        Calculate grade based on time and diamonds collected.
        
        Args:
            time_seconds: float - Time taken to complete level in seconds
            diamonds_collected: int - Number of diamonds collected
            total_diamonds: int - Total diamonds available
            
        Returns:
            str - Grade letter (A, B, C, or D)
        """
        if total_diamonds == 0:
            diamonds_percent = 100
        else:
            diamonds_percent = (diamonds_collected / total_diamonds) * 100
        
        # Check for A grade
        if (time_seconds <= self.grade_thresholds['A']['max_time'] and 
            diamonds_percent >= self.grade_thresholds['A']['min_diamonds_percent']):
            return 'A'
        
        # Check for B grade
        elif (time_seconds <= self.grade_thresholds['B']['max_time'] and 
              diamonds_percent >= self.grade_thresholds['B']['min_diamonds_percent']):
            return 'B'
        
        # Check for C grade
        elif (time_seconds <= self.grade_thresholds['C']['max_time'] and 
              diamonds_percent >= self.grade_thresholds['C']['min_diamonds_percent']):
            return 'C'
        
        # Otherwise D grade
        else:
            return 'D'
    
    def calculate_score(self, time_seconds, points_collected, total_points):
        """
        Calculate numerical score based on time and points.
        
        Args:
            time_seconds: float - Time taken to complete level
            points_collected: int - Points from diamonds collected
            total_points: int - Total possible points
            
        Returns:
            int - Numerical score
        """
        # Base score from points collected
        if total_points == 0:
            points_score = 1000
        else:
            points_score = int((points_collected / total_points) * 1000)
        
        # Time bonus (faster = more bonus)
        time_bonus = max(0, 500 - int(time_seconds * 5))
        
        total_score = points_score + time_bonus
        return max(0, total_score)
    
    def get_grade_description(self, grade):
        """
        Get description text for a grade.
        
        Args:
            grade: str - Grade letter
            
        Returns:
            str - Description of the grade
        """
        descriptions = {
            'A': 'Outstanding! You are a master!',
            'B': 'Great job! Well done!',
            'C': 'Good effort! Keep practicing!',
            'D': 'You completed it! Try for better time and more diamonds!'
        }
        return descriptions.get(grade, 'Completed!')
    
    def format_time(self, time_seconds):
        """
        Format time in seconds to MM:SS format.
        
        Args:
            time_seconds: float - Time in seconds
            
        Returns:
            str - Formatted time string
        """
        minutes = int(time_seconds // 60)
        seconds = int(time_seconds % 60)
        return f"{minutes:02d}:{seconds:02d}"
