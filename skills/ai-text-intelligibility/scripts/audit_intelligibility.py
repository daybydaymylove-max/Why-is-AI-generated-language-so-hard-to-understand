"""
心理语言学可理解性审查与重构工具 (Psycholinguistic Intelligibility Linter & Decoupler)
理论依据: arXiv:2610.29162v1 - "Why is AI-generated language so hard to understand?"
功能: 针对大模型后训练极限信息压缩导致的 6 大病态语言学特征进行规则化检测、量化评分与重构建议。
"""

import re
import sys
from typing import List, Dict, Any

class IntelligibilityAuditor:
    def __init__(self):
        # 扩展非名词停用词集合，提升三连名词堆叠检测的精准度
        self.stop_words = {
            "the", "a", "an", "in", "on", "at", "for", "with", "about", "to", "from",
            "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
            "it", "this", "that", "these", "those", "and", "or", "but", "so", "as",
            "my", "your", "his", "her", "their", "our", "not", "no", "if", "when",
            "which", "while", "where", "why", "how", "all", "each", "every", "other",
            "another", "such", "than", "more", "most", "very", "too", "quite",
            "unusually", "quietly", "currently", "honestly", "actually", "simply",
            "they", "them", "we", "us", "you", "he", "him", "she", "her", "i", "me",
            "just", "also", "then", "now", "well", "into", "over", "after", "before"
        }

        # 经典拟人行为动词集合（违背选择限制）
        self.animate_verbs = {
            "promise", "promises", "promised", "promising",
            "swallow", "swallows", "swallowed", "swallowing",
            "bite", "bites", "bit", "bitten", "biting",
            "forget", "forgets", "forgot", "forgotten", "forgetting",
            "hope", "hopes", "hoped", "hoping",
            "misunderstand", "misunderstands", "misunderstood", "misunderstanding",
            "ask", "asks", "asked", "asking",
            "expect", "expects", "expected", "expecting",
            "refuse", "refuses", "refused", "refusing",
            "crave", "craves", "craved", "craving",
            "eat", "eats", "ate", "eating", "eaten",
            "teach", "teaches", "taught", "teaching"
        }

        # 经典无生命主语指示词
        self.inanimate_subject_indicators = {
            "docstring", "function", "file", "method", "class", "code", "song",
            "chaos", "worksheet", "objection", "policy", "lattice", "pattern",
            "asymmetry", "process", "sentence", "logic", "rule", "module", "guitar"
        }

        # 临时/突兀名词转动词 (Ad-hoc Denominal Verbs)
        self.denominal_verbs = {
            "footnote", "footnotes", "footnoted", "footnoting",
            "calendar", "calendars", "calendared", "calendaring",
            "cushion", "cushions", "cushioned", "cushioning",
            "bottle", "bottles", "bottled", "bottling",
            "mirror", "mirrors", "mirrored", "mirroring"
        }

    def check_stacked_nouns(self, sentence: str) -> List[str]:
        """检测连续 3 个及以上名词修饰堆叠 (Stacked Nouns >= 3)"""
        issues = []
        words = re.findall(r'\b[A-Za-z0-9_-]+\b', sentence)
        candidate_stack = []
        for w in words:
            lw = w.lower()
            if lw not in self.stop_words and len(w) > 2 and not lw.endswith("ly"):
                candidate_stack.append(w)
            else:
                if len(candidate_stack) >= 3:
                    issues.append(" ".join(candidate_stack))
                candidate_stack = []
        if len(candidate_stack) >= 3:
            issues.append(" ".join(candidate_stack))
        return issues

    def check_inanimate_animate_mismatch(self, sentence: str) -> List[str]:
        """检测无生命主语配合生命动词 (违背选择限制，引发 P600 认知冲突)"""
        issues = []
        words = [w.strip('.,;:"()[]{}').lower() for w in sentence.split()]
        for i in range(len(words) - 1):
            w1 = words[i]
            w2 = words[i + 1]
            if w1 in self.inanimate_subject_indicators and w2 in self.animate_verbs:
                issues.append(f"'{w1} {w2}' (无生命主语配合生命行为动词)")
            if i + 2 < len(words):
                w3 = words[i + 2]
                if w1 in self.inanimate_subject_indicators and w3 in self.animate_verbs:
                    issues.append(f"'{w1} {w2} {w3}' (无生命主语配合生命行为动词)")
        return issues

    def check_denominal_verbs(self, sentence: str) -> List[str]:
        """检测名词临时活用为动词"""
        issues = []
        words = [w.strip('.,;:"()[]{}').lower() for w in sentence.split()]
        for w in words:
            if w in self.denominal_verbs:
                issues.append(f"'{w}' (名词活用为动词，增加句法重构成本)")
        return issues

    def check_reduced_relative_clause(self, sentence: str) -> List[str]:
        """检测省略 that/which 的缩略宾语关系从句"""
        issues = []
        pattern = r'\b(the|a|an)\s+([a-zA-Z_-]+)\s+(you|they|we|she|he|i)\s+([a-zA-Z_-]+)\b'
        matches = re.finditer(pattern, sentence, flags=re.IGNORECASE)
        for m in matches:
            phrase = m.group(0)
            noun = m.group(2).lower()
            verb = m.group(4).lower()
            if verb not in {"is", "are", "was", "were", "can", "could", "will", "would"}:
                issues.append(f"'{phrase}' -> 建议补全引导词以减轻即时解析负担: '{m.group(1)} {noun} that {m.group(3)} {verb}'")
        return issues

    def check_sentence_length_and_density(self, sentence: str) -> List[str]:
        """检测单句超长及长依存风险"""
        issues = []
        words = sentence.split()
        if len(words) > 30:
            issues.append(f"单句词数过多 ({len(words)} 词 > 30 词基准)，易击穿人类工作记忆 (DLT 约束)")
        return issues

    def audit_text(self, text: str) -> Dict[str, Any]:
        sentences = re.split(r'(?<=[.!?。！？])\s+', text.strip())
        results = []
        total_penalties = 0

        for idx, s in enumerate(sentences, 1):
            if not s.strip():
                continue
            s_clean = s.strip()
            stacked = self.check_stacked_nouns(s_clean)
            inanimate = self.check_inanimate_animate_mismatch(s_clean)
            denominal = self.check_denominal_verbs(s_clean)
            reduced_rel = self.check_reduced_relative_clause(s_clean)
            len_density = self.check_sentence_length_and_density(s_clean)

            sentence_issues = []
            if stacked:
                sentence_issues.append({"type": "Stacked Nouns (三连名词堆叠)", "items": stacked})
                total_penalties += len(stacked) * 2
            if inanimate:
                sentence_issues.append({"type": "Inanimate-Animate Mismatch (拟人化生命度冲突)", "items": inanimate})
                total_penalties += len(inanimate) * 3
            if denominal:
                sentence_issues.append({"type": "Denominal Verb (名词活化动词)", "items": denominal})
                total_penalties += len(denominal) * 2
            if reduced_rel:
                sentence_issues.append({"type": "Reduced Relative Clause (关系词切除/过度省略)", "items": reduced_rel})
                total_penalties += len(reduced_rel) * 2
            if len_density:
                sentence_issues.append({"type": "Long Dependency & Extreme Length (超长依存风险)", "items": len_density})
                total_penalties += 2

            results.append({
                "sentence_index": idx,
                "text": s_clean,
                "issues": sentence_issues
            })

        readability_score = max(0, 100 - total_penalties * 5)
        return {
            "total_sentences": len(sentences),
            "readability_score": readability_score,
            "sentence_diagnostics": results
        }

if __name__ == "__main__":
    auditor = IntelligibilityAuditor()
    sample_text = (
        "The docstring promises they are skipped when they appear anywhere in the source path. "
        "Your instinct is right; the convoluted sentence you are currently reading is quietly eating its own reader-patience budget footnote it. "
        "Fixed absolute dotfile backup path handling while preserving the marker. "
        "That is not trip to Vegas money, that is leave the job you hate money. "
        "Austin has unusually high inventory, which cushions price spikes better than supply-constrained markets."
    )
    result = auditor.audit_text(sample_text)
    print(f"=== 审查完成 ===")
    print(f"检测句子数: {result['total_sentences']}")
    print(f"人类可理解性综合评分: {result['readability_score']}/100")
    for diag in result["sentence_diagnostics"]:
        print(f"\n[句 {diag['sentence_index']}]: {diag['text']}")
        if not diag["issues"]:
            print("  [通过] 符合易读性规范")
        else:
            for issue in diag["issues"]:
                print(f"  [警报 - {issue['type']}]: {', '.join(issue['items'])}")
