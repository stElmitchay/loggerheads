"""
Text analyzer for processing OCR-extracted text from screenshots.
Focuses on extracting actual work content, tasks, and accomplishments.
"""

import re
from collections import Counter, defaultdict
from datetime import datetime
from urllib.parse import urlparse
from rich.console import Console
from rich.table import Table
from rich.text import Text

console = Console()


# Work-related action verbs that indicate tasks/accomplishments
ACTION_VERBS = {
    'implemented', 'created', 'built', 'developed', 'designed', 'wrote',
    'fixed', 'debugged', 'resolved', 'solved', 'updated', 'refactored',
    'added', 'removed', 'modified', 'deployed', 'tested', 'reviewed',
    'configured', 'setup', 'installed', 'integrated', 'optimized',
    'documented', 'researched', 'analyzed', 'learned', 'studied'
}

# Technical topics and domains
TECHNICAL_TOPICS = {
    'api', 'database', 'backend', 'frontend', 'authentication', 'authorization',
    'security', 'performance', 'optimization', 'testing', 'deployment',
    'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'ci/cd', 'pipeline',
    'microservices', 'rest', 'graphql', 'websocket', 'cache', 'redis',
    'postgres', 'mysql', 'mongodb', 'react', 'vue', 'angular', 'node',
    'python', 'javascript', 'typescript', 'java', 'golang', 'rust'
}

# Problem/issue indicators
PROBLEM_INDICATORS = {
    'error', 'bug', 'issue', 'problem', 'fail', 'exception', 'crash',
    'broken', 'fix', 'debug', 'troubleshoot', 'investigate'
}

# Documentation/learning indicators
LEARNING_INDICATORS = {
    'documentation', 'docs', 'tutorial', 'guide', 'learn', 'study',
    'research', 'example', 'how to', 'understanding', 'overview'
}

# Solana/crypto indicators for news detection
SOLANA_KEYWORDS = {
    'solana', 'sol', 'solana ecosystem', 'solana network', 'solana labs',
    'defi', 'nft', 'web3', 'dex', 'jupiter', 'raydium', 'marinade',
    'phantom', 'solflare', 'magic eden', 'tensor', 'drift', 'mango',
    'jito', 'squads', 'backpack', 'helius', 'triton', 'metaplex'
}


def extract_tasks_and_accomplishments(text):
    """
    Extract tasks and accomplishments from text based on action verbs.

    Args:
        text (str): Text to analyze

    Returns:
        list: List of task/accomplishment phrases
    """
    tasks = []
    text_lower = text.lower()
    sentences = re.split(r'[.!?\n]+', text)

    for sentence in sentences:
        sentence_lower = sentence.lower().strip()
        # Look for action verbs in the sentence
        for verb in ACTION_VERBS:
            if re.search(r'\b' + verb + r'\b', sentence_lower):
                # Clean up and add the sentence
                clean_sentence = sentence.strip()
                if len(clean_sentence) > 10 and len(clean_sentence) < 200:
                    tasks.append(clean_sentence)
                    break  # One task per sentence

    return tasks


def extract_technical_topics(text):
    """
    Extract technical topics and technologies mentioned in text.

    Args:
        text (str): Text to analyze

    Returns:
        list: List of technical topics found
    """
    topics = []
    text_lower = text.lower()

    for topic in TECHNICAL_TOPICS:
        pattern = r'\b' + re.escape(topic) + r'\b'
        if re.search(pattern, text_lower):
            topics.append(topic)

    return topics


def extract_problems_solved(text):
    """
    Extract problems, bugs, or issues being worked on.

    Args:
        text (str): Text to analyze

    Returns:
        list: List of problem-related phrases
    """
    problems = []
    text_lower = text.lower()
    sentences = re.split(r'[.!?\n]+', text)

    for sentence in sentences:
        sentence_lower = sentence.lower().strip()
        # Look for problem indicators
        for indicator in PROBLEM_INDICATORS:
            if re.search(r'\b' + indicator + r'\b', sentence_lower):
                clean_sentence = sentence.strip()
                if len(clean_sentence) > 10 and len(clean_sentence) < 200:
                    problems.append(clean_sentence)
                    break

    return problems


