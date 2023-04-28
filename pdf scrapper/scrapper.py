import os
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from pdfdocument.document import PDFDocument
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

docs_urls = [
    "https://python.langchain.com/en/latest/",
    "https://js.langchain.com/docs/"
]

def get_links(url):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = []

    for link in soup.select("nav a"):
        href = link.get("href")
        if href:
            if href.startswith("http"):
                links.append(href)
            else:
                links.append(url + href)

    return links


def scrape_content(url):
    driver.get(url)
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    content = []

    for header in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        content.append(("\n" + header.text + "\n", "header"))

    for paragraph in soup.find_all("p"):
        content.append((paragraph.text + "\n", "paragraph"))

    for code in soup.find_all("pre"):
        content.append((code.text + "\n", "code"))

    return content

def create_pdf(content, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Monospace', fontName='Courier', fontSize=10))

    story = []

    for text, style in content:
        if style == "header":
            story.append(Paragraph(text, styles['Heading2']))
        elif style == "paragraph":
            story.append(Paragraph(text, styles['Normal']))
        elif style == "code":
            story.append(Paragraph(text, styles['Monospace']))

        story.append(Spacer(1, 12))

    doc.build(story)

if __name__ == "__main__":
    content = []

    # Set the path to the WebDriver if not in PATH
    driver_path = os.path.join(os.getcwd(), "chromedriver")
    driver = webdriver.Chrome(executable_path=driver_path)

    for url in docs_urls:
        links = get_links(url)
        for link in links:
            content.extend(scrape_content(link))

    driver.quit()

    create_pdf(content, "langchain_docs.pdf")
