chrome.tabs.query({'active': true, 'currentWindow': true}, function (tabs) {
  chrome.tabs.sendMessage(
    tabs[0].id,
    {from: 'popup', subject: 'brand info'},
    function(response) {
      if (response) {
        fill_popup_with_info(response);
      } else {
        display_no_info_available();
      }
    });
});

function display_no_info_available() {
  document.getElementById('brand_name').innerText = 'Ratings Unavailable';
}

function fill_popup_with_info(response) {
  fix_spacing_between_elements();
  set_brand_name(response.name);
  // if no price info available
  if (response.data['price']) {
    set_price(response.data['price'].length);
  }
  set_rating_title(response.data['rating'].toUpperCase());
  set_rating(rating_score[response.data['rating'].toLowerCase()]);
  set_rating_message(rating_message[response.data['rating'].toLowerCase()]);

  var people_rating = parseInt(response.data['people_rating']);
  var planet_rating = parseInt(response.data['planet_rating']);
  var animals_rating = parseInt(response.data['animals_rating']);
  set_subcategory_ratings(people_rating, planet_rating, animals_rating);
  set_brand_message(response.data['message']);
  set_brand_read_more_url(response.data['GoodOnYou_url']);
}

function set_brand_name(name) {
  document.getElementById('brand_name').innerText = name;
}

function set_rating_title(title) {
  document.getElementById('rating_title').innerText = title;
}

function set_rating_message(message) {
  document.querySelector("#brand_rating_body > span").innerText = message;
}

function set_brand_message(message) {
  document.querySelector("#brand_message > span").innerText = message;
}

function fix_spacing_between_elements() {
  document.getElementById('brand_name').style.marginBottom = "6px";
  document.getElementById('brand_rating_body').style.marginTop = "12px";
  document.getElementById('brand_message').style.marginBottom = "15px";
}

function set_brand_read_more_url(url){
  var brand_read_more = document.getElementById('brand_read_more');
  brand_read_more.style.display = 'block';
  brand_read_more.querySelector("a").href = url;
  brand_read_more.querySelector("a").setAttribute('target', '_blank');
}

function set_price(dollar_sign_count) {
  var brand_price = document.getElementById('brand_price');
  var dollar_signs = brand_price.querySelectorAll(".fa-dollar-sign");
  brand_price.style.display = 'block';
  for (var i = 0; i < dollar_sign_count; i++) {
    dollar_signs[i].classList.add('lit-icon');
  }
}

function set_rating(brand_rating) {
  var star_signs = document.querySelectorAll("#rating_graphic > .fa-star");
  for (var i = 0; i < brand_rating; i++) {
    star_signs[i].classList.add('lit-icon');
  }
}

function set_subcategory_ratings(people_rating, planet_rating, animals_rating) {
  var people_star_signs = document.querySelectorAll("#people_rating_graphic > .fa-star");
  var planet_star_signs = document.querySelectorAll("#planet_rating_graphic > .fa-star");
  var animals_star_signs = document.querySelectorAll("#animals_rating_graphic > .fa-star");
  for (var i = 0; i < people_rating; i++) {
    people_star_signs[i].classList.add('lit-icon');
  }
  for (var i = 0; i < planet_rating; i++) {
    planet_star_signs[i].classList.add('lit-icon');
  }
  for (var i = 0; i < animals_rating; i++) {
    animals_star_signs[i].classList.add('lit-icon');
  }
}

var rating_message = {
  "we avoid": "Brands with this rating provide little to no " +
              "relevant or concrete information. In some cases, " + 
              "the brand may make ambiguous claims that look like greenwash. " + 
              "You have a right to comprehensive and accurate information " + 
              "about how a brand impacts on people, planet and animals!",
  "not good enough" : "Brands with this rating have provided some information in several " +
                      "areas, but not enough to truly know what happens in their supply chains.",
  "it's a start" : "Brands with this rating are transparent in at least one area and making " +
                   "good progress on one or more of the main issues.",
  "good" : "Brands with this rating have taken several significant positive initiatives, are " + 
            "often leaders on one or more key issues, and in most case are very transparent.",
  "great" : "Brands with this rating score highly in at least two categories and have one " + 
            "or more certifications or accreditations. They're often designed from the " + 
            "ground up to be sustainable and ethical, and they're usually super transparent."
};

var rating_score = {
  "we avoid": 1,
  "not good enough": 2,
  "it's a start": 3,
  "good": 4,
  "great": 5
};