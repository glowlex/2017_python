'use strict';
$(document).ready(function() {
  //TODO проверяется на странице лука или нет, иначе с главной идёт запрос на серв с получением луков

  //исправлние ксс, принудительная перестройка
  $('nav').find('figure').hide()
  $('#look_choice').css('display', 'flex');
  setTimeout(function(){$('nav').find('figure').show();}, 1);

  if($('#look_window').length==0){return;}

  //TODO пока так
  window.my_items = new My_items();

  window.looks_s = new Look_list('s');
  let c = new window.Calendar();
  $("#select_item_window").click(function(){
    if(!window.my_items){
      window.my_items = new My_items();
    }
    $('#look_window').hide();
    $('#item_window').show();
    window.my_items.change_item();
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
    if(!window.looks_s){
      window.looks_s = new Look_list('s');
    }
    //TODO: для демонстрации
    window.looks_s.get_looks();

    $('#look_window').show();
    $('#item_window').hide();
    window.looks_s.init();
    $('.like__choice-menu').css("opacity", 'inherit');
  });

  //test
  //$("#select_item_window").click();
  window. first_toasty = true;
  weather();
});

function toasty(){
  if(!(window.first_toasty || Math.floor(Math.random() * 20)==6)){return;}
  window. first_toasty = false;
  let t = document.createElement('div');
  $(t).addClass('toasty');
  let aud = document.getElementsByTagName('audio')[0];

  $(aud).on('ended', function(e) {
  $('body')[0].removeChild(($('.toasty')[0]));
  $(e.target).off();
});

  let body = $('body')[0];
  body.appendChild(t);
  aud.play();

}

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
    if(this.type =='s'){this.s_init();}
  }
  get current_look(){
    if(this._current_look<0){this._current_look=0;}
    if(this._current_look>=this.list.length){this._current_look=this.list.length-1;}
    return this._current_look;
  }
  set current_look(val){
    this._current_look =val;
    if(this._current_look+2>this.list.length){
      this.get_looks(this.list.length);
    }

    if(this._current_look<0){
      this._current_look= this.list.length + this._current_look%this.list.length;
    }
    if(this._current_look>=this.list.length){
      this._current_look=this._current_look%this.list.length;
    }
    /*if(val<this.list.length && val>=0){
      this._current_look=val;
    }*/
  }


  init(){
    Look_list.look_window_type = this.type;
    if(this.type=='c'){
      $('#look_window').find('.choice-window__item__next').css("opacity", '0')
      $('#look_window').find('.choice-window__item__previous').css("opacity", '0')
    }else{
      $('#look_window').find('.choice-window__item__next').css("opacity", '')
      $('#look_window').find('.choice-window__item__previous').css("opacity", '')
    }
    $("#choice_prev").unbind();
    $("#choice_prev").click(function(){
      if(this.list.length>0){
        this.current_look--;
        this.new_look = undefined;
        this.change_look(this.current_look);
      }
    }.bind(this));

    $("#choice_next").unbind();
    $("#choice_next").click(function(){
      if(this.list.length>0){
        ++this.current_look;
        this.new_look = undefined;
        this.change_look(this.current_look);
      }
    }.bind(this));

    $("#choice_like").unbind();
    $("#choice_like").click(this.click_choice_like.bind(this));

    this.change_look(this.current_look);
  }

  click_choice_like(){
    if(this.list.length==0 && (!this.new_look || this.new_look.items.length<2)){return;}
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
        if(this.new_look){
          toasty();
        }
        this.new_look = undefined;
        this.list.splice(this.current_look, 1);
        this.change_look();
        //TODO пиздец
        if(result.length>0){
        //$('#choice_like').find('i.fa').toggleClass('fa-heart fa-heart-o');
        //$('#choice_like').find('span').toggleClass('heart_red');
        if(window.looks_c){
            window.looks_c.list = result.concat(window.looks_c.list);
        }
      }
      }.bind(this)
    });
  }

  s_init(){
    let items = $('#look_window').find('.choice-window__item');
    items.each(function(index, elem){
      $(elem).find('.choice-window__item__next').click(function(){
        if(Look_list.look_window_type=='c'){return;}
        this.items.change_item(1, elem.id, elem);
        this.change_new_look(elem.id);
      }.bind(this));
      $(elem).find('.choice-window__item__previous').click(function(){
        if(Look_list.look_window_type=='c'){return;}
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
    if(this.items.dict[id].items.length==0){return;}
    if(!this.new_look){
      if(this.list.length==0){
        this.new_look={};
        this.new_look.items = [];
      }else{
      this.new_look = JSON.parse(JSON.stringify(this.list[this.current_look]));
    }
    }
    let ex_cl = false;
    if(this.list.length!=0){
    for(let i in this.list[this.current_look].items){
      if(this.get_category(this.list[this.current_look].items[i].fields.item_type)==id){
        ex_cl = true;
        break;
      }
    }
  }

    for(let i in this.new_look.items){
      if(this.get_category(this.new_look.items[i].fields.item_type)==id && (this.items.dict[id].items.length!=1 || ex_cl != true)){
        debugger;
        this.new_look.items[i] = this.items.dict[id].items[this.items.dict[id].current];
        break;
      }
    }
  if(this.new_look.pk){
    if(this.new_look.items.length != this.list[this.current_look].items.length){return;}
    for(let i in this.new_look.items){
      if(this.new_look.items[i].pk !=this.list[this.current_look].items[i].pk){
        return;
      }
    }
  }else{
    this.new_look.items.push(this.items.dict[id].items[this.items.dict[id].current]);
    return;
  }
  debugger;
    this.new_look=undefined;

  }

  change_look(val=this.current_look){
    if(this.type=='s' && this.list.length==0 && $('#choice_like').find('i.fa').hasClass('fa-heart')){
      $('#choice_like').find('i.fa').toggleClass('fa-heart fa-heart-o');
      $('#choice_like').find('span').toggleClass('heart_red');
    }

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

  change_item_type(type=this.keys[this.selected_type]){
    let t = $('#item_type').find('.choice-window__item__image');
    t.css('background-image', 'url(/static/images/other/'+type+'.png)');

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
    if(obj.items.length==0){return;}
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
    this.item_to_change_arr = [];
    //выкл кнопку
    $("#item_submit_button").prop('disabled', true);
    let ph = $('#item_photo_button')[0].files;
    let data=new FormData($('#item_selects')[0]);
    let obj = this.dict[this.keys[this.selected_type]];
    if(ph.length==0){
      this.item_to_change = obj.current;
      this.item_to_change_arr = obj.items;
      if(obj.items.length==0){return;}
      data.append('item_id', obj.items[obj.current].pk);
    }
    data.append('photo', ph[0])

    this.send_item(data).then(function(result){
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
                let category = this.get_category(result[0].fields.item_type);
                if(this.item_to_change_arr.length>0 && this.get_category(this.item_to_change_arr[this.item_to_change].fields.item_type)==category){
                  this.item_to_change_arr[this.item_to_change] = result[0];
                }else{
                  this.item_to_change_arr.splice(this.item_to_change, 1);
                  this.dict[category].items.unshift(result[0]);
                  this.dict[category].current = 0;
                  this.selected_type = $.inArray(category, this.keys)
                }
        }.bind(this)
      }).done(resolve).fail(reject)}.bind(this));
    }

    change_item(val=0, type=this.keys[this.selected_type], dom='#item'){
      this.change_item_type();
      let obj = this.dict[type];
      if(obj.items.length==0 || obj.empty ==true){
        //this.get_items().then(function(result){this.change_item();}.bind(this));
        $(dom).find('.choice-window__item__image').css('background-image', 'url(/static/images/other/'+type+'.png)');
      }
      if(obj.items.length==1 && obj.current==0){val=0;};
      if(obj.items.length==0){return;}
      obj.current+=val;
      if(obj.items.length<= obj.current){
        obj.current= obj.current%obj.items.length;
      }else if (obj.current<0) {
        obj.current = obj.items.length + obj.current%obj.items.length;
      }
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
