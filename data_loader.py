from cidb_processor import CIDBProcessor
from jkr_processor import JKRProcessor

def main():
    cidb = CIDBProcessor()
    cidb.process_documents()
    jkr = JKRProcessor()
    jkr.process_documents()

if __name__ == "__main__":
    main()
