"""
Prompt Analysis Techniques for Large Language Model Optimization

This guide explores advanced techniques for analyzing and improving prompts
to enhance Large Language Model (LLM) performance across various tasks.
"""

import re
import json
import numpy as np
from typing import List, Dict, Any
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


class PromptAnalyzer:
    def __init__(self):
        """
        Initialize the PromptAnalyzer with essential NLP tools and configurations.
        """
        # Ensure you have nltk downloaded:
        # import nltk
        # nltk.download('punkt')
        # nltk.download('stopwords')

        self.stop_words = set(stopwords.words("english"))

    def complexity_analysis(self, prompt: str) -> Dict[str, Any]:
        """
        Perform a comprehensive complexity analysis of the prompt.

        Args:
            prompt (str): Input prompt to analyze

        Returns:
            Dict containing various complexity metrics
        """
        return {
            "total_characters": len(prompt),
            "total_words": len(word_tokenize(prompt)),
            "unique_words": len(set(word_tokenize(prompt.lower()))),
            "avg_word_length": np.mean([len(word) for word in word_tokenize(prompt)]),
            "stopword_ratio": self._calculate_stopword_ratio(prompt),
        }

    def _calculate_stopword_ratio(self, prompt: str) -> float:
        """
        Calculate the ratio of stopwords in the prompt.

        Args:
            prompt (str): Input prompt

        Returns:
            Float representing stopword ratio
        """
        words = word_tokenize(prompt.lower())
        stopword_count = sum(1 for word in words if word in self.stop_words)
        return stopword_count / len(words) if words else 0

    def intent_extraction(self, prompt: str) -> Dict[str, Any]:
        """
        Extract potential intent and key semantic components from the prompt.

        Args:
            prompt (str): Input prompt

        Returns:
            Dict with intent-related insights
        """
        # Core intent identification techniques
        keywords = self._extract_keywords(prompt)

        return {"primary_keywords": keywords[:3], "action_verbs": self._identify_action_verbs(prompt), "intent_type": self._classify_intent(prompt)}

    def _extract_keywords(self, prompt: str, top_n: int = 5) -> List[str]:
        """
        Extract top keywords using TF-IDF vectorization.

        Args:
            prompt (str): Input prompt
            top_n (int): Number of top keywords to return

        Returns:
            List of top keywords
        """
        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform([prompt])
        feature_names = vectorizer.get_feature_names_out()

        # Get TF-IDF scores and sort
        tfidf_scores = dict(zip(feature_names, tfidf_matrix.toarray()[0]))
        return sorted(tfidf_scores, key=tfidf_scores.get, reverse=True)[:top_n]

    def _identify_action_verbs(self, prompt: str) -> List[str]:
        """
        Identify primary action verbs in the prompt.

        Args:
            prompt (str): Input prompt

        Returns:
            List of identified action verbs
        """
        # Common action verb patterns
        action_verb_patterns = [
            r"\b(create|generate|write|develop|design|analyze|explain|compare)\b",
            r"\b(solve|implement|produce|summarize|evaluate|describe)\b",
        ]

        actions = []
        for pattern in action_verb_patterns:
            actions.extend(re.findall(pattern, prompt.lower()))

        return list(set(actions))

    def _classify_intent(self, prompt: str) -> str:
        """
        Rudimentary intent classification based on prompt characteristics.

        Args:
            prompt (str): Input prompt

        Returns:
            Classified intent type
        """
        intent_classifiers = [
            (r"\b(how to|explain|describe)\b", "Explanation"),
            (r"\b(create|generate|write|develop)\b", "Generation"),
            (r"\b(solve|calculate|compute|analyze)\b", "Problem-Solving"),
            (r"\b(compare|contrast|differentiate)\b", "Comparative Analysis"),
        ]

        for pattern, intent in intent_classifiers:
            if re.search(pattern, prompt.lower()):
                return intent

        return "General Inquiry"

    def semantic_structure_analysis(self, prompt: str) -> Dict[str, Any]:
        """
        Analyze the semantic structure and potential LLM interaction patterns.

        Args:
            prompt (str): Input prompt

        Returns:
            Dict with semantic structure insights
        """
        return {
            "question_type": self._detect_question_type(prompt),
            "context_complexity": self._assess_context_complexity(prompt),
            "potential_ambiguity": self._detect_potential_ambiguities(prompt),
        }

    def _detect_question_type(self, prompt: str) -> str:
        """
        Detect the type of question or prompt structure.

        Args:
            prompt (str): Input prompt

        Returns:
            Detected question type
        """
        question_patterns = [
            (r"^(how|what|why|when|where|which)", "Wh-Question"),
            (r"\?$", "Direct Question"),
            (r"(please|kindly)\s", "Polite Request"),
            (r"^(explain|describe|detail)", "Explanatory Prompt"),
        ]

        for pattern, q_type in question_patterns:
            if re.search(pattern, prompt.lower()):
                return q_type

        return "Declarative Statement"

    def _assess_context_complexity(self, prompt: str) -> str:
        """
        Assess the potential contextual complexity of the prompt.

        Args:
            prompt (str): Input prompt

        Returns:
            Complexity rating
        """
        # Heuristics for context complexity
        context_indicators = [
            (len(word_tokenize(prompt)) > 30, "High"),
            (len(word_tokenize(prompt)) > 15, "Medium"),
            (len(word_tokenize(prompt)) <= 15, "Low"),
        ]

        for condition, rating in context_indicators:
            if condition:
                return rating

        return "Minimal"

    def _detect_potential_ambiguities(self, prompt: str) -> List[str]:
        """
        Detect potential sources of ambiguity in the prompt.

        Args:
            prompt (str): Input prompt

        Returns:
            List of potential ambiguity indicators
        """
        ambiguity_patterns = [
            (r"\b(might|maybe|perhaps|could)\b", "Uncertain Language"),
            (r"\b(\w+)\s+\1\b", "Repetitive Phrasing"),
            (r"\b(etc\.|and so on|and so forth)\b", "Incomplete Specification"),
        ]

        ambiguities = []
        for pattern, description in ambiguity_patterns:
            if re.search(pattern, prompt.lower()):
                ambiguities.append(description)

        return ambiguities

    def generate_improvement_recommendations(self, prompt: str) -> Dict[str, List[str]]:
        """
        Generate recommendations for prompt improvement.

        Args:
            prompt (str): Input prompt

        Returns:
            Dict of improvement recommendations
        """
        analysis = {"clarity_suggestions": [], "specificity_recommendations": [], "structure_improvements": []}

        # Clarity suggestions
        if len(word_tokenize(prompt)) < 10:
            analysis["clarity_suggestions"].append("Consider providing more context to clarify your intent.")

        # Specificity recommendations
        if self._calculate_stopword_ratio(prompt) > 0.4:
            analysis["specificity_recommendations"].append("Reduce generic stopwords to make the prompt more precise.")

        # Structure improvements
        if not any(char in prompt for char in ["?", ".", "!"]):
            analysis["structure_improvements"].append("Add punctuation to clearly delineate the prompt's structure.")

        return analysis


