// window.onload= function() {
//     var current_url = window.location.href.toString();
// }

chrome.runtime.onMessage.addListener(
    function(request, sender, sendResponse) {
        if ((request.from === 'popup') && (request.subject === 'brand info')) {
            var info = {
                url : window.location.href.toString()
              };
            sendResponse(info);
        }
});

// chrome.storage.local.get('names_to_data', function(data) {
//     console.log(data)
//   });
