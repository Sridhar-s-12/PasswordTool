"""
Password Strength Analyzer with Comprehensive Wordlist Integration
Created by Sridhar S
Version 2.0 - Enhanced with india_passwords_wordlist.txt support

CRITICAL SECURITY ENHANCEMENT:
- Now checks passwords against 1,000+ Indian breach database passwords
- Uses O(1) lookup performance with Python sets
- Case-insensitive matching for maximum coverage
- Maintains full backward compatibility with existing GUI

This module replaces the original analyzer.py with enhanced vulnerability detection
while keeping the same public API that gui.py expects.
"""

from __future__ import annotations

import math
import re
import os
from typing import Dict, Any, Optional, Set

# Optional zxcvbn import
try:
    from zxcvbn import zxcvbn
    ZXCVBN_AVAILABLE = True
except ImportError:
    ZXCVBN_AVAILABLE = False


class PasswordAnalyzer:
    """Enhanced Password Analyzer with comprehensive wordlist integration."""

    # Public constants (unchanged for GUI compatibility)
    STRENGTH_LEVELS = {
        0: "Very Weak",
        1: "Weak",
        2: "Fair",
        3: "Good",
        4: "Strong",
    }

    STRENGTH_COLORS = {
        0: "#FF4444",  # red
        1: "#FF8800",  # orange
        2: "#FFAA00",  # yellow-orange
        3: "#88AA00",  # yellow-green
        4: "#00AA44",  # green
    }

    def __init__(self) -> None:
        """Initialize analyzer with wordlist loading."""
        self.use_zxcvbn = ZXCVBN_AVAILABLE
        self.wordlist_passwords: Set[str] = set()
        self.wordlist_loaded = False
        
        # Load the comprehensive Indian password wordlist
        self._load_wordlist("india_passwords_wordlist.txt")

    def _load_wordlist(self, wordlist_path: str) -> None:
        """
        Load the password wordlist into memory for O(1) lookup performance.
        This dramatically improves vulnerability detection accuracy.
        """
        try:
            if os.path.exists(wordlist_path):
                with open(wordlist_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        password = line.strip()
                        # Skip empty lines and comments (lines starting with #)
                        if password and not password.startswith('#'):
                            # Store in lowercase for case-insensitive matching
                            self.wordlist_passwords.add(password.lower())
                
                self.wordlist_loaded = True
                print(f"🔒 Security Enhanced: Loaded {len(self.wordlist_passwords)} passwords from breach database")
            else:
                print(f"⚠️  Wordlist file '{wordlist_path}' not found. Place it in project root for enhanced security.")
                self.wordlist_loaded = False
                
        except Exception as e:
            print(f"⚠️  Error loading wordlist: {e}. Using basic patterns only.")
            self.wordlist_loaded = False

    def analyze_password(self, password: str) -> Dict[str, Any]:
        """
        Main password analysis function with enhanced vulnerability detection.
        
        Analysis Priority (in order):
        1. Check if password is blank
        2. Check against comprehensive Indian wordlist (1,000+ passwords)
        3. Check basic vulnerability patterns 
        4. Perform standard zxcvbn or entropy analysis
        
        Returns: Dictionary compatible with existing GUI
        """
        if not password:
            return self._blank_result()

        # CRITICAL SECURITY CHECK: Comprehensive wordlist lookup
        if self.wordlist_loaded:
            wordlist_result = self._check_wordlist_vulnerability(password)
            if wordlist_result:
                return wordlist_result

        # FALLBACK: Basic pattern checking (if wordlist unavailable)
        pattern_result = self._check_basic_vulnerabilities(password)
        if pattern_result:
            return pattern_result

        # STANDARD ANALYSIS: zxcvbn or entropy calculation
        if self.use_zxcvbn:
            return self._analyze_with_zxcvbn(password)
        return self._analyze_with_entropy(password)

    def _check_wordlist_vulnerability(self, password: str) -> Optional[Dict[str, Any]]:
        """
        Check password against comprehensive Indian breach database.
        Returns vulnerability result if found, None if safe.
        """
        password_lower = password.lower()
        
        if password_lower in self.wordlist_passwords:
            # Provide specific feedback based on password pattern
            if any(pattern in password_lower for pattern in ['@123', '#123', '$123', '!123', '*123']):
                feedback = "CRITICAL: This password uses the '@123' pattern found in multiple Indian data breaches"
            elif password_lower in ['password', 'admin', 'welcome', 'login', 'user', 'guest']:
                feedback = "CRITICAL: This is among the top 10 most common passwords globally"
            elif any(city in password_lower for city in ['mumbai', 'delhi', 'bangalore', 'chennai', 'kolkata', 'hyderabad']):
                feedback = "CRITICAL: City names are prime targets in Indian-focused password attacks"
            elif any(cultural in password_lower for cultural in ['india', 'bollywood', 'cricket', 'diwali', 'holi']):
                feedback = "CRITICAL: Cultural references are heavily targeted in localized attacks"
            elif any(company in password_lower for company in ['tcs', 'infosys', 'wipro', 'reliance', 'airtel']):
                feedback = "CRITICAL: Company names are easily guessed in corporate environments"
            else:
                feedback = "CRITICAL: This password appears in known breach databases"
            
            return {
                "score": 0,
                "strength": self.STRENGTH_LEVELS[0],
                "color": self.STRENGTH_COLORS[0],
                "feedback": feedback,
                "entropy": 0,
                "crack_time": "Seconds to Minutes",
                "method": "wordlist_breach",
            }
        
        return None

    def _check_basic_vulnerabilities(self, password: str) -> Optional[Dict[str, Any]]:
        """
        Fallback vulnerability checking when wordlist is unavailable.
        Checks for the most dangerous patterns manually.
        """
        pwd_lower = password.lower()

        # Most dangerous exact matches
        critical_passwords = {
            'password@123', 'admin@123', 'welcome@123', 'india@123',
            'password123', 'admin123', 'welcome123', 'qwerty123',
            '123456', '123456789', '1234567890', 'password', 'admin'
        }
        
        if pwd_lower in critical_passwords:
            return {
                "score": 0,
                "strength": self.STRENGTH_LEVELS[0],
                "color": self.STRENGTH_COLORS[0],
                "feedback": "CRITICAL: This is a top-10 most common password globally",
                "entropy": 0,
                "crack_time": "Instant",
                "method": "pattern_exact",
            }

        # Pattern-based vulnerability detection
        vulnerability_patterns = [
            (r'^[a-z]+@123!*$', "CRITICAL: Word + @123 pattern is extremely common in breaches"),
            (r'^[a-z]+123!*$', "VERY WEAK: Word + 123 pattern is easily guessed"),
            (r'^(password|admin|welcome|login)', "CRITICAL: Dictionary word base is trivial to crack"),
            (r'^(qwerty|asdf|zxcv)', "VERY WEAK: Keyboard sequence detected"),
            (r'^[0-9]{6,10}$', "VERY WEAK: Numeric-only passwords are easily cracked"),
        ]
        
        for pattern, message in vulnerability_patterns:
            if re.match(pattern, pwd_lower):
                return {
                    "score": 0,
                    "strength": self.STRENGTH_LEVELS[0],
                    "color": self.STRENGTH_COLORS[0],
                    "feedback": message,
                    "entropy": 0,
                    "crack_time": "Minutes to Hours",
                    "method": "pattern_match",
                }
        
        return None

    def _analyze_with_zxcvbn(self, password: str) -> Dict[str, Any]:
        """Standard zxcvbn analysis for non-vulnerable passwords."""
        try:
            result = zxcvbn(password)
            score = result["score"]

            # Build comprehensive feedback
            feedback_parts = []
            warning = result["feedback"]["warning"]
            if warning:
                feedback_parts.append(warning)
            feedback_parts.extend(result["feedback"]["suggestions"])
            feedback = ". ".join(feedback_parts) if feedback_parts else "Strong password!"

            crack_time = self._format_crack_time(
                result["crack_times_seconds"]["offline_slow_hashing_1e4_per_second"]
            )

            return {
                "score": score,
                "strength": self.STRENGTH_LEVELS[score],
                "color": self.STRENGTH_COLORS[score],
                "feedback": feedback,
                "entropy": result["entropy"],
                "crack_time": crack_time,
                "method": "zxcvbn",
            }
        except Exception:
            # Graceful fallback to entropy if zxcvbn fails
            return self._analyze_with_entropy(password)

    def _analyze_with_entropy(self, password: str) -> Dict[str, Any]:
        """Entropy-based analysis fallback."""
        entropy = self._calculate_entropy(password)
        score = self._entropy_to_score(entropy)
        feedback = self._generate_entropy_feedback(password, entropy)
        crack_time = self._estimate_crack_time(entropy)

        return {
            "score": score,
            "strength": self.STRENGTH_LEVELS[score],
            "color": self.STRENGTH_COLORS[score],
            "feedback": feedback,
            "entropy": entropy,
            "crack_time": crack_time,
            "method": "entropy",
        }

    @staticmethod
    def _blank_result() -> Dict[str, Any]:
        """Result for blank passwords."""
        return {
            "score": 0,
            "strength": PasswordAnalyzer.STRENGTH_LEVELS[0],
            "color": PasswordAnalyzer.STRENGTH_COLORS[0],
            "feedback": "Password cannot be blank",
            "entropy": 0,
            "crack_time": "N/A",
            "method": "none",
        }

    @staticmethod
    def _calculate_entropy(password: str) -> float:
        """Shannon-style entropy calculation."""
        if not password:
            return 0.0

        pool = 0
        if re.search(r"[a-z]", password):
            pool += 26
        if re.search(r"[A-Z]", password):
            pool += 26
        if re.search(r"[0-9]", password):
            pool += 10
        if re.search(r"[^a-zA-Z0-9]", password):
            pool += 32  # special characters

        if pool == 0:
            return 0.0
        return len(password) * math.log2(pool)

    @staticmethod
    def _entropy_to_score(entropy: float) -> int:
        """Map entropy bits to strength score (0-4)."""
        if entropy < 28:
            return 0
        if entropy < 36:
            return 1
        if entropy < 60:
            return 2
        if entropy < 120:
            return 3
        return 4

    @staticmethod
    def _generate_entropy_feedback(password: str, entropy: float) -> str:
        """Generate helpful feedback based on entropy analysis."""
        suggestions = []

        # Length recommendations
        if len(password) < 8:
            suggestions.append("Use at least 8 characters")
        elif len(password) < 12:
            suggestions.append("Consider using 12+ characters for better security")

        # Character variety recommendations  
        if not re.search(r"[a-z]", password):
            suggestions.append("Add lowercase letters")
        if not re.search(r"[A-Z]", password):
            suggestions.append("Add uppercase letters")
        if not re.search(r"[0-9]", password):
            suggestions.append("Add numbers")
        if not re.search(r"[^a-zA-Z0-9]", password):
            suggestions.append("Add special characters")

        # Pattern warnings
        if re.search(r"(.)\1\1", password):
            suggestions.append("Avoid repeating characters")
        if re.search(r"(012|123|234|345|456|567|678|789|890)", password):
            suggestions.append("Avoid sequential numbers")
        if re.search(
            r"(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz)",
            password.lower(),
        ):
            suggestions.append("Avoid sequential letters")

        return "Strong password!" if not suggestions else ". ".join(suggestions)

    @staticmethod
    def _format_crack_time(seconds: float) -> str:
        """Format crack time in human-readable format."""
        if seconds < 1:
            return "Instant"
        if seconds < 60:
            return f"{int(seconds)} seconds"
        if seconds < 3600:
            return f"{int(seconds / 60)} minutes"
        if seconds < 86400:
            return f"{int(seconds / 3600)} hours"
        if seconds < 31_536_000:
            return f"{int(seconds / 86_400)} days"
        if seconds < 3_153_600_000:
            return f"{int(seconds / 31_536_000)} years"
        return "Centuries"

    def _estimate_crack_time(self, entropy: float) -> str:
        """Estimate crack time from entropy (conservative)."""
        guesses_per_second = 10_000  # Conservative offline attack estimate
        total_combinations = 2 ** entropy
        avg_seconds = total_combinations / (2 * guesses_per_second)  # Average case
        return self._format_crack_time(avg_seconds)

    def get_security_stats(self) -> Dict[str, Any]:
        """Get security enhancement statistics."""
        return {
            "wordlist_loaded": self.wordlist_loaded,
            "wordlist_size": len(self.wordlist_passwords),
            "zxcvbn_available": self.use_zxcvbn,
            "security_level": "Enhanced" if self.wordlist_loaded else "Basic"
        }


# --------------------------------------------------------------------------- #
# Self-test functionality for verification
# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    print("🔒 Enhanced Password Strength Analyzer Test")
    print("=" * 55)
    
    analyzer = PasswordAnalyzer()
    
    # Display security stats
    stats = analyzer.get_security_stats()
    print(f"Security Level: {stats['security_level']}")
    print(f"Wordlist: {'✅ Loaded' if stats['wordlist_loaded'] else '❌ Not Available'}")
    if stats['wordlist_loaded']:
        print(f"Database Size: {stats['wordlist_size']:,} passwords")
    print(f"ZXCVBN: {'✅ Available' if stats['zxcvbn_available'] else '❌ Fallback Mode'}")
    print()
    
    # Test critical passwords that should be caught
    critical_tests = [
        "Password@123",      # Should be Very Weak (wordlist)
        "admin@123",         # Should be Very Weak (wordlist)  
        "123456",            # Should be Very Weak (wordlist)
        "welcome@123",       # Should be Very Weak (wordlist)
        "india@123",         # Should be Very Weak (wordlist)
    ]
    
    # Test strong passwords that should pass
    strong_tests = [
        "MyStr0ng!P@ssw0rd2024",   # Should be Strong
        "C0mpl3x$Secur1ty!Key",    # Should be Strong
        "UniqueP@ssphrase#2024",   # Should be Good/Strong
    ]
    
    print("🧪 Testing Critical Vulnerabilities (should all be Very Weak):")
    print("-" * 55)
    for password in critical_tests:
        result = analyzer.analyze_password(password)
        status = "✅ CAUGHT" if result['score'] == 0 else "❌ MISSED"
        print(f"{password:20} | {result['strength']:>10} | {status}")
    
    print(f"\n🧪 Testing Strong Passwords (should be Good/Strong):")
    print("-" * 55)
    for password in strong_tests:
        result = analyzer.analyze_password(password)
        status = "✅ GOOD" if result['score'] >= 3 else "⚠️  WEAK"
        print(f"{password:25} | {result['strength']:>10} | {status}")
    
    print(f"\n🎯 Test Summary:")
    print("Place this file as pass_tool/analyzer.py to enable enhanced security.")
    print("Ensure india_passwords_wordlist.txt is in your project root directory.")