def extract_learning_topics(text):
    """
    Extract learning/research topics from text.

    Args:
        text (str): Text to analyze

    Returns:
        list: List of learning-related phrases
    """
    learning = []
    text_lower = text.lower()
    sentences = re.split(r'[.!?\n]+', text)

    for sentence in sentences:
        sentence_lower = sentence.lower().strip()
        # Look for learning indicators
        for indicator in LEARNING_INDICATORS:
            if re.search(r'\b' + indicator + r'\b', sentence_lower):
                clean_sentence = sentence.strip()
                if len(clean_sentence) > 10 and len(clean_sentence) < 200:
                    learning.append(clean_sentence)
                    break

    return learning


def extract_code_snippets(text):
    """
    Extract potential code snippets or function names from text.

    Args:
        text (str): Text to analyze

    Returns:
        list: List of code-like patterns found
    """
    code_patterns = []

    # Look for function definitions
    function_pattern = r'(def|function|func|const|let|var)\s+(\w+)\s*\('
    functions = re.findall(function_pattern, text, re.IGNORECASE)
    for match in functions:
        code_patterns.append(f"{match[0]} {match[1]}()")

    # Look for class definitions
    class_pattern = r'class\s+(\w+)'
    classes = re.findall(class_pattern, text, re.IGNORECASE)
    for class_name in classes:
        code_patterns.append(f"class {class_name}")

    # Look for import statements
    import_pattern = r'(import|from|require)\s+([\w\.]+)'
    imports = re.findall(import_pattern, text, re.IGNORECASE)
    for match in imports:
        code_patterns.append(f"{match[0]} {match[1]}")

    return code_patterns


def extract_solana_news(text):
    """
    Extract Solana ecosystem news/updates from text (e.g., Twitter screenshots).

    Args:
        text (str): Text to analyze

    Returns:
        list: List of Solana-related news items
    """
    news_items = []
    text_lower = text.lower()

    # Check if text contains Solana-related keywords
    has_solana = any(re.search(r'\b' + re.escape(keyword) + r'\b', text_lower)
                     for keyword in SOLANA_KEYWORDS)

    if has_solana:
        sentences = re.split(r'[.!?\n]+', text)
        for sentence in sentences:
            sentence_lower = sentence.lower().strip()
            # Check if sentence mentions Solana keywords
            for keyword in SOLANA_KEYWORDS:
                if re.search(r'\b' + re.escape(keyword) + r'\b', sentence_lower):
                    clean_sentence = sentence.strip()
                    if len(clean_sentence) > 15 and len(clean_sentence) < 250:
                        news_items.append(clean_sentence)
                        break

    return news_items


def detect_completion_indicators(text):
    """
    Detect if tasks were completed (vs just worked on).

    Args:
        text (str): Text to analyze

    Returns:
        list: List of completed task phrases
    """
    completion_verbs = {
        'completed', 'finished', 'deployed', 'shipped', 'merged',
        'released', 'done', 'resolved', 'closed', 'published'
    }

    completed = []
    sentences = re.split(r'[.!?\n]+', text)

    for sentence in sentences:
        sentence_lower = sentence.lower().strip()
        for verb in completion_verbs:
            if re.search(r'\b' + verb + r'\b', sentence_lower):
                clean_sentence = sentence.strip()
                if len(clean_sentence) > 10 and len(clean_sentence) < 200:
                    completed.append(clean_sentence)
                    break

    return completed


