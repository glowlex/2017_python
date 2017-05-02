(function(){

  class Calendar{
    constructor(year=new Date().getFullYear(), month=new Date().getMonth(), day=new Date().getDate()){
      this.date = new Date(year, month, day);
      this.now = new Date();
      this.calendar = [];
      this.styles=[];
      this.SHORT_DAY_NAMES = new Array(
        'Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс');

        this.MONTH_NAMES = new Array(
          'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август',
          'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь');
          this.init();

          //test
          this.refresh();
        }

        init(){
          this.get_calendar().then(function(){this.refresh();}.bind(this));
          this.make_template();
          $("#month_next").click(function(){
            this.date.setMonth(this.date.getMonth()+1);
            this.refresh();
          }.bind(this));
          $("#month_prev").click(function(){
            this.date.setMonth(this.date.getMonth()-1);
            this.refresh();
          }.bind(this));

          let lmonth = $('#calendar').find('td>a');
          $(lmonth).click(this.click_on_date.bind(this));


//чтобы окно со стилем события убиралось если кликнуть куда угодно
          $(function($){
            $(document).mouseup(function (e){
              let div = $('#calendar').find('tbody');
              if (!div.is(e.target)
              &&!($('#event-window').is(e.target))
              && div.has(e.target).length === 0
              &&($('#event-window').has(e.target).length === 0)) {
                $('#event-window').hide();
              }
            });
          });

          $('#event-window').find('select').change(function(e) {
            if(e.target.value!=''){
              this.send_event(e.target.value).then(
                function(result){$('#event-window').toggleClass('event-window_ok', true);
                setTimeout(function(){$('#event-window').toggleClass('event-window_ok', false);}, 1000);
                this.refresh();   debugger;}.bind(this),

                function(result){$('#event-window').toggleClass('event-window_error', true);
                $('#event-window').find('select').val('');
                setTimeout(function(){$('#event-window').toggleClass('event-window_error', false);}, 1000);}.bind(this)
              );
            }else{
              this.delete_event();
            }
          }.bind(this));
          console.log("calendar init");
        }

        delete_event(){

        }

        send_event(type, date=this.date){
          let t = JSON.stringify({year:date.getFullYear(), month:date.getMonth()+1, day:date.getDate()});
          return new Promise(function (resolve, reject) {
            $.ajax({
              type: 'POST',
              url: "/api/set_event/",
              data: {
                etype: type,
                date: t
              },
              success: function(result) {
                result[0].fields.date = this.make_date(result[0].fields.date);
                this.calendar.push(result[0]);
              }.bind(this)
            }).done(resolve).fail(reject)}.bind(this));
        }

        get_calendar(){
          return new Promise(function (resolve, reject) {
            $.ajax({
              url: "/api/get_calendar/",
              success: function(result) {
                this.styles = result.styles;
                for(let i in result.calendar){
                  result.calendar[i].fields.date = this.make_date(result.calendar[i].fields.date);
                  this.calendar.push(result.calendar[i]);
                }
                this.make_styles_template();
              }.bind(this)
            }).done(resolve).fail(reject)}.bind(this));
        }

        make_date(d){
          let m = new Date(d);
          m.setMinutes(new Date().getTimezoneOffset());
          return m;
        }

        click_on_date(e){
          $('#calendar').find('td[class~=active]').toggleClass('active', false);
          $(e.target.parentNode).toggleClass('active', true);
          if($(e.target.parentNode).hasClass('off')){
            this.date.setDate(1);
            if(e.target.innerText<15){
              this.date.setMonth(this.date.getMonth()+1);
            }else{
              this.date.setMonth(this.date.getMonth()-1);
            }
            this.refresh();
          }else{
            let ev = $('#event-window')[0];
            $(ev).css({'left':e.target.offsetLeft, 'top':e.target.offsetTop+e.target.offsetHeight*2});
            let s = this.get_style(e.target.innerText);
            if(s){
            $(ev).find('select').val(s.fields.event_type);
          }else{
            $(ev).find('select').val('');
          }
            $(ev).show();
          }
          this.date.setDate(e.target.innerText);
        }


        refresh(){
          $('#calendar').find('caption>div')[0].innerText=this.MONTH_NAMES[this.date.getMonth()]+
          "   "+this.date.getFullYear();
          let lmonth = $('#calendar').find('tbody>tr');
          $(lmonth).find('.active').toggleClass('active', false);
          $(lmonth).find('td[class~=now]').toggleClass('now', false);
          $(lmonth).find('td[class~=marked]').toggleClass('marked', false);

          let i= new Date(this.date.getYear(), this.date.getMonth(), 1).getDay();
          let lweek = $(lmonth[0]).find('td>a');
          let preweek = 33 - new Date(this.date.getYear(), this.date.getMonth()-1, 33).getDate();
          for(let j=i; j>=0; j--){
            lweek[j].innerText=preweek--;
            $(lweek[j].parentNode).toggleClass('off', true);
          }

          let edays = this.get_dates(this.date.getYear(), this.date.getMonth());

          let amount = 33 - new Date(this.date.getYear(), this.date.getMonth(), 33).getDate();
          let date = 1, flag = false;
          for(i=0; i<lmonth.length;  i++){
            lweek = $(lmonth[i]).find('td>a');
            let j=0;
            if(i==0){j=new Date(this.date.getYear(), this.date.getMonth(), 1).getDay()+1;}
            for(j; j<7; j++){
              if(flag){
                $(lweek[j].parentNode).toggleClass('off', true);
              }else{
                $(lweek[j].parentNode).toggleClass('off', false);
                if(date==this.now.getDate() && this.now.getYear()==this.date.getYear() && this.now.getMonth()==this.date.getMonth()){
                  $(lweek[j].parentNode).toggleClass('now', true);
                }
                if(date==this.date.getDate()){
                  $(lweek[j].parentNode).toggleClass('active', true);
                }
                if($.inArray(date, edays)>-1){
                  $(lweek[j].parentNode).toggleClass('marked', true);
                }
              }
              lweek[j].innerText=date++;
              if(amount+1==date){
                date=1;
                flag=true;
              }
            }
          }
        }

        get_dates(y, m){
          let res = [];
          for(let i in this.calendar){
            let date = this.calendar[i].fields.date;
            if(date.getYear()==y && date.getMonth()==m){
              res.push(date.getDate());
            }
          }
          return res;
        }

        get_style(d){
          let y = this.date.getYear(), m = this.date.getMonth();
          for(let i in this.calendar){
            let date = this.calendar[i].fields.date;
            if(date.getYear()==y && date.getMonth()==m && date.getDate()==d){
              return this.calendar[i];
            }
          }
          return false;
        }

        make_template(){
          let days = $('#calendar').find('thead>tr');
          for(let i in this.SHORT_DAY_NAMES){
            let tmp = document.createElement('th');
            tmp.innerText = this.SHORT_DAY_NAMES[i];
            days[0].appendChild(tmp);
          }
          let lmonth = $('#calendar').find('tbody');
          for(let i=0; i<6;i++){
            let tmp = document.createElement('tr');
            for(let j=0; j<7; j++){
              let td = document.createElement('td');
              td.appendChild(document.createElement('a'));
              tmp.appendChild(td);
            }
            lmonth[0].appendChild(tmp);
          }
        }

        make_styles_template(){
          let sel =  $('#event-window_id_style')[0];
          let tmp = document.createElement('option');
          $(tmp).val('');
          tmp.innerText='-------';
          sel.appendChild(tmp);
          for(let i in this.styles){
            tmp = document.createElement('option');
            $(tmp).val(this.styles[i][0]);
            tmp.innerText=this.styles[i][1];
            sel.appendChild(tmp);
          }
        }


      }

    window.Calendar = Calendar;

    })();
