"""
Wordlist generator module

Creates attack-oriented wordlists based on user-supplied personal clues
with various transformations including leetspeak, case variations,
and year/number appendages.
"""

import itertools
import re
from typing import List, Set, Dict, Any
from datetime import datetime


class WordlistGenerator:
    """
    Generates custom wordlists from personal information with various transformations.
    """

    # Common leetspeak substitutions
    LEET_SUBSTITUTIONS = {
        'a': ['@', '4'],
        'e': ['3'],
        'i': ['1', '!'],
        'o': ['0'],
        's': ['$', '5'],
        't': ['7'],
        'l': ['1'],
        'g': ['9'],
        'b': ['6'],
        'z': ['2']
    }

    # Common prefixes and suffixes
    COMMON_PREFIXES = ['', 'my', 'the', 'super', 'best', 'cool', 'new']
    COMMON_SUFFIXES = ['', '!', '!!', '123', '1', '01', 'x', 'er', 'est']

    def __init__(self):
        """Initialize the wordlist generator."""
        self.base_words = set()
        self.final_wordlist = set()

    def clear_wordlist(self):
        """Clear the current wordlist."""
        self.base_words.clear()
        self.final_wordlist.clear()

    def add_personal_info(self, personal_data: Dict[str, str]):
        """
        Add personal information to generate base words.

        Args:
            personal_data: Dictionary containing personal information
        """
        # Extract and clean personal data
        for key, value in personal_data.items():
            if value and value.strip():
                clean_value = self._clean_input(value.strip())
                if clean_value:
                    self.base_words.add(clean_value)

                    # Add variations of names (first name only, last name only)
                    if key in ['name', 'full_name'] and ' ' in clean_value:
                        parts = clean_value.split()
                        for part in parts:
                            if len(part) > 2:  # Only add meaningful parts
                                self.base_words.add(part)

    def add_custom_words(self, words: List[str]):
        """
        Add custom words to the base wordlist.

        Args:
            words: List of custom words to add
        """
        for word in words:
            clean_word = self._clean_input(word)
            if clean_word:
                self.base_words.add(clean_word)

    def generate_years(self, birth_year: int = None) -> List[str]:
        """
        Generate relevant years for password variations.

        Args:
            birth_year: Birth year if provided

        Returns:
            List of year strings
        """
        current_year = datetime.now().year
        years = []

        # Current year and nearby years
        for year in range(current_year - 5, current_year + 2):
            years.append(str(year))
            years.append(str(year)[2:])  # Two-digit year

        # Birth year and related years
        if birth_year:
            years.append(str(birth_year))
            years.append(str(birth_year)[2:])

            # Graduation years (assuming 18, 22 for college)
            for grad_offset in [18, 22]:
                grad_year = birth_year + grad_offset
                years.append(str(grad_year))
                years.append(str(grad_year)[2:])

        # Common significant years
        common_years = ['2020', '2021', '2022', '2023', '2024', '2025',
                       '20', '21', '22', '23', '24', '25']
        years.extend(common_years)

        return list(set(years))  # Remove duplicates

    def generate_wordlist(self, personal_data: Dict[str, str] = None, 
                         custom_words: List[str] = None,
                         include_leetspeak: bool = True,
                         include_case_variations: bool = True,
                         include_years: bool = True,
                         include_prefixes_suffixes: bool = True,
                         max_words: int = 50000) -> List[str]:
        """
        Generate the complete wordlist with all transformations.

        Args:
            personal_data: Dictionary of personal information
            custom_words: List of additional custom words
            include_leetspeak: Whether to include leetspeak variations
            include_case_variations: Whether to include case variations
            include_years: Whether to include year appendages
            include_prefixes_suffixes: Whether to include prefixes/suffixes
            max_words: Maximum number of words to generate

        Returns:
            List of generated password candidates
        """
        # Clear and rebuild wordlist
        self.clear_wordlist()

        # Add personal information
        if personal_data:
            self.add_personal_info(personal_data)

        # Add custom words
        if custom_words:
            self.add_custom_words(custom_words)

        # If no base words, add some common defaults
        if not self.base_words:
            self.base_words.update(['password', 'admin', 'user', 'login', 'welcome'])

        # Generate transformations
        transformed_words = set()

        for base_word in self.base_words:
            # Add original word
            transformed_words.add(base_word)

            # Case variations
            if include_case_variations:
                transformed_words.update(self._generate_case_variations(base_word))

            # Leetspeak variations
            if include_leetspeak:
                leet_variations = self._generate_leetspeak(base_word)
                transformed_words.update(leet_variations)

                # Case variations of leetspeak
                if include_case_variations:
                    for leet_word in leet_variations:
                        transformed_words.update(self._generate_case_variations(leet_word))

        # Add prefixes and suffixes
        if include_prefixes_suffixes:
            prefixed_words = set()
            for word in list(transformed_words):
                prefixed_words.update(self._add_prefixes_suffixes(word))
            transformed_words.update(prefixed_words)

        # Add years and numbers
        if include_years:
            birth_year = None
            if personal_data and personal_data.get('birth_date'):
                birth_year = self._extract_birth_year(personal_data['birth_date'])

            years = self.generate_years(birth_year)
            year_variations = set()

            for word in list(transformed_words):
                for year in years:
                    year_variations.add(word + year)
                    year_variations.add(year + word)

            transformed_words.update(year_variations)

        # Convert to list and limit size
        final_list = list(transformed_words)
        final_list.sort()  # Sort for consistency

        # Limit to max_words to prevent excessive memory usage
        if len(final_list) > max_words:
            final_list = final_list[:max_words]

        self.final_wordlist = set(final_list)
        return final_list

    def _clean_input(self, text: str) -> str:
        """
        Clean and normalize input text.

        Args:
            text: Input text to clean

        Returns:
            Cleaned text
        """
        # Remove extra whitespace and convert to lowercase
        cleaned = re.sub(r'\s+', '', text.strip().lower())

        # Remove non-alphanumeric characters for base words
        cleaned = re.sub(r'[^a-zA-Z0-9]', '', cleaned)

        # Only return words that are at least 3 characters
        return cleaned if len(cleaned) >= 3 else ''

    def _generate_case_variations(self, word: str) -> List[str]:
        """
        Generate different case variations of a word.

        Args:
            word: Input word

        Returns:
            List of case variations
        """
        variations = []

        # All lowercase (original)
        variations.append(word.lower())

        # All uppercase
        variations.append(word.upper())

        # Title case (first letter uppercase)
        variations.append(word.capitalize())

        # AlTeRnAtInG case (if word is long enough)
        if len(word) > 4:
            alternating = ''
            for i, char in enumerate(word.lower()):
                if i % 2 == 0:
                    alternating += char.upper()
                else:
                    alternating += char
            variations.append(alternating)

        return variations

    def _generate_leetspeak(self, word: str) -> List[str]:
        """
        Generate leetspeak variations of a word.

        Args:
            word: Input word

        Returns:
            List of leetspeak variations
        """
        variations = []
        word_lower = word.lower()

        # Find positions that can be substituted
        substitutable_positions = []
        for i, char in enumerate(word_lower):
            if char in self.LEET_SUBSTITUTIONS:
                substitutable_positions.append((i, char))

        if not substitutable_positions:
            return [word]  # No substitutions possible

        # Generate combinations (limit to prevent explosion)
        max_substitutions = min(3, len(substitutable_positions))

        for num_subs in range(1, max_substitutions + 1):
            # Try different combinations of substitutions
            for positions in itertools.combinations(substitutable_positions, num_subs):
                for substitutions in itertools.product(*[
                    self.LEET_SUBSTITUTIONS[char] for _, char in positions
                ]):
                    leet_word = list(word_lower)
                    for (pos, _), sub in zip(positions, substitutions):
                        leet_word[pos] = sub
                    variations.append(''.join(leet_word))

        # Remove duplicates and limit results
        return list(set(variations))[:10]  # Limit to prevent too many variations

    def _add_prefixes_suffixes(self, word: str) -> List[str]:
        """
        Add common prefixes and suffixes to a word.

        Args:
            word: Input word

        Returns:
            List of words with prefixes/suffixes
        """
        variations = []

        # Add prefixes
        for prefix in self.COMMON_PREFIXES:
            if prefix:  # Skip empty prefix
                variations.append(prefix + word)

        # Add suffixes
        for suffix in self.COMMON_SUFFIXES:
            if suffix:  # Skip empty suffix
                variations.append(word + suffix)

        # Add prefix + suffix combinations (limited)
        for prefix in self.COMMON_PREFIXES[:3]:  # Limit prefixes
            for suffix in self.COMMON_SUFFIXES[:3]:  # Limit suffixes
                if prefix or suffix:  # At least one should be non-empty
                    variations.append(prefix + word + suffix)

        return variations

    def _extract_birth_year(self, date_str: str) -> int:
        """
        Extract birth year from date string.

        Args:
            date_str: Date string in various formats

        Returns:
            Birth year as integer, or None if not found
        """
        # Look for 4-digit years
        year_match = re.search(r'\b(19|20)\d{2}\b', date_str)
        if year_match:
            return int(year_match.group())

        # Look for 2-digit years and assume 1900s/2000s
        two_digit_match = re.search(r'\b\d{2}\b', date_str)
        if two_digit_match:
            year = int(two_digit_match.group())
            # Assume years 00-30 are 2000s, 31-99 are 1900s
            if year <= 30:
                return 2000 + year
            else:
                return 1900 + year

        return None

    def save_wordlist(self, filename: str, wordlist: List[str] = None) -> bool:
        """
        Save wordlist to a file.

        Args:
            filename: Output filename
            wordlist: Wordlist to save (uses internal if None)

        Returns:
            True if successful, False otherwise
        """
        try:
            words_to_save = wordlist if wordlist is not None else list(self.final_wordlist)

            with open(filename, 'w', encoding='utf-8') as f:
                for word in sorted(words_to_save):
                    f.write(word + '\n')

            return True
        except Exception as e:
            print(f"Error saving wordlist: {e}")
            return False

    def get_wordlist_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the generated wordlist.

        Returns:
            Dictionary with wordlist statistics
        """
        if not self.final_wordlist:
            return {'total_words': 0, 'base_words': 0}

        stats = {
            'total_words': len(self.final_wordlist),
            'base_words': len(self.base_words),
            'average_length': sum(len(word) for word in self.final_wordlist) / len(self.final_wordlist),
            'min_length': min(len(word) for word in self.final_wordlist),
            'max_length': max(len(word) for word in self.final_wordlist)
        }

        return stats


def test_wordlist_generator():
    """Test the wordlist generator functionality."""
    generator = WordlistGenerator()

    # Test personal data
    personal_data = {
        'name': 'John Smith',
        'birth_date': '1990-05-15',
        'pet_name': 'fluffy',
        'favorite_team': 'Lakers',
        'company': 'TechCorp'
    }

    # Generate wordlist
    wordlist = generator.generate_wordlist(
        personal_data=personal_data,
        custom_words=['password', 'admin'],
        max_words=100  # Limit for testing
    )

    print(f"Generated {len(wordlist)} words from personal data:")
    print("Sample words:")
    for word in sorted(wordlist)[:20]:  # Show first 20
        print(f"  {word}")

    if len(wordlist) > 20:
        print(f"  ... and {len(wordlist) - 20} more")

    # Show statistics
    stats = generator.get_wordlist_stats()
    print(f"\nStatistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    test_wordlist_generator()