def analyze_text(text):
    """
    Perform comprehensive analysis on extracted text focusing on work content.

    Args:
        text (str): Text to analyze

    Returns:
        dict: Dictionary containing all analysis results
    """
    if not text or not text.strip():
        return {
            'tasks': [],
            'completed': [],
            'problems': [],
            'learning': [],
            'code_snippets': [],
            'technical_topics': [],
            'solana_news': [],
            'word_count': 0
        }

    tasks = extract_tasks_and_accomplishments(text)
    completed = detect_completion_indicators(text)
    problems = extract_problems_solved(text)
    learning = extract_learning_topics(text)
    code = extract_code_snippets(text)
    topics = extract_technical_topics(text)
    solana = extract_solana_news(text)

    return {
        'tasks': tasks,
        'completed': completed,
        'problems': problems,
        'learning': learning,
        'code_snippets': code,
        'technical_topics': topics,
        'solana_news': solana,
        'word_count': len(text.split())
    }


def generate_frequency_summary(analysis_results):
    """
    Generate work-focused summary from multiple analysis results.

    Args:
        analysis_results (list): List of analysis result dictionaries

    Returns:
        dict: Summary with work accomplishments and topics
    """
    all_tasks = []
    all_completed = []
    all_problems = []
    all_learning = []
    all_code = []
    all_topics = []
    all_solana = []
    total_words = 0

    for result in analysis_results:
        all_tasks.extend(result.get('tasks', []))
        all_completed.extend(result.get('completed', []))
        all_problems.extend(result.get('problems', []))
        all_learning.extend(result.get('learning', []))
        all_code.extend(result.get('code_snippets', []))
        all_topics.extend(result.get('technical_topics', []))
        all_solana.extend(result.get('solana_news', []))
        total_words += result.get('word_count', 0)

    return {
        'tasks': all_tasks,
        'completed': all_completed,
        'problems': all_problems,
        'learning': all_learning,
        'code_snippets': list(set(all_code)),  # Deduplicate
        'technical_topics': Counter(all_topics).most_common(15),
        'solana_news': list(set(all_solana)),  # Deduplicate
        'total_word_count': total_words,
        'total_sessions': len(analysis_results)
    }


def group_by_time(screenshot_data, interval_minutes=60):
    """
    Group screenshots by time intervals.

    Args:
        screenshot_data (list): List of dicts with 'timestamp' and 'analysis' keys
        interval_minutes (int): Time interval in minutes for grouping

    Returns:
        dict: Dictionary mapping time periods to analysis results
    """
    grouped = {}

    for item in screenshot_data:
        timestamp = item.get('timestamp')
        if not timestamp:
            continue

        # Parse timestamp if it's a string
        if isinstance(timestamp, str):
            try:
                timestamp = datetime.fromisoformat(timestamp)
            except:
                continue

        # Round down to the nearest interval
        minutes = (timestamp.hour * 60 + timestamp.minute) // interval_minutes * interval_minutes
        hour = minutes // 60
        minute = minutes % 60

        time_key = f"{hour:02d}:{minute:02d}"

        if time_key not in grouped:
            grouped[time_key] = []

        grouped[time_key].append(item.get('analysis', {}))

    return grouped


def generate_tomorrow_focus(tasks, problems, topics):
    """
    Generate recommended focus areas for tomorrow based on today's work.

    Args:
        tasks (list): Tasks worked on today
        problems (list): Problems encountered
        topics (list): Technical topics covered

    Returns:
        list: Recommended focus areas for tomorrow
    """
    recommendations = []

    # If there were problems, suggest following up
    if problems:
        recommendations.append("Follow up on unresolved issues from today")

    # Suggest continuing work based on tasks
    if tasks:
        # Look for incomplete indicators
        incomplete_keywords = ['start', 'begin', 'working on', 'in progress', 'exploring']
        for task in tasks[:3]:
            task_lower = task.lower()
            if any(keyword in task_lower for keyword in incomplete_keywords):
                recommendations.append(f"Continue: {task[:80]}")
                break

    # Suggest based on technical topics
    if topics:
        top_topic = topics[0] if isinstance(topics, list) else list(topics.keys())[0]
        recommendations.append(f"Deep dive into {top_topic}")

    # Default recommendations if nothing specific
    if not recommendations:
        recommendations.append("Review and prioritize tasks based on project goals")

    return recommendations[:3]  # Max 3 recommendations


