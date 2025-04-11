# Blob Trigger with SQL Input Binding

This Azure Function demonstrates how to use a blob trigger to initiate a SQL database query. When a blob is uploaded to the configured container, the function extracts a product ID from the blob content and uses it to query a SQL database.

## Prerequisites

- [Azure Functions Core Tools](https://github.com/Azure/azure-functions-core-tools)
- Python 3.8 or later
- [Azurite](https://github.com/Azure/Azurite) (for local storage emulation)
- Access to an Azure SQL Database

## Setup Instructions

### 1. Configure local.settings.json

Ensure your `local.settings.json` file is configured with the necessary connection strings:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "SqlConnectionString": "Server=your-server.database.windows.net;Database=your-database;Authentication=Active Directory Default;"
  }
}
```

For SQL authentication:
- Using Managed Identity (recommended): `Authentication=Active Directory Default;`

### 2. Start Azurite

Before running the function app, start Azurite to emulate Azure Storage locally:

```bash
azurite --silent
```

### 3. Install Dependencies

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### 4. Run the Function

Start the function app using Azure Functions Core Tools:

```bash
func start
```

## How It Works

1. The function is triggered when a blob is uploaded to the `mycontainer` container.
2. The function parses the blob content as JSON and extracts the `productId`.
3. **Key Implementation**: On line 28 of `function_app.py`, the SQL input binding executes a parameterized query using the extracted product ID:
   ```python
   # SQL input binding parameters
   params = {"ProductID": product_id}
   ```
4. The function processes the query results and logs product details.

## Blob Content Format

The function expects the blob to contain JSON data with a `productId` field:

```json
{
  "productId": "123"
}
```

## SQL Table Requirements

The function expects a SQL database with a `Products` table containing at least:
- ProductID
- ProductName
- Price

## Testing

To test the function, upload a JSON file to the `mycontainer` blob container with the following structure:

```json
{
  "productId": "YOUR_PRODUCT_ID"
}
```

Check the function logs to see if the product was found in the database.