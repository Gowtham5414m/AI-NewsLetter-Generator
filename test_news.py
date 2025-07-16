from news_api import get_top_headlines
from pdf_generator import create_newsletter_pdf
from send_email import send_email_with_pdf


articles = get_top_headlines(category="technology", country="us")

if articles:
    pdf_file = create_newsletter_pdf(articles, category="Technology")
    print("PDF created:", pdf_file)
    send_email_with_pdf(pdf_file)

else:
    print("No articles found.")