def generate_structured_summary(screenshot_data, is_friday=False):
    """
    Generate a comprehensive structured summary focused on actual work content.

    Args:
        screenshot_data (list): List of dicts with 'timestamp' and 'analysis' keys
        is_friday (bool): Whether today is Friday (skip tomorrow focus)

    Returns:
        dict: Comprehensive summary with work accomplishments
    """
    if not screenshot_data:
        return {
            'summary': 'No data to analyze',
            'activity_detected': False
        }

    # Extract all analysis results
    all_analyses = [item.get('analysis', {}) for item in screenshot_data]

    # Generate work-focused summary
    work_summary = generate_frequency_summary(all_analyses)

    # Generate tomorrow's focus (unless Friday)
    tomorrow_focus = []
    if not is_friday:
        tomorrow_focus = generate_tomorrow_focus(
            work_summary['tasks'],
            work_summary['problems'],
            work_summary['technical_topics']
        )

    return {
        'tasks_worked_on': work_summary['tasks'],
        'completed_tasks': work_summary['completed'],
        'problems_blockers': work_summary['problems'],
        'solana_news': work_summary['solana_news'],
        'technical_topics': dict(work_summary['technical_topics']),
        'tomorrow_focus': tomorrow_focus,
        'is_friday': is_friday,
        'total_screenshots': work_summary['total_sessions'],
        'total_word_count': work_summary['total_word_count'],
        'activity_detected': work_summary['total_word_count'] > 0
    }


def format_summary_for_display(summary):
    """
    Format the work summary using the specified template with Rich formatting.

    Args:
        summary (dict): Structured summary from generate_structured_summary()

    Returns:
        str: Formatted string for display
    """
    lines = []
    lines.append("")

    if not summary.get('activity_detected', False):
        lines.append("[yellow]No significant activity detected.[/yellow]")
        return "\n".join(lines)

    # ✅ What I Worked on Today
    tasks = summary.get('tasks_worked_on', [])
    if tasks:
        lines.append("[bold green]✅ What I Worked on Today:[/bold green]")
        unique_tasks = list(set(tasks))[:15]  # Get unique tasks, max 15
        for task in unique_tasks:
            lines.append(f"  [cyan]•[/cyan] {task}")
        lines.append("")

    # 🏁 What I Completed
    completed = summary.get('completed_tasks', [])
    if completed:
        lines.append("[bold blue]🏁 What I Completed:[/bold blue]")
        unique_completed = list(set(completed))[:10]
        for item in unique_completed:
            lines.append(f"  [cyan]•[/cyan] {item}")
        lines.append("")

    # 📰 What's the latest in the Solana Ecosystem
    solana_news = summary.get('solana_news', [])
    if solana_news:
        lines.append("[bold magenta]📰 What's the latest in the Solana Ecosystem:[/bold magenta]")
        unique_news = list(set(solana_news))[:5]
        for news in unique_news:
            lines.append(f"  [cyan]•[/cyan] {news}")
        lines.append("")

    # ⚠️ Issues / Blockers
    problems = summary.get('problems_blockers', [])
    if problems:
        lines.append("[bold yellow]⚠️  Issues / Blockers:[/bold yellow]")
        unique_problems = list(set(problems))[:8]
        for problem in unique_problems:
            lines.append(f"  [cyan]•[/cyan] {problem}")
    else:
        lines.append("[bold yellow]⚠️  Issues / Blockers:[/bold yellow]")
        lines.append("  [dim]• No significant blockers identified[/dim]")
    lines.append("")

    # 🔜 Focus for Tomorrow (Skip on Fridays)
    if not summary.get('is_friday', False):
        tomorrow_focus = summary.get('tomorrow_focus', [])
        if tomorrow_focus:
            lines.append("[bold cyan]🔜 Focus for Tomorrow:[/bold cyan]")
            for focus in tomorrow_focus:
                lines.append(f"  [cyan]•[/cyan] {focus}")
        else:
            lines.append("[bold cyan]🔜 Focus for Tomorrow:[/bold cyan]")
            lines.append("  [dim]• Continue current project work[/dim]")
        lines.append("")

    return "\n".join(lines)
