$(document).ready(function() {
  window.looks_s = new Look_list('s');

  $("#select_item_window").click(function(){
    if(!window.my_items){
      window.my_items = new My_items();
    }
    $('#look_window').hide();
    $('#item_window').show();
    $('.like__choice-menu').css("pointer-events", 'none')
  });

  $("#select_look_window_c").click(function(){
    if(!window.looks_c){
      window.looks_c = new Look_list('c');
    }
    $('#look_window').show();
    $('#item_window').hide();
    window.looks_c.init();
    $('.like__choice-menu').css("pointer-events", 'auto')
  });
  $("#select_look_window_s").click(function(){
    if(!window.looks_c){
      window.looks_c = new Look_list('s');
    }
    $('#look_window').show();
    $('#item_window').hide();
    window.looks_s.init();
    $('.like__choice-menu').css("pointer-events", 'auto')
  });

});

const clothes = {'body':['dress', 'blouse', 'tshirt'],
'pants':['pants', 'skirt'],
'outerwear':['outerwear',],
'glasses':['cap', 'glasses'],
'shoes':['sneakers', 'shoes', 'boots', 'footwear'],
'bag':['bag',]};

/**
* луки
* @param {string} type - s - предложеные, c - ранее лайкнутые
*/
class Look_list{
  constructor(type='s'){
    this.type = type;
    this.list = [];
    this._current_look =0;
    this.get_looks();
    this.init();
  }
  get current_look(){
    return this._current_look
  }
  set current_look(val){
    if(val+2>this.list.length){
      this.get_looks(this.list.length);
    }
    if(val<this.list.length && val>=0){
      this._current_look=val;
    }
  }


  init(){
    $("#choice_prev").click(function(){
      if(this.list.length>0){
        this.change_look(--this.current_look);
      }
    }.bind(this));

    $("#choice_next").click(function(){
      if(this.list.length>0){
        this.change_look(++this.current_look);
      }
    }.bind(this));

    $("#choice_like").click(function(){
      $.ajax({
        url: "/like_look/",
        data: {
          up: !this.list[this.current_look].like,
          look_id:this.list[this.current_look].pk
        },
        success: function(result){
          if(result.status){
            $('#choice_like').find('i.fa').toggleClass('fa-heart fa-heart-o');
            $('#choice_like').find('span').toggleClass('heart_red');
            this.like=!this.like;
          }
        }.bind(this.list[this.current_look])
      });
    }.bind(this));
    if(this.list.length>0){this.change_look(this.current_look);}
  }

  change_look(val){
    if(this.list.length<=val || val<0){return;}
    let tmp;
    let items =this.list[val].items;
    for(let i in items){
      tmp = $(this.get_field_id(items[i].fields.item_type)).find('.choice-window__item__image');
      $(tmp).css('background-image', 'url(/'+items[i].fields.photo+')');
    }

    if(this.list[val].like && $('#choice_like').find('i.fa').hasClass('fa-heart-o')){
      $('#choice_like').find('i.fa').toggleClass('fa-heart fa-heart-o');
      $('#choice_like').find('span').toggleClass('heart_red');
    }else if(!this.list[val].like && $('#choice_like').find('i.fa').hasClass('fa-heart')){
      $('#choice_like').find('i.fa').toggleClass('fa-heart fa-heart-o');
      $('#choice_like').find('span').toggleClass('heart_red');
    }
  }

  get_field_id(type){
    for(let i in clothes){
      if(clothes[i].includes(type)){
        return '#'+i;
      }
    }
  }


  get_looks(last=0){
    $.ajax({
      url: "/get_looks/",
      data: {
        last: last,
        type: this.type
      },
      success: function(result) {
        this.list = this.list.concat(result);
        if(last==0){this.change_look(0);}
      }.bind(this)
    });
  }
}


/**
* луки
* используется словарь и типы из clothes
*/
class My_items{
  constructor(){
  this.dict = {};
  this.get_page();
  for(let i in clothes){
    this.dict[i] = {'current':0, 'type':i, 'items':[]};
  }
  this.keys = Object.keys(this.dict);
  this.selected_type = 0;
  this.get_items();
}


init(){
  $("#item_next").click(function(){
    this.change_item(1);
  }.bind(this));
  $("#item_prev").click(function(){
    this.change_item(-1);
  }.bind(this));

  $("#item_type_next").click(function(){
    if(this.selected_type<this.keys.length-1){
    this.selected_type++;
    this.change_item();
  }
  }.bind(this));
  $("#item_type_prev").click(function(){
    if(this.selected_type>0){
    this.selected_type--;
    this.change_item();
  }
  }.bind(this));
}

change_item(val=0, type=this.keys[this.selected_type]){
  let obj = this.dict[this.keys[this.selected_type]];
  if(obj.items.length==0){this.get_items();}
  if(obj.items.length<= obj.current + val || obj.current + val<0){return;}
  obj.current+=val;
  let tmp = $('#item').find('.choice-window__item__image');
  $(tmp).css('background-image', 'url(/'+obj.items[obj.current].fields.photo+')');
}

get_page(){
  $.ajax({
    url: "/item_window/",
    data: {},
    success: function(result) {
      $('#windows').prepend(result);
      this.init()
    }.bind(this)
  });
}

get_items(last=0, type=this.keys[this.selected_type]){
  new Promise(function (resolve, reject) {
  $.ajax({
    url: "/get_items/",
    data: {
      last: last,
      itype: JSON.stringify(clothes[type])
    },
    success: function(result) {
      this.items = JSON.parse(result);
    }.bind(this.dict[this.keys[this.selected_type]])
  }).done(resolve).fail(reject)}.bind(this)).then(result =>{this.change_item();});
}
}



//tt
