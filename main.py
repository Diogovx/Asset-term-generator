import logging
import api_call
import os
from util import configure_logging
from document_processor import DocumentProcessor


configure_logging()
logger = logging.getLogger(__name__)


def main():
    documentProcessor = DocumentProcessor()
    documentProcessor.load_template()
    # while True:
    assigned_to = input("Digite a matrícula: ")
    try:
        assetList = api_call.hardwareApiCall(assigned_to)
        documentProcessor.process_assets(assetList)
        documentProcessor.save(assetList.get('user_name', ''))
        
        logger.info(f"Termo de responsabilidade do usuário {assetList.get('user_name', '')} criado!")
    except Exception as e:
        logger.error(f"Erro ao processar termo: {e}")
    os.system("PAUSE")
        
if __name__ == "__main__":
    main()