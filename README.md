# Memory Trainer

Prosty szkielet aplikacji Streamlit wspierającej trening tabliczki mnożenia.

## Uruchamianie aplikacji

1. Zainstaluj zależności:

   ```bash
   pip install -r requirements.txt
   ```

2. Uruchom serwer Streamlit:

   ```bash
   streamlit run app.py
   ```

3. W przeglądarce wpisz adres wyświetlony w terminalu (np. `http://localhost:8501`).

Aplikacja losuje 10 zadań z mnożenia liczb z zakresu 2-12. Po wprowadzeniu odpowiedzi w formularzu
naciśnij przycisk "Sprawdź odpowiedzi", aby zobaczyć wynik w formacie `poprawne/wszystkie`. Możesz również wylosować nowy zestaw pytań przyciskiem "Nowy zestaw pytań".

## Testy

Do sprawdzenia logiki aplikacji wykorzystano pytest. Uruchom wszystkie testy poleceniem:

```bash
pytest
```
