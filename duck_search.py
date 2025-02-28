from duckduckgo_search import DDGS

def web_search(query):
    results = DDGS().text(query, max_results=5)
    return results

def video_search(query):
    results = DDGS().videos(query, max_results=5)
    return results

def image_search(query):
    results = DDGS().images(query, max_results=5)
    return results

# if __name__ == "__main__":
#     query = "doge"
    
#     print("Web Search Results:")
#     web_results = web_search(query)
#     for result in web_results:
#         print(result)
    
#     print("\nVideo Search Results:")
#     video_results = video_search(query)
#     for result in video_results:
#         print(result)
    
#     print("\nImage Search Results:")
#     image_results = image_search(query)
#     for result in image_results:
#         print(result)