# Drona AI Startup Script

# Add Tesseract OCR to PATH for image text extraction
$env:Path += ";C:\Program Files\Tesseract-OCR"

# Ensure Endee vector database is running
docker start endee-oss 2>$null | Out-Null
Start-Sleep -Seconds 2

# Activate conda and run Streamlit
& "C:\Users\satvi\anaconda3\Scripts\activate"
conda activate drona_ai
streamlit run ui/app.py --server.port 8501
