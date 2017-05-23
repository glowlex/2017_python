function weather(){

  $.ajax({
    url: 'http://api.openweathermap.org/data/2.5/weather?id=524901&mode=json&units=metric&APPID=0b1eaf7ce235a1ebaba14d5e07ee4228',
    success: set_weather,
  });

function set_weather(result){
  debugger;
  let tmp = $('.weather');
  $(tmp).find('.weather__temp__high')[0].innerText= (result.main.temp_max>0 ? '+':' ') + result.main.temp_max;
  $(tmp).find('.weather__temp__low')[0].innerText = (result.main.temp_min>0 ? '+':' ') + result.main.temp_min;
  $(tmp).find('.weather-info>p')[0].innerText = 'облачность:  ' + result.clouds.all + '%';
  $(tmp).find('.weather-info>p')[1].innerText = 'влажность:  ' + result.main.humidity + '%';
  $(tmp).find('.weather-info>p')[2].innerText = 'ветер:  ' + result.wind.speed + ' м/с';
  let img = $(tmp).find('figure')[1];
  switch (Math.floor(result.weather[0].id/100)) {
    case 8:
    if(result.weather[0].id>800){
      $(img).css('background-image', 'url(/other/802-804.png), url(/other/8.png)');
    }else{
      $(img).css('background-image', 'url(/other/8.png)');
    }
    break;

    default:
    $(img).css('background-image', 'url(/other/'+Math.floor(result.weather[0].id/100)+'.png)');
  }

}

}
