chrome.runtime.onInstalled.addListener(function() {
    const names_to_data_mapping = chrome.runtime.getURL('brand_names_to_data.txt');
        fetch(names_to_data_mapping)
        .then((response) => response.json())
        .then((json) => {
            chrome.storage.local.set({names_to_data: json}, function() {
            });
        });
    const urls_to_names_mapping = chrome.runtime.getURL('brand_urls_to_brand_names.txt');
        fetch(urls_to_names_mapping)
        .then((response) => response.json())
        .then((json) => {
            chrome.storage.local.set({urls_to_names: json}, function() {
            });
        });
    

        chrome.declarativeContent.onPageChanged.removeRules(undefined, function() {
            chrome.declarativeContent.onPageChanged.addRules([{
              conditions: [new chrome.declarativeContent.PageStateMatcher({
              })
              ],
                  actions: [new chrome.declarativeContent.ShowPageAction()]
            }]);
          });

});



