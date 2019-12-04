chrome.runtime.onInstalled.addListener(function() {
    const url = chrome.runtime.getURL('json.txt');
        fetch(url)
        .then((response) => response.json())
        .then((json) => {
            chrome.storage.local.set({names_to_data: json}, function() {
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

