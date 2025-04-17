from docx import Document
from docx.shared import Pt
import sys
sys.path.insert(0, './api_call.py')
import api_call


def replace_in_paragraph(paragraph, key, value):
    if key in paragraph.text:
        inline = paragraph.runs
        for item in inline:
            if key in item.text:
                item.text = item.text.replace(key, value)



document = Document("./docx-template/TERMO DE RESPONSABILIDADES V2.04.04.2025-1752.docx")
style = document.styles['Normal']
font = style.font
font.name = 'Montserrat'
font.size = Pt(9)

assigned_to = input("Digite a matrícula: ")

assetList = api_call.hardwareApiCall(assigned_to)

hasLaptop = False
hasMonitor = False

for asset in assetList.get('assets', []):
    if asset.get('category') == 'Laptops':
        hasLaptop = True
    if asset.get('category') == 'Monitors':
        hasMonitor = True


for paragraph in document.paragraphs:
    replace_in_paragraph(paragraph, "[NAME]", assetList.get('user_name', ''))
    replace_in_paragraph(paragraph, "[EMPLOYEE_NUMBER]", assetList.get('employee_number', ''))
    
    if hasLaptop:
        replace_in_paragraph(paragraph, "[ISLAPTOPS]", "X")
        for asset in assetList.get('assets', []):
            if asset.get('category') == 'Laptops':
                replace_in_paragraph(paragraph, "[LAPTOPMODEL]", asset.get('model', ''))
    else:
        replace_in_paragraph(paragraph, "[ISLAPTOPS]", " ")
        replace_in_paragraph(paragraph, "[LAPTOPMODEL]", "_____________________________")
    
    if hasMonitor:
        replace_in_paragraph(paragraph, "[ISMONITORS]", "X")
        for asset in assetList.get('assets', []):
            if asset.get('category') == 'Monitors':
                replace_in_paragraph(paragraph, "[MONITORMODEL]", asset.get('model', ''))
    else:
        replace_in_paragraph(paragraph, "[ISMONITORS]", " ")
        replace_in_paragraph(paragraph, "[MONITORMODEL]", "_____________________________")
    
document.save("./Termos/" + f"Termo - {assetList.get('user_name')}.docx")