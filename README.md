# curry_company
This repository contains files and script to build a company strategy dashboard


# 1) The Business Problem

Cury Company is a technology company that created an application that connects
restaurants, deliveries and people.
Through this application, it is possible to order a meal, at any
registered restaurant, and receive it in the comfort of your home by a delivery man
also registered in the Cury Company application.

The company conducts business between restaurants, deliveries and people. Also generates
lots of data about deliveries, types of orders, weather conditions, evaluation of
couriers and etc. Despite the increase in delivery, in terms of deliveries, the
CEO does not have complete visibility into company growth KPIs.

The Cury Company has a business model called Marketplace, which mediates the business between three main customers: 
Restaurants, couriers and buyers. To track the growth of these businesses, the CEO would like to see the following growth metrics:

- On the company's side
1. Number of orders per day
2. Quantity of orders per week
3. Distribution of requests by type of traffic
4. Comparison of order volume by city and type of traffic
5. The number of orders per delivery person per week.
6. The central location of each city by type of traffic

- On the delivery side
1. The lowest and highest age of the couriers
2. Worst and best condition of vehicles
3. The average rating per courier
4. Average rating and standard deviation by traffic type
5. Average rating and standard deviation by weather conditions
6. The 10 fastest couriers by city
7. The 10 slowest couriers by city

- On the side of the restaurant:
1. The amount of unique couriers.
2. The average distance to restaurants and delivery locations
3. Average delivery time and standard deviation by city
4. Average delivery time and standard deviation by city and order type
5. Average delivery time and standard deviation by city and type of traffic
6. The average time during the Festivals

The objective of this project is to create a set of graphs and/or tables that display these metrics in the best possible way for the CEO.

# 2) Business assumptions
1. The analysis was performed with data between 02/11/2022 and 04/06/2022
2. Marketplace was the assumed business model
3. The 3 main views of the business were: order transaction view, restaurant view and courier view.

# 3) Solution Strategy
The strategic dashboard was developed using metrics that reflect the 3 main views of the company's business model:

1. Company growth vision
2. Vision of the restaurant's growth
3. Vision of growth of couriers

Each view is represented by the following set of metrics


1. Company growth vision
    1. Orders per day
    2. Percentage of orders by transit conditions
    3. Number of orders by type and by city
    4. Orders per week
    5. Quantity of orders by type of delivery
    6. Number of orders by traffic conditions and type of city

2. Restaurant growth vision
    1. Quantity of single orders
    2. Average distance covered
    3. Average delivery time during festival and normal day
    4. Standard deviation of delivery time during festivals and normal days
    5. Average Delivery Time by City
    6. Distribution of average time by city
    7. Average delivery time by order type

3. Vision of growth of couriers
    1. Age of oldest and youngest courier
    2. Evaluation of the best and worst vehicle
    3. Average rating by traffic condition
    4. Average rating by weather condition
    5. Fastest Average Delivery Time
    6. Fastest Average Delivery Time by City

#4) Top 3 Insights

1. Seasonality of order quantity is daily. There is approximately a 10% variance in the number of orders on sequential days
2. Semi-Urban type cities do not have low traffic conditions
3. The biggest variations in delivery time happen during sunny weather.

# 5) Final Project Product

An online panel, hosted on a Cloud and available for access on any device connected to the internet.
The panel can be accessed through the link:https://jonatas-curry-company.streamlit.app/

# 6) Conclusion

The goal of this project is to create a set of charts and tables that best display these metrics for a CEO.
From the company view, we can conclude that the number of orders grew between week 06 and week 13 of the year 2022

# 7) Next Steps

1. Reduce the amount of metrics
2. Create new filters
3. Add new business views.




































