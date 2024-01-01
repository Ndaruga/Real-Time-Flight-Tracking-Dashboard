import logging
import azure.functions as func

app = func.FunctionApp()

@app.schedule(schedule="0 0/10 * * * *", arg_name="myTimer", run_on_startup=True,
              use_monitor=False) 
def timer_trigger_10_mins(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')
    
    api

    logging.info('Python timer trigger function executed.')