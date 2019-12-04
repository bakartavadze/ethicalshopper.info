let brand_info = document.getElementById('brand_info');

chrome.tabs.query({'active': true, 'currentWindow': true}, function (tabs) {
  chrome.tabs.sendMessage(
    tabs[0].id,
    {from: 'popup', subject: 'brand info'},
    function(response) {
      // brand_info.innerText = response.url
    });
});


