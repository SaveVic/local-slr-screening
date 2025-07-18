### Preparation
Make sure to have minimum py version 3.11. 
Install dependencies
```
pip install -r requirements.txt
```
Then change the model configuration in the `config.yaml`
```yaml
models:
  local:
    - id: <ollama_model_name>
      name: <Customized Name>
    ...
  api:
    - id: <together_ai_model_name>
      name: <Customized Name>
    ...
```
Create `.env` file and insert the Together API key
```
TOGETHER_API_KEY=<your_api_key>
```