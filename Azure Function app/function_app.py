import logging
import azure.functions as func

app = func.FunctionApp()

@app.schedule(schedule="0 0/10 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def timer_trigger_10_mins(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')
    
    API_KEY = "ec3717ce-36bf-46b8-b8fe-356638bd8236"
    BASE_URL = f"https://airlabs.co/api/v9/flight?api_key={API_KEY}"
    

    logging.info('Python timer trigger function executed.')