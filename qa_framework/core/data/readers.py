import openpyxl

class DataLoader:
    """
    Utility class to load data from various file formats.
    """
    @staticmethod
    def load_json(path: str) -> Any:
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception as e:
            raise DataLoadingError(f"Failed to load JSON from {path}", e)

    @staticmethod
    def load_yaml(path: str) -> Any:
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise DataLoadingError(f"Failed to load YAML from {path}", e)

    @staticmethod
    def load_csv(path: str) -> List[Dict[str, str]]:
        try:
            with open(path, 'r') as f:
                reader = csv.DictReader(f)
                return [row for row in reader]
        except Exception as e:
            raise DataLoadingError(f"Failed to load CSV from {path}", e)

    @staticmethod
    def load_xlsx(path: str, sheet_name: str = None) -> List[Dict[str, Any]]:
        """
        Loads data from an Excel file. 
        Returns a list of dictionaries where keys are header row values.
        """
        try:
            workbook = openpyxl.load_workbook(path, data_only=True)
            if sheet_name:
                sheet = workbook[sheet_name]
            else:
                sheet = workbook.active
            
            data = []
            rows = list(sheet.iter_rows(values_only=True))
            if not rows:
                return []
                
            headers = rows[0]
            for row in rows[1:]:
                # Create dict only if row is not completely empty
                if any(row):
                    data.append(dict(zip(headers, row)))
            
            return data
        except Exception as e:
            raise DataLoadingError(f"Failed to load XLSX from {path}", e)
