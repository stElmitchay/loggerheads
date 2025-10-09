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

    prompt = f"""You are analyzing screenshots from a user's workday to generate an accurate daily work summary.

Today is: {today}

{user_context_prompt}

Below is OCR-extracted text from screenshots taken throughout the day. The text is messy and fragmented because it's from OCR.

CRITICAL RULES - READ CAREFULLY:
1. ONLY report what you can DIRECTLY OBSERVE in the screenshots
2. DO NOT infer, assume, or guess activities that aren't clearly visible
3. DO NOT make up tasks based on what you think the user should have done
4. If you see code editors, browser tabs, terminals - describe ONLY what's visible in the text
5. IGNORE: advertisements, social media browsing, entertainment, personal content, UI chrome
6. BE CONSERVATIVE: If unsure whether something is work, DON'T include it
7. Write in first person ("I worked on...", "I completed...")
8. Be specific - use actual project names, file names, technologies you see in the screenshots
9. DO NOT fabricate completion status - only mark as completed if there's clear evidence
10. If you see very little work content, it's OK to have a short summary

QUALITY CHECK BEFORE RESPONDING:
- Can I point to specific text in the OCR that supports this item? If NO, remove it.
- Am I making assumptions about what happened? If YES, remove it.
- Is this based on visible evidence? If NO, remove it.

OCR TEXT FROM SCREENSHOTS:
{combined_text}

Analyze ONLY what you can directly observe and generate a work summary in this EXACT format:

WORKED_ON:
[List ONLY tasks you can directly see evidence of in the screenshots. Be specific and cite what you saw (e.g., "Edited main.py file based on visible code", "Read documentation about Docker deployment"). If you cannot identify clear work activities, write "Limited work activity detected in screenshots"]

COMPLETED:
[List ONLY tasks with clear evidence of completion (e.g., closed PR, finished tutorial, deployed code). If no clear completions visible, write "No specific completions identified from screenshots"]

SOLANA_NEWS:
[List ONLY if you see actual Twitter/news content about Solana in the screenshots. Quote or paraphrase what you saw. If none found, write "No Solana news captured in screenshots"]

BLOCKERS:
[List ONLY specific errors, failed commands, or explicit blocker statements you see in the screenshots. If none visible, write "No significant blockers identified"]

TOMORROW_FOCUS:
{"[Skip this section - it's Friday]" if is_friday else "[Based ONLY on incomplete work visible in screenshots, suggest 2-3 follow-up items. If unclear what should be next, write 'Continue with current project work']"}

ACCURACY CHECK:
- Every item must be traceable to visible OCR text
- Zero hallucination or assumption
- When in doubt, leave it out
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
    Format AI-generated summary for display using exact specified template.

    Args:
        summary (dict): Structured summary from AI

    Returns:
        str: Formatted string for display
    """
    lines = []

    # ✅ What I Worked on Today
    lines.append("✅ What I Worked on Today:")
    tasks = summary.get('tasks_worked_on', [])
    if tasks:
        for task in tasks:
            lines.append(f"{task}")
    else:
        lines.append("[List specific tasks you worked on - be detailed, not vague]")
        lines.append("[Mention key progress made on projects]")
    lines.append("")

    # 🏁 What I Completed
    completed = summary.get('completed_tasks', [])
    if completed:
        lines.append("🏁 What I Completed:")
        for item in completed:
            lines.append(f"{item}")
        lines.append("")

    # 📰 What's the latest in the Solana Ecosystem
    solana_news = summary.get('solana_news', [])
    if solana_news and solana_news[0] != "No Solana news captured in screenshots":
        lines.append("📰 What's the latest in the Solana Ecosystem:")
        for news in solana_news:
            lines.append(f"{news}")
        lines.append("")

    # ⚠️ Issues / Blockers
    lines.append("⚠️ Issues / Blockers:")
    blockers = summary.get('problems_blockers', [])
    if blockers and blockers[0] != "No significant blockers identified":
        for blocker in blockers:
            lines.append(f"{blocker}")
    else:
        lines.append("[Mention specific challenges or dependencies]")
        lines.append("[Explain what help you need or how you're addressing them]")
    lines.append("")

    # 🔜 Focus for Tomorrow
    if not summary.get('is_friday', False):
        lines.append("🔜 Focus for Tomorrow:")
        tomorrow = summary.get('tomorrow_focus', [])
        if tomorrow:
            for focus in tomorrow:
                lines.append(f"{focus}")
        else:
            lines.append("[List specific priorities for the next day]")
        lines.append("")

    return "\n".join(lines)
