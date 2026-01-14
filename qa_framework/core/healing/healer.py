from bs4 import BeautifulSoup
from typing import Optional, List, Dict, Any
import re
from qa_framework.core.logger import get_logger

logger = get_logger("self_healing")

class Healer:
    """
    Intelligent Self-Healing mechanism.
    Analyzes page source to find alternative selectors when the primary one fails.
    """

    def __init__(self, page_source: str):
        self.soup = BeautifulSoup(page_source, 'html.parser')

    def heal(self, failed_selector: str) -> Optional[str]:
        """
        Attempts to find a better selector for the failed one.
        Returns the new selector string if found, else None.
        """
        logger.info(f"Attempting to heal selector: {failed_selector}")
        
        # 1. Parse metadata from the failed selector
        meta = self._parse_selector(failed_selector)
        if not meta:
            logger.warning("Could not parse selector metadata. Skipping healing.")
            return None

        # 2. Find Candidates in the current DOM
        candidates = self._find_candidates(meta)
        
        # 3. Score Candidates
        best_match = None
        highest_score = 0.0

        for candidate in candidates:
            score = self._score_match(meta, candidate)
            if score > highest_score:
                highest_score = score
                best_match = candidate

        # 4. Threshold Check (e.g., 80% confidence)
        if highest_score > 0.8:
            new_selector = self._generate_selector(best_match)
            logger.info(f"Healed! New Selector: {new_selector} (Score: {highest_score:.2f})")
            return new_selector
            
        logger.warning(f"Healing failed. Best match score {highest_score:.2f} was too low.")
        return None

    def _parse_selector(self, selector: str) -> Dict[str, str]:
        """
        Extracts key attributes (id, name, class, text) from a selector.
        Very basic heuristic parser.
        """
        meta = {}
        
        # ID selector (#foo or [id='foo'])
        if '#' in selector:
            meta['id'] = selector.split('#')[-1].split(' ')[0]
        elif 'id=' in selector:
            match = re.search(r"id=['\"](.*?)['\"]", selector)
            if match: meta['id'] = match.group(1)

        # Name selector
        if 'name=' in selector:
            match = re.search(r"name=['\"](.*?)['\"]", selector)
            if match: meta['name'] = match.group(1)
            
        # Text selector (xpath)
        if 'text()' in selector:
            match = re.search(r"text\(\)\s*=\s*['\"](.*?)['\"]", selector)
            if match: meta['text'] = match.group(1)
            
        return meta

    def _find_candidates(self, meta: Dict[str, str]) -> List[Any]:
        """
        Finds elements that match *at least one* attribute partially.
        """
        candidates = []
        
        # Search by ID (fuzzy)
        if 'id' in meta:
            # Find all elements with an id
            elements = self.soup.find_all(attrs={"id": True})
            candidates.extend(elements)
            
        # Search by Name
        if 'name' in meta:
            elements = self.soup.find_all(attrs={"name": True})
            candidates.extend(elements)
            
        # Search by Text
        if 'text' in meta:
            # Find all elements with text
            elements = self.soup.find_all(string=True)
            # Get their parents
            candidates.extend([e.parent for e in elements if e.parent.name != 'script'])

        return list(set(candidates)) # Dedupe

    def _score_match(self, meta: Dict[str, str], element) -> float:
        """
        Scores an element based on how many attributes match the metadata.
        Uses simplistic scoring for demonstration.
        """
        score = 0.0
        total_weight = 0.0
        
        # Check ID
        if 'id' in meta:
            total_weight += 1.0
            el_id = element.get('id', '')
            if el_id == meta['id']:
                score += 1.0
            elif meta['id'] in el_id or el_id in meta['id']:
                score += 0.7 # Partial match
        
        # Check Name
        if 'name' in meta:
            total_weight += 1.0
            el_name = element.get('name', '')
            if el_name == meta['name']:
                score += 1.0
        
        # Check Text
        if 'text' in meta:
            total_weight += 1.0
            el_text = element.get_text(strip=True)
            if meta['text'] == el_text:
                score += 1.0
            elif meta['text'] in el_text:
                score += 0.8
        
        if total_weight == 0: return 0.0
        return score / total_weight

    def _generate_selector(self, element) -> str:
        """
        Generates a robust selector for the found element.
        """
        # Prefer ID
        if element.get('id'):
            return f"#{element.get('id')}"
        
        # Prefer Name
        if element.get('name'):
            return f"[name='{element.get('name')}']"
        
        # Fallback to loose CSS path (simplified)
        return f"{element.name}"
