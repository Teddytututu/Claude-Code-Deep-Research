#!/usr/bin/env python3
"""
Link Validator Agent - Validates all links in research reports
"""

import json
import asyncio
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any
from urllib.parse import urlparse

# Categories
URL_CATEGORIES = {
    'arxiv': 'arxiv.org',
    'github': 'github.com',
    'doi': 'doi.org',
    'csdn': 'blog.csdn.net|m.blog.csdn.net',
    'ultralytics': 'ultralytics.com',
    'sohu': 'sohu.com',
    'sina': 'sina.com.cn',
    'northnews': 'northnews.cn',
    'mdpi': 'mdpi.com',
    'gitcode': 'gitcode.com',
}

def categorize_url(url: str) -> str:
    """Categorize URL by domain"""
    url_lower = url.lower()
    for category, pattern in URL_CATEGORIES.items():
        if re.search(pattern, url_lower):
            return category
    return 'other'


async def validate_link_with_webreader(url: str, timeout: int = 15) -> Dict[str, Any]:
    """
    Validate a single link using webReader

    Note: This function should be called via MCP web-reader tool
    """
    result = {
        'url': url,
        'status': 'unknown',
        'error': None,
        'response_time': None,
        'content_length': 0
    }

    # This will be called via MCP tool, so we return the structure
    return result


def generate_validation_report(
    validation_results: List[Dict[str, Any]],
    reports_validated: List[str]
) -> Dict[str, Any]:
    """Generate final validation report"""

    total_links = len(validation_results)
    valid_links = sum(1 for r in validation_results if r['status'] == 'valid')
    broken_links = sum(1 for r in validation_results if r['status'] == 'broken')
    timeout_links = sum(1 for r in validation_results if r['status'] == 'timeout')

    # Group by type
    by_type = {}
    for result in validation_results:
        link_type = result.get('link_type', 'other')
        if link_type not in by_type:
            by_type[link_type] = {'total': 0, 'valid': 0, 'broken': 0, 'timeout': 0}
        by_type[link_type]['total'] += 1
        by_type[link_type][result['status']] += 1

    # Group by file
    by_file = {}
    for result in validation_results:
        source_file = result.get('source_file', 'unknown')
        if source_file not in by_file:
            by_file[source_file] = {'total': 0, 'valid': 0, 'broken': 0, 'timeout': 0}
        by_file[source_file]['total'] += 1
        by_file[source_file][result['status']] += 1

    # Broken links detail
    broken_links_detail = [
        {
            'url': r['url'],
            'link_type': r.get('link_type', 'unknown'),
            'source_file': r.get('source_file', 'unknown'),
            'line_number': r.get('line_number'),
            'markdown_context': r.get('markdown_context'),
            'error': r.get('error', 'Unknown error')
        }
        for r in validation_results
        if r['status'] in ['broken', 'timeout']
    ]

    validation_rate = (valid_links / total_links * 100) if total_links > 0 else 0

    report = {
        'validation_id': f'link_validation_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
        'timestamp': datetime.now().isoformat(),
        'reports_validated': reports_validated,
        'total_links_found': total_links,
        'valid_links': valid_links,
        'broken_links': broken_links,
        'timeout_links': timeout_links,
        'validation_rate': round(validation_rate, 2),
        'summary': {
            'by_type': by_type,
            'by_file': by_file
        },
        'broken_links_detail': broken_links_detail
    }

    return report


if __name__ == '__main__':
    # Load links to validate
    links_file = Path('research_data/links_to_validate.json')

    if not links_file.exists():
        print('Error: links_to_validate.json not found')
        exit(1)

    with open(links_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f'Loaded {data["total_unique_links"]} links to validate')
    print(f'  arXiv: {data["by_type"]["arxiv"]}')
    print(f'  GitHub: {data["by_type"]["github"]}')
    print(f'  CSDN: {data["by_type"]["csdn"]}')
    print(f'  Other: {data["by_type"]["other"]}')
