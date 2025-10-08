"""
AI-powered summarization using Ollama local LLM.
Converts raw OCR text into intelligent work summaries.
"""

import requests
import json
from datetime import datetime
from rich.console import Console
from .user_context import get_user_context

console = Console()


def summarize_work_with_ai(all_ocr_text, ollama_url, ollama_model, is_friday=False):
    """
    Use Ollama local LLM to analyze all OCR text and generate intelligent work summary.

    Args:
        all_ocr_text (list): List of OCR text strings from all screenshots
        ollama_url (str): Ollama API URL (e.g., http://localhost:11434)
        ollama_model (str): Ollama model name (e.g., llama3.2)
        is_friday (bool): Whether today is Friday

    Returns:
        dict: Structured summary with all sections
    """
    if not all_ocr_text or len(all_ocr_text) == 0:
        console.print("[bold red]❌ No OCR text to analyze[/bold red]")
        return None

    # Sample screenshots if too many (take every Nth screenshot for better coverage)
    original_count = len(all_ocr_text)
    if len(all_ocr_text) > 30:
        sample_rate = max(2, len(all_ocr_text) // 30)
        all_ocr_text = all_ocr_text[::sample_rate]
        console.print(f"[cyan]📊 Sampled {len(all_ocr_text)} screenshots from {original_count} total (every {sample_rate}th)[/cyan]")

    # Combine all OCR text
    combined_text = "\n\n---SCREENSHOT---\n\n".join(all_ocr_text)

    # Truncate if still too long
    max_chars = 5000000  # Conservative limit for local models
    if len(combined_text) > max_chars:
        console.print(f"[yellow]⚠️  Text still too long ({len(combined_text)} chars), truncating to {max_chars}[/yellow]")
        combined_text = combined_text[:max_chars]

    # Get user context for intelligent categorization
    user_context = get_user_context()
    user_context_prompt = user_context.get_user_context_prompt()

    # Create the prompt
    today = datetime.now().strftime("%A, %B %d, %Y")

    prompt = f"""You are analyzing screenshots from a user's workday to generate an intelligent daily work summary.

Today is: {today}

{user_context_prompt}

Below is OCR-extracted text from screenshots taken throughout the day. The text is messy and fragmented because it's from OCR. Your job is to intelligently analyze this text and understand what the person actually worked on.

IMPORTANT INSTRUCTIONS:
1. ONLY include work-related activities based on the user's role and industry defined above
2. IGNORE personal activities, social media browsing, entertainment, personal messaging
3. Look for patterns and context to understand actual work activities
4. Identify courses taken, projects worked on, code written, problems solved
5. Extract Solana ecosystem news if any Twitter/news screenshots are present
6. Identify actual blockers or technical issues encountered
7. Be specific and detailed - don't just list file names or fragments
8. Write in first person ("I worked on...", "I completed...")
9. Ignore UI elements, random text, timestamps, etc.
10. Focus on ACTUAL WORK CONTENT that's relevant to the user's professional role

OCR TEXT FROM SCREENSHOTS:
{combined_text}

Please analyze the above text and generate a work summary in this EXACT format:

WORKED_ON:
[List 3-8 specific detailed WORK tasks/activities you identified from the screenshots. Be descriptive and specific about what was actually done. ONLY include professional work activities. Examples: "Took AI Intro to MCP course", "Debugged authentication error in user service", "Researched deployment strategies"]

COMPLETED:
[List 2-5 WORK tasks that were clearly finished/completed. Only include if there's clear evidence of completion. If nothing was clearly completed, write "No specific completions identified from screenshots"]

SOLANA_NEWS:
[List 1-3 Solana ecosystem updates/news if you found any Twitter/news screenshots or Solana-related content. Include brief context. If none found, write "No Solana news captured in screenshots"]

BLOCKERS:
[List 1-3 specific technical issues, errors, or blockers encountered. Be specific about the actual problem. If none found, write "No significant blockers identified"]

TOMORROW_FOCUS:
{"[Skip this section - it's Friday]" if is_friday else "[List 2-3 intelligent recommendations for tomorrow based on what was worked on today and what seems incomplete or needs follow-up]"}

IMPORTANT:
- Do NOT just list raw OCR fragments
- Do NOT list file names without context
- DO extract actual work activities and meaning
- DO be specific and detailed
- DO write in first person
"""

    try:
        console.print(f"[bold magenta]🤖 Calling Ollama ({ollama_model}) to analyze work...[/bold magenta]")

        # Call Ollama API
        response = requests.post(
            f"{ollama_url}/api/generate",
            json={
                "model": ollama_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 2000
                }
            },
            timeout=120  # 2 minute timeout for local processing
        )

        if response.status_code != 200:
            console.print(f"[bold red]❌ Ollama API error: {response.status_code}[/bold red]")
            return None

        # Parse the response
        response_json = response.json()
        response_text = response_json.get("response", "")

        if not response_text:
            console.print("[bold red]❌ No response from Ollama[/bold red]")
            return None

        # Parse the structured response
        summary = parse_ai_response(response_text, is_friday)

        console.print("[bold green]✅ AI analysis complete[/bold green]")
        return summary

    except requests.exceptions.ConnectionError:
        console.print("[bold red]❌ Could not connect to Ollama.[/bold red] Make sure Ollama is running (ollama serve)")
        return None
    except requests.exceptions.Timeout:
        console.print("[bold red]❌ Ollama request timed out.[/bold red] The model might be too slow or the text too long.")
        return None
    except Exception as e:
        console.print(f"[bold red]❌ Error calling Ollama: {e}[/bold red]")
        return None


