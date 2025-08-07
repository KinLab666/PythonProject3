# журнал изменений

### Конфигурация

- Добавлена новая опция проверка курса валют относительно рубля:

	```
 	@app.get("/currency_rate")
	def currency_rate(currency: str):

   	 url = "https://www.cbr-xml-daily.ru/daily_json.js"

    	try:
        	response = requests.get(url)
        	response.raise_for_status()
        	result = response.json()["Valute"][f"{currency}"]["Value"]

        	if not result:
 			raise HTTPException(status_code=404, detail="валюта не найдена")

        	return {f"{currency}": result}
    		except requests.exceptions.RequestException as e:
        		raise HTTPException(status_code=500, detail=f"Ошибка при запросе к cbr-xml-daily: {str(e)}")
	```
	Doing so, Rome won't emit diagnostics for file that it doesn't know how to handle.

- Добавлена новая опция проверка на ошибку 404 у всех запросов.

	```
 	standardize_party
 	        if not result:
           		 raise HTTPException(status_code=404, detail="Организация не найдена")
	standardize_phone
 		if not result:
 			raise HTTPException(status_code=404, detail="Номер не найден")
 		
 	```
- удален отдельный заголовок у "standardize_party".

	```
 	headers = {
   	 "Content-Type": "application/json",
    	"Accept": "application/json",
    	"Authorization": "Token "
	}
	```
- исправлена ошибка работы в "standardize_party".

	```
 	result = response.json().get("suggestions")
	```
