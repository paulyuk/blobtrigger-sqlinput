import azure.functions as func
import logging
import json

app = func.FunctionApp()

@app.blob_trigger(arg_name="myblob", path="mycontainer", source="EventGrid",
                            connection="AzureWebJobsStorage") 
@app.sql_input(arg_name="sqldata", 
               connection_string_setting="SqlConnectionString",
               command_text="SELECT * FROM Products WHERE ProductID = @ProductID")
def load_sql_data(myblob: func.InputStream, sqldata: func.SqlRowList):
    logging.info(f"Python blob trigger (using Event Grid) function processed blob"
                f"Name: {myblob.name}"
                f"Blob Size: {myblob.length} bytes")
    
    # Read blob content and extract product ID
    try:
        blob_content = myblob.read().decode('utf-8')
        blob_data = json.loads(blob_content)
        product_id = blob_data.get("productId")
        
        if not product_id:
            logging.error("No productId found in blob content")
            return
        
        # SQL input binding parameters
        params = {"ProductID": product_id}
        
        # Process the query results
        results = list(sqldata.get_results(params))
        if results:
            for row in results:
                product_name = row["ProductName"] if "ProductName" in row else "Unknown"
                price = row["Price"] if "Price" in row else 0
                logging.info(f"Found product: {product_name}, Price: ${price}")
        else:
            logging.info(f"No product found with ID: {product_id}")
            
    except ValueError as e:
        logging.error(f"Error parsing blob content as JSON: {str(e)}")
    except Exception as e:
        logging.error(f"Error processing blob: {str(e)}")