def parse_ai_response(response_text, is_friday):
    """
    Parse Claude's response into structured format.

    Args:
        response_text (str): Claude's response
        is_friday (bool): Whether today is Friday

    Returns:
        dict: Structured summary
    """
    summary = {
        'tasks_worked_on': [],
        'completed_tasks': [],
        'solana_news': [],
        'problems_blockers': [],
        'tomorrow_focus': [],
        'is_friday': is_friday
    }

    current_section = None

    for line in response_text.split('\n'):
        line = line.strip()

        if line.startswith('WORKED_ON:'):
            current_section = 'tasks_worked_on'
            continue
        elif line.startswith('COMPLETED:'):
            current_section = 'completed_tasks'
            continue
        elif line.startswith('SOLANA_NEWS:'):
            current_section = 'solana_news'
            continue
        elif line.startswith('BLOCKERS:'):
            current_section = 'problems_blockers'
            continue
        elif line.startswith('TOMORROW_FOCUS:'):
            current_section = 'tomorrow_focus' if not is_friday else None
            continue

        # Add content to current section
        if current_section and line and not line.startswith('['):
            # Remove bullet points and clean up
            clean_line = line.lstrip('•-*').strip()
            if clean_line and len(clean_line) > 5:
                summary[current_section].append(clean_line)

    return summary


def format_ai_summary_for_display(summary):
    """
    Format AI-generated summary for display with Rich formatting.

    Args:
        summary (dict): Structured summary from AI

    Returns:
        str: Formatted string for display
    """
    lines = []
    lines.append("")

    # ✅ What I Worked on Today
    tasks = summary.get('tasks_worked_on', [])
    if tasks:
        lines.append("[bold green]✅ What I Worked on Today:[/bold green]")
        for task in tasks:
            lines.append(f"  [cyan]•[/cyan] {task}")
        lines.append("")
    else:
        lines.append("[bold green]✅ What I Worked on Today:[/bold green]")
        lines.append("  [dim]• No significant work activities identified[/dim]")
        lines.append("")

    # 🏁 What I Completed
    completed = summary.get('completed_tasks', [])
    if completed:
        lines.append("[bold blue]🏁 What I Completed:[/bold blue]")
        for item in completed:
            lines.append(f"  [cyan]•[/cyan] {item}")
        lines.append("")

    # 📰 What's the latest in the Solana Ecosystem
    solana_news = summary.get('solana_news', [])
    if solana_news and solana_news[0] != "No Solana news captured in screenshots":
        lines.append("[bold magenta]📰 What's the latest in the Solana Ecosystem:[/bold magenta]")
        for news in solana_news:
            lines.append(f"  [cyan]•[/cyan] {news}")
        lines.append("")

    # ⚠️ Issues / Blockers
    blockers = summary.get('problems_blockers', [])
    if blockers and blockers[0] != "No significant blockers identified":
        lines.append("[bold yellow]⚠️  Issues / Blockers:[/bold yellow]")
        for blocker in blockers:
            lines.append(f"  [cyan]•[/cyan] {blocker}")
    else:
        lines.append("[bold yellow]⚠️  Issues / Blockers:[/bold yellow]")
        lines.append("  [dim]• No significant blockers identified[/dim]")
    lines.append("")

    # 🔜 Focus for Tomorrow
    if not summary.get('is_friday', False):
        tomorrow = summary.get('tomorrow_focus', [])
        if tomorrow:
            lines.append("[bold cyan]🔜 Focus for Tomorrow:[/bold cyan]")
            for focus in tomorrow:
                lines.append(f"  [cyan]•[/cyan] {focus}")
            lines.append("")

    return "\n".join(lines)
