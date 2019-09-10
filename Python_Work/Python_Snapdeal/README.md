## Sammary

**Intro:**

The projects are industry level cover the scrapping of SnapDeal website where the data sale for comparison purpose and financial forecasting; the link for scrapping- 
-http://www.snapdeal.com/seller/football-specialists/657d99

**Things to scrape in bulk and save in CSV format:**
- Image Links
- Item Details
- Item Title
- Category - (breadcrumbs)

**Note:**
This site has an ajax call at the page end scroll where more products are loaded.
So We took the SUPC code for every product shared by the client.

So the input will be SUPC code and output will be scrapped data for the Product.
There are 3 steps involved in this scrapping.
- Search the SUPC code in the search box of Snapdeal website and split the success and failed URL's.
- Search the URL and Get the actual link for the Product.
- Scrape the asked data from the actual url.

**For example"** 
- Use the below link for success and fail - 
- Status - Fail
- supc code - SDL281657177
- search link - http://www.snapdeal.com/search?keyword=SDL281657177
- Message - Sorry, we've got no results for "SDL281657177"

