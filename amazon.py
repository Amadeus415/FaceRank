from paapi5_python_sdk.api.default_api import DefaultApi
from paapi5_python_sdk.models.partner_type import PartnerType
from paapi5_python_sdk.models.search_items_request import SearchItemsRequest
from paapi5_python_sdk.rest import ApiException

# Initialize the API client
api = DefaultApi(
    access_key='YOUR_ACCESS_KEY',
    secret_key='YOUR_SECRET_KEY',
    host='webservices.amazon.com',
    region='us-east-1'
)

# Set up the search request
search_request = SearchItemsRequest(
    partner_tag='YOUR_PARTNER_TAG',
    partner_type=PartnerType.ASSOCIATES,
    keywords='laptop',
    search_index='All'
)

try:
    # Perform the search
    response = api.search_items(search_request)
    
    # Get the first item from the search results
    item = response.search_result.items[0]
    
    # Generate an affiliate link
    affiliate_link = item.detail_page_url
    
    print(f"Affiliate link: {affiliate_link}")
except ApiException as e:
    print(f"Exception when calling API: {e}")