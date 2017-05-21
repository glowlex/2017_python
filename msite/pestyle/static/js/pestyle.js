'use strict';
$(document).ready(function() {
  //TODO проверяется на странице лука или нет, иначе с главной идёт запрос на серв с получением луков

  //исправлние ксс, принудительная перестройка
  $('nav').find('figure').hide()
  $('#look_choice').css('display', 'flex');
  setTimeout(function(){$('nav').find('figure').show();}, 1);

  //TODO пока так
  window.my_items = new My_items();

  if($('#look_window').length==0){return;}
  window.looks_s = new Look_list('s');
  let c = new window.Calendar();
  $("#select_item_window").click(function(){
    if(!window.my_items){
      window.my_items = new My_items();
    }
    $('#look_window').hide();
    $('#item_window').show();
    $('.like__choice-menu').css("opacity", '0')
  });

  $("#select_look_window_c").click(function(){
    if(!window.looks_c){
      window.looks_c = new Look_list('c');
    }
    $('#look_window').show();
    $('#item_window').hide();
    window.looks_c.init();
    $('.like__choice-menu').css("opacity", 'inherit')
  });
  $("#select_look_window_s").click(function(){
    if(!window.looks_c){
      window.looks_c = new Look_list('s');
    }
    $('#look_window').show();
    $('#item_window').hide();
    window.looks_s.init();
    $('.like__choice-menu').css("opacity", 'inherit')
  });

  //test
  //$("#select_item_window").click();

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
    //TODO пиздец пиздец
    this.items = window.my_items;
    this.new_look = undefined;
  }
  get current_look(){
    if(this._current_look<0){this._current_look=0;}
    if(this._current_look>=this.list.length){this._current_look=this.list.length-1;}
    return this._current_look;
  }
  set current_look(val){
    if(val<0){this._current_look=0;}
    if(val>=this.list.length){this._current_look=this.list.length-1;}
    if(val+2>this.list.length){
      this.get_looks(this.list.length);
    }
    if(val<this.list.length && val>=0){
      this._current_look=val;
    }
  }


  init(){
    $("#choice_prev").unbind();
    $("#choice_prev").click(function(){
      if(this.list.length>0){
        this.change_look(--this.current_look);
      }
    }.bind(this));

    $("#choice_next").unbind();
    $("#choice_next").click(function(){
      if(this.list.length>0){
        this.change_look(++this.current_look);
      }
    }.bind(this));

    $("#choice_like").unbind();
    $("#choice_like").click(this.click_choice_like.bind(this));

    if(this.list.length>0){this.change_look(this.current_look);}
    if(this.type =='s'){this.s_init();}
  }

  click_choice_like(){
    if(this.list.length==0 && !this.new_look){return;}
    //тут, чтобы было видно при нажатии
    $('#choice_like').find('i.fa').toggleClass('fa-heart fa-heart-o');
    $('#choice_like').find('span').toggleClass('heart_red');

    let url, data;
    if(this.new_look){
      this.list[this.current_look]=this.new_look;
      let ar = [];
      for(let i in this.new_look.items){
        ar.push(this.new_look.items[i].pk);
      }
      url = "/api/new_look/";
      data = {ids:JSON.stringify(ar),};
    }else{
      url = "/api/like_look/";
      data = {
        up: !this.list[this.current_look].like,
        look_id:this.list[this.current_look].pk
      };
    }

    $.ajax({
      url: url,
      type:'POST',
      data: data,
      success: function(result){
        this.new_look = undefined;
        this.list.splice(this.current_look, 1);
        this.change_look();
        //TODO пиздец
        if(window.looks_c && result.length>0){
          window.looks_c.list = result.concat(window.looks_c.list);
        }
      }.bind(this)
    });
  }

  s_init(){
    let items = $('#look_window').find('.choice-window__item');
    items.each(function(index, elem){
      $(elem).find('.choice-window__item__next').click(function(){
        this.items.change_item(1, elem.id, elem);
        this.change_new_look(elem.id);
      }.bind(this));
      $(elem).find('.choice-window__item__previous').click(function(){
        this.items.change_item(-1, elem.id, elem);
        this.change_new_look(elem.id);
      }.bind(this));
    }.bind(this));
  }

  get_category(type){
    for(let i in clothes){
      if(clothes[i].includes(type)){
        return i;
      }
    }
    return undefined;
  }

  change_new_look(id){
    if(!this.new_look){
      this.new_look = JSON.parse(JSON.stringify(this.list[this.current_look]));
    }
    for(let i in this.new_look.items){
      if(this.get_category(this.new_look.items[i].fields.item_type)==id){
        this.new_look.items[i] = this.items.dict[id].items[this.items.dict[id].current];
        return;
      }
    }
    this.new_look.items.push(this.items.dict[id].items[this.items.dict[id].current]);
  }

  change_look(val=this.current_look){
    if((this.list.length>val && val>=0)||this.list.length==0){
      $('#pants').hide();
      let items = $('.choice-window').find('.choice-window__item__image');
      items.each(function(index, elem) {
        $(elem).css('background-image', '');
      });
    }

    if(this.list.length<=val || val<0){return;}
    let tmp;
    let items =this.list[val].items;
    for(let i in items){
      if(this.get_field_id(items[i].fields.item_type)=='#pants'){
        $('#pants').show();
      }
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
      url: "/api/get_looks/",
      data: {
        last: last,
        type: this.type
      },
      context:{obj:this, last:last},
      success: function(result) {
        this.obj.list = this.obj.list.concat(result);
        if(this.last==0){this.obj.change_look(0);}
      }
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
      this.dict[i] = {'current':0, 'type':i, 'empty':false, 'items':[]};
    }
    this.keys = Object.keys(this.dict);
    this.selected_type = 0;
    this.item_to_change;
    this.item_to_change_arr;
  }


  init(){
    $("#item_submit_button").click(this.click_item_submit.bind(this));
    $("#item_delete_button").click(this.click_item_delete.bind(this));

    //TODO редактирование изображения
    $("#item_photo_button").change(function(){
      let ph = $('#item_photo_button')[0].files;
      if(ph.length==0){return;}
    }.bind(this));


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

  get_category(type){
    for(let i in clothes){
      if(clothes[i].includes(type)){
        return i;
      }
    }
    return undefined;
  }

  click_item_delete(e){
    //выкл кнопку
    $(e.target).prop('disabled', true);
    let obj = this.dict[this.keys[this.selected_type]];
    this.item_to_change = obj.current;
    this.item_to_change_arr = obj.items;
    let d = obj.items[obj.current].pk;
    $.ajax({
      type: 'POST',
      url: "/api/delete_item/",
      data: {
        item_id:d
      },
      context:{obj:this, e:e},
      success: function(result, e) {

        this.obj.item_to_change_arr.splice(this.obj.item_to_change, 1);
        this.obj.change_item();
        $(this.e.target).prop('disabled', false);
      }
    });
  }

  click_item_submit(){
    //выкл кнопку
    $("#item_submit_button").prop('disabled', true);
    let ph = $('#item_photo_button')[0].files;
    let data=new FormData($('#item_selects')[0]);
    let obj = this.dict[this.keys[this.selected_type]];
    this.item_to_change = obj.current;
    this.item_to_change_arr = obj.items;
    if(ph.length==0){
      data.append('item_id', obj.items[obj.current].pk);
    }
    data.append('photo', ph[0])

    this.send_item(data).then(function(result){

      let category = this.get_category(result[0].fields.item_type);
      if(this.item_to_change_arr.length>0 && this.get_category(this.item_to_change_arr[this.item_to_change].fields.item_type)==category){
        this.item_to_change_arr[this.item_to_change] = result[0];
      }else{
        this.item_to_change_arr.splice(this.item_to_change, 1);
        this.dict[category].items.push(result[0]);
        this.dict[category].current = this.dict[category].items.length-1;
        this.selected_type = $.inArray(category, this.keys)
      }
      //вкл кнопку
      $("#item_submit_button").prop('disabled', false);
      this.change_item();
    }.bind(this));
  }

  send_item(data){
    return new Promise(function (resolve, reject) {
      $.ajax({
        cache: false,
        processData: false,
        contentType: false,
        type: 'POST',
        url: "/api/set_item/",
        data: data,
        success: function(result) {
        }.bind(this)
      }).done(resolve).fail(reject)}.bind(this));
    }

    change_item(val=0, type=this.keys[this.selected_type], dom='#item'){
      let obj = this.dict[type];
      if(obj.items.length==0 && obj.empty ==false){
        this.get_items().then(function(result){this.change_item();}.bind(this));
        $(dom).find('.choice-window__item__image').css('background-image', 'url(/)');
      }
      if(obj.items.length<= obj.current + val || obj.current + val<0){return;}
      obj.current+=val;
      let item = obj.items[obj.current];
      let tmp = $(dom).find('.choice-window__item__image');
      $(tmp).css('background-image', 'url(/'+item.fields['photo']+')');
      tmp = $('#item_selects').find('select');
      $(tmp).each(function(index, elem) {
        $(elem).val(item.fields[elem.name]);
      });
    }

    get_page(){
      $.ajax({
        url: "/api/get_item_window/",
        data: {},
        success: function(result) {
          $('#windows').prepend(result);
          this.get_items().then(function(result){this.change_item();}.bind(this));
          this.init();
          $('#item_window').hide();
        }.bind(this)
      });
    }

    get_items(last=0, type=this.keys[this.selected_type]){
      return new Promise(function (resolve, reject) {
        $.ajax({
          url: "/api/get_items/",
          data: {
            last: last,
            itype: JSON.stringify(clothes[type])
          },
          success: function(result){
            for(let i=0; i<result.length; i++){
              let t = this.get_category(result[i].fields.item_type);
              if(t != undefined){
                this.dict[t].items.push(result[i]);
              }
            }
            //this.items = this.items.concat(result);
            //для борьбы с многократной загрузкой если нет итемов
            for(let i in this.dict){
              if(this.dict[i].items.length==0){
                this.dict[i].empty = true;
              }
            }
          }.bind(this)
        }).done(resolve).fail(reject)}.bind(this));
      }
    }






    //tt
