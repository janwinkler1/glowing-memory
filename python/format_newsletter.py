import re

def format_summary(text):
    # Split the input text into sections for "Title:" and "Summary:"
    sections = re.split(r'\n\n', text)
    
    # Process each section to format titles and summaries
    formatted_sections = []
    for section in sections:
        # Check if the section starts with "Title:" and format accordingly
        if section.startswith('Title:'):
            # Remove "Title:" and bold the title
            title = section.replace('Title:', '').strip()
            formatted_sections.append(f'<b>{title}</b>')
        elif section.startswith('Summary:'):
            # Keep the summary as is, but remove "Summary:" prefix
            summary = section.replace('Summary:', '').strip()
            formatted_sections.append('\n\n' + summary)
    
    # Join the formatted sections with newlines
    return '\n\n'.join(formatted_sections)


def create_html_newsletter(summary_hn, summary_lobsters, hn_stories, lobsters_stories):
    # Apply formatting to summaries
    summary_hn_html = f"<div class='summary'><h2>Hacker News Top Story Summary</h2><p>{format_summary(summary_hn)}</p></div>"
    summary_lobsters_html = f"<div class='summary'><h2>Lobsters Top Story Summary</h2><p>{format_summary(summary_lobsters)}</p></div>"
    
    # Generate HTML for story links (remains unchanged)
    hn_links_html = '<ol>' + ''.join(f'<li><a href="{story["url"]}" class="story-link">{story["title"]}</a></li>' for story in hn_stories) + '</ol>'
    lobsters_links_html = '<ol>' + ''.join(f'<li><a href="{story["url"]}" class="story-link">{story["title"]}</a></li>' for story in lobsters_stories) + '</ol>'

    # Define footer HTML (remains unchanged)
    footer_html = """<footer style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #ccc;"><p style="font-size: 14px; color: #666;">Disclaimer: All summaries were generated by AI. Hallucinations and formatting inconsistencies may occur.</p></footer>"""

    # Combine all HTML sections (remains unchanged)
    newsletter_html = f"""<!DOCTYPE html><html><head><style>body {{ font-family: Arial, sans-serif; }}.exec-summary, .story-section, footer {{ margin-bottom: 20px; }}.story-header {{ font-size: 20px; color: #333; }}.story-link {{ text-decoration: none; color: #007bff; }}ol {{ padding-left: 20px; }}h2 {{ color: #333; }}p, footer p {{ margin: 10px 0; font-size: 16px; }}footer {{ font-size: 14px; color: #666; text-align: center; }}</style></head><body>{summary_hn_html}{summary_lobsters_html}<div class="story-section"><h2 class="story-header">Top Hacker News Stories</h2>{hn_links_html}</div><div class="story-section"><h2 class="story-header">Top Lobsters Stories</h2>{lobsters_links_html}</div>{footer_html}</body></html>"""

    return newsletter_html

