FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY InsurMinds_Projeto_Final ./InsurMinds_Projeto_Final
WORKDIR /app/InsurMinds_Projeto_Final
ENV PORT=3000
EXPOSE 3000
CMD ["sh", "-c", "python app.py"]
