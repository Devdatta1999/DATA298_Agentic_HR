"""Generate PDF from comprehensive questions dataset"""
import json
import os
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def generate_questions_pdf(output_file: str = None):
    """Generate PDF with all questions for testing"""
    if output_file is None:
        output_file = os.path.join(
            os.path.dirname(__file__),
            "HR_Analytics_Test_Questions.pdf"
        )
    
    # Load questions
    questions_file = os.path.join(
        os.path.dirname(__file__),
        "comprehensive_questions.json"
    )
    
    with open(questions_file, 'r') as f:
        data = json.load(f)
    
    questions = data.get('questions', [])
    metadata = data.get('metadata', {})
    
    # Create PDF
    doc = SimpleDocTemplate(output_file, pagesize=letter)
    story = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1e3a8a'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#3b82f6'),
        spaceAfter=12,
        spaceBefore=12
    )
    
    question_style = ParagraphStyle(
        'Question',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#1f2937'),
        spaceAfter=6,
        leftIndent=20
    )
    
    sql_style = ParagraphStyle(
        'SQL',
        parent=styles['Code'],
        fontSize=9,
        textColor=colors.HexColor('#059669'),
        fontName='Courier',
        leftIndent=30,
        spaceAfter=8
    )
    
    # Title
    story.append(Paragraph("HR Analytics Agent - Test Questions", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Metadata
    story.append(Paragraph(f"<b>Total Questions:</b> {metadata.get('total_questions', len(questions))}", styles['Normal']))
    story.append(Paragraph(f"<b>Created:</b> {metadata.get('created_date', 'N/A')}", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Group by category
    categories = {}
    for q in questions:
        cat = q.get('category', 'unknown')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(q)
    
    # Questions by category
    for category in ['easy', 'medium', 'tricky']:
        if category not in categories:
            continue
        
        cat_questions = categories[category]
        story.append(Paragraph(f"{category.upper()} Questions ({len(cat_questions)})", heading_style))
        story.append(Spacer(1, 0.1*inch))
        
        for idx, q in enumerate(cat_questions, 1):
            # Question
            q_text = f"<b>Q{q['id']}:</b> {q['question']}"
            story.append(Paragraph(q_text, question_style))
            
            # Pattern type
            pattern = q.get('pattern_type', 'N/A')
            story.append(Paragraph(f"<i>Pattern: {pattern}</i>", styles['Italic']))
            
            # SQL (truncated if too long)
            sql = q.get('sql', '')
            if len(sql) > 150:
                sql_display = sql[:150] + "..."
            else:
                sql_display = sql
            story.append(Paragraph(f"SQL: <font face='Courier' size='8'>{sql_display}</font>", sql_style))
            
            # Visualization
            viz = q.get('visualization', 'N/A')
            story.append(Paragraph(f"Visualization: <b>{viz}</b>", styles['Normal']))
            
            story.append(Spacer(1, 0.15*inch))
        
        story.append(PageBreak())
    
    # Summary table
    story.append(Paragraph("Question Summary by Pattern Type", heading_style))
    
    # Count by pattern
    pattern_counts = {}
    for q in questions:
        pattern = q.get('pattern_type', 'unknown')
        pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
    
    # Create table
    table_data = [['Pattern Type', 'Count']]
    for pattern, count in sorted(pattern_counts.items(), key=lambda x: x[1], reverse=True):
        table_data.append([pattern, str(count)])
    
    table = Table(table_data, colWidths=[4*inch, 1*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3b82f6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
    ]))
    
    story.append(table)
    
    # Build PDF
    doc.build(story)
    print(f"✅ PDF generated: {output_file}")
    return output_file


if __name__ == "__main__":
    generate_questions_pdf()

