"""Extract query patterns from comprehensive questions dataset"""
import json
import os
import re
from typing import Dict, List, Any
from collections import defaultdict

class PatternExtractor:
    """Extract and structure query patterns from question dataset"""
    
    def __init__(self, questions_file: str = None):
        if questions_file is None:
            questions_file = os.path.join(
                os.path.dirname(__file__),
                "comprehensive_questions.json"
            )
        self.questions_file = questions_file
        self.patterns = {}
    
    def load_questions(self) -> List[Dict]:
        """Load questions from JSON file"""
        with open(self.questions_file, 'r') as f:
            data = json.load(f)
        return data.get('questions', [])
    
    def extract_parameters(self, question: str, sql: str) -> Dict[str, Any]:
        """Extract parameters from question and SQL"""
        params = {}
        question_lower = question.lower()
        
        # Extract N from "top N", "bottom N", etc.
        top_match = re.search(r'top\s+(\d+)', question_lower)
        bottom_match = re.search(r'bottom\s+(\d+)', question_lower)
        if top_match:
            params['n'] = int(top_match.group(1))
            params['order'] = 'DESC'
        elif bottom_match:
            params['n'] = int(bottom_match.group(1))
            params['order'] = 'ASC'
        
        # Extract field being ranked
        if 'salary' in question_lower:
            params['field'] = 'Salary'
        elif 'performance' in question_lower or 'rating' in question_lower:
            params['field'] = 'PerformanceRating'
        elif 'engagement' in question_lower or 'satisfaction' in question_lower:
            params['field'] = 'OverallSatisfaction'
        elif 'headcount' in question_lower:
            params['field'] = 'headcount'
        
        # Extract filters
        if 'active' in question_lower or 'current' in question_lower:
            params['status_filter'] = 'Active'
        
        # Extract date ranges
        if 'last year' in question_lower:
            params['date_range'] = "CURRENT_DATE - INTERVAL '1 year'"
        elif 'last 6 months' in question_lower:
            params['date_range'] = "CURRENT_DATE - INTERVAL '6 months'"
        elif 'this year' in question_lower:
            params['date_range'] = "EXTRACT(YEAR FROM CURRENT_DATE)"
        
        return params
    
    def create_sql_template(self, sql: str, params: Dict) -> str:
        """Convert SQL to template by replacing parameters"""
        template = sql
        
        # Replace LIMIT N with {limit}
        template = re.sub(r'LIMIT\s+\d+', 'LIMIT {limit}', template, flags=re.IGNORECASE)
        
        # Replace specific numbers that are parameters
        if 'n' in params:
            template = re.sub(rf'\b{params["n"]}\b', '{n}', template)
        
        # Replace ORDER BY ... DESC/ASC with {order}
        if 'order' in params:
            template = re.sub(r'ORDER BY\s+[^"]+"[^"]+"\s+(DESC|ASC)', 
                            r'ORDER BY {order_field} {order}', template, flags=re.IGNORECASE)
        
        return template
    
    def extract_keywords(self, question: str) -> List[str]:
        """Extract keywords from question"""
        question_lower = question.lower()
        keywords = []
        
        # Common keywords
        keyword_patterns = [
            r'\btop\s+\d+', r'\bbottom\s+\d+', r'\bhighest\b', r'\blowest\b',
            r'\bmaximum\b', r'\bminimum\b', r'\baverage\b', r'\btotal\b',
            r'\bcount\b', r'\bdistribution\b', r'\btrends?\b', r'\bover time\b',
            r'\bby month\b', r'\bmonthly\b', r'\bdepartment\b', r'\bgender\b',
            r'\bsalary\b', r'\bperformance\b', r'\bengagement\b', r'\bskills?\b',
            r'\btraining\b', r'\bheadcount\b', r'\battrition\b', r'\bhiring\b',
            r'\btermination\b', r'\bactive\b', r'\bcurrent\b'
        ]
        
        for pattern in keyword_patterns:
            if re.search(pattern, question_lower):
                keyword = re.search(pattern, question_lower).group(0)
                keywords.append(keyword.strip())
        
        return list(set(keywords))
    
    def extract_patterns(self) -> Dict[str, Any]:
        """Extract all patterns from questions"""
        questions = self.load_questions()
        pattern_groups = defaultdict(list)
        
        # Group by pattern type
        for q in questions:
            pattern_type = q.get('pattern_type', 'unknown')
            pattern_groups[pattern_type].append(q)
        
        # Create pattern definitions
        patterns = {}
        for pattern_type, questions_list in pattern_groups.items():
            if not questions_list:
                continue
            
            # Use first question as template
            template_q = questions_list[0]
            
            # Extract common elements
            keywords = set()
            tables = set()
            visualizations = set()
            sql_templates = []
            
            for q in questions_list:
                keywords.update(self.extract_keywords(q['question']))
                tables.update(q.get('tables', []))
                visualizations.add(q.get('visualization', 'none'))
                
                # Extract parameters
                params = self.extract_parameters(q['question'], q['sql'])
                sql_template = self.create_sql_template(q['sql'], params)
                sql_templates.append({
                    'sql': sql_template,
                    'example_sql': q['sql'],
                    'parameters': params
                })
            
            # Find most common SQL template (by SQL string)
            if sql_templates:
                template_counts = {}
                for t in sql_templates:
                    sql_key = t['sql']
                    if sql_key not in template_counts:
                        template_counts[sql_key] = {'count': 0, 'template': t}
                    template_counts[sql_key]['count'] += 1
                most_common_template = max(template_counts.values(), key=lambda x: x['count'])['template']
            else:
                most_common_template = {'sql': '', 'example_sql': '', 'parameters': {}}
            
            patterns[pattern_type] = {
                'pattern_type': pattern_type,
                'keywords': list(keywords),
                'tables': list(tables),
                'visualization': list(visualizations)[0] if visualizations else 'bar',
                'sql_template': most_common_template['sql'],
                'example_questions': [q['question'] for q in questions_list[:5]],
                'example_sql': most_common_template['example_sql'],
                'parameter_extraction': self._extract_parameter_rules(questions_list),
                'count': len(questions_list)
            }
        
        return patterns
    
    def _extract_parameter_rules(self, questions: List[Dict]) -> Dict[str, str]:
        """Extract rules for parameter extraction"""
        rules = {}
        
        # Check for N parameter
        has_n = any(re.search(r'top\s+\d+|bottom\s+\d+', q['question'].lower()) for q in questions)
        if has_n:
            rules['n'] = "Extract number from 'top N' or 'bottom N' pattern"
        
        # Check for order parameter
        has_order = any('highest' in q['question'].lower() or 'lowest' in q['question'].lower() for q in questions)
        if has_order:
            rules['order'] = "DESC for highest/maximum/top, ASC for lowest/minimum/bottom"
        
        # Check for field parameter
        fields = set()
        for q in questions:
            if 'salary' in q['question'].lower():
                fields.add('Salary')
            if 'performance' in q['question'].lower() or 'rating' in q['question'].lower():
                fields.add('PerformanceRating')
            if 'engagement' in q['question'].lower():
                fields.add('OverallSatisfaction')
        
        if fields:
            rules['field'] = f"Field to rank by: {', '.join(fields)}"
        
        return rules
    
    def save_patterns(self, output_file: str = None):
        """Save extracted patterns to JSON"""
        if output_file is None:
            output_file = os.path.join(
                os.path.dirname(__file__),
                "query_patterns.json"
            )
        
        patterns = self.extract_patterns()
        
        output = {
            "metadata": {
                "total_patterns": len(patterns),
                "source": "comprehensive_questions.json",
                "description": "Query patterns extracted from 100 comprehensive HR questions"
            },
            "patterns": list(patterns.values())
        }
        
        with open(output_file, 'w') as f:
            json.dump(output, f, indent=2)
        
        print(f"✅ Saved {len(patterns)} patterns to {output_file}")
        return output


if __name__ == "__main__":
    extractor = PatternExtractor()
    patterns = extractor.save_patterns()
    
    print("\n" + "="*80)
    print("PATTERN EXTRACTION SUMMARY")
    print("="*80)
    print(f"Total Patterns: {len(patterns['patterns'])}")
    print("\nPattern Types:")
    for pattern in sorted(patterns['patterns'], key=lambda x: x['count'], reverse=True):
        print(f"  {pattern['pattern_type']}: {pattern['count']} questions")

