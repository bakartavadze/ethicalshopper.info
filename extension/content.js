chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        if ((request.from === 'popup') && (request.subject === 'brand info')) {
            chrome.storage.local.get('urls_to_names', function(urls_to_names_mapping) {
                urls_to_names = urls_to_names_mapping
                // check if a known brand url is found
                var found = false
                for (var url in urls_to_names['urls_to_names']){
                    var current_url = window.location.href.toString();
                    if(current_url.includes(url)) {
                        found = true
                        chrome.storage.local.get('names_to_data', function(names_to_data_mapping) {
                            names_to_data = names_to_data_mapping
                            brand_name = urls_to_names['urls_to_names'][url]
                            brand_data = names_to_data['names_to_data'][brand_name]
                            sendResponse({name: brand_name, data:brand_data});
                        });
                        break;
                    } 
                  }
                  if (!found) {
                    sendResponse(undefined);
                  }
                
              });
        }
        return true;
});
