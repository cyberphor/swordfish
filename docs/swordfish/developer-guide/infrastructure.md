# Infrastructure

## Azure
 
**Step 1.** Deploy cloud resources using Infrastructure-as-Code. Said resources must ensure there is an Azure OpenAI (AOAI) service with a deployment specific for your project.
 
**Step 2.** Activate your Owner role on the AOAI service and then, login to Azure via CLI.
```bash
az login --use-device-code
```
 
**Step 3.** Get the client ID and client secret for your Service Principal and then add them as environment variables to your project.
 
**Step 4.** Get the object ID of service principal.
```bash
export OBJECT_ID=$(az ad sp show --id $CLIENT_ID --query id -o tsv)
```
 
**Step 5.** Get the resource ID of Azure OpenAI service.
```bash
export RESOURCE_ID=$(az cognitiveservices account show \
  --name $AOAI_SERVICE_NAME \
  --resource-group $AOAI_SERVICE_RESOURCE_GROUP \
  --query id -o tsv)
```
 
**Step 6.** Assign the service principal the "Cognitive Services OpenAI User" role on the object ID.
```bash
az role assignment create \
  --assignee $OBJECT_ID \
  --role "Cognitive Services OpenAI User" \
  --scope $RESOURCE_ID
```
 
**Step 7.** Assign the service principal the "Cognitive Services OpenAI Contributor" role on the object ID.
```bash
az role assignment create \
  --assignee $OBJECT_ID \
  --role "Cognitive Services OpenAI Contributor" \
  --scope $RESOURCE_ID
```
 
**Step 8.** Run your project. Running your project should include executing code that authenticates with the AOAI service as your Service Principal.
 
## References
* [Compare Azure Government and global Azure](https://learn.microsoft.com/en-us/azure/azure-government/compare-azure-government-global-azure)
* [How to switch between OpenAI and Azure OpenAI endpoints](https://learn.microsoft.com/en-us/azure/developer/ai/how-to/switching-endpoints?tabs=azure-openai&pivots=python)
