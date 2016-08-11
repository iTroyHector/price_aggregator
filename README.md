
### Price Aggregator Software

#### Summary

This module aims to serve as a price aggregator for different products over a 
set of e-commerce websites. It will track, store and display the prices of the
products on a simple website and will allow people to search for the cheapest 
options. The Price Aggregator will ultimately redirect the user to the original
website where the information was extracted from, so that the person can make 
the purchase. 

#### Technology

- Python 2.7
- Selenium
- Scrapy 
- MongoDB
- Flask

#### Flow

##### Introduction 

Let's assume that we want to get the prices for a certain product in many 
e-commerce platforms, store them, and then compare them. In fact, what we really
want is to do this, but with many products. But, for the sake of simplicity, our
explanation will be just focused on *one and only one product*: Iphone 6S. 

Our assumption is that our sources of information have good search engines. 
Based on that, what we do is to mimic the User's behavior and then select those
products that matche the best what we are looking for, and store its more 
relevant information. The definition of relevance is based on an algorithm that
computes some statistical information and discards those products that are 
considered outliers. After that selection, the three cheapest are stored in our
database. 

##### Step one - Searching for the product and collecting several samples

For this stage, we use *Selenium*. It is an easy-to-use library that mimics the 
experience of using a web browser. Thus, we prevent services kicking our 
robots, and it also allows us to easily use their search engines.

In esence what we do is to search in the search field that every e-commerce 
site has for a certain product. In this case, we will search for the "Iphone 
6S". 

##### Step Two - getting relevant samples

Once the website with a big amount of results is retrieved, then it is the time 
to select the 3 best products and then store its information on our database. 
The way we will do this is by using the following strategy:

1. Record all the products of the first page (maybe consider further pages)
2. Sort prices in ascending order
3. Calculate the MEDIAN price
4. Calculate the coefficient of variation (stdev / mean)
5. Check the price that is closest to x * coefficient of variation * MEDIAN is 
equal to 0.7 MEDIAN (30% cheaper than median)
6. Verify if the price is in a percentile higher than 30%. Otherwise iterate to 
a price that is 5% more. Repeat this process until one price is found. Then 
select the next two other products that follow this price, but are more 
expensive.

After following this algorithm, we ensure that no outliers are selected. Plus, 
we get three products. This is done in case a link fails, or users report that 
the product is not what they expected. In case this happens, we could easily 
switch it for another. And this process could be done twice. 

##### Step Three - Storing And displaying

The information will be stored into a MongoDB collection. Each product will 
have its own collection. And for every document there will be a field that 
contains the url where the product can be found, a url of a picture of this 
product, its price, the date that says when the information was retrieved and
the price of the product.

For the first version, a naive search engine will be provided. If the search 
matches any of the products stored in the database, a list of one product per 
site will be showed ordered increasingly by price. The list will contain a 
picture for each product, a link to its original webiste and the price. 

#### Concerns and possible extensions

Using Selenium is resource-intensive. But there are some workarounds to have a 
headless library that consumes less memory and CPU. A possibility for extending 
our service in next versions would be to include a Library called PhantomJS.  
