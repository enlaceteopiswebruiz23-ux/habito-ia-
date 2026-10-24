# Coach de hábitos con IA (Flask + Supabase + OpenAI)

Función de IA: **resumen semanal** que combina rachas/% de cumplimiento (calculados en Python)
con las **notas de texto libre** del usuario, y devuelve 4 oraciones de coaching.

## Estructura
- `app.py` – rutas Flask. Lee Supabase y devuelve JSON.
- `services/ai_service.py` – ÚNICO lugar donde se llama a OpenAI.
- `services/supabase_client.py` – cliente de Supabase.
- `templates/index.html` – UI con estados de carga y error.

## Correr en local
```bash
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env     # y llena tus llaves reales
python app.py
```

## Tablas esperadas en Supabase (ajusta a las tuyas)
- `habits(id, user_id, name)`
- `habit_logs(id, habit_id, date, completed, note)`

## Despliegue en Vercel
1. Sube el repo a GitHub (verifica que `.env` NO aparezca).
2. En vercel.com → Add New Project → importa el repo.
3. Settings → Environment Variables: agrega `OPENAI_API_KEY`, `SUPABASE_URL`, `SUPABASE_KEY`, `OPENAI_MODEL`.
4. Deploy.

## Seguridad
- La API key vive solo en variables de entorno del servidor.
- `.env` está en `.gitignore` desde el primer commit.
- El frontend solo llama a `/api/ai/weekly-summary`, nunca a OpenAI.
