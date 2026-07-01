import logging
from typing import List, Dict, Any
from scipy.stats import kendalltau

logger = logging.getLogger(__name__)

class RankingComparator:
    def __init__(self):
        pass

    def _overlap_at_k(self, list1: List[str], list2: List[str], k: int) -> float:
        l1_k = list1[:k]
        l2_k = list2[:k]
        if not l1_k or not l2_k:
            return 0.0
        return len(set(l1_k) & set(l2_k)) / len(l2_k)

    def _kendall_tau(self, list1: List[str], list2: List[str]) -> float:
        """Compute Kendall's tau between two lists of URLs.
        Only considers items present in both lists.
        """
        common = list(set(list1) & set(list2))
        if len(common) < 2:
            return 0.0
            
        rank1 = [list1.index(url) for url in common]
        rank2 = [list2.index(url) for url in common]
        
        tau, p_value = kendalltau(rank1, rank2)
        # NaN handling if lists are identical and small
        if tau != tau:
            return 1.0 if rank1 == rank2 else 0.0
        return tau

    def compare(self, fc_urls: List[str], ideal_urls: List[str], kb_urls: List[str]) -> Dict[str, Any]:
        """
        Compare the three rankings and compute metrics.
        """
        logger.info("Comparing FC vs KB vs Ideal rankings...")
        
        fc_tau = self._kendall_tau(fc_urls, ideal_urls)
        kb_tau = self._kendall_tau(kb_urls, ideal_urls)
        
        common_kb = [u for u in kb_urls if u in ideal_urls]
        
        return {
            "fc_vs_ideal": {
                "kendall_tau": fc_tau,
                "overlap_at_3": self._overlap_at_k(fc_urls, ideal_urls, 3),
                "overlap_at_5": self._overlap_at_k(fc_urls, ideal_urls, 5),
            },
            "kb_vs_ideal": {
                "kendall_tau": kb_tau,
                "overlap_at_3": self._overlap_at_k(kb_urls, ideal_urls, 3),
                "overlap_at_5": self._overlap_at_k(kb_urls, ideal_urls, 5),
            },
            "kb_outperforms_fc": kb_tau > fc_tau,
            "kb_coverage": len(common_kb) / max(1, len(ideal_urls)),
        }
