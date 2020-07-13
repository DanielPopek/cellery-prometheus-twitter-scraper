# Twitter scrapper with Cellery, Prometheus and Grafana

The aim of this project is to implement live tweets scrpaer with task queue and data fetching monitoring. 
The project uses Twint library for data aquisition.

## Subtasks: 

1. Implement tweets scrapper that utilizes Twint
2. Take care of new tweets fetching. Add appropriate task scheduling, that will fetch new tweets. 
4. Add process monitoring:
    - Utilize Prometheus 
    - Publish  metrics about the data fetching process 
    - publish general celery metrics (using ovalmoney/celery-exporter library)
    - visualize metrics using Grafana 