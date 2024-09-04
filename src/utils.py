# src/utils.py
import pandas as pd
from io import BytesIO
import tempfile

def save_file(df):
    output = BytesIO()
    df.to_excel(output, index=False, engine='xlsxwriter')
    output.seek(0)
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
    with open(temp_file.name, 'wb') as f:
        f.write(output.read())
    
    return temp_file.name