# Demonstration of usage
def main():
    example_prompts = [
        "Write a Python script to analyze customer feedback",
        "How might we improve machine learning model performance?",
        "Create a concise summary of recent advancements in AI",
        "Can you please produce an incredibly detailed explanation with sample python examples of prompt analysis techniques to help better define prompts for llm execution, include links to associated opensource research",
    ]

    analyzer = PromptAnalyzer()

    for prompt in example_prompts:
        print(f"\nAnalyzing Prompt: {prompt}")
        print("\nComplexity Analysis:")
        print(json.dumps(analyzer.complexity_analysis(prompt), indent=2))

        print("\nIntent Extraction:")
        print(json.dumps(analyzer.intent_extraction(prompt), indent=2))

        print("\nSemantic Structure:")
        print(json.dumps(analyzer.semantic_structure_analysis(prompt), indent=2))

        print("\nImprovement Recommendations:")
        print(json.dumps(analyzer.generate_improvement_recommendations(prompt), indent=2))


if __name__ == "__main__":
    main()

"""
Recommended Research and References:

1. Prompt Engineering Techniques:
   - "Large Language Models: A Survey" - arXiv:2303.18223
   - "Prompt Engineering: A Guide to Crafting Effective Prompts" - OpenAI Research

2. Semantic Analysis Techniques:
   - "Semantic Analysis in NLP" - ACL Anthology
   - "Context-Aware Prompt Optimization" - NeurIPS Proceedings

3. Open-Source Research Links:
   - https://github.com/dair-ai/Prompt-Engineering-Guide
   - https://github.com/promptslab/Promptify
   - https://github.com/microsoft/LMOps

Note: This is a comprehensive framework and should be adapted to specific 
use cases and model-specific requirements.
"""